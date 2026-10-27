# Screening criteria

Apply in cost order — cheap disqualifiers first. The need brief parameterizes
everything here; where the brief is silent, these defaults apply.

## Cheap checks (apply to every find)

1. **Scope** — covers the brief's geography and theme at all? If not, stop.
2. **Admin level** — meets `geography.required_level`? Datasets that stop one
   level above are `reject` unless plausibly disaggregable (then `investigate`).
3. **License** — graded per brief. Default: open/public preferred; unclear
   licensing is `investigate`, not `reject`; explicit no-redistribution is
   disqualifying for production but may still inform (note it).
4. **Access** — API/bulk preferred. Manual download is acceptable; per-record
   scraping or login-walled is `investigate` with the obstacle named.

## Expensive checks (survivors only)

5. **Methodology consistency** — single methodology across the units being
   compared? Critical when the use case is ranking or comparison;
   cross-source stitching is a quiet failure mode — flag it in notes.
6. **Mapping cost** — how much work to map onto the required taxonomy/schema
   (GPC, TEF, locodes)? Native < documented crosswalk < bespoke crosswalk.
   Bespoke mapping doesn't disqualify but must be named in the verdict notes.
7. **Provenance** — methodology documented? Publisher likely to persist and
   update? Undocumented methods cap the verdict at `investigate`.

## Verdict guide

- `promote` — fits must-haves, evidence verified; recommend full review.
- `investigate` — promising; named obstacle (license, access, export,
  publisher contact) blocks a confident verdict.
- `deprioritize` — usable but not the backbone (e.g. single-country context
  layer for a global need); revisit after a primary source is chosen.
- `reject` — fails a must-have or has no usable data product. Always record
  why and what would reopen it.

## Calibration

Strictness scales with catalog coverage: a greenfield domain (nothing in the
catalog) warrants loose screening to map the landscape; a well-covered domain
warrants strict screening because candidates must beat what we already have.
