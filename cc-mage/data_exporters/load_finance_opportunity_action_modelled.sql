-- raw_data.finance_opportunity_action_staging -> modelled.finance_opportunity_action
-- opportunity_id is MD5 of source_opportunity_id and the source release_id, matching
-- finance_opportunity. Joining finance_opportunity keeps it FK-safe (only existing funds).
-- Idempotent: delete the affected releases then insert. Runs after finance_opportunity loads.

DELETE FROM modelled.finance_opportunity_action
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.finance_source_catalog);

INSERT INTO modelled.finance_opportunity_action (
    opportunity_id, action_id, mapping_source, confidence, rationale, release_id
)
SELECT
    fo.opportunity_id,
    NULLIF(TRIM(s.action_id), ''),
    NULLIF(TRIM(s.mapping_source), ''),
    NULLIF(TRIM(s.confidence), ''),
    NULLIF(TRIM(s.rationale), ''),
    c.release_id::UUID
FROM raw_data.finance_opportunity_action_staging s
JOIN raw_data.finance_source_catalog c ON c.source_dataset = s.source_dataset
JOIN modelled.finance_opportunity fo
  ON fo.opportunity_id = MD5(CONCAT_WS('-', s.source_opportunity_id, c.release_id::TEXT))::UUID
WHERE NULLIF(TRIM(s.action_id), '') IS NOT NULL;
