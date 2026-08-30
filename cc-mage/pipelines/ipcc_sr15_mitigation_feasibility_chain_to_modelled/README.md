# IPCC SR1.5 mitigation feasibility chain pipeline

This pipeline replaces the database rows for the configured release with the complete
`scoring_chain.csv` stored in S3. The production database release label remains `2018`;
the new one-channel methodology replaces the earlier rows in place.

## API trigger

Mage synchronizes `triggers.yaml` into its pipeline-schedule database. After the
trigger appears in the Mage UI, retrieve its numeric schedule ID and generated token
from the trigger page or from:

```text
GET /api/pipelines/ipcc_sr15_mitigation_feasibility_chain_to_modelled/pipeline_schedules
```

Run the pipeline with:

```text
POST /api/pipeline_schedules/{pipeline_schedule_id}/pipeline_runs/{token}
Content-Type: application/json
```

For example:

```bash
curl --request POST \
  "https://<mage-host>/api/pipeline_schedules/{pipeline_schedule_id}/pipeline_runs/{token}" \
  --header "Content-Type: application/json" \
  --data @request.json
```

Save the request body as `request.json`:

```json
{
  "pipeline_run": {
    "variables": {
      "bucket_name": "test-global-api",
      "expected_action_count": 86,
      "expected_active_bridge_count": 373,
      "expected_row_count": 1895,
      "scoring_chain_key": "raw_data/ipcc/ipcc-sr15-mitigation-feasibility/releases/2018-v2/data/scoring_chain.csv",
      "source_url": "s3://test-global-api/raw_data/ipcc/ipcc-sr15-mitigation-feasibility/releases/2018-v2/data/scoring_chain.csv",
      "source_release_label": "2018-v2",
      "version_label": "2018"
    }
  }
}
```

The trigger supplies these values as defaults, so the body may be omitted when the
default object is being reloaded. Keep `version_label` as `2018` for the in-place
replacement. `source_release_label` validates the methodology label embedded in the
CSV independently of the database release label. Runtime variables override the
trigger and pipeline defaults.

The three expected-count variables are hard structural checks for this uploaded
artifact. Update them only when a deliberately regenerated replacement changes those
counts.

The trigger rejects overlapping runs because the pipeline uses a shared staging table
and performs a full release replacement.

A successful response contains a top-level `pipeline_run`. Treat a top-level `error`
as a failed request even if the installed Mage build returns HTTP 200 for that error.
