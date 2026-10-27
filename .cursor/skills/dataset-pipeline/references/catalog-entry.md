# Catalog entry — index.yaml release

Add/update the dataset in `dataset-review/catalog/index.yaml`. The full field list
is in `engineering-standards/documentation-and-metadata.md`; the gating subset is in
`definition-of-done.md`. This is the shape to fill — **note there is no `themes` key**
(themes are assigned in `dataset-review/collections/`, not here).

```yaml
- id: <publisher>-<dataset>                 # canonical slug, e.g. cl-mma-fondos
  name: <Human readable dataset name>
  # dataset_url = the AUTHORITATIVE SOURCE where a person can verify the data
  # (publisher page or API endpoint, e.g. https://www.ine.gob.cl/… or http://api.gcfund.org/v1/projects).
  # NOT the transformed-data / S3 / GitHub-review location. For a derived dataset that
  # integrates several sources with no single origin, set it to null and rely on the
  # per-row source_url + each source's own catalog entry for verification.
  dataset_url: <authoritative source url | null>
  publisher:
    id: <publisher-slug>
    name: <Publisher name>
    url: <publisher url>
  description: >
    <2–3 lines: what the dataset is and the city-relevant content.>
  coverage:
    geography: country | region | global
    countries: [CL]
    spatial_levels: [country, region, comuna]
  update_frequency: <annual | irregular | ongoing | one-off>
  priority: <high | medium | low>
  releases:
    - version: "<v1 | 2024 | …>"           # matches metadata.yaml version_label
      version_number: 1                     # increment per release; flip prior is_latest:false
      source_url: <where the source was retrieved>
      released_at: <YYYY-MM-DD | null>
      retrieved_at: <YYYY-MM-DD>
      retrieval_method: <api | manual_download | scrape>
      path: "reviews/<publisher>/<dataset>/releases/<version>"
      is_latest: true
      production_approved: false            # human flips to true only after Step 4
      pipeline_name: <prefix>_<source>_<description>   # set in Step 3
      pipeline_version: "<v1>"
      methodology_url: <publisher methodology page>
      internal_review_url: <Notion review url>
      license:
        id: <SPDX id, e.g. CC-BY-4.0>
        name: <license name>
        url: <license url>
        commercial_use: <true | false | unresolved>
        note: "<terms as actually stated; confirm per release>"
      data_quality:                          # all six scored per release, not copied forward
        documentation: <0-5 | null>
        methodology: <0-5 | null>
        coverage: <0-5 | null>
        granularity: <0-5 | null>
        freshness: <0-5 | null>
        accessibility: <0-5 | null>
```

After editing, regenerate the collection views and verify they're in sync:

```bash
python .cursor/skills/dataset-themes/references/group_by_theme.py
python .cursor/skills/dataset-themes/references/group_by_theme.py --check
```

> Migration note: theme assignment is moving out of `index.yaml` into
> `collections/`. Until `group_by_theme.py` is reworked to read themes from the
> collections, omit `themes` from new entries; do not reintroduce it.
