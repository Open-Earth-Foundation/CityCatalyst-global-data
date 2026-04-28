# Benchmark Assumptions — C40 Benchmark Context (2024)

## Objective

Define baseline assumptions used to generate QA flags from sector emissions
values and changes over time.

## Assumptions

1. **Context-first interpretation**
   - A flagged value is unusual, not necessarily wrong.
   - Investigations should prioritize explanation quality and traceability.

2. **Normalization defaults**
   - Use per-capita normalization for I.1, I.2, II.1, III.1, and III.4.
   - Use absolute or share-of-total context for I.4 and IV where per-capita can
     be misleading.

3. **Year-over-year sensitivity**
   - Start with a soft-flag threshold at 30% absolute YoY change.
   - Escalate only when no methodological, boundary, or activity explanation is
     documented.

4. **Missing vs true zero**
   - Zero values in typically non-zero subsectors (for example I.1, II.1,
     III.1) are treated as likely data gaps pending investigation.

5. **Sector coupling checks**
   - I.3 and IV should be reviewed together for industrial cities.
   - High I.4 should trigger boundary/power-export interpretation checks.

## DOD-aligned outputs for this release

- Machine-readable rule set present in
  `knowledge-base/topics/emissions/sector-value-context.thresholds.yaml`.
- Each triggered flag should include `rule_id`, severity, and rationale.
- Review notes for accepted anomalies should be recorded in release docs.
