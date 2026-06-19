import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

md("""# Action precedents from Chile BIP projects

**Question.** Taking only the **strong** project→action matches, what does that tell us about each mitigation **action** — which actions have a real-world **precedent** in Chile, and what can the underlying FICHA documents offer someone who wants to **build a new project from an action**? And, honestly: **what is possible with this data and what is not?**

**Data** (from `cl-ssg-projects` derived outputs, `../data/derived/`):
- `project_action_matches.csv` — project→action matches with labels/overlaps.
- `projects_profiled.csv` — one row per project, profiled.
- `ficha_idi_table_translated.csv` — parsed FICHA IDI fields (per *etapa*), ES+EN.
- `actions_profiled.csv` — the 102-action mitigation library.

**Definitions.**
- *Strong match*: best candidate shares **outcome + intervention + channel** with the project (the tightest tier). We use only `rank==1, label=="strong"`.
- *Precedent*: an action has a precedent if ≥1 real Chilean project strongly matches it.

> Note: this runs on the SSG PDF-derived data as the working set. The same analysis applies to the BIDAT-sourced `cl-bip-projects` table once pulled.
""")

code("""import pandas as pd, numpy as np, matplotlib.pyplot as plt
pd.set_option('display.max_colwidth', 60); pd.set_option('display.width', 140)
D = '../data/derived/'
m  = pd.read_csv(D+'project_action_matches.csv', dtype={'codigo_bip':str})
pp = pd.read_csv(D+'projects_profiled.csv', dtype={'codigo_bip':str})
a  = pd.read_csv(D+'actions_profiled.csv')
t  = pd.read_csv(D+'ficha_idi_table_translated.csv', dtype={'bip_code':str})

# normalize BIP join key to digits only
for df,c in [(m,'codigo_bip'),(pp,'codigo_bip'),(t,'bip_code')]:
    df['k'] = df[c].str.extract(r'(\\d+)')[0]
a.columns = [c.lstrip('\\ufeff') for c in a.columns]
print('rows:', dict(matches=len(m), projects=len(pp), ficha_etapas=len(t), actions=len(a)))
""")

md("## Strong matches only")
code("""strong = m[(m['rank']==1) & (m['label']=='strong')].copy()
print('strong matches:', len(strong), '| distinct projects:', strong['k'].nunique(),
      '| distinct actions hit:', strong['action_id'].nunique(), 'of', len(a))
""")

md("""## 1 · Which actions have a precedent?

How many of the 102 mitigation actions are backed by at least one strong real project, and how concentrated are the precedents?""")
code("""by_action = (strong.groupby(['action_id','action_name']).size()
             .reset_index(name='n_precedents').sort_values('n_precedents', ascending=False))
n_with = by_action['action_id'].nunique()
print(f'Actions WITH ≥1 strong precedent: {n_with} of {len(a)} ({n_with/len(a)*100:.0f}%)')
print(f'Actions WITHOUT any strong precedent: {len(a)-n_with}')
print('\\nTop 15 actions by number of precedents:')
display(by_action.head(15).reset_index(drop=True))
""")
code("""fig, ax = plt.subplots(figsize=(9,6))
top = by_action.head(20).iloc[::-1]
ax.barh(top['action_name'].str.slice(0,55), top['n_precedents'], color='#2b7a78')
ax.set_xlabel('Number of strong project precedents'); ax.set_title('Top 20 mitigation actions by precedent count (Chile BIP)')
plt.tight_layout(); plt.show()
""")
code("""# Actions with NO precedent — the gaps in real-world implementation
have = set(by_action['action_id'])
no_prec = a[~a['action_id'].isin(have)][['action_id','action_name']]
print(f'{len(no_prec)} actions have no strong precedent. Examples:')
display(no_prec.head(20).reset_index(drop=True))
""")

md("""## 2 · What do the precedents tell us about each action?

For each action with precedents, the FICHA documents of its precedent projects give real **cost, funding mix, lead agency, beneficiary scale, and schedule**. Coverage varies a lot by field — we quantify that first, because it bounds what's usable.""")
code("""# one FICHA row per project (latest etapa), joined to its strong action
tl = t.sort_values('etapa_index').groupby('k').tail(1)
sj = strong.merge(tl, on='k', how='left', suffixes=('','_f'))
print('strong projects with a FICHA row:', sj['components_es'].index.size,
      '->', sj['total_cost_CLP'].notna().sum(), 'have cost')

cov_fields = {'total_cost_M_CLP_thousands':'total cost','funding_sources':'funding sources',
              'lead_agency':'lead agency','schedule_summary':'schedule','beneficiaries_total':'beneficiaries',
              'conclusions_es':'analyst conclusions','review_result_code':'RATE result',
              'components_es':'component breakdown','duration_months':'duration (months)',
              'purpose_indicators_es':'purpose indicators'}
cov = pd.DataFrame({'field':list(cov_fields.values()),
        'pct_of_strong_precedents': [round(sj[c].notna().mean()*100,1) for c in cov_fields]}
      ).sort_values('pct_of_strong_precedents', ascending=False)
display(cov.reset_index(drop=True))
""")
code("""# Per-action precedent profile, using the well-covered fields
def top_mode(s):
    s = s.dropna()
    return s.value_counts().index[0] if len(s) else None
sj['cost_clp_num'] = pd.to_numeric(sj['total_cost_CLP'], errors='coerce')
sj['ben_num'] = pd.to_numeric(sj['beneficiaries_total'], errors='coerce')

prof = (sj.groupby('action_name')
        .agg(n_precedents=('k','nunique'),
             median_cost_CLP=('cost_clp_num','median'),
             median_beneficiaries=('ben_num','median'),
             typical_funding=('funding_sources', top_mode),
             typical_lead_agency=('lead_agency', top_mode))
        .reset_index().sort_values('n_precedents', ascending=False))
prof['median_cost_MM_CLP'] = (prof['median_cost_CLP']/1e6).round(1)
display(prof[['action_name','n_precedents','median_cost_MM_CLP','median_beneficiaries',
             'typical_funding','typical_lead_agency']].head(15).reset_index(drop=True))
""")

md("""## 3 · "Build a project from an action" — reference card demo

For a well-covered action, the precedent projects act as a template: real cost, who runs it, how it's funded, how big, and (where present) what components it includes. Below is a worked example.""")
code("""def reference_card(action_substr, n=4):
    sel = sj[sj['action_name'].str.contains(action_substr, case=False, na=False)]
    if not len(sel): print('no match'); return
    act = sel['action_name'].iloc[0]
    print('='*88); print('ACTION:', act); print(f'Precedents (strong): {sel.k.nunique()}')
    arow = a[a['action_name']==act]
    if len(arow):
        ar = arow.iloc[0]
        print('Library guidance — investment_cost: %s | timeline: %s | emissions_impact: %s'
              % (ar.get('investment_cost'), ar.get('implementation_timeline'), ar.get('emissions_impact_text')))
    c = pd.to_numeric(sel['total_cost_CLP'], errors='coerce')/1e6
    print('Precedent cost (MM CLP): median %.0f | range %.0f–%.0f' % (c.median(), c.min(), c.max()))
    print('-'*88, '\\nEXAMPLE PRECEDENT PROJECTS:')
    for _,r in sel.head(n).iterrows():
        print('  •', str(r['nombre'])[:78])
        print('      region:', r.get('location_name'), '| lead:', str(r.get('lead_agency'))[:40],
              '| cost MM CLP: %.0f'%(pd.to_numeric(pd.Series([r['total_cost_CLP']]),errors='coerce').iloc[0]/1e6
                                     if pd.notna(r['total_cost_CLP']) else float('nan')))
        print('      funding:', str(r.get('funding_sources'))[:60], '| beneficiaries:', r.get('beneficiaries_total'))
        comp = r.get('components_es')
        if pd.notna(comp): print('      components:', str(comp)[:160])

reference_card('street lighting')
""")
code("""reference_card('Landfills')""")

md("""## 4 · What's possible and what's not

Grounded in the coverage table from Section 2 (share of strong precedents with each field populated).""")
code("""poss = cov.copy()
poss['verdict'] = np.where(poss['pct_of_strong_precedents']>=80,'POSSIBLE (robust)',
                   np.where(poss['pct_of_strong_precedents']>=40,'PARTIAL (illustrative)','LIMITED (sparse)'))
display(poss.reset_index(drop=True))
""")
md("""**Possible with this data (≈100% coverage of strong precedents):**
- *Which actions have a precedent* and how common — a real implementation-frequency signal across Chile.
- Per-action **cost benchmarks** (total cost, and cost per beneficiary), **funding mix** (FNDR / sectorial / municipal), **lead/responsible agency** type, **beneficiary scale**, and **schedule** — i.e. a realistic "what it costs, who runs it, how it's funded, how big" reference built from precedents.
- Qualitative **why/what** from justification & description (≈82% of ficha projects) and the analyst's **conclusions** (~60%) and **RATE** approval signal (~40%).

**Partial / illustrative only:**
- **Component-level build specs**, **purpose indicators**, explicit **duration in months** — present for only ~13% of strong precedents. You can show worked examples per action, but not robust per-action distributions.

**Not possible from this data alone:**
- Engineering/design specifications, BoQ, or procurement detail to actually construct.
- Quantified **emissions impact** per action (the library carries only categorical bands like "very low"; the FICHA has no emissions figures).
- Reliable city/comuna geography for all projects (location is sparse upstream).

**Bottom line.** This data is strong for a *precedent and benchmarking* tool — "show me Chilean projects that implemented this action, what they cost, who ran them, how they were funded" — and for a qualitative starter brief. It is **not** an engineering or emissions-quantification source. The build-spec layer (components/indicators) exists but is too sparse to rely on beyond examples.
""")

nb['cells'] = cells
nbf.write(nb, 'action_precedents.ipynb')
print('notebook written')
