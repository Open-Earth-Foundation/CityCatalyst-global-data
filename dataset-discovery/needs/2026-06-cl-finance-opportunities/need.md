---
id: 2026-06-cl-finance-opportunities
title: Current climate-relevant finance opportunities for Chilean cities (live, verifiable)
status: open            # open | resolved | gap_confirmed | superseded
opened: 2026-06-08
requested_by: amanda
serves: action-prioritization

outcome:
  candidates:           # promote/investigate ids from candidates.yaml
    promote:
      - cl-mma-fpr                # municipalities apply; waste/REP
      - cl-minvu-espacios-publicos
      - cl-minenergia-fae
      - cl-subdere-pmu            # FLAG broad fund (over-matches in scoring)
      - cl-subdere-pmb            # FLAG broad fund
      - cl-corfo-credito-verde    # private firms; kept under broad capture, actor tagged
      - cl-mma-recambio-calefactores  # households; kept under broad capture, actor tagged
    investigate:
      - cl-mma-fpa                # actor = community orgs (tagged, not excluded)
      - cl-minenergia-casa-solar
      - cl-minenergia-comuna-energetica
      - cl-minenergia-parque-solar-comunitario
      - cl-minvu-parques-urbanos
      - cl-gore-fndr-8pct         # regional tier model
      - gcf-chile                 # multilateral; intermediated access (Accredited Entity)
      - cl-fondos-mma-portal      # institution-level source surfaced by the pivot
    deprioritize: []              # none — broad-capture strategy keeps all relevant entries
    reject:
      - cl-fondos-gob-portal      # ToU forbids copy/redistribution/mirroring; discovery-index only
  resolution_notes: >
    First run 2026-06-08. 15 candidates recorded, all with live verified-2026
    sources — directly addresses the SSG inventory's staleness (2023 docs,
    default "recurring" status, 86% missing URLs). Strategy set to BROAD CAPTURE
    (Amanda, 2026-06-08): no premature filtering; actor/access/tier/specificity
    are row attributes, not exclusion grounds; deprioritize is now empty.
    Key cross-cutting finding: most Chilean concursable funds are annual and
    several 2026 cycles are ALREADY CLOSED (e.g. FPA, FPR), so the schema must
    carry a real status + next-call estimate per row, not a static "recurring".
    Fundability score is back IN scope but its methodology is undecided — being
    designed separately (see Open questions).
    SOURCING DECISION (2026-06-08): the original "harvest fondos.gob.cl fichas"
    plan is RETRACTED. A dataset-review Step 1 on fondos.gob.cl found its SEGEGOB
    Terms & Conditions are restrictive (personal/non-commercial transient viewing
    only; no copy, modify, redistribution, public display, or mirroring; must
    destroy downloads) — incompatible with ingesting/storing/redistributing in a
    product, and it offers no open API (only scraping, which the ToU forbids). It
    is also a current-cycle noticeboard, not a historical archive. Decision
    (Amanda): keep fondos.gob.cl as a HUMAN discovery index only, and source/cite
    each opportunity from its administering institution's own official page.
    Institution-level fund portals (esp. fondos.mma.gob.cl for the environment
    category) are the authoritative sources to review/catalog instead.
---

## Context

We hold an SSG-curated finance inventory (`dataset-review/reviews/cl-ssg/cl-ssg-finance`, 405 rows) but it is a static 2023 snapshot: `status` is almost entirely the default `recurring` (357/405), `last_updated_at` is a single bulk curation date (2026-03-19) rather than per-opportunity verification, the most common `application_window` value is the expired "Ley de Presupuestos 2023", and only 58/405 rows carry a `source_url`. It is curated from a fixed set of 2023 consultancy reports by one collaborator. Good for landscape context and analyst notes/barriers; not trustworthy as a live reference a city can act on.

Two use cases drive this need. Primary: a city-facing reference — a list of funding programs a Chilean city could realistically pursue, each with a working link and a verifiable current application status/window. Secondary: an input layer that could inform a fundability score/band for our actions. (The existing SSG-based fundability scoring is not in production and is out of scope here — see Open questions.)

Scope decision (2026-06-08): start at the national level (Chilean public/government instruments) but design the schema so adding regional and multilateral/global tiers later does not break it. The SSG inventory's GPC sector mapping and `notes_internal` barrier/eligibility context are worth preserving as a curation base to layer verification onto, rather than discarding.

Greenfield for this domain: no finance entry exists in `dataset-review/catalog/index.yaml` and no finance playbook exists in `knowledge-base/topics/data-sources/`. Screening is therefore loosened to map the landscape (per screening-criteria calibration).

## Open questions

- ~~What makes a program belong on a *city-facing* list — must a municipality be the eligible applicant?~~ Resolved 2026-06-08 (broad capture): include programs regardless of who applies; record `eligible_actor` and `access_pathway` (direct / facilitated-by-city / intermediated) as attributes so the score and the UI can filter later.
- ~~"Climate-relevant" boundary — explicit climate line only, or also general municipal funds?~~ Resolved 2026-06-08 (broad capture): include both; record `climate_relevance` (explicit / climate-adjacent / indirect) and `specificity` (sector-specific / broad). Broad funds stay IN the dataset but are flagged so the score can down-weight them.
- Does each opportunity need a structured, comparable `application_window` (open/close dates), or is a verified live URL + current status enough? Still open — leaning "status + next-call estimate required, exact dates nice-to-have," given many cycles are annual and currently closed.
- FUNDABILITY SCORE — direction decided 2026-06-08 (Amanda). Purpose: ordinal ranking of candidate actions by fundability. Logic: hybrid (depth-dominant + capped breadth). Method: simple, transparent rule-based tiers (not a weighted/statistical model). Output: tier + a lexicographic ordinal rank, not an absolute 0-100 score. Concretely: (1) match action→opportunities on sector relevance, keeping broad matches but tagged; (2) classify each match Strong / Moderate / Weak by simple rules — Strong = sector-specific AND currently available AND realistic actor/access; Moderate = sector-specific with one gap, or a broad fund that is open+accessible; Weak = broad-only or major timing/access gap; (3) action tier: High = ≥1 Strong, Medium = ≥1 Moderate (no Strong), Low = only Weak/none; (4) ordinal rank = lexicographic sort by [tier, #Strong capped at 3, #Moderate capped at 3, has-open-Strong]. Key property: broad/cross-sector funds can only ever be Moderate/Weak, never Strong, so they cannot lift an action into High — this is the explicit fix for the SSG ~87/100 inflation. Caveats: ordinal only (do not read absolute fundability); ranking quality depends on match accuracy and on action sector/actor metadata. Implementation deferred until the broad dataset is built (this need → review → dataset); thresholds/caps to be tuned on real data.

