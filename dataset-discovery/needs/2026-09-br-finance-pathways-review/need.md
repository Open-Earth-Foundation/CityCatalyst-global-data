---
id: 2026-09-br-finance-pathways-review
title: Public Brazilian finance datasets that evidence the six municipal finance pathways and supply comparable projects
status: open
opened: 2026-09-22
requested_by: Amanda (OEF), for the Brazil adaptation methodology, Feasibility pillar
serves: action-prioritization

outcome:
  candidates:
    - br-bndes-operacoes-financiamento
    - br-fnmc-projetos
    - br-fnma-instrumentos
    - br-sadipem-operacoes-credito
    - br-novopac-drenagem-encostas
    - br-cofiex-meeting-results
    - br-transparencia-transferencias
    - br-transferegov-discricionarias-legais
    - idb-projects
    - world-bank-projects
    - br-carteira-investimento
    - br-dou-novopac-portarias
    - br-dou-cofiex-resolucoes
    - br-dou-sedec-portarias
    - br-transferegov-transferencias-especiais
    - br-bndes-operacoes-automaticas
    - br-fundoamazonia-projetos-apoiados
  resolution_notes: >
    Ten sources are reviewed and feed the comparable-project catalogue in oef/br-city-finance-feasibility release v2. Novo PAC, COFIEX and
    CGU records are withheld from the public repository until their reuse terms are resolved. The remaining candidates are applicable but
    not profilable now; each carries its blocker in candidates.yaml.
---

## Context

Financing in the Brazil adaptation methodology is guidance beside the ranking, not a ranking input. The pathway directory and the comparable-project catalogue need public records that show which pathway a city could use and how similar projects were financed. Comparable projects will appear in a commercial product, so reuse rights are a hard constraint and are checked source by source before any record is shown.

The source-by-source reviews were run between 22 and 25 September 2026. The earlier `br-climate-awards` staging compile was retired on 29 September 2026 once each of its sources had graduated into a review; the Novo PAC, COFIEX and FNMC reviews keep the rows they need in their own `sample/` folders.

## Open questions

- Publication design for ODbL sources (BNDES, SADIPEM): how the platform meets attribution and derivative-database share-alike obligations.
- Whether the federal free-use basis is enough for public redistribution of CGU payment rows, and whether Transferegov has an operative dataset licence.
- Whether official DOU acts (Lei 9.610 article 8 IV) can replace the CC BY-ND Novo PAC and COFIEX pages; this needs legal review.
- Human adjudication of the Medium-confidence action mappings in every reviewed source.
