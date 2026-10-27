---
id: 2026-06-cl-international-climate-finance
title: International / multilateral climate finance accessible to or relevant for Chilean cities
status: open            # open | resolved | gap_confirmed | superseded
opened: 2026-06-18
requested_by: Amanda
serves: action-prioritization

outcome:
  candidates: [gef-sgp-chile, gcf-chile, euroclima, bloomberg-mayors-challenge, subnational-climate-fund, idb-chile, caf-chile, world-bank-chile, gef-chile, iki-germany, agcid-gateway]   # city-gap-fund & c40-cff deprioritized (DAC gate); adaptation-fund-chile deprioritized (adaptation-only, out of scope)
  resolution_notes: >
    Status 2026-06-18: a source is promoted to dataset-review only once it is both applicable to Chile AND has profilable Chilean content (an operational call or a national portfolio) — to avoid dead/empty reviews. GCF content folded into the existing global review **gcf/gcf-projects** (Chile = a `countries=Chile` filter, not a separate dataset; carries the 7-FP Chile slice, NDA=Hacienda/AE=FYNSA access structure, and the FP→action crosswalk). **gef-sgp-chile** is the strongest community-direct candidate (not DAC-gated) but its Chile programme is not yet operational → stays investigate ("promote when live"). **adaptation-fund-chile** promote-ready (AGCID NIE + 2 projects: O'Higgins US$9.96M, Quilpué innovation US$230k) but thin → kept as candidate. **city-gap-fund & c40-cff** deprioritized (Chile DAC-graduation gate). Pattern confirmed: Chile's access is the non-ODA-gated multilateral tier (GCF, AF, GEF/SGP), not the ODA city facilities.
    The international/multilateral tier was the largest gap when the SSG 2023 snapshot
    was reconciled against the live cl-*-fondos reviews — 112 of 405 SSG rows are
    international funders with no review (≈55-60 distinct institutions). This need
    catalogues them per-funder and screens for Chilean-city relevance and access path.
    Structure decision (Amanda 2026-06-18): build PER-FUNDER reviews, extending the
    existing global project dirs (gcf/, idb/, world-bank/) for the supply/opportunity
    side, and new dirs for funders not yet present (adaptation-fund, gef-sgp, euroclima,
    gap-fund). First reviews to open = the community/city-DIRECT ones (GEF Small Grants,
    City Climate Finance Gap Fund, GCF), which carry the highest direct relevance.
---

## Context

Reconciling the legacy SSG finance snapshot (`cl-ssg/cl-ssg-finance`) against the ten built `cl-*-fondos` supply reviews showed the domestic public core is now well covered, but the entire international/multilateral/bilateral/philanthropic tier is not. The `oef/cl-city-action-fundability` union never ingested a multilateral row, and the prior need `2026-06-cl-finance-opportunities` carried only a single `gcf-chile` investigate candidate (gap #3 in its `gaps.md`). This need turns that gap into a per-funder catalogue.

The defining feature of this tier is the **access pathway**: almost none of it is directly city-accessible — it flows through a national entity (Min. Hacienda as GCF NDA; AGCID as Adaptation Fund NIE), an Accredited Entity (IDB, CAF, FYNSA), or a national/sectoral programme. Under the repo's broad-capture strategy that is an attribute to tag (`access_pathway = intermediated`), not a reason to exclude — but it sets the priority order: the handful of community/city-DIRECT facilities come first.

Key structural facts verified 2026-06-18: **AGCID** (Agencia Chilena de Cooperación Internacional para el Desarrollo) is Chile's gateway — the Adaptation Fund National Implementing Entity and co-administrator of Fondo Chile; **GCF** routes via Min. Hacienda (NDA) + FYNSA (direct-access AE); **GEF Small Grants (UNDP)** is the rare community-direct window (≤US$75k to CBOs/NGOs, Chile newly eligible in GEF-8); the **City Climate Finance Gap Fund** (WB+EIB) and **C40 Cities Finance Facility** are city-applied but TA-only. Note: **Fondo Chile is outbound** South-South cooperation (Chilean orgs funded to help *other* countries) — not inbound finance for local climate action, so its city-relevance is low despite appearing in SSG.

## Scope note — mitigation only (2026-06-18)

We do not cover adaptation actions (the city action list is mitigation-only), so **adaptation-specific sources are out of scope**: the **Adaptation Fund** is deprioritized as adaptation-only, and adaptation items inside otherwise-relevant sources are flagged out-of-scope rather than treated as taxonomy gaps (e.g. GCF **FP254** resilient water). The earlier "water-action gap" framing is therefore not a gap to fill — it is simply outside scope. Mitigation finance (energy, transport, waste, AFOLU-mitigation) is what to pursue.

## Key cross-cutting finding (2026-06-18)

**Chile's high-income / OECD status is itself a gate.** Chile graduated from the OECD-DAC List of ODA Recipients (effective 2018 flows), so **ODA-funded city facilities exclude it** — confirmed for the City Climate Finance Gap Fund (eligibility = DAC recipients only) and very likely for C40 CFF (developing-country cities; no Chile project found). Both were deprioritized on this basis. Implication for the rest of this need: the international money realistically open to Chilean cities is the **non-ODA-gated multilateral tier (GEF/SGP, GCF, Adaptation Fund) and EU/bilateral cooperation**, not the ODA city-preparation facilities. Prioritise the GEF/GCF/AF and EUROCLIMA candidates accordingly.

## Open questions

- Relevance line: do we list funds a Chilean city can only reach *through* a national entity / Accredited Entity (intermediated), or only the few it can apply to directly? Broad-capture says include both, tier-tagged — confirm this holds for the multilateral tier.
- Is the supply (opportunity) side of GCF/IDB/World Bank a *new review* or an extension of the existing `gcf/`, `idb/`, `world-bank/` project (awards-side) dirs? Per-funder decision taken; confirm naming (`<funder>/<funder>-finance` vs reusing the projects dir).
- Private impact finance (Oikocredit, Doble Impacto, Fis Ameris, Rabofinance, Sembrador) and carbon markets (bonos de carbono): in scope at all, or out as non-city, non-grant instruments? Currently deprioritized.
- Are Chilean cities actually eligible/active in the Gap Fund and C40 CFF? Santiago is a C40 city; Gap Fund LAC cities are listed but Chile not confirmed in the 2022 list — verify at review.
