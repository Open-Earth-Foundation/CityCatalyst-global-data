# Comparison with the earlier HIAP model: what it shows

Draft, 15 Oct 2026. Five test cities: Caxias do Sul, Sobral, Santa Cruz do Arari, São Luís, Itaubal. New-model ranks use the default weights (impact 55%, feasibility 22.5%, alignment 22.5%) and the methodology cost scale (low 0.6, medium 0.5, high 0.4). Sources: `releases/v1/data/output/` and `releases/v1/data/mapping/`.

## The two models

| | Earlier model | New model |
| --- | --- | --- |
| Actions | 53 original adaptation actions | 38 updated actions: originals merged, revised or split, plus 2 new |
| Risk data | CCRA: 15 risks per city, each an impact area × hazard | AdaptaBrasil: 12 risks per city, each a sector × risk |
| How risk is scored | Hazard × exposure × vulnerability, scaled 0–1 and capped at 0.99 | AdaptaBrasil's overall risk index, 0–1 |
| How actions are ranked | One score per city; top 20 exported | Climate impact 55%, feasibility 22.5% (cost, legal), policy alignment 22.5% |
| Not ranked | – | Planning, monitoring and regulatory actions, which do not reduce a risk directly |

## Across the five cities

The two models give different top 10s: each city shares 2 to 4 actions between them. Two things changed together, the risk data and the ranking method, and each contributes to the difference.

### Changes from the risk data (CCRA → AdaptaBrasil)

- **The two datasets spread risk differently.** CCRA scores are scaled and capped at 0.99, so in the larger cities many risks share the top score (8 of 15 in Sobral, 11 in São Luís), and in the small cities most sit close to zero. AdaptaBrasil gives more spread within each city.
- **They weigh exposure and vulnerability differently.** Both agree on the flood hazard (0.27 in Itaubal; 0.17 and 0.16 in Santa Cruz do Arari). CCRA gives the small cities very low exposure (0.01), so their flood risk comes out near zero; AdaptaBrasil gives them high vulnerability (0.91–1.00), so floods are among their highest risks. AdaptaBrasil also puts disease near the top in most cities.
- **They cover different risks.** AdaptaBrasil has no heat or sea-level rise risk, which CCRA includes, so cooling and coastal actions score lower in the new model.

### Changes from the ranking method

- **Impact is scored against each city's own risks.** For each risk, the city's risk score is multiplied by how effective the action is against it, and the action keeps its best result. In the earlier results the link between rank and city risk is looser: in Itaubal, half the top 10 deal with the city's smaller risks.
- **Actions are matched to what drives the risk.** The new method knows whether an action reduces exposure or vulnerability. Most flood actions (early warning, shelters, drainage) reduce vulnerability: on impact they rank in the top 10 in Itaubal and Santa Cruz do Arari, where flood vulnerability is high, and 16th to 24th in Caxias do Sul, Sobral and São Luís, where flood risk comes from exposure. Relocation also reduces exposure, so it stays in the top 5 in those three cities. The earlier action data links actions to hazards and impact areas, not to exposure or vulnerability.
- **Plans and monitoring sit outside the impact ranking.** The climate action plan was #1 or #2 in every city in the earlier model. As agreed, the new method does not give planning, monitoring or regulatory actions an impact score.
- **Cost, legal feasibility and policy alignment now count.** They make up 45% of the score and set the order where impact scores are close. They are not what changed the top 10: ranking on impact alone gives the same overlap with the earlier model.

## City by city

**Caxias do Sul**
- Risk data: CCRA ties floods and landslides at 0.99 with two other risks; AdaptaBrasil separates them (visceral leishmaniasis 0.84, landslides 0.80, floods 0.70). Food security moves down from CCRA's #2 (0.93) to AdaptaBrasil's #7 (0.17).
- Ranking: leishmaniasis lifts water and sanitation (#1), waste collection (#2) and health services (#3); food storage falls from 7th to 25th. Flood risk comes from exposure, so relocation is #4 while early warning (#6) and shelters (#12) sit lower. The climate action plan, building codes and education plan sit outside the impact ranking.

**Sobral**
- Risk data: 8 of 15 CCRA risks share the 0.99 cap, including heat. AdaptaBrasil: food access 1.00, leishmaniasis 0.85, water stress 0.80, floods 0.53.
- Ranking: urban agriculture moves from 13th to 1st; food storage stays near the top (6th to 5th). Flood vulnerability is low (0.11), so early warning is #21 and the emergency plan falls from 2nd to 15th; relocation is #2. The climate action plan, hydrological monitoring and education plan sit outside the impact ranking.

**Santa Cruz do Arari**
- Risk data: same flood hazard in both; CCRA exposure 0.01 gives flood risk 0.01, AdaptaBrasil vulnerability 0.91 makes floods its highest risk (0.59). Food security drops from 0.60 to 0.09.
- Ranking: early warning #1, emergency plan #2, shelters #6. Malaria lifts water and sanitation, waste collection and health services (#3 to #5). Food storage (3rd to 26th) and urban gardens (4th to 24th) fall.

**São Luís**
- Risk data: 11 of 15 CCRA risks share the 0.99 cap. AdaptaBrasil leads with disease (malaria 0.83, arboviruses 0.80, leishmaniasis 0.73). Heat and sea-level rise have no AdaptaBrasil counterpart; water stress goes from 0.99 to 0.00.
- Ranking: water and sanitation, waste collection and health services take the top 3. Flood risk comes from exposure, so the emergency plan falls from 1st to 16th; relocation is #5.

**Itaubal**
- Risk data: every CCRA risk is below 0.21. Same flood hazard in both (0.27); AdaptaBrasil vulnerability 1.00 makes floods 0.41. Its top risk is leishmaniasis (0.67), with low vulnerability.
- Ranking: early warning #1, emergency plan #2 (earlier #12), shelters #3, health services #4; floods drive 9 of the top 10. Many flood actions tie on impact, so feasibility and alignment set their order. The climate action plan and hydrological monitoring sit outside the impact ranking.

## What cities picked

`data/mapping/previous_city_selections.csv` has the 3 adaptation actions each of 35 cities picked in the earlier model. 39 of 105 picks came from the earlier top 3 and 27 from outside the top 20. 26 picks are plans or monitoring actions that sit outside the new impact ranking (22 of 35 cities picked at least one), which is a case for showing these actions to cities in their own list.

Only Caxias do Sul and Sobral are test cities. Sobral's two physical picks, water capture (now #6) and ecosystem-based adaptation (now #8), are in the new top 10; its third pick, the climate action plan, is not scored. Caxias do Sul's restoration pick is now relocation at #4; its financial support pick is #26; its risk reduction plan is not scored.

## Questions to take forward

1. How should plans and monitoring actions appear to cities: a separate list, or as enablers of the ranked actions?
2. Should heat and sea-level rise come back in from another source alongside AdaptaBrasil?
3. Best-risk scoring gives sectors with several risk cells (health has four) more chances to score high. Is that the rule we want?
4. I Care rates drainage and coastal protection as reducing vulnerability only. Should they also reduce exposure?
5. Five cities is a thin basis. Rank the 35 cities in the selection data to test whether their picks rank higher in the new model.
