"""DEPRECATED — superseded by per-source ingestion blocks.

This single looping loader was replaced by one thin ingestion block per source
(`load_<dataset_key>_finance_from_s3.py`) feeding the integration transformer
(`transformers/merge_finance_opportunity.py`), per the "one ingestion block per
source" rule in engineering-standards/pipeline-design-patterns.md. It is no longer
referenced by the pipeline DAG and can be deleted.
"""
