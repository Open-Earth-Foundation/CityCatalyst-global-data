"""Shape the raw INDAP fund->action rows for raw_data.finance_opportunity_action_staging.

Takes the raw mapping rows (from load_finance_opportunity_action_from_s3) and produces the
columns the modelled SQL expects: source_opportunity_id (derived the same way as the supply
pipeline, so opportunity_id matches), action_id, mapping_source, confidence, rationale,
source_dataset. Keeps only rows that actually carry an action_id.
"""
import re
import unicodedata

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer

SOURCE = "cl-indap/cl-indap-fondos"


def _slug(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:120]


@transformer
def transform(df, *args, **kwargs):
    df = df.where(pd.notna(df), None)
    rows = []
    for _, r in df.iterrows():
        action_id = (str(r.get("action_id") or "")).strip()
        name = (str(r.get("program_name") or "")).strip()
        if not action_id or not name:
            continue
        rows.append({
            "source_dataset": SOURCE,
            "source_opportunity_id": f"cl-indap-{_slug(name)}",
            "action_id": action_id,
            "mapping_source": "indap-review",
            "confidence": (str(r.get("mapping_confidence") or "").strip() or None),
            "rationale": (str(r.get("rationale") or "").strip() or None),
        })
    out = pd.DataFrame(rows)
    print(f"finance_opportunity_action: {len(out)} fund->action pairs from {SOURCE}")
    return out
