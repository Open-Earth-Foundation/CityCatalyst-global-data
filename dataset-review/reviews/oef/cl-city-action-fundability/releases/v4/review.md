# Review — cl-city-action-fundability, release v4 (city profile)

## Scope and status

Research, not production-approved and not loaded. v4 applies SSG's review of the city side of the model (MEED consolidated methodology, annex section 5.3) to the v3 city profile. Capacity is unchanged. Autonomy changes in one way, and one label is added:

- **Own money now includes other permanent income (OI).** `autonomy = (IPP + OI) / (IPP + OI + FCM)`. IPP and FCM still come from the public SIM/BEP release, so the only difference from v3 is the OI top-up.
- **FCM position** marks each comuna as a net contributor to, or net recipient of, the Fondo Común Municipal.

OI is read from SSG's line-item sheet (`cl-ssg-municipal-income`) and defined by `data/income_classification.csv`. Route logic, score bands, finance inventory and the modelled table schema are unchanged.

| Check | Result | Status |
| ----- | ----- | ----- |
| Rows | 345 unique CUT codes, no nulls | verified |
| Capacity | identical to v3 | verified |
| Classification covers total income | every peso of all 340 reporting comunas is IPP, OI, FCM or excluded, no remainder | verified |
| Classified codes nest | none | verified |
| IPP codes reproduce SIM/BEP IPP | 286 of 298 comunas where the snapshots agree | verified |
| Comunas without line items | 5, kept at their v3 autonomy (`oi_reported = false`) | verified |
| Autonomy change from v3 | never negative; median +0.013, largest +0.077 (San Ignacio) | verified |
| Archetype changes from v3 | 1 (Natales, Delivery-ready → Self-sufficient) | verified |
| Archetype counts | 66 Self-sufficient / 104 Delivery-ready / 25 Well-resourced / 150 Support-ready | verified |
| Net contributors to the FCM | 17, all already above 0.5 (lowest 0.554) | verified |
| OI licence | programme-internal; commercial use not cleared | decided here, not verified |
| OI snapshot | differs from SIM/BEP for 42 of 340 comunas | verified |
| T4 band, T1 gate, Padre Hurtado | carried over from v3 | unanswered |

## What changed and why

**Other permanent income.** SSG's point is that IPP alone understates the money a municipality can actually plan around. Some recurring income is neither a municipal tax or fee nor FCM: regular SUBDERE transfers (*Fortalecimiento de la Gestión Municipal*, *Compensación por Viviendas Sociales*), recurring Treasury transfers, and minor own taxes and fees that fall outside SUBDERE's IPP definition. These now count as own money.

The classification table is the definition. Each budget code is one of four classes, with a one-line reason:

| Class | What it holds | Codes |
| ----- | ----- | ----- |
| `ipp` | SUBDERE's IPP, line by line | 15 |
| `oi_permanent` | recurring income the municipality can plan around, outside IPP | 8 |
| `fcm` | the FCM received | 1 |
| `excluded` | everything else, each with its reason | 41 |

The `ipp` and `fcm` rows are not used to calculate autonomy; SIM/BEP's published figures are. They are there so the notebook can prove OI does not overlap them.

Excluded income falls into five groups. Transfers tied to services the municipality runs for someone else (education, health, childcare, child protection), which is SSG's main point. Money collected for someone else (the FCM's share of permits and licences, fines for the health service or other municipalities, third-party funds). Project-specific capital transfers (PMU, PMB, FNDR, FRIL and similar). One-off or financing items (asset sales, loan recoveries, borrowing, opening cash). And income that only offsets a cost (sick-leave reimbursements, and sales of goods and services).

**Sales of goods and services are excluded on purpose.** They are recurring, but they are gross revenue that pays for the service sold. Maipú shows why it matters: its own water utility puts 38.8 bn of sales into this line. Counting that would lift Maipú's autonomy from 0.39 to about 0.54 on money that is already spent running the utility.

**FCM position.** SSG asks for the FCM to be read as a position (does the comuna pay in more than it gets back?) rather than only as a share of income. SIM/BEP already publishes the ratio of what a comuna pays into the FCM to what it receives; above 1 is a net contributor. All 17 net contributors already have autonomy above 0.5, so a rule using the position would change no route. It is carried as a label. The notebook fails if a net contributor ever falls below 0.5, which is when it would need a rule.

**What SSG asked for that was already in v3.** Excluding education and health money: SIM/BEP's IPP and FCM never included it. Replacing the SINIM staff measure of capacity with the MEED Local Governance tramo: done in v3.

**What SSG asked for that is not adopted.** Judging fund access without regard to the city's capacity. The model keeps capacity as part of what unlocks a fund, because channels such as SNI/BIP need staff to formulate and pass a project. Changing that would reshape the route and score for every comuna. Recorded in `methodology.md`.

## What this data supports

A city profile for all 345 comunas whose autonomy counts recurring other income, as SSG's methodology describes, with the change from v3 traceable to named budget lines. The same database columns and the same score function remain valid.

The change is small. Median autonomy rises by 0.013 and only Natales changes archetype. Natales sat 8 parts per million under the 0.5 line in v3 (an open v3 decision). With 0.33 bn of recurring SUBDERE and Treasury transfers counted it reaches 0.513, which settles which side of the line it is on.

## What this data does not support

Do not call the v4 city profile commercially reusable. v3's was. v4's OI input is SSG-supplied data that most likely comes from SINIM, so v4 inherits a non-commercial restriction until that source is cleared (see `cl-ssg-municipal-income`).

Do not treat OI as being from the same snapshot as IPP and FCM. For 42 comunas the SSG sheet and SIM/BEP differ on FCM or total income. OI is a small top-up, so the effect on autonomy is small, but it is a mix of two downloads.

Do not read `oi_reported = false` as zero OI. Those five comunas have no line items.

Do not treat the `oi_permanent` list as settled. It applies SSG's principle (recurring, free to spend, not tied to a transferred service) code by code. SSG has not reviewed the code-level calls, in particular the Treasury's *otras transferencias corrientes* (52 bn across 235 comunas, included) and sales of goods and services (excluded).

## Using it downstream

Join on `comuna_cut` as a zero-padded five-character string. The modelled contract is the same as v3:

`actor_id`, `autonomy`, `capacity`, `city_archetype`, `country_code`, `source_dataset`, `release_id`.

The extra columns (`ipp_mclp`, `oi_permanent_mclp`, `fcm_mclp`, `oi_reported`, `fcm_contribution_ratio`, `fcm_position`) are release-level audit fields. The modelled table does not need them.

To load v4 the existing pipeline needs only its input path and release id changed. It has not been run. Before loading, decide whether a non-commercial city layer is acceptable in the configured database; v3 was loaded because it was commercially clear.

## Notes on non-obvious fields

`ipp_mclp` and `fcm_mclp` are SIM/BEP's published *percibido* figures, unchanged. `oi_permanent_mclp` is the sum of the `oi_permanent` codes from SSG's sheet. All three are thousands of nominal pesos.

`autonomy_basis` is `sim_bep_ipp_fcm_plus_ssg_oi_percibido`. `autonomy_source_vintage` is still the SIM/BEP stamp; the SSG sheet has none.

`fcm_contribution_ratio` is SIM/BEP's *Relación entre Aportes Municipales y Recepción del FCM*. `fcm_position` is `net_contributor` when it is above 1.

## Open decisions before promotion

1. Clear the OI source: SSG confirms an open upstream for the line items, or SUBDERE publishes them. Until then v4 is not commercially reusable.
2. Have SSG confirm the code-level `oi_permanent` list.
3. Decide the T4 capacity value (from v3).
4. Decide whether T1 is evidence-gated (from v3).
5. Resolve or accept Padre Hurtado's SIM/BEP figure (from v3). The SSG sheet gives yet another FCM for it (15.9 bn against SIM/BEP's 8.2 bn), which v4 does not use.

Natales, the fourth v3 decision, no longer sits on the threshold.

## Traceability

**References**

- build, checks and comparison with v3: `01_city_profile_v4.ipynb`
- OI definition: `data/income_classification.csv`
- output: `data/city_finance_profile.csv`
- post-load expectations: `tests/expectations_city_finance_profile.yaml`
- OI line items: `reviews/cl-ssg/cl-ssg-municipal-income/releases/2025`
- IPP, FCM, FCM ratio: `reviews/cl-subdere/cl-subdere-sim-bep/releases/2025`
- capacity: `reviews/oef/cl-municipal-capacity-tier/releases/v1`
- previous release: `../v3/review.md`
- SSG methodology: `MEED_Metodologia_Consolidada_y_Anexo_HIAP VF Consolidado.docx`, section 5 (project drive, *08 Law and Regulations Analysis*)
- model methodology: `../../methodology.md`
