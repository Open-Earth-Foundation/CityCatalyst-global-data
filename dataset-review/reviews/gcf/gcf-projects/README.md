# Green Climate Fund — projects (gcf-projects)

Project-level records of **Green Climate Fund (GCF)**-funded climate programmes, from the **GCF Projects API** (`http://api.gcfund.org/v1/projects`). Global coverage, one row per Funded Activity (FP), with the country/ies, accredited entity, GCF financing, result areas, status and approval date. This is the single GCF review — the **Chile slice lives here as a filter** (`countries = Chile`), not as a separate dataset.

## Where this sits (layer & level)

**Awards/Projects layer, multilateral level, intermediated access** — see `knowledge-base/topics/climate-finance/cl-climate-finance.md` ("Funder levels"). GCF is *not* a Supply/opportunity (application) source: a city cannot apply to GCF directly, so there is no open-call catalogue. These are **projects that got funded**, reached only through a national gatekeeper plus an Accredited Entity. So for GCF, "opportunity (application)" and "projects happening" collapse into this one projects layer.

For Chile the access chain is: **NDA = Ministerio de Hacienda** (Sustainable Finance Office) → an **Accredited Entity** (IDB, CAF, FAO, IFC, or the Chilean direct-access AE **FYNSA**) → GCF Board. Tag every Chile row `access_pathway = intermediated`.

## Why we use it

- Source of GCF-funded **mitigation** projects (adaptation is out of scope — see below), with a repeatable API ingestion path.
- The non-ODA-gated multilateral Chile can actually access (unlike the DAC-gated city facilities), and it carries a genuinely city-facing programme — **FP189 E-Mobility for Sustainable Cities** (electric buses/EV fleets).
- Global portfolio enables cross-country comparison; the `countries` field makes the Chile slice a filter.

## Canonical downloads and source gate

**[verified]** The IATI reporting-organisations dashboard lists Green Climate Fund under publisher identifier `gcf`, with 350 activities, one organisation record, two datasets, about 3.8 MB of published data and 134 recipient countries. This establishes that a current GCF IATI publication exists and is the preferred structured source to investigate for a Brazil adaptation release.

**[verified]** IATI is a publication standard and registry, not the licensor of every publisher's records. IATI's licensing guidance says a publisher selects the licence for its files and that the licence is displayed in each file's registry metadata. The same guidance says a file without a licence is not considered open. A general statement that “IATI data is open” therefore does not substitute for GCF's publisher-specific metadata and terms.

**[unanswered]** The current GCF file entries, canonical XML resource URLs and publisher-selected licence could not be retrieved and retained during this review. The old IATI Registry was replaced by IATI Account in December 2025, with read-only publication information moved to the dashboard, and the available dashboard evidence did not expose the GCF file-level licence in a form that could be verified here. No `license_id`, licence URL or GCF attribution statement has been captured.

The earlier projects API remains relevant only to the preserved Chile `v1` research release. Its documented endpoint is `http://api.gcfund.org/v1/projects`, with nested country, entity, funding, result-area, status and date fields. It is not used to manufacture a new distributable release because its publisher terms have not been verified.

### References

- IATI reporting-organisations dashboard → `https://merged.dashboard.iatistandard.org/publishers/` (publisher `gcf`)
- IATI licensing guidance → `https://reference.iatistandard.org/en/guidance/publishing-data/what-data-to-publish/how-to-license-your-data/`
- IATI registry migration note → `https://docs.account.iatistandard.org/en/latest/registry/`
- GCF Open Data Library → `https://data.greenclimate.fund/`
- legacy GCF Projects API → `http://api.gcfund.org/v1/projects`

## Licence and redistribution decision

**[verified]** No publisher-specific GCF IATI licence has been verified for this review. Consequently, commercial reuse, derivative redistribution and the required attribution wording remain unanswered.

No GCF IATI or website records may be copied into a new committed Brazil output until the current GCF IATI file metadata supplies an explicit commercially reusable licence and its conditions are recorded. The presence of data in IATI does not by itself pass this gate. This is a licence-evidence blocker, not evidence that GCF prohibits reuse.

**[inferred]** OECD Creditor Reporting System (CRS) records are the appropriate alternative investigation route for GCF-to-Brazil provider/recipient flows because they are an official reporting product independent of the GCF website. OECD CRS requires its own source, licence, coverage and granularity review before any derivative is committed; it may describe aid-flow records rather than one row per GCF funded activity, so it is a complement or fallback, not an assumed drop-in replacement.

## Scope: mitigation only

We cover mitigation actions, so adaptation-only FPs are flagged out of scope (not taxonomy gaps) — e.g. Chile's **FP254** (resilient water infrastructure) is `in_scope = no`.

## Chile slice + action mapping (verified 2026-06-18)

`releases/v1/data/gcf_chile_slice.csv` — the 8 Chile entries (7 FPs + 1 readiness), hand-verified from the GCF Chile country page as a first cut pending an API pull. `releases/v1/data/gcf_chile_to_actions.csv` + `gcf_chile_analysis.ipynb` map each to the city action list at the FP grain (restart-and-run-all passes, chart inline). **3 of 8 in-scope FPs map**: FP189 → zero-emission bus fleets (`c40_0023`, high); FP120 REDD+ → reduce deforestation (`ipcc_0052`, high); FP017 solar → solar generation (`icare_0012`, medium). The rest are `none`: finance vehicles (FP151/152 Subnational Climate Fund, FP149 FI facility) are instruments not interventions; FP254 is adaptation (out of scope); the FAO readiness grant is capacity. **These are approved/under-implementation programmes, not open calls** (`application_status` per row); GCF's apply route (project cycle) is continuous/rolling.

## Interpretation warnings

- **Multi-country FP financing is not a Chile figure** — FP189's US$450M etc. are programme totals across countries; `chile_scope` flags single- vs multi-country.
- **Awarded/approved ≠ disbursed**; every Chile row is intermediated by an AE — the city is a beneficiary/partner, not the recipient.
- Mapping is link-don't-attribute at FP grain; medium/none rows await human adjudication.

## Status

The preserved Chile `v1` release remains a research artifact and is not production-approved. No Brazil/adaptation release was opened because the GCF IATI licence gate failed on missing verifiable publisher-specific metadata. A later review may open a separate release only after it captures the canonical current GCF activity file, the file-level licence and attribution conditions, and confirms that commercial derivative redistribution is allowed. OECD CRS is the next source to review if that evidence remains unavailable.

### References

- Chile project dataset → `releases/v1/data/gcf_chile_slice.csv`
- Chile action crosswalk → `releases/v1/data/gcf_chile_to_actions.csv`
- Chile analysis notebook → `releases/v1/gcf_chile_analysis.ipynb`
- Chile release review → `releases/v1/review.md`
