WITH raw_risk AS (
    SELECT 
        impact_id,
        actor_id,
        NULL AS risk_score,
        SUM(CASE WHEN category = 'hazard' THEN indicator_score * indicator_weight END) AS hazard_score,
        SUM(CASE WHEN category = 'exposure' THEN indicator_score * indicator_weight END) AS exposure_score,
        SUM(CASE WHEN category = 'vulnerability' THEN indicator_score * indicator_weight END) AS vulnerability_score,
        NULL AS adaptive_capacity_score,
        NULL AS sensitivity_score
    FROM modelled.ccra_impactchain_indicator
    GROUP BY impact_id, actor_id
),
risk_scores AS (
    SELECT
        impact_id,
        actor_id,
        hazard_score * exposure_score * vulnerability_score AS risk_score,
        hazard_score,
        exposure_score,
        vulnerability_score,
        adaptive_capacity_score,
        sensitivity_score
    FROM raw_risk
),
percentiles AS (
    SELECT
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY risk_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY risk_score) AS upper_limit
    FROM risk_scores 
),
risk_scaled AS (
    SELECT
        rs.impact_id,
        rs.actor_id,
        CASE
            WHEN rs.risk_score < p.lower_limit THEN p.lower_limit
            WHEN rs.risk_score > p.upper_limit THEN p.upper_limit
            ELSE rs.risk_score
        END AS adjusted_risk_score,
        p.lower_limit as risk_lower_limit,
        p.upper_limit as risk_upper_limit,
        hazard_score,
        exposure_score,
        vulnerability_score,
        adaptive_capacity_score,
        sensitivity_score
    FROM risk_scores rs
    CROSS JOIN percentiles p
)
INSERT INTO modelled.ccra_riskassessment (impact_id, actor_id, risk_score, hazard_score, exposure_score, vulnerability_score, adaptive_capacity_score, sensitivity_score, risk_lower_limit, risk_upper_limit)
SELECT 	impact_id,
		actor_id,
		0.01 + ( adjusted_risk_score - risk_lower_limit) * (0.99 - 0.01) / NULLIF( risk_upper_limit - risk_lower_limit, 0) AS risk_score,
		hazard_score,
		exposure_score,
		vulnerability_score,
		adaptive_capacity_score::numeric as adaptive_capacity_score,
		sensitivity_score::numeric as sensitivity_score,
		risk_lower_limit,
		risk_upper_limit
FROM 	risk_scaled
ON CONFLICT (impact_id, actor_id) DO UPDATE SET
    risk_score = excluded.risk_score,
    hazard_score = excluded.hazard_score,
    exposure_score = excluded.exposure_score,
    vulnerability_score = excluded.vulnerability_score,
    adaptive_capacity_score = excluded.adaptive_capacity_score,
    sensitivity_score = excluded.sensitivity_score,
    risk_lower_limit = excluded.risk_lower_limit,
    risk_upper_limit = excluded.risk_upper_limit;