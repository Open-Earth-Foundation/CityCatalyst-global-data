# Deep-dive checklist

Every review answers these. Tag each answer **verified** (read it in a
primary source / observed it in the file), **inferred** (probable, from
secondary evidence), or **unanswered** (say what would answer it). The
exploration order is free; the destination is not.

## Provenance and access

1. What is the canonical source and version? Are there multiple published
   versions, and which is ours?
2. How is it actually retrieved (API / bulk / manual), and did a retrieval
   actually work?
3. Is it frozen or updated? What supersedes it?

## License

4. What do the actual license terms say (not the landing page)? Attribution
   or citation requirements? Redistribution permitted?

## Data reality

5. What are the real tables/sheets/layers, columns, and units?
6. Does claimed coverage survive contact — all claimed geographies/levels/
   options actually present, or a subset?
7. What quirks would break naive parsing? (working rows, padding, inline
   headers, trailing spaces, sentinels, merged cells, export artifacts)
8. Can its identifiers map to ours (locode, GPC ref, taxonomy in use)?
   Native, documented crosswalk, or bespoke — and what does bespoke cost?

## Methodology

9. What do the values measure, against what baseline/reference, for what
   target year?
10. What uncertainty do the authors state, and is it usable (bounds present
    for all records or a subset)?
11. What do the authors explicitly exclude or warn about — and what does
    each exclusion mean for *our* use case?

## Fit

12. Each must-have and constraint from the originating search.yaml:
    pass / fail / conditional, with evidence.
13. What sibling datasets in the catalog complement or overlap this one?
    (Search index.yaml by theme keywords, not expected publisher.)
14. What surprised you? (Always answer — "nothing" is suspicious.)
