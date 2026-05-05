# Review Notes

This release includes legal, governance, and finance source inputs, but this version uses only the legal dimension.  
In the database and scoring model, each dimension is treated as a separate domain with its own reference data, inputs, and logic.

Policy alignment content was removed from the legal section so legal outputs remain focused on legal authority/restriction signals and scoring only. National, local, and regional PARCC considerations are handled as a separate feature in the prioritisation module.

Reason for this separation: alignment with national policy (LMCC, sector plans, etc.) does not create municipal legal competence by itself.

Category definitions used in this release:
- **enabled**: both legal ownership and legal restrictions are fully enabled (`1/1`).
- **conditional**: mixed or partial legal conditions (typically includes `0.5` scores and no blocking `0`).
- **blocked**: at least one core legal criterion is not enabled (`0` in ownership or restrictions), so the action is treated as a hard filter under current conditions.

Legal interpretation notes:
- Distinguish legal authority (**competencia normativa**) from implementation mechanism (**instrumento habilitante**); both matter for scoring.
- Where there is no firm CGR/judicial ruling, legal risk is treated as prudential under a conservative legality approach.
- `blocked` means not actionable under current legal/institutional conditions; it is not a permanent impossibility if enabling conditions change.
- Ownership interpretation scale:
  - `1`: Municipality has explicit legal authority to act directly.
  - `0.5`: Authority exists but is conditional, ambiguous, or mediated by an enabling instrument.
  - `0`: Authority belongs to another level of government; municipality cannot act alone.
- Restrictions interpretation scale:
  - `1`: No legal restrictions; no additional authorization required.
  - `0.5`: Moderate legal risk; may require prior authorization or face potential legal challenge.
  - `0`: There is a legal prohibition/restriction, or legal reform is needed.

Legal caveats:
- Legal viability is in principle the same for all municipalities, and this assessment is analytical (not a binding legal opinion).