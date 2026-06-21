# S3 upload — the two stages

## One dataset per upload — never pre-aggregate

Upload **each source dataset on its own**, under its own naming-convention path.
Do **not** merge multiple sources into one combined file before uploading — that
makes refreshing a single source mean regenerating the whole blob and muddies
per-row provenance. Cleaning/analysis is per-dataset (review stage); the
**integration of several sources happens inside the pipeline** (one loader per
source reading its own S3 file → a merge transformer; see
`pipeline-design-patterns.md` → "Multiple Sources"). If a pipeline draws on ten
reviews, that is ten uploads and ten reads, unioned in the pipeline — not one
pre-built file.

A pipeline reads from S3, not from the repo. Put the data in **two** stages
(snake_case paths per `naming-conventions.md`, deriving `publisher_key`/`dataset_key`
by replacing `-` with `_`):

| Stage | What goes here | Path pattern |
|---|---|---|
| `files/` | the original source file(s), as retrieved | `s3://test-global-api/files/<publisher_key>/<dataset_key>/release/<version>/<dataset_key>_<domain>.<ext>` |
| `raw_data/` | the cleaned, tidy release data the loader reads | `s3://test-global-api/raw_data/<publisher_key>/<dataset_key>/release/<version>/<dataset_key>_<domain>.parquet` |

The local review folder holds both; the `sample/` segment present locally is
**dropped** in the S3 path.

## Generate the commands (do not execute)

1. Verify credentials: `aws sts get-caller-identity`
2. Find the files: `find dataset-review/reviews/<publisher>/<dataset> -name "raw_data*" -o -name "files*"`
3. Emit one `aws s3 cp` per file, dropping `sample/`, and present them for the human to run. Use individual `cp` (not `sync`) — source and destination differ by the dropped segment. Add `--dryrun` to preview.

```bash
# source file -> files/ stage
aws s3 cp \
  "dataset-review/reviews/cl-mma/cl-mma-fondos/releases/v1/sample/files_cl_mma_fondos.html" \
  "s3://test-global-api/files/cl_mma/cl_mma_fondos/release/v1/cl_mma_fondos.html"

# cleaned data -> raw_data/ stage
aws s3 cp \
  "dataset-review/reviews/cl-mma/cl-mma-fondos/releases/v1/sample/raw_data_cl_mma_fondos.parquet" \
  "s3://test-global-api/raw_data/cl_mma/cl_mma_fondos/release/v1/cl_mma_fondos.parquet"
```

## Notes

- Run from the repo root (`CityCatalyst-global-data/`).
- The `source_path` the pipeline uses (a `metadata.yaml` variable) is the S3 key
  **relative to the bucket**, e.g. `raw_data/cl_mma/cl_mma_fondos/release/v1/cl_mma_fondos.parquet`.
- Bucket is environment config, never hardcoded in block code.

> Absorbed: this replaces the standalone `s3-upload-raw-data` skill, adding the
> `files/` stage alongside `raw_data/`.
