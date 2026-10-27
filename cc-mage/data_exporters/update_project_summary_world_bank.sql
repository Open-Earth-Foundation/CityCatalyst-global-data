WITH release_ctx AS (
    SELECT dr.release_id
    FROM modelled.dataset_release dr
    WHERE dr.dataset_id = MD5(CONCAT_WS('-', 'world-bank-projects', 'World Bank Projects API', 'https://search.worldbank.org/api/v2/projects'))::UUID
    ORDER BY dr.is_latest DESC, dr.released_at DESC NULLS LAST, dr.retrieved_at DESC NULLS LAST
    LIMIT 1
),
synth AS (
    SELECT
        s.source_project_id::TEXT AS source_project_id,
        CASE
            WHEN to_jsonb(s) ? 'synthesis_json'
                 AND NULLIF(to_jsonb(s)->>'synthesis_json', '') IS NOT NULL
            THEN (to_jsonb(s)->>'synthesis_json')::JSONB
            ELSE NULL
        END AS synthesis
    FROM raw_data.world_bank_project_synthesis_enriched_staging s
    WHERE s.source_project_id IS NOT NULL
      AND COALESCE(
          NULLIF(to_jsonb(s)->>'status', ''),
          NULLIF(to_jsonb(s)->>'_status', '')
      ) IN ('synthesized', 'skipped_existing_synthesis')
),
upsert_portfolio AS (
    INSERT INTO modelled.project_portfolio (
        project_id,
        source_name,
        source_project_id,
        source_project_url,
        project_name,
        release_id,
        updated_at
    )
    SELECT
        MD5(CONCAT_WS('-', 'world_bank', s.source_project_id))::UUID AS project_id,
        'world_bank' AS source_name,
        s.source_project_id AS source_project_id,
        NULL::TEXT AS source_project_url,
        COALESCE(NULLIF(s.synthesis->>'projectTitle', ''), s.source_project_id) AS project_name,
        rc.release_id,
        NOW() AS updated_at
    FROM synth s
    JOIN release_ctx rc ON TRUE
    WHERE s.synthesis IS NOT NULL
    ON CONFLICT (project_id)
    DO UPDATE SET
        source_name = EXCLUDED.source_name,
        source_project_id = EXCLUDED.source_project_id,
        project_name = COALESCE(EXCLUDED.project_name, modelled.project_portfolio.project_name),
        release_id = EXCLUDED.release_id,
        updated_at = NOW()
    RETURNING project_id, source_project_id, project_name
),
portfolio AS (
    SELECT
        p.project_id,
        p.source_project_id::TEXT AS source_project_id,
        p.project_name
    FROM modelled.project_portfolio p
    WHERE p.source_name = 'world_bank'
)
INSERT INTO modelled.project_summary (
    project_summary_id,
    project_id,
    source_project_id,
    project_title,
    funder_id,
    funder_name,
    country_name,
    country_code,
    region_name,
    city_name,
    project_type,
    sector_name,
    subsector_name,
    approval_at,
    closing_at,
    project_status,
    total_budget_amount_usd,
    primary_funder_amount_usd,
    financing_instrument,
    project_summary_text,
    lessons_learned,
    synthesis_notes,
    site_context,
    financing_structure,
    data_completeness,
    actions_implemented,
    key_risks,
    evidence_anchors,
    secondary_project_types,
    co_financiers,
    co_benefits,
    key_interventions,
    replicability_conditions,
    model_metadata,
    release_id,
    updated_at
)
SELECT
    MD5(CONCAT_WS('-', 'world_bank', pf.source_project_id, 'project_summary'))::UUID AS project_summary_id,
    pf.project_id,
    pf.source_project_id,
    COALESCE(NULLIF(s.synthesis->>'projectTitle', ''), pf.project_name) AS project_title,
    COALESCE(NULLIF(s.synthesis->>'funderId', ''), 'world_bank') AS funder_id,
    COALESCE(NULLIF(s.synthesis->>'funderName', ''), 'World Bank') AS funder_name,
    NULLIF(s.synthesis->>'country', '') AS country_name,
    NULLIF(s.synthesis->>'countryCode', '') AS country_code,
    NULLIF(s.synthesis->>'region', '') AS region_name,
    NULLIF(s.synthesis->>'city', '') AS city_name,
    NULLIF(s.synthesis->>'projectType', '') AS project_type,
    NULLIF(s.synthesis->>'sector', '') AS sector_name,
    NULLIF(s.synthesis->>'subsector', '') AS subsector_name,
    NULLIF(s.synthesis->>'approvalDate', '')::TIMESTAMPTZ AS approval_at,
    NULLIF(s.synthesis->>'closingDate', '')::TIMESTAMPTZ AS closing_at,
    NULLIF(s.synthesis->>'projectStatus', '') AS project_status,
    NULLIF(s.synthesis->>'totalBudgetUsd', '')::NUMERIC AS total_budget_amount_usd,
    NULLIF(s.synthesis->>'primaryFunderAmountUsd', '')::NUMERIC AS primary_funder_amount_usd,
    NULLIF(s.synthesis->>'financingInstrument', '') AS financing_instrument,
    NULLIF(s.synthesis->>'projectSummary', '') AS project_summary_text,
    NULLIF(s.synthesis->>'lessonsLearned', '') AS lessons_learned,
    NULLIF(s.synthesis->>'synthesisNotes', '') AS synthesis_notes,
    COALESCE(s.synthesis->'siteContext', '{}'::JSONB) AS site_context,
    COALESCE(s.synthesis->'financingStructure', '{}'::JSONB) AS financing_structure,
    COALESCE(s.synthesis->'dataCompleteness', '{}'::JSONB) AS data_completeness,
    COALESCE(s.synthesis->'actionsImplemented', '[]'::JSONB) AS actions_implemented,
    COALESCE(s.synthesis->'keyRisks', '[]'::JSONB) AS key_risks,
    COALESCE(s.synthesis->'evidenceAnchors', '[]'::JSONB) AS evidence_anchors,
    COALESCE(s.synthesis->'secondaryProjectTypes', '[]'::JSONB) AS secondary_project_types,
    COALESCE(s.synthesis->'coFinanciers', '[]'::JSONB) AS co_financiers,
    COALESCE(s.synthesis->'coBenefits', '[]'::JSONB) AS co_benefits,
    COALESCE(s.synthesis->'keyInterventions', '[]'::JSONB) AS key_interventions,
    COALESCE(s.synthesis->'replicabilityConditions', '[]'::JSONB) AS replicability_conditions,
    COALESCE(s.synthesis->'_meta', '{}'::JSONB) AS model_metadata,
    rc.release_id,
    NOW() AS updated_at
FROM synth s
JOIN portfolio pf
  ON pf.source_project_id = s.source_project_id
JOIN release_ctx rc ON TRUE
WHERE s.synthesis IS NOT NULL
ON CONFLICT (project_id)
DO UPDATE SET
    source_project_id = EXCLUDED.source_project_id,
    project_title = EXCLUDED.project_title,
    funder_id = EXCLUDED.funder_id,
    funder_name = EXCLUDED.funder_name,
    country_name = EXCLUDED.country_name,
    country_code = EXCLUDED.country_code,
    region_name = EXCLUDED.region_name,
    city_name = EXCLUDED.city_name,
    project_type = EXCLUDED.project_type,
    sector_name = EXCLUDED.sector_name,
    subsector_name = EXCLUDED.subsector_name,
    approval_at = EXCLUDED.approval_at,
    closing_at = EXCLUDED.closing_at,
    project_status = EXCLUDED.project_status,
    total_budget_amount_usd = EXCLUDED.total_budget_amount_usd,
    primary_funder_amount_usd = EXCLUDED.primary_funder_amount_usd,
    financing_instrument = EXCLUDED.financing_instrument,
    project_summary_text = EXCLUDED.project_summary_text,
    lessons_learned = EXCLUDED.lessons_learned,
    synthesis_notes = EXCLUDED.synthesis_notes,
    site_context = EXCLUDED.site_context,
    financing_structure = EXCLUDED.financing_structure,
    data_completeness = EXCLUDED.data_completeness,
    actions_implemented = EXCLUDED.actions_implemented,
    key_risks = EXCLUDED.key_risks,
    evidence_anchors = EXCLUDED.evidence_anchors,
    secondary_project_types = EXCLUDED.secondary_project_types,
    co_financiers = EXCLUDED.co_financiers,
    co_benefits = EXCLUDED.co_benefits,
    key_interventions = EXCLUDED.key_interventions,
    replicability_conditions = EXCLUDED.replicability_conditions,
    model_metadata = EXCLUDED.model_metadata,
    release_id = EXCLUDED.release_id,
    updated_at = NOW();
