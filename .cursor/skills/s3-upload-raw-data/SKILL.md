---
name: s3-upload-raw-data
description: Generates aws s3 cp commands to upload raw_data files from dataset-review/reviews/ to s3://test-global-api/raw_data/, dropping the sample/ folder from the S3 path. Use when the user asks to upload raw data files to S3, generate S3 upload commands, or deploy dataset review samples to the raw_data bucket.
---

# S3 Upload — Raw Data Files

Generates `aws s3 cp` commands to upload `raw_data*` files from the local review folder to S3.

## Path mapping rules

| Component | Local | S3 |
|-----------|-------|----|
| Root | `dataset-review/reviews/` | `s3://test-global-api/raw_data/` |
| Publisher + dataset + release | preserved as-is | preserved as-is |
| `sample/` subfolder | present locally | **dropped** in S3 path |

**Pattern:**
```
dataset-review/reviews/{publisher}/{dataset-id}/releases/{version}/sample/raw_data_*
→ s3://test-global-api/raw_data/{publisher}/{dataset-id}/releases/{version}/raw_data_*
```

## Steps

1. Find all `raw_data*` files under `dataset-review/reviews/`:
   ```bash
   find dataset-review/reviews -name "raw_data*"
   ```

2. For each file, generate an `aws s3 cp` command dropping `sample/` from the S3 destination.

3. Output all commands for the user to review and run. Do not execute them.

## Example output

```bash
# cl-ine-censo
aws s3 cp \
  "dataset-review/reviews/cl-ine/cl-ine-censo/releases/2024/sample/raw_data_cl_ine_censo.csv" \
  "s3://test-global-api/raw_data/cl-ine/cl-ine-censo/releases/2024/raw_data_cl_ine_censo.csv"

# uncece-unlocode
aws s3 cp \
  "dataset-review/reviews/uncece/uncece-unlocode/releases/2024/sample/raw_data_uncece_unlocode.gpkg" \
  "s3://test-global-api/raw_data/uncece/uncece-unlocode/releases/2024/raw_data_uncece_unlocode.gpkg"

# cl-ocha-ab
aws s3 cp \
  "dataset-review/reviews/ocha-rolac/cl-ocha-ab/releases/2021/sample/raw_data_cl_ocha_ab.gpkg" \
  "s3://test-global-api/raw_data/ocha-rolac/cl-ocha-ab/releases/2021/raw_data_cl_ocha_ab.gpkg"
```

## Notes

- Run commands from the repo root (`CityCatalyst-global-data/`)
- Verify AWS credentials first: `aws sts get-caller-identity`
- Use individual `cp` commands (not `sync`) — source and destination paths differ due to the dropped `sample/` segment
- Add `--dryrun` to any command to preview without uploading
