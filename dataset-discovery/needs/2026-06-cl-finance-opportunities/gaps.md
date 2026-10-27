# Coverage gaps — cl-city-action-fundability v1

Analysis date: 2026-06-16. Compares the aggregated inventory
(`dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/data/chile_finance_inventory.csv`,
78 rows) against the city-relevant Chilean climate-finance landscape and the
institutions named in `search.yaml` screening guidance.

## What v1 already covers

Six administering institutions, all national/regional public:

- **MMA** (55 rows) — FPA variants, FPR, Recambio Calefactores
- **MinEnergía / AgenciaSE** (6) — Comuna Energética, FAE, Casa Solar, Parque Solar Comunitario, Mejor Escuela, AT municipal
- **CORFO** (5) — Crédito Verde, Expande, Garantías/FOGAIN, H2V, Innova Chile
- **SUBDERE** (4) — PMU, PMB, PMR, FRC
- **MINVU** (4) — Espacios Públicos, Parques Urbanos, Pavimentación Participativa, Quiero Mi Barrio
- **GORE** (4) — FNDR/SNI, FRIL, FNDR 8%, FRPD

Heavy concentration in MMA (70% of rows). Two GPC sectors are well-served:
**waste** (FPR) and **stationary energy** (MinEnergía suite). Coverage thins
sharply outside those.

## Key gaps — recommended for a new dataset-review

Ordered by city-facing value × confidence. The first four are confirmed live
for 2026.

### 1. Transportation — entirely absent (highest priority)
No transport instrument is in v1, yet transport is a core GPC sector and a major
municipal mitigation lever. **MTT / DTPR** runs the public-transport subsidy law
(reformed Aug 2024) that earmarks ≥50% of Regional Support Funds to fleet
renewal and zero-emission buses (1,028 e-buses awarded for 2026–27), plus a
long-running collective-taxi renewal subsidy weighted toward EVs (~CLP 6.8M).
MinEnergía's electromobility platform overlaps. This is the single biggest
sector hole.

### 2. Forestry / nature-based — AFOLU underserved
v1 has no **CONAF / MINAGRI** line. The **Fondo de Conservación, Recuperación y
Manejo Sustentable del Bosque Nativo (Ley 20.283)** is open now: 2026 cycle
applications through **1 Jul 2026**, results 28 Aug 2026; funds regeneration,
firebreaks, infiltration ditches, etc. Strong adaptation + mitigation relevance.
Actor is property owners (incl. municipal land) — tag and keep per broad-capture.
Worth pairing with CONAF urban arborization / wildfire-prevention lines.

### 3. Multilateral / bilateral tier — flagged in v1, never ingested
`candidates.yaml` carried `gcf-chile` as *investigate* but no multilateral row
made the CSV. The most directly city/community-accessible is the **GEF Small
Grants Programme (UNDP)** — grants to CBOs/NGOs up to US$75k, active in Chile.
Also: **Fondo Chile** (MINREL+UNDP, up to US$85k, 2026 call Jan 5–Feb 20), GCF
city programmes (FP189 e-mobility), IDB/BID, CAF, Adaptation Fund. Intermediated
access is an attribute, not an exclusion.

### 4. Housing energy efficiency — missing despite being in-sector
**MINVU DS 27 / PPPF "Eficiencia Energética y Acondicionamiento Térmico"** funds
wall/roof insulation, thermopanels and clean heating (up to 100–130 UF), targeted
at PDA pollution zones. Household beneficiary, municipally facilitated — same
profile as Recambio Calefactores, which v1 *does* include, so this is an
inconsistency worth closing.

## Secondary gaps — lower priority / confirm scope

- **ANID** (FONDEF, climate/sustainability research, Centros) — named in
  `search.yaml` guidance, absent. Weaker direct city fit; capture as "enabling".
- **Water infrastructure** — **MOP/DOH** stormwater & flood works,
  **Servicios Sanitarios Rurales (ex-APR)**. Strong adaptation; PMB only partly
  covers sanitation.
- **Disaster risk** — **SENAPRED** DRR financing beyond SUBDERE PMR.
- **Ministerio de Hacienda** sustainable-finance / green bonds — likely out of
  city-applicant scope (sovereign), note and skip.

## Recommendation

Open one dataset-review covering gaps 1–4 (they're all confirmed-live and
city-relevant), prioritizing **MTT transport** and **CONAF Bosque Nativo** since
the latter's 2026 window closes 1 Jul. Treat the secondary list as
investigate-tier within the same review rather than separate needs.
