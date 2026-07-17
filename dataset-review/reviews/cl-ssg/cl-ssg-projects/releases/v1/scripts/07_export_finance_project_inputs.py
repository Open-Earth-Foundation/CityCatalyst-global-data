"""Build and validate the two S3 inputs for ``cl_finance_project_to_modelled``.

The Mage pipeline loads every BIP project into ``modelled.finance_project`` and
reads a separate project-to-action link file into
``modelled.finance_project_action``.  The candidate matcher deliberately
retains several ranked candidates for QA.  Those candidates are not all
appropriate production links: a rank-5, outcome-only public-transport action,
for example, is not evidence that a cycleway project implemented that action.

This export retains rank-1 ``strong`` matches as a baseline, removes known
semantic false positives, and adds only individually reviewed similar-project
links.  It does not turn the rest of the matcher candidates into precedents.

Inputs (regenerate the matcher first):
  data/derived/projects_profiled.csv
  data/derived/project_action_matches.csv
  data/derived/actions_profiled.csv

Outputs:
  data/pipeline/cl_ssg_projects.csv
  data/pipeline/cl_ssg_projects_action_matches.csv
  data/pipeline/action_precedent_audit.csv
  data/pipeline/manifest.json

Usage:
  python scripts/06_match_to_actions.py
  python scripts/07_export_finance_project_inputs.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DERIVED = ROOT / "data" / "derived"
DEFAULT_OUT = ROOT / "data" / "pipeline"

PROJECTS = DERIVED / "projects_profiled.csv"
MATCHES = DERIVED / "project_action_matches.csv"
ACTIONS = DERIVED / "actions_profiled.csv"

PROJECT_OUT = "cl_ssg_projects.csv"
MATCH_OUT = "cl_ssg_projects_action_matches.csv"
MANIFEST_OUT = "manifest.json"
AUDIT_OUT = "action_precedent_audit.csv"
MATCH_COLUMNS = ["codigo_bip", "action_id", "label", "rationale"]

# The facet matcher makes these rank-1 links look strong, but the project
# title/narrative describes a different intervention. Keep the exclusions
# explicit rather than teaching a source-specific exception into the matcher.
REJECTED_PRIMARY_PAIRS = {
    ("30136287-0", "icare_0016"): "ERNC self-supply for SMEs is not solar thermal or heat-pump water heating.",
    ("30397477-0", "icare_0024"): "Wind/solar technology transfer does not establish a municipal water-system intervention.",
    ("30123598-0", "icare_0053"): "Composting training is not a voluntary-waste-collector cooperative programme.",
    ("30116875-0", "ipcc_0068"): "Native-forest management is not bioenergy with carbon capture.",
    ("30129207-0", "ipcc_0068"): "Native-forest management is not bioenergy with carbon capture.",
    ("30283372-0", "ipcc_0068"): "Waste valorisation has no evidence of carbon capture.",
    ("30318723-0", "ipcc_0068"): "Native-forest management is not bioenergy with carbon capture.",
    ("30326072-0", "ipcc_0068"): "Firewood-development work is not bioenergy with carbon capture.",
    ("30367333-0", "ipcc_0068"): "Forestation is not bioenergy with carbon capture.",
    ("30437447-0", "ipcc_0068"): "Forest-resource valorisation is not bioenergy with carbon capture.",
    ("30459304-0", "icare_0049"): "Hydrogen recovery alone does not evidence a regional renewable-energy hub.",
    ("30358325-0", "icare_0040"): "A pedestrian bridge and cycleway does not evidence efficient or solar-powered public lighting.",
    ("30375122-0", "icare_0040"): "Green-space lighting is not evidenced as energy-efficient or solar-powered.",
    ("30399589-0", "icare_0040"): "A regional energy-efficiency programme does not establish a public-lighting intervention.",
    ("30399589-0", "icare_0137"): "A regional energy-efficiency programme does not establish LED public-lighting installation.",
}

# These projects are comparable to the named action but their title/source
# does not establish every action component. Keep their precedent link while
# preventing them from being used as exact-match financial benchmarks.
ACTION_CONFIDENCE_OVERRIDES = {
    "c40_0036": "Landfill construction, closure, or remediation is comparable, but gas capture is not consistently evidenced.",
    "icare_0006": "ERNC self-generation is comparable, but the source does not verify integrated solar-battery microgrids or planning.",
    "icare_0033": "Biogas or wastewater-energy production is related, but the source does not establish biodigesters on rural properties.",
    "icare_0045": "Agronomic biosolids valorisation is comparable, but the source does not establish a regenerative-agriculture programme.",
    "icare_0122": "Waste-treatment and transfer facilities are comparable, but the source does not consistently establish an integrated eco-park.",
    "ipcc_0038": "Solar panels at ZOFRI are comparable, but the source does not establish an industrial-facility intervention.",
    "ipcc_0076": "Mining energy-efficiency work is comparable, but the source does not explicitly document an energy audit.",
    "ipcc_0105": "Cycleway construction supports active mobility, but the source does not establish road-space reallocation.",
}

# These titles establish a useful neighbouring intervention but not every material
# component of the named city action. Preserve them as related examples rather than
# allowing them into the direct "Similar projects" list.
RELATED_PAIR_OVERRIDES = {
    # Solar generation is a direct precedent only where the municipal/public asset is explicit.
    **{
        (code, "icare_0012"): "Photovoltaic generation is comparable, but municipal/public-asset ownership is not evidenced."
        for code in (
            "30113025-0", "30115587-0", "30125568-0", "30132282-0", "30209422-0", "30320823-0",
            "30388028-0", "30396577-0", "30397626-0", "30399972-0", "30413089-0", "30413426-0",
            "30413431-0", "30429623-0", "30436688-0", "30444373-0",
        )
    },
    # Efficiency or replacement alone is not proof that the public-lighting technology is LED.
    ("30117865-0", "icare_0137"): "Energy-efficient public lighting is related, but LED technology is not stated.",
    ("30137337-0", "icare_0137"): "Energy-efficient public lighting is related, but LED technology is not stated.",
    ("30217572-0", "icare_0137"): "Energy-efficient public lighting is related, but LED technology is not stated.",
    ("30389922-0", "icare_0137"): "Public-luminaire replacement is related, but LED technology is not stated.",
    ("30404623-0", "icare_0040"): "Public-luminaire improvement is related, but efficient or solar technology is not stated.",
    ("30404623-0", "icare_0137"): "Public-luminaire improvement is related, but LED technology is not stated.",
    # Nursery production is an upstream input, not evidence that restoration planting occurred.
    ("30394035-0", "ipcc_0053"): "Forest-plant production supports restoration, but does not itself evidence afforestation or restoration work.",
}

# Copy carried through to modelled.finance_project_action.rationale. This is
# deliberately phrased for a city user asking why a project is a useful direct
# precedent, rather than exposing the matcher's internal facet vocabulary.
DIRECT_PRECEDENT_RATIONALES = {
    "c40_0042": "Direct precedent: the project creates or improves urban green space.",
    "icare_0015": "Direct precedent: the project delivers micro-hydro, biogas, or biomass energy.",
    "icare_0033": "Direct precedent: the project produces energy from organic waste or wastewater.",
    "icare_0040": "Direct precedent: the project upgrades public lighting with efficient or solar-powered luminaires.",
    "icare_0137": "Direct precedent: the project installs or replaces public lighting with LED technology.",
    "ipcc_0053": "Direct precedent: the project carries out afforestation, reforestation, or ecosystem restoration.",
    "ipcc_0105": "Direct precedent: the project builds or improves cycling and pedestrian infrastructure.",
}

# These links have been reviewed against project and action titles. They either
# recover a specific near-equivalent action that ranked below another valid
# action, or connect an otherwise-unrepresented action to a clear precedent.
CURATED_ADDITIONAL_MATCHES = [
    # LED / energy-efficient public lighting also evidences the broader lighting action.
    ("30117865-0", "icare_0040", "strong", "Energy-efficient public-lighting replacement."),
    ("30137337-0", "icare_0040", "strong", "Energy-efficient pedestrian public lighting."),
    ("30217572-0", "icare_0040", "strong", "Public-lighting energy-efficiency upgrade."),
    ("30292222-0", "icare_0040", "strong", "LED street-light replacement."),
    ("30369479-0", "icare_0040", "strong", "LED public-lighting construction."),
    ("30374524-0", "icare_0040", "strong", "LED neighbourhood-lighting upgrade."),
    ("30389922-0", "icare_0040", "strong", "Public-lighting replacement in streets and passages."),
    ("30404623-0", "icare_0040", "strong", "Partial public-luminaire upgrade."),
    # Only titles that explicitly identify LED/high-efficiency technology support the LED action.
    ("30157122-0", "icare_0137", "strong", "High-efficiency LED luminaire acquisition."),
    ("30348628-0", "icare_0137", "strong", "Replacement with LED technology."),
    ("30421774-0", "icare_0137", "strong", "LED lighting installation on a cycleway."),
    ("30444175-0", "icare_0137", "strong", "LED luminaire replacement."),
    ("30455924-0", "icare_0137", "strong", "LED lighting installation."),
    # Solar lighting projects can legitimately evidence both public lighting and solar generation.
    ("30135934-0", "icare_0012", "strong", "Solar plant and public-lighting project."),
    ("30137644-0", "icare_0012", "strong", "Photovoltaic luminaires on municipal public assets."),
    # Biogas/wastewater energy projects are valid biomass-energy precedents as well as biodigester links.
    ("30233424-0", "icare_0015", "strong", "Biogas production from organic waste."),
    ("30413079-0", "icare_0015", "strong", "Electricity generation from wastewater."),
    # The project titles explicitly include active-mobility infrastructure.
    ("30358325-0", "ipcc_0105", "strong", "Pedestrian bridge and cycleway project."),
    ("30421774-0", "ipcc_0105", "strong", "Cycleway lighting project."),
    # Action-centred additions: similar projects exist despite a lower facet score.
    ("30459952-0", "c40_0037", "goal_aligned", "Network of recycling drop-off points supports segregated collection."),
    ("30288773-0", "icare_0064", "goal_aligned", "Integrated solid-waste treatment centre is a comparable organic-waste-management precedent."),
    ("30079482-0", "icare_0117", "goal_aligned", "Public-transport corridor directly supports modal shift."),
    ("30437447-0", "ipcc_0054", "goal_aligned", "Forest-resource valorisation programme is a sustainable-forest-management precedent."),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_rank_one_strong(row: dict[str, str]) -> bool:
    return (row.get("rank") or "").strip() == "1" and (row.get("label") or "").strip() == "strong"


def validate(projects: list[dict[str, str]], links: list[dict[str, str]], actions: list[dict[str, str]]) -> None:
    if not projects:
        raise ValueError("project export is empty")
    if not links:
        raise ValueError("action-link export is empty")

    project_ids = [(row.get("codigo_bip") or "").strip() for row in projects]
    if any(not value for value in project_ids):
        raise ValueError("projects contain blank codigo_bip values")
    if len(project_ids) != len(set(project_ids)):
        raise ValueError("projects contain duplicate codigo_bip values")
    if any(not (row.get("nombre") or "").strip() for row in projects):
        raise ValueError("projects contain blank nombre values")

    action_ids = {(row.get("action_id") or "").strip() for row in actions}
    pairs: list[tuple[str, str]] = []
    for row in links:
        code = (row.get("codigo_bip") or "").strip()
        action = (row.get("action_id") or "").strip()
        label = (row.get("label") or "").strip()
        if not code or not action:
            raise ValueError("links contain a blank codigo_bip or action_id")
        if code not in set(project_ids):
            raise ValueError(f"link references a project absent from export: {code}")
        if action not in action_ids:
            raise ValueError(f"link references an action absent from taxonomy: {action}")
        if label not in {"strong", "goal_aligned"}:
            raise ValueError(f"production links must be strong or goal_aligned, found {label!r}")
        pairs.append((code, action))
    if len(pairs) != len(set(pairs)):
        raise ValueError("links contain duplicate (codigo_bip, action_id) pairs")
    rejected = sorted(set(pairs) & set(REJECTED_PRIMARY_PAIRS))
    if rejected:
        raise ValueError(f"links contain explicitly rejected project-action pair(s): {rejected}")


def build_action_audit(actions: list[dict[str, str]], links: list[dict[str, str]]) -> list[dict[str, str]]:
    """One decision row for every action, including deliberately unmatched actions."""
    by_action: dict[str, list[dict[str, str]]] = {}
    for link in links:
        by_action.setdefault(link["action_id"], []).append(link)
    rows = []
    for action in sorted(actions, key=lambda row: (row.get("action_id") or "")):
        action_id = (action.get("action_id") or "").strip()
        matches = by_action.get(action_id, [])
        confidence = Counter(row["label"] for row in matches)
        rows.append({
            "action_id": action_id,
            "action_name": (action.get("action_name") or "").strip(),
            "precedent_status": "matched" if matches else "no_reviewed_bip_precedent",
            "project_link_count": str(len(matches)),
            "strong_link_count": str(confidence.get("strong", 0)),
            "goal_aligned_link_count": str(confidence.get("goal_aligned", 0)),
            "decision": (
                "At least one project passed action-specific semantic review."
                if matches else
                "No BIP project was accepted as a defensible precedent; do not infer one from a broad facet match."
            ),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT, help=f"Output directory (default: {DEFAULT_OUT})")
    args = parser.parse_args()

    projects = read_rows(PROJECTS)
    candidates = read_rows(MATCHES)
    actions = read_rows(ACTIONS)

    required_project_columns = {"codigo_bip", "nombre"}
    required_match_columns = {"codigo_bip", "action_id", "label", "rank"}
    if not required_project_columns <= set(projects[0] if projects else {}):
        raise ValueError(f"projects missing required columns: {sorted(required_project_columns)}")
    if not required_match_columns <= set(candidates[0] if candidates else {}):
        raise ValueError(f"matches missing required columns: {sorted(required_match_columns)}")

    # A matcher direct-link baseline, corrected with the explicit curation
    # table above. All other ranked candidates remain in the QA artefact.
    links = [
        {
            "codigo_bip": (row.get("codigo_bip") or "").strip(),
            "action_id": (row.get("action_id") or "").strip(),
            "label": "strong",
            "rationale": "Rank-1 direct match; outcome and intervention both align.",
        }
        for row in candidates
        if is_rank_one_strong(row)
        and ((row.get("codigo_bip") or "").strip(), (row.get("action_id") or "").strip()) not in REJECTED_PRIMARY_PAIRS
    ]
    links.extend(
        {"codigo_bip": code, "action_id": action, "label": label, "rationale": rationale}
        for code, action, label, rationale in CURATED_ADDITIONAL_MATCHES
    )
    for link in links:
        if link["action_id"] in ACTION_CONFIDENCE_OVERRIDES:
            link["label"] = "goal_aligned"
            link["rationale"] = ACTION_CONFIDENCE_OVERRIDES[link["action_id"]]
        elif (link["codigo_bip"], link["action_id"]) in RELATED_PAIR_OVERRIDES:
            link["label"] = "goal_aligned"
            link["rationale"] = RELATED_PAIR_OVERRIDES[(link["codigo_bip"], link["action_id"])]
        elif link["action_id"] in DIRECT_PRECEDENT_RATIONALES:
            link["rationale"] = DIRECT_PRECEDENT_RATIONALES[link["action_id"]]
    links.sort(key=lambda row: (row["codigo_bip"], row["action_id"]))
    validate(projects, links, actions)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    project_path = out_dir / PROJECT_OUT
    match_path = out_dir / MATCH_OUT
    audit_path = out_dir / AUDIT_OUT
    manifest_path = out_dir / MANIFEST_OUT
    write_rows(project_path, list(projects[0]), projects)
    write_rows(match_path, MATCH_COLUMNS, links)
    audit = build_action_audit(actions, links)
    write_rows(audit_path, list(audit[0]), audit)

    action_counts = Counter(row["action_id"] for row in links)
    manifest = {
        "source_dataset": "cl-ssg/cl-ssg-projects",
        "release_version": "v1",
        "project_action_policy": "rank-1 strong baseline; documented semantic exclusions and curated similar-project additions",
        "excluded_match_count": len(REJECTED_PRIMARY_PAIRS),
        "curated_addition_count": len(CURATED_ADDITIONAL_MATCHES),
        "action_audit": {
            "path": AUDIT_OUT,
            "actions_reviewed": len(audit),
            "actions_with_reviewed_precedent": sum(row["precedent_status"] == "matched" for row in audit),
            "actions_without_reviewed_precedent": sum(row["precedent_status"] != "matched" for row in audit),
            "sha256": sha256(audit_path),
        },
        "projects": {"path": PROJECT_OUT, "rows": len(projects), "sha256": sha256(project_path)},
        "project_action_matches": {
            "path": MATCH_OUT,
            "rows": len(links),
            "distinct_projects": len({row["codigo_bip"] for row in links}),
            "confidence_counts": dict(sorted(Counter(row["label"] for row in links).items())),
            "action_counts": dict(sorted(action_counts.items())),
            "sha256": sha256(match_path),
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {project_path}: {len(projects)} projects")
    print(f"wrote {match_path}: {len(links)} curated project-action links")
    print(f"wrote {audit_path}: {len(audit)} action decisions")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
