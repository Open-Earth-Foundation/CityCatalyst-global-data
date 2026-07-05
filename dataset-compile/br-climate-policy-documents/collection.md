# br-climate-policy-documents — collection notes

Provenance and method for the compiled dataset in this folder. Staging dataset:
manufactured from public government sources, not ingested, not yet vetted through
dataset-review.

## What this is

The **inventory layer** of Brazil's climate-policy document universe — one row per
policy or climate-relevant planning instrument. It is the Brazil analogue of the
Chile `cl-ssg` source-document registry and the policy sibling of the
`mn-climate-awards` compile.

The **rollup dimension is the policy stack tier** (`stack_tier`): where the
instrument sits in the national→subnational hierarchy — `ndc`, `framework-law`,
`national-plan`, `national-strategy`, `sector-plan-mitigation`,
`sector-plan-adaptation`, `state-policy`, `municipal-plan`, plus the four mandatory
municipal **carriers** `plano-diretor`, `saneamento`, `mobilidade`, `gestao-riscos`.
Tier is the natural parent because it determines a document's shape and, crucially,
**how it applies to a city** (national applies to all; state/municipal only where the
instrument exists). Facet axes — `source_level`, `document_type`, `strand`, `sector`,
`uf_code`/`territory_code`/`region`, `status` — back a general
`get_policy_documents(level=, tier=, uf=, sector=, status=)` query and let the
inventory be turned into a per-city coverage view.

This compile holds **both** the climate-badged instruments (national stack + state
and municipal climate plans) **and** the mandatory non-climate **municipal carriers**
that carry climate signal (Plano Diretor, sanitation, mobility, disaster-risk plans)
— they were merged into one table rather than kept separate, because a carrier is
itself a climate-relevant planning instrument and shares this grain. The carriers'
federal mandate, mandatory threshold, national registry, and climate signal are fixed
once per carrier type in `references/carrier-types.csv` (joined by `stack_tier`), so
those facts are derived-by-rule rather than repeated per row. Carrier rows carry a
`present:true|partial|false` tag in `notes` (specific instrument confirmed / exists
but not pinned to a law / obligation applies but no confirmed instrument).

Navigated by the landscape map `knowledge-base/topics/climate-policy/br-climate-policy.md`,
which predicted the shape this data confirms.

## How it was collected

1. Navigated by the Brazil policy landscape map (knowledge-base) — it named the
   stack (NDC → PNMC → Plano Clima → ENM/ENA → sectoral plans) and the subnational
   reality (voluntary, sparse) before any search.
2. Fanned out three targeted research passes: national umbrella instruments; the
   7 mitigation + 16 adaptation sectoral plans; state PEMCs + notable municipal plans.
3. Fetched primary sources where possible (UNFCCC PDF, Planalto law text, MMA PDFs,
   state legislative portals). See sources.yaml.
4. Structured every instrument into schema.json; tagged each field's provenance.
5. Reconciled tier counts to MMA's published control totals.

## Provenance is a gradient

- `stack_tier` — **derived** (rollup). Assigned from level + document_type per the
  landscape map's stack; not a label the sources carry.
- `strand` — **derived**. Stated by the source for sectoral plans (ENM vs ENA);
  assigned (`cross-cutting`) for frameworks/NDC.
- `territory_code`, `region` — **derived-by-rule** via `references/br-uf-codes.csv`
  (UF→IBGE code + macro-region; 7-digit IBGE codes for the 7 municipalities).
  Reproducible; correct in one place.
- `publisher` — **sourced**, but for the 23 sectoral plans the **lead ministry is
  mostly inferred** (only Cidades and the MMA/MCTI/Casa Civil coordinating roles are
  confirmed). Flagged per row with `verified=false` + `confidence`.
- `title_pt` for the 23 sectoral plans — **sourced sector name, reconstructed title**:
  the sector/theme is verbatim from MMA, but the exact cover wording follows MMA's
  naming convention and is unconfirmed pending per-PDF fetch (`verified=false`).
- Everything else (`title_pt` for umbrella/state/municipal, `law_ref`,
  `publication_year`, `status`, `source_url`) is **sourced**.

## Verification status

- **National umbrella (5 rows): fully verified.** NDC, PNMC, Plano Clima executive
  summary, ENM, and ENA each fetched from a primary PDF/law portal.
- **Sectoral plans (23 rows): counts verified, per-plan links not.** The tier totals
  reconcile exactly to MMA's published framing — **7 mitigation** ("sete planos
  setoriais") and **16 adaptation** ("16 Planos Setoriais e Temáticos", the 16 sector
  names transcribed verbatim). Individual PDF deep-links and lead ministries are
  behind the gov.br `documentos-oficiais` hub, which blocks automated fetch, so all 23
  are `verified=false` on identity even though the set is complete and correct.
- **State policies (16 rows): 13 verified, 3 low-confidence.** Law references fetched
  from primary hosts for AM, SP, SC, RJ, PE, ES, RS, BA, CE (high) and corroborated
  for GO, MS, PR, MT (med). PB, RO, MG are `low`/`uncertain` (MG governs by decree +
  plan; a dedicated law was at bill stage). **Control total: 21 of 27 UFs have a
  state climate law** (ICS) — so ~5-8 UFs are known to exist but not yet pinned to a
  reference (the gap, below).
- **Municipal plans (7 rows): 5 verified, 2 med.** Sao Paulo, Rio, Salvador, Recife,
  Belo Horizonte fetched; Curitiba and Porto Alegre corroborated via hub pages.

Nothing unverified is presented as checked: `verified` and `confidence` carry the
truth per row.

## Insights — what the data says

- **The lopsidedness is the headline, and it matches the map.** 28 of 51 rows (55%)
  are national; the national tier is deep, complete, and freshly consolidated
  (Plano Clima 2024-2035, launched 2026). The subnational tier is where the data thins
  — exactly the enumeration-not-inheritance reality the landscape map flagged.
- **Adaptation now outweighs mitigation in instrument count** (17 adaptation vs 8
  mitigation rows), driven by the 16-plan adaptation strategy — a very recent shift
  (adaptation plans published Feb 2026, mitigation Jul 2025).
- **State coverage is real but partial and old.** ~21/27 UFs have a climate law, but
  most date to 2009-2012 — they **predate the current national framework** and won't
  map cleanly onto Plano Clima's mitigation/adaptation sector split. Regionally, the
  verified state laws skew Sudeste/Sul/Nordeste; the Norte (beyond AM) and several
  Centro-Oeste UFs are the thinnest.
- **The municipal layer barely differentiates cities.** Only ~7 municipalities of
  5,570 have a climate law; dedicated plans cluster in ~7-10 capitals. For almost
  every Brazilian city, the *only* local instruments carrying climate signal are the
  non-climate mandatory carriers (Plano Diretor, PMSB, mobility, risk) — now included
  as a 7-city sample (below).

### Municipal carriers (merged in — 28 rows, 7 anchor cities x 4 carriers)

The mandatory non-climate instruments that carry climate signal, sampled for the 7
cities that also have a dedicated climate plan (so the two views describe the same
municipalities). Carrier mandates verified against the four federal laws on Planalto
(Estatuto da Cidade 10.257/2001; Marco do Saneamento 11.445/2007; PNMU 12.587/2012;
PNPDEC 12.608/2012); city instruments from prefeitura / camara / leismunicipais /
legisweb. Findings:

- **The Plano Diretor is the dependable carrier: 7/7 confirmed, all codified as
  municipal law.** When a Brazilian city has no climate plan, its master plan is the
  reliable place to read local climate commitments (and above 20k inhabitants it is
  legally required, with mandatory risk-mapping for cadastro municipalities).
- **Disaster-risk is the weakest-codified carrier** (1 formal instrument of 7; the
  rest `partial`/`false`) — not because the obligation is missing (PNPDEC binds all
  municipalities) but because it is discharged through operational contingency plans,
  not laws, so it rarely yields a stable citable document. A signal layer must look
  for risk content inside the Plano Diretor (Art. 42-A/42-B) as much as in standalone
  risk plans. Sanitation and mobility sit in between (3/7 and 5/7 pinned).
- **Carriers are enumerable to the full country**, unlike the sparse climate plans:
  IBGE MUNIC carries a variable for all four carrier types across the 5,570
  municipalities, with SINISA (sanitation) and the CENAD/CEMADEN cadastro (disaster
  risk) as cross-checks. This 7-city sample is the seed; the full pull is the main
  promotion step.

## Known gaps (the to-proper checklist)

1. **Pin the remaining state laws.** ~5-8 UFs toward the 21-of-27 control total are
   not yet rowed (candidates: AC, TO, AP, MA, RN, AL, SE, PI, DF). A Brazil-domain
   re-crawl (WebSearch is US-biased) would likely surface them.
2. **Source-read the 23 sectoral plans.** Fetch each per-plan PDF from the
   `documentos-oficiais` hub in a browser to confirm exact titles and promote the
   lead-ministry field from inferred (`derived`) to sourced.
3. **Extend the municipal carriers from 7 cities to all 5,570** via the IBGE MUNIC
   backbone (has/uses each instrument), reconciled against SINISA (sanitation) and the
   CENAD/CEMADEN cadastro (disaster risk). This is now the biggest single extension.
   Also pin the carrier partials (Salvador/Recife sanitation; Salvador/Porto Alegre
   mobility; most disaster-risk plans) and confirm Porto Alegre's new PDUS (approved
   Apr 2026) and Curitiba's PMSB decree number.
4. **Confirm low-confidence rows.** PB, RO, MG state laws; Curitiba/Porto Alegre climate
   plan status/year; Fortaleza and Brasília/DF (seen, not yet rowed).
5. **Promote `strand` and `stack_tier` derivations to documented rules** before review.
6. **Consider added carriers** the map implies: PMGIRS (solid waste), habitação,
   arborização/green-area plans.

## Refresh model

No feed. Refresh = re-run the three research passes against sources.yaml and diff.
The gov.br fetch block means the sectoral-plan hub must be checked in a browser, not
by code, until per-plan PDFs are captured to `raw/`.

## Promotion

Graduates into dataset-review when the state set is complete against the 21-UF
control total, the 23 sectoral plans are source-read (titles + ministries), the
non-climate municipal carriers are scoped, and all `derived` fields are computed by
rule. Review then wires it to the coverage/applicability layer that turns this
inventory into a per-city policy environment.
