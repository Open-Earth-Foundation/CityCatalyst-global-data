"""Unit tests for v1_aggregate_per_city.py — deterministic, no I/O to real alignment."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "v1_aggregate_per_city.py"
spec = importlib.util.spec_from_file_location("v1_aggregate_per_city", SCRIPT_PATH)
m = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def _write_registry(path: Path, docs: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": "1.0.0", "source_documents": docs}, indent=2),
        encoding="utf-8",
    )


def _write_local_codes(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "region_code",
                "region_name",
                "region_abbreviation",
                "province_code",
                "province_name",
                "commune_code_2018",
                "commune_name",
            ],
        )
        w.writeheader()
        w.writerows(rows)


def _card(pid: str, aid: str, score: float, level: str, region: str, commune: str, rel: str, mq: str = "moderate") -> dict:
    return {
        "schema_version": "1.0.0",
        "action_id": aid,
        "action_name": f"Action {aid}",
        "source_document_id": pid,
        "source_name": pid,
        "source_level": level,
        "region_code": region,
        "communal_code": commune,
        "policy_score": score,
        "match_count": 1,
        "top_relation_type": rel,
        "match_quality": mq,
        "matched_signals": [],
    }


def test_national_applies_everywhere() -> None:
    doc = {
        "source_document_id": "nat1",
        "source_level": "national",
        "region_code": "00",
        "document_status": "final",
        "access_type": "pdf",
    }
    assert m.policy_applies_to_commune(doc, "08101", "08")
    assert m.policy_applies_to_commune(doc, "13101", "13")


def test_regional_only_same_region() -> None:
    doc = {
        "source_document_id": "reg8",
        "source_level": "regional",
        "region_code": "08",
        "document_status": "final",
        "access_type": "pdf",
    }
    assert m.policy_applies_to_commune(doc, "08101", "08")
    assert not m.policy_applies_to_commune(doc, "13101", "13")


def test_municipal_code_match() -> None:
    doc = {
        "source_document_id": "mun",
        "source_level": "municipal",
        "region_code": "05",
        "communal_code": "05108",
        "document_status": "final",
        "access_type": "pdf",
    }
    assert m.policy_applies_to_commune(doc, "05108", "05")
    assert not m.policy_applies_to_commune(doc, "05107", "05")


def test_intercommunal_multi_comuna() -> None:
    doc = {
        "source_document_id": "ic",
        "source_level": "intercommunal",
        "region_code": "99",
        "communal_code": "05107, 05108",
        "document_status": "final",
        "access_type": "pdf",
    }
    assert m.policy_applies_to_commune(doc, "05107", "05")
    assert m.policy_applies_to_commune(doc, "05108", "05")
    assert not m.policy_applies_to_commune(doc, "08101", "08")


def test_weighted_city_score_regional_counts_more() -> None:
    cards = [
        _card("nat", "a1", 0.5, "national", "00", "", "supports"),
        _card("reg", "a1", 0.5, "regional", "08", "", "supports"),
    ]
    reg = {
        "nat": {"source_document_id": "nat", "source_level": "national", "source_name": "N", "region_code": "00", "document_status": "final", "access_type": "pdf"},
        "reg": {"source_document_id": "reg", "source_level": "regional", "source_name": "R", "region_code": "08", "document_status": "final", "access_type": "pdf"},
    }
    commune = {
        "region_code": "08",
        "region_name": "Biobío",
        "commune_code_2018": "08101",
        "commune_name": "Concepción",
    }
    applicable = m.applicable_policies_for_commune(reg, "08101", "08")
    app_ids = {p["source_document_id"] for p in applicable}
    sup = m.build_supporting_entries(cards, app_ids, reg)
    assert m.compute_city_score(sup) == pytest.approx((0.5 * 1.0 + 0.5 * 2.0) / 3.0)


def test_has_local_evidence() -> None:
    sup = [{"source_level": "national"}, {"source_level": "regional"}]
    assert m.has_local_evidence(sup)
    assert not m.has_local_evidence([{"source_level": "national"}])


def test_top_relation_tie_break() -> None:
    assert m.top_relation_from_supporting(["prioritizes", "supports", "supports"]) == "supports"


def test_zero_supporting_no_payload() -> None:
    reg = {
        "p1": {"source_document_id": "p1", "source_level": "national", "source_name": "P1", "region_code": "00", "document_status": "final", "access_type": "pdf"},
    }
    commune = {
        "region_code": "13",
        "region_name": "RM",
        "commune_code_2018": "13101",
        "commune_name": "Santiago",
    }
    summary, payloads, _idx = m.aggregate_one_city(commune, [], reg, {})
    assert payloads == []
    assert summary["action_count_with_matches"] == 0


def test_summary_top_actions_order() -> None:
    reg = {
        "n": {"source_document_id": "n", "source_level": "national", "source_name": "Nat", "region_code": "00", "document_status": "final", "access_type": "pdf"},
    }
    cards = [
        _card("n", "low", 0.4, "national", "00", "", "supports"),
        _card("n", "high", 0.9, "national", "00", "", "targets"),
    ]
    commune = {
        "region_code": "08",
        "region_name": "Biobío",
        "commune_code_2018": "08101",
        "commune_name": "Concepción",
    }
    actions = {"low": {"action_name": "L"}, "high": {"action_name": "H"}}
    summary, _, _ = m.aggregate_one_city(commune, cards, reg, actions)
    tops = summary["top_actions"]
    assert tops[0]["action_id"] == "high"
    assert tops[1]["action_id"] == "low"


def test_aggregate_writes_files(tmp_path: Path) -> None:
    root = tmp_path / "v2"
    (root / "data/registry").mkdir(parents=True)
    _write_registry(
        root / "data/registry/source_documents.json",
        [
            {
                "source_document_id": "pol_nat",
                "source_name": "National Plan",
                "source_level": "national",
                "region_code": "00",
                "document_status": "final",
                "access_type": "pdf",
            },
        ],
    )
    _write_local_codes(
        root / "data/registry/local_codes.csv",
        [
            {
                "region_code": "08",
                "region_name": "Biobío",
                "region_abbreviation": "BIO",
                "province_code": "081",
                "province_name": "Concepción",
                "commune_code_2018": "08101",
                "commune_name": "Concepción",
            },
        ],
    )
    align = root / "data/policy_action_alignment"
    align.mkdir(parents=True)
    sub = align / "pol_nat"
    sub.mkdir(parents=True, exist_ok=True)
    c = _card("pol_nat", "act1", 0.8, "national", "00", "", "supports")
    (sub / "act1.json").write_text(json.dumps(c, indent=2), encoding="utf-8")
    with open(align / "_index.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "source_document_id",
                "action_id",
                "policy_score",
                "match_count",
                "top_relation_type",
                "source_level",
                "region_code",
                "communal_code",
            ],
        )
        w.writeheader()
        w.writerow(
            {
                "source_document_id": "pol_nat",
                "action_id": "act1",
                "policy_score": "0.8",
                "match_count": "1",
                "top_relation_type": "supports",
                "source_level": "national",
                "region_code": "00",
                "communal_code": "",
            }
        )
    (root / "data/derived").mkdir(parents=True)
    with open(root / "data/derived/actions_profiled.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["action_id", "action_name"])
        w.writeheader()
        w.writerow({"action_id": "act1", "action_name": "Test"})

    out = root / "data/city_action_alignment"
    assert (
        m.main(
            [
                "aggregate",
                "--root",
                str(root),
                "--alignment-dir",
                str(align),
                "--output-dir",
                str(out),
                "--only-city",
                "08101",
                "--force",
            ]
        )
        == 0
    )
    assert (out / "08101" / "_city_summary.json").is_file()
    assert (out / "08101" / "act1.json").is_file()


def test_top_n_limits_files(tmp_path: Path) -> None:
    root = tmp_path / "v3"
    (root / "data/registry").mkdir(parents=True)
    _write_registry(
        root / "data/registry/source_documents.json",
        [
            {
                "source_document_id": "pol_nat",
                "source_name": "National Plan",
                "source_level": "national",
                "region_code": "00",
                "document_status": "final",
                "access_type": "pdf",
            },
        ],
    )
    _write_local_codes(
        root / "data/registry/local_codes.csv",
        [
            {
                "region_code": "08",
                "region_name": "Biobío",
                "region_abbreviation": "BIO",
                "province_code": "081",
                "province_name": "X",
                "commune_code_2018": "08101",
                "commune_name": "Concepción",
            },
        ],
    )
    align = root / "data/policy_action_alignment"
    align.mkdir(parents=True)
    sub = align / "pol_nat"
    sub.mkdir(parents=True, exist_ok=True)
    for aid, sc in [("a1", 0.9), ("a2", 0.5)]:
        (sub / f"{aid}.json").write_text(
            json.dumps(_card("pol_nat", aid, sc, "national", "00", "", "supports")),
            encoding="utf-8",
        )
    with open(align / "_index.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "source_document_id",
                "action_id",
                "policy_score",
                "match_count",
                "top_relation_type",
                "source_level",
                "region_code",
                "communal_code",
            ],
        )
        w.writeheader()
        for aid, sc in [("a1", "0.9"), ("a2", "0.5")]:
            w.writerow(
                {
                    "source_document_id": "pol_nat",
                    "action_id": aid,
                    "policy_score": sc,
                    "match_count": "1",
                    "top_relation_type": "supports",
                    "source_level": "national",
                    "region_code": "00",
                    "communal_code": "",
                }
            )
    (root / "data/derived").mkdir(parents=True)
    with open(root / "data/derived/actions_profiled.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["action_id", "action_name"])
        w.writeheader()
        w.writerow({"action_id": "a1", "action_name": "A1"})
        w.writerow({"action_id": "a2", "action_name": "A2"})

    out = root / "data/out"
    assert (
        m.main(
            [
                "aggregate",
                "--root",
                str(root),
                "--alignment-dir",
                str(align),
                "--output-dir",
                str(out),
                "--only-city",
                "08101",
                "--top-n",
                "1",
                "--force",
            ]
        )
        == 0
    )
    assert (out / "08101" / "a1.json").is_file()
    assert not (out / "08101" / "a2.json").is_file()
