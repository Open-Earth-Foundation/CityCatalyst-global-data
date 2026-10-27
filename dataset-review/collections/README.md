# Collections

Denormalised views of the dataset catalog for discovery — "what datasets do we have on X?" and "what do we have for Chile / globally?" — without scanning every entry in `catalog/index.yaml`.

## Files

Both files here are **generated** by the `dataset-themes` skill and must not be hand-edited:

- `by-theme.yaml` — one collection per canonical theme (ids like `theme-climate-finance`). A dataset appears under every theme it carries.
- `by-geography.yaml` — one collection per country plus `geo-global` and one per region (ids like `geo-chile`, `geo-global`). A dataset lands in exactly one geography bucket.

The source of truth is `catalog/index.yaml`: themes come from each entry's `themes:` list (normalised through the controlled vocabulary in `.cursor/skills/dataset-themes/references/themes.yaml`), and geography from each entry's `coverage` block. Every dataset id referenced here must exist in `index.yaml`.

## Regenerate

After any change to `index.yaml` (or the theme vocabulary), regenerate both files:

```
python .cursor/skills/dataset-themes/references/group_by_theme.py
```

To verify they're current without writing (used by the pre-commit hook and suitable for CI):

```
python .cursor/skills/dataset-themes/references/group_by_theme.py --check
```

This exits non-zero if regeneration would change the files, so a stale view never gets committed silently.

## Curated collections

There is intentionally no hand-curated `collection.yaml` here right now — theme and geography are both auto-derived. If you later need a judgment-based bundle that isn't a single facet (a specific need's working set, a pilot-city bundle), add it as its own file with collection ids that avoid the `theme-` and `geo-` prefixes, and document it here.
