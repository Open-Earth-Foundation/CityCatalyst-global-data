-- raw_data.finance_project_action_staging -> modelled.finance_project_action
-- project_id is MD5 of source_project_id and the source release_id, matching finance_project.
-- Joining finance_project keeps it FK-safe (only existing projects). Idempotent: delete the
-- affected releases then insert. Runs after finance_project loads.
-- ids: project_action_id = MD5(project_id-action_id-mapping_source).

DELETE FROM modelled.finance_project_action
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.finance_project_catalog);

INSERT INTO modelled.finance_project_action (
    project_action_id, project_id, action_id, mapping_source, confidence, rationale, release_id
)
SELECT
    MD5(CONCAT_WS('-', fp.project_id::TEXT, NULLIF(TRIM(s.action_id), ''), NULLIF(TRIM(s.mapping_source), '')))::UUID,
    fp.project_id,
    NULLIF(TRIM(s.action_id), ''),
    NULLIF(TRIM(s.mapping_source), ''),
    NULLIF(TRIM(s.confidence), ''),
    NULLIF(TRIM(s.rationale), ''),
    c.release_id::UUID
FROM raw_data.finance_project_action_staging s
JOIN raw_data.finance_project_catalog c ON c.source_dataset = s.source_dataset
JOIN modelled.finance_project fp
  ON fp.project_id = MD5(CONCAT_WS('-', s.source_project_id, c.release_id::TEXT))::UUID
WHERE NULLIF(TRIM(s.action_id), '') IS NOT NULL;
