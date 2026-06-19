import nbformat as nbf
nb = nbf.read('action_precedents.ipynb', as_version=4)

def md(s): nb.cells.append(nbf.v4.new_markdown_cell(s))
def code(s): nb.cells.append(nbf.v4.new_code_cell(s))

md("""## 5 · Triage — are the "missing" actions recoverable or genuinely absent?

Every action that lacks a rank-1 strong precedent is classified into one of three buckets, so we have a concrete worklist of what to chase versus accept:

- **precedent_rank1** — already has a strong precedent at rank 1 (nothing to do).
- **recount_recoverable** — has a strong match at rank 2–5 only; surfaces just by counting strong at *any* rank.
- **matcher_miss** — no strong at any rank, but appears as a `compatible_context` / `goal_aligned` candidate for real projects → recoverable by loosening the matcher (relax the 3-facet rule, handle outcome-actions, embedding re-rank).
- **genuinely_absent** — never a candidate at all (no facet overlap), or only `wrong_scope`/`unrelated` → out of scope for a public-investment registry (mostly industrial/private).
""")

code("""# classify all 102 actions
strong_r1  = set(m[(m['rank']==1) & (m['label']=='strong')]['action_id'])
strong_any = set(m[m['label']=='strong']['action_id'])

appear = m.groupby('action_id')
times_candidate = appear.size()
best_label = appear['label'].agg(lambda s: s.dropna().value_counts().index[0] if s.notna().any() else None)
strong_any_count = m[m['label']=='strong'].groupby('action_id')['k'].nunique()

def bucket(aid):
    if aid in strong_r1: return 'precedent_rank1'
    if aid in strong_any: return 'recount_recoverable'
    bl = best_label.get(aid)
    if bl in ('compatible_context','goal_aligned'): return 'matcher_miss'
    return 'genuinely_absent'   # never a candidate, or only wrong_scope/unrelated

tri = a[['action_id','action_name']].copy()
tri['bucket'] = tri['action_id'].map(bucket)
tri['strong_precedents_any_rank'] = tri['action_id'].map(strong_any_count).fillna(0).astype(int)
tri['times_as_candidate'] = tri['action_id'].map(times_candidate).fillna(0).astype(int)
tri['best_candidate_label'] = tri['action_id'].map(best_label).fillna('never_a_candidate')

order = {'precedent_rank1':0,'recount_recoverable':1,'matcher_miss':2,'genuinely_absent':3}
tri = tri.sort_values([tri['bucket'].map(order).name if False else 'bucket','times_as_candidate'],
                      key=lambda col: col.map(order) if col.name=='bucket' else col,
                      ascending=[True,False])
print('Bucket counts (all 102 actions):')
print(tri['bucket'].value_counts().reindex(list(order)).to_string())
""")

code("""# RECOUNT-RECOVERABLE: strong precedent exists at rank>1 — count it and you gain these
display(tri[tri['bucket']=='recount_recoverable']
        [['action_name','strong_precedents_any_rank','best_candidate_label']].reset_index(drop=True))
""")

code("""# MATCHER-MISS: real projects relate but never scored strong — the worklist to chase
display(tri[tri['bucket']=='matcher_miss']
        [['action_name','times_as_candidate','best_candidate_label']].reset_index(drop=True))
""")

code("""# GENUINELY-ABSENT: out of scope for a public-investment registry (mostly industrial/private)
display(tri[tri['bucket']=='genuinely_absent'][['action_name','times_as_candidate']].reset_index(drop=True))
""")

code("""# export the worklist
tri.to_csv('action_triage.csv', index=False)
print('wrote action_triage.csv (%d actions)' % len(tri))
print(tri['bucket'].value_counts().to_dict())
""")

md("""**How to read this.**
- **recount_recoverable** + **matcher_miss** together are the *recoverable* set — coverage that better counting/matching would surface. Start with recount (free), then the matcher_miss transport actions (highest project counts).
- **genuinely_absent** is the *accept* set — predominantly industrial decarbonization, which a municipal/regional public-investment bank like BIP structurally does not contain. Chasing more BIP examples won't help here; these need an industrial/private source or development-bank documentation (cf. `other_projects`).

The exported `action_triage.csv` is the worklist.
""")

nbf.write(nb, 'action_precedents.ipynb')
print('appended triage section')
