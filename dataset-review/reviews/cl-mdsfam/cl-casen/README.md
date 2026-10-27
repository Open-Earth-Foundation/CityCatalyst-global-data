# Chile CASEN (Encuesta de Caracterización Socioeconómica Nacional)

National socioeconomic household survey led by the Chilean Ministry of Social Development and Family (MDSF), with microdata and published tabulations used for official poverty and income statistics.

## Why we use it

Complements the population census with **sample-based** estimates for:

- poverty by income and multidimensional poverty
- household income distributions (including medians where published)
- labour market indicators (including unemployment) at territorial levels where the sample supports it
- housing, health, education, and thematic modules (varies by survey round)

Natural join partner to **INE census** comuna indicators when city context needs income or poverty lines not available from census forms alone.

## Current catalogued release

**2022** (see `releases/2022/review.yaml`). Newer rounds (e.g. 2024) may appear on the same observatory; add a new release folder when adopted.

## Known strengths

- Official input to national poverty and inequality measurement
- Comuna- and province-level **aggregated** bases and result tables available from the observatory
- Harmonised questionnaires across rounds for longitudinal comparison (with methodological notes)

## Known limitations

- Sample design: small comunas may have **high variance or suppressed cells**; always check design effects and MDSF technical notes
- Not annual for all indicators; cadence is survey-round-based
- Microdata use requires following **MDSF database use notes** (weighting, strata)

## Links

- [Observatorio Social — CASEN 2022](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2022)
