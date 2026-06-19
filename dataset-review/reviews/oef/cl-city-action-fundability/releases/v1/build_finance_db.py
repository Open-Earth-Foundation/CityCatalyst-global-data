"""Build finance_db: a traceable view of the repo's finance data across four concepts
(funder, opportunity, project, action) plus a project_funding link. Award is no longer a
separate concept: the money lives as aggregate attributes on the project (cost, committed,
paid) and the many-to-many to funders/opportunities is the project_funding link table.
Every row carries `source_dataset`. See finance_db/README.md."""
import pandas as pd, numpy as np, re, json, pathlib
R=str(pathlib.Path(__file__).resolve().parents[4])   # repo-relative reviews root (portable)
OUT="finance_db"
def slug(s): return re.sub(r'[^a-z0-9]+','-',str(s).lower()).strip('-')[:48]
def num(s): return pd.to_numeric(s,errors='coerce')

# ---------- load sources ----------
inv=pd.read_csv(f"{R}/oef/cl-city-action-fundability/releases/v1/data/chile_finance_inventory.csv")
conaf=pd.read_csv(f"{R}/cl-conaf/cl-conaf-bn-awards/releases/v1/data/cl_conaf_bn_awards_projects.csv")
fpa=pd.read_csv(f"{R}/cl-mma/cl-mma-fpa-awards/releases/v1/data/cl_mma_fpa_awards_projects.csv")
mtt=pd.read_csv(f"{R}/cl-mtt/cl-mtt-fondos/releases/v1/data/cl_mtt_programs_v1.csv")
fpa['gpc_sector']=fpa['gpc_sector'].replace({'cross':'cross_sector'})
fs=pd.read_csv("data/fundability_scored.csv")
ficha=pd.read_csv(f"{R}/cl-ssg/cl-ssg-projects/releases/v1/data/derived/ficha_idi_table.csv",dtype={'codigo_bip':str})
# BIP ficha has one row per project-stage; keep the latest stage per project so counts are per-project
ficha=(ficha.sort_values('etapa_index').drop_duplicates('codigo_bip',keep='last')
       if 'etapa_index' in ficha.columns else ficha.drop_duplicates('codigo_bip'))
# rerun matching (channel experiment) — adds a quality `label` per match (strong / goal_aligned / compatible_context / ...)
pam=pd.read_csv(f"{R}/cl-ssg/cl-ssg-projects/releases/v1/data/qa/channel_experiment/project_action_matches_exp.csv",dtype=str)
pam.columns=[c.lstrip('﻿') for c in pam.columns]; pam['rank']=num(pam['rank'])
HIQ={'strong','goal_aligned'}   # only trust high-quality matches for benchmarks/precedent
acov=pd.read_csv(f"{R}/cl-ssg/cl-ssg-projects/releases/v1/data/qa/action_coverage.csv")[['action_id','rank1_dominant_label']]

# --- award/project -> action crosswalks (so award precedent is MULTI-SECTOR, not afolu-only) ---
import unicodedata
def _norm(s): return ''.join(c for c in unicodedata.normalize('NFD',str(s).strip().lower()) if unicodedata.category(c)!='Mn')
fpa_x=pd.read_csv(f"{R}/cl-mma/cl-mma-fpa-awards/releases/v1/data/cl_mma_fpa_awards_to_actions.csv")     # clasificacion -> action
conaf_x=pd.read_csv(f"{R}/cl-conaf/cl-conaf-bn-awards/releases/v1/data/cl_conaf_bn_awards_to_actions.csv")  # objetivo_manejo -> action
FPA_CLAS2ACT={_norm(r['src_clasificacion']):r['action_id'] for _,r in fpa_x.iterrows() if str(r.get('mapping_confidence'))in('high','medium') and str(r.get('action_id')).strip()}
CONAF_OBJ2ACT={_norm(r['src_objetivo_manejo']):r['action_id'] for _,r in conaf_x.iterrows() if str(r.get('mapping_confidence'))=='high' and str(r.get('action_id')).strip()}
# --- international (GCF) Chile projects: awards/projects layer, INTERMEDIATED (city cannot apply directly) ---
gcf=pd.read_csv(f"{R}/gcf/gcf-projects/releases/v1/data/gcf_chile_slice.csv")
gcf_x=pd.read_csv(f"{R}/gcf/gcf-projects/releases/v1/data/gcf_chile_to_actions.csv")
GCF_FP2ACT={str(r['fp_id']).strip():r['action_id'] for _,r in gcf_x.iterrows() if str(r.get('mapping_confidence'))in('high','medium') and str(r.get('action_id')).strip()}
SRC_MAP={'cl-mma':'cl-mma/cl-mma-fondos','cl-minenergia':'cl-minenergia/cl-minenergia-fondos',
 'cl-corfo':'cl-corfo/cl-corfo-finance','cl-subdere':'cl-subdere/cl-subdere-fondos',
 'cl-minvu':'cl-minvu/cl-minvu-fondos','cl-gore':'cl-gore/cl-gore-fndr'}

# ---------- ACTIONS (+ benchmark rolled up from matched BIP projects) ----------
acts=fs.drop_duplicates('action_id')[['action_id','action_name','sector','archetype','capital_demand']].copy()
# benchmark from each project's BEST-matching action only (rank 0 / lowest), so a project is not
# counted under every action it weakly resembles. NOTE: costo_total_M_CLP is MILES (thousands) of
# CLP, so /1000 -> millions of CLP.
ficha['cost_MMCLP']=pd.to_numeric(ficha['costo_total_M_CLP'],errors='coerce')/1000.0
m=pam[pam['action_id'].notna() & pam['label'].isin(HIQ)].sort_values('rank').drop_duplicates('codigo_bip')  # best HIGH-QUALITY action per project
mj=m.merge(ficha[['codigo_bip','duracion_meses','cost_MMCLP']],on='codigo_bip',how='left')
bench=mj.groupby('action_id').agg(bench_n_projects=('codigo_bip','nunique'),
    bench_duration_median_months=('duracion_meses','median'),bench_duration_n=('duracion_meses','count'),
    bench_cost_median_MMCLP=('cost_MMCLP','median'),bench_cost_n=('cost_MMCLP','count')).reset_index()
acts=acts.merge(bench,on='action_id',how='left').merge(acov,on='action_id',how='left')
acts=acts.rename(columns={'rank1_dominant_label':'match_confidence'})
acts['bench_duration_n']=acts['bench_duration_n'].fillna(0)
pick=acts.sort_values(['sector','bench_duration_n'],ascending=[True,False]).reset_index(drop=True)
pick['source_dataset']='cl-ssg/cl-ssg-projects (actions catalog; benchmark from BIP projects)'
for c in ['bench_duration_median_months','bench_cost_median_MMCLP']: pick[c]=pick[c].round(1)
pick[['bench_n_projects','bench_duration_n','bench_cost_n']]=pick[['bench_n_projects','bench_duration_n','bench_cost_n']].fillna(0).astype(int)
pick['match_confidence']=pick['match_confidence'].fillna('none')   # rerun matching: trustworthiness of the benchmark
ACTION_IDS=set(pick['action_id']); pick.to_csv(f"{OUT}/actions.csv",index=False)

# ---------- OPPORTUNITIES (+ CONAF BN fund) ----------
inv['secs']=inv['gpc_sectors'].map(lambda s:(json.loads(s) if str(s).startswith('[') else [str(s)]))
opps=pd.DataFrame({'opportunity_id':inv['program_name'].map(slug),'opportunity_name':inv['program_name'],
  'funder_id':inv['funder_institution'].map(slug),'funder_name':inv['funder_institution'],
  'instrument':inv['instrument_type'],'gpc_sectors':inv['gpc_sectors'],'eligible_actor':inv['eligible_actor'],
  'access_pathway':inv['access_pathway'],'status':inv['status'],'recurrence':inv['recurrence'],
  'amount_note':inv['amount_note'].fillna(''),'climate_relevance':inv['climate_relevance'],
  'specificity':inv['specificity'],'source_url':inv['source_url'],
  'source_dataset':inv['source_dataset'].map(lambda s:SRC_MAP.get(s,s))}).drop_duplicates('opportunity_id')
opps=pd.concat([opps,pd.DataFrame([{'opportunity_id':'fondo-bosque-nativo-ley-20283',
  'opportunity_name':'Fondo de Conservación, Recuperación y Manejo Sustentable del Bosque Nativo (Ley 20.283)',
  'funder_id':'conaf','funder_name':'Corporación Nacional Forestal (CONAF)','instrument':'grant (bonificación)',
  'gpc_sectors':'["afolu"]','eligible_actor':'forest landowner (small owners + others)','access_pathway':'direct application',
  'status':'recurring','recurrence':'annual','amount_note':'per-hectare bonificación; literal C cap ~10 UTM/ha',
  'climate_relevance':'explicit','specificity':'sector-specific','source_url':'https://concursolbn.conaf.cl/',
  'source_dataset':'cl-conaf/cl-conaf-fondos'}])],ignore_index=True)
# MTT transport funds (fills the transport supply gap) + the FPA fund (parent of the FPA awards)
mtt_opps=pd.DataFrame({'opportunity_id':mtt['program'].map(slug),'opportunity_name':mtt['program'],
  'funder_id':mtt['funder_institution'].map(slug),'funder_name':mtt['funder_institution'],
  'instrument':mtt['instrument_type'],'gpc_sectors':mtt['gpc_sectors'],'eligible_actor':mtt['eligible_actor'],
  'access_pathway':mtt['access_pathway'],'status':mtt['status'],'recurrence':mtt['recurrence'],
  'amount_note':mtt['amount_note'].fillna(''),'climate_relevance':mtt['climate_relevance'],
  'specificity':mtt['specificity'],'source_url':mtt['source_url'],'source_dataset':'cl-mtt/cl-mtt-fondos'})
fpa_opp=pd.DataFrame([{'opportunity_id':'fondo-proteccion-ambiental-fpa',
  'opportunity_name':'Fondo de Protección Ambiental (FPA)','funder_id':slug(fpa['funder_institution'].iloc[0]),
  'funder_name':fpa['funder_institution'].iloc[0],'instrument':'grant','gpc_sectors':'["cross_sector","waste","afolu","stationary_energy","water"]',
  'eligible_actor':'organizacion sin fines de lucro (community/citizen org)','access_pathway':'intermediated (community org applies; city facilitates)',
  'status':'recurring','recurrence':'annual','amount_note':'~CLP 6M median per project','climate_relevance':'explicit',
  'specificity':'sector-specific','source_url':'https://fondos.mma.gob.cl/fpa/','source_dataset':'cl-mma/cl-mma-fpa-awards'}])
opps=pd.concat([opps,mtt_opps,fpa_opp],ignore_index=True).drop_duplicates('opportunity_id')
# ROUTE: an opportunity is, by definition, Route A (a competitive fund a city/community applies to).
# city_can_apply preserves the access nuance (direct vs facilitated vs intermediated) — so we never lose
# the "the city cannot apply directly" signal even when a fund exists.
def _city_can_apply(ap):
    a=str(ap).lower()
    if 'intermediated' in a: return 'no — intermediated (via bank / operator / accredited entity)'
    if 'statutory' in a: return 'no — statutory administration, not an application'
    if 'facilitated' in a: return 'facilitated — city enables applicants, not a direct city grant'
    if 'municipality applies' in a or 'direct application' in a: return 'yes — city applies directly'
    return 'unknown'
opps['access_route']='Route A — competitive fund (concurso)'
opps['city_can_apply']=opps['access_pathway'].map(_city_can_apply)
opps.to_csv(f"{OUT}/opportunities.csv",index=False)
# FNDR opportunity (for mapping BIP F.N.D.R. financing)
fndr=opps[opps['opportunity_name'].str.contains('FNDR',case=False,na=False)].head(1)
FNDR_OPP=fndr['opportunity_id'].iloc[0] if len(fndr) else ''
FNDR_FUNDER=fndr['funder_id'].iloc[0] if len(fndr) else ''

# ---------- FUNDERS ----------
fr=opps[['funder_id','funder_name','source_dataset']].drop_duplicates('funder_id').copy()
fr['level']=fr['funder_name'].str.lower().map(lambda n:'regional' if 'regional' in n else ('national (agency)' if 'corfo' in n else 'national'))
fr['type']=np.where(fr['funder_name'].str.contains('CORFO|Agencia|CONAF',case=False),'agency / public corp','ministry')
# route + city access: domestic public funders run Route A (competitive funds the city applies to)
fr['route']='Route A — competitive funds (direct application)'
fr['city_can_apply']='yes — direct or facilitated'
# INTERNATIONAL funders (multilateral): Awards/Projects layer, INTERMEDIATED — the city CANNOT apply directly.
# Listed so the funder universe is complete and the access barrier is explicit on the data.
intl=pd.DataFrame([
 dict(funder_id='green-climate-fund',funder_name='Green Climate Fund (GCF)',level='multilateral',type='climate fund',
   route='Route C — intermediated (via National Designated Authority + accredited entity)',
   city_can_apply='no — via NDA (Min. Hacienda) + an accredited entity (IDB, CAF, FAO, FYNSA)',
   source_dataset='gcf/gcf-projects'),
 dict(funder_id='inter-american-development-bank',funder_name='Inter-American Development Bank (IDB)',level='multilateral',type='MDB',
   route='Route C — intermediated (sovereign / accredited entity)',
   city_can_apply='no — sovereign lending; city benefits via a national programme',
   source_dataset='idb/idb-projects'),
 dict(funder_id='world-bank',funder_name='World Bank (IBRD/IDA)',level='multilateral',type='MDB',
   route='Route C — intermediated (sovereign)',
   city_can_apply='no — sovereign lending; city benefits as a sub-borrower',
   source_dataset='world-bank/world-bank-projects'),
 dict(funder_id='gef-undp-sgp',funder_name='GEF Small Grants Programme (UNDP)',level='multilateral',type='community grant fund',
   route='Route C — intermediated, but community-DIRECT (CBOs/NGOs apply via the National Coordinator)',
   city_can_apply='no for the city directly; community orgs apply (city is enabler)',
   source_dataset='undp/cl-undp-sgp'),
])
fr=pd.concat([fr,intl],ignore_index=True).drop_duplicates('funder_id')
fr[['funder_id','funder_name','level','type','route','city_can_apply','source_dataset']].to_csv(f"{OUT}/funders.csv",index=False)

# ---------- PROJECTS (work + funding aggregates) ----------
psel=m[m['action_id'].isin(ACTION_IDS)].sort_values('rank').drop_duplicates('codigo_bip')
proj=psel.merge(ficha,on='codigo_bip',how='inner',suffixes=('_match','')).drop_duplicates('codigo_bip')
# all *_M / *_M_CLP fields are MILES (thousands) of CLP -> /1000 to millions of CLP
committed=(num(proj.get('historial_ejecucion_monto_vigente_total_M')).fillna(num(proj['costo_total_M_CLP']))/1000.0)
paid=num(proj.get('historial_ejecucion_gasto_total_M'))/1000.0
bip=pd.DataFrame({'project_id':proj['codigo_bip'],'project_name':proj['nombre'].str.slice(0,80),
  'action_id':proj['action_id'],'sector':proj['sector'],
  'jurisdiction':(proj.get('comuna').fillna(proj.get('region')) if 'comuna' in proj else proj.get('region')),
  'lifecycle_stage':proj['etapa_actual'],
  'evaluation_verdict':proj['resultado_analisis_latest_rate'].fillna(''),
  'cost_total':(num(proj['costo_total_M_CLP'])/1000.0).round(1),'amount_committed':committed.round(1),'amount_paid':paid.round(1),
  'amount_unit':'CLP_millions','duration_months':proj['duracion_meses'],'beneficiaries_total':proj.get('beneficiarios_total'),
  'owner_formulator':proj['institucion_formuladora'],'match_label':proj['label'],
  'source_dataset':'cl-ssg/cl-ssg-projects (canonical: cl-mdsfam/cl-bip-projects)'})
bip['_fuentes']=proj['fuentes_financiamiento'].values

conaf['project_id']="conaf-bn-"+conaf['award_id'].astype(str)
cpaid=np.where(conaf['tiene_bonificacion_saff'].eq('Si'),num(conaf['monto_total_utm']),np.nan)
cf=pd.DataFrame({'project_id':conaf['project_id'],'project_name':"Manejo bosque nativo, "+conaf['region'].astype(str),
  'action_id':conaf['objetivo_manejo'].map(lambda o: CONAF_OBJ2ACT.get(_norm(o),'')),'sector':'afolu','jurisdiction':conaf['region'],
  'lifecycle_stage':np.where(conaf['tiene_bonificacion_saff'].eq('Si'),'executed','awarded'),'evaluation_verdict':'',
  'cost_total':'','amount_committed':num(conaf['monto_total_utm']).round(1),'amount_paid':pd.Series(cpaid).round(1),
  'amount_unit':'UTM','duration_months':'','beneficiaries_total':'','owner_formulator':conaf['presenter_type'],
  'match_label':'','source_dataset':'cl-conaf/cl-conaf-bn-awards'})
cf['_fuentes']='__CONAF__'

# FPA award projects (a second, multi-sector, comuna-level award source). monto_clp is full pesos -> /1e6 millions
fpa['project_id']="fpa-"+fpa['concurso_year'].astype(str)+"-"+fpa['folio'].astype(str)
fp=pd.DataFrame({'project_id':fpa['project_id'],'project_name':fpa['nombre_proyecto'].str.slice(0,80),
  'action_id':fpa['clasificacion'].map(lambda c: FPA_CLAS2ACT.get(_norm(c),'')),'sector':fpa['gpc_sector'],'jurisdiction':fpa['comuna'],
  'lifecycle_stage':'awarded','evaluation_verdict':'','cost_total':'',
  'amount_committed':(num(fpa['monto_clp'])/1e6).round(2),'amount_paid':'','amount_unit':'CLP_millions',
  'duration_months':'','beneficiaries_total':'','owner_formulator':fpa['organizacion_tipo'],
  'match_label':'','source_dataset':'cl-mma/cl-mma-fpa-awards'})
fp['_fuentes']='__FPA__'

# GCF Chile projects — INTERNATIONAL, intermediated (city cannot apply directly). amounts are programme
# totals (often multi-country), so kept as a note, not attributed to Chile.
gcf['project_id']="gcf-"+gcf['fp_id'].astype(str)
gp=pd.DataFrame({'project_id':gcf['project_id'],'project_name':gcf['title'].str.slice(0,80),
  'action_id':gcf['fp_id'].map(lambda f: GCF_FP2ACT.get(str(f).strip(),'')),
  'sector':gcf['gpc_sector'],'jurisdiction':'Chile (national; multi-comuna programmes)',
  'lifecycle_stage':gcf['status'],'evaluation_verdict':'','cost_total':'',
  'amount_committed':'','amount_paid':'','amount_unit':'USD (programme total; often multi-country)',
  'duration_months':'','beneficiaries_total':'','owner_formulator':gcf['accredited_entity'],
  'match_label':'','source_dataset':'gcf/gcf-projects'})
gp['_fuentes']='__GCF__'

# ---------- PROJECT_FUNDING (the many-to-many link, in place of an Award concept) ----------
rows=[]
for _,r in bip.iterrows():                       # unpack BIP fuentes ("F.N.D.R. | SECTORIAL") into one row per source
    for tok in [t.strip() for t in str(r['_fuentes']).split('|') if t.strip() and t.strip()!='nan']:
        is_fndr='F.N.D.R.' in tok or 'FNDR' in tok
        rows.append(dict(project_id=r['project_id'],funder_id=FNDR_FUNDER if is_fndr else '',
            opportunity_id=FNDR_OPP if is_fndr else '',source_label=tok,amount='',amount_unit='CLP_millions',
            paid_amount='',cycle='',source_dataset='cl-ssg/cl-ssg-projects'))
for _,r in conaf.iterrows():                      # CONAF: one funding line per forestry project (1:1)
    rows.append(dict(project_id=r['project_id'],funder_id='conaf',opportunity_id='fondo-bosque-nativo-ley-20283',
        source_label='CONAF bonificación',amount=round(float(r['monto_total_utm']),1),amount_unit='UTM',
        paid_amount=(round(float(r['monto_total_utm']),1) if r['tiene_bonificacion_saff']=='Si' else ''),
        cycle=int(r['ano']),source_dataset='cl-conaf/cl-conaf-bn-awards'))
FPA_FUNDER=slug(fpa['funder_institution'].iloc[0])
for _,r in fpa.iterrows():                         # FPA: one funding line per awarded citizen project (1:1)
    rows.append(dict(project_id=r['project_id'],funder_id=FPA_FUNDER,opportunity_id='fondo-proteccion-ambiental-fpa',
        source_label='FPA grant',amount=round(float(r['monto_clp'])/1e6,2),amount_unit='CLP_millions',
        paid_amount='',cycle=int(r['concurso_year']),source_dataset='cl-mma/cl-mma-fpa-awards'))
for _,r in gcf.iterrows():                         # GCF: one funding line per FP, INTERMEDIATED (no opportunity_id; via accredited entity)
    rows.append(dict(project_id=r['project_id'],funder_id='green-climate-fund',opportunity_id='',
        source_label='GCF via '+str(r.get('accredited_entity','accredited entity')),amount='',amount_unit='USD (programme total)',
        paid_amount='',cycle='',source_dataset='gcf/gcf-projects'))
pf=pd.DataFrame(rows); pf.insert(0,'funding_id',['pf-%05d'%i for i in range(1,len(pf)+1)])
pf.to_csv(f"{OUT}/project_funding.csv",index=False)

nfund=pf.groupby('project_id').size().rename('n_funding_sources')
projects=pd.concat([bip.drop(columns='_fuentes'),cf.drop(columns='_fuentes'),fp.drop(columns='_fuentes'),gp.drop(columns='_fuentes')],ignore_index=True)
projects=projects.merge(nfund,on='project_id',how='left'); projects['n_funding_sources']=projects['n_funding_sources'].fillna(0).astype(int)
# ROUTE on each project: how the money reached it (Route A competitive fund / Route B public investment / Route C intermediated multilateral)
_ROUTE={'cl-conaf/cl-conaf-bn-awards':'Route A — competitive fund (CONAF bonificación; landowner applies, city facilitates)',
 'cl-mma/cl-mma-fpa-awards':'Route A — competitive fund (FPA; community org applies, city facilitates)',
 'gcf/gcf-projects':'Route C — intermediated multilateral (city cannot apply directly; via NDA + accredited entity)'}
projects['route']=projects['source_dataset'].map(lambda s:_ROUTE.get(s,'Route B — public investment (SNI/BIP: city formulates, draws FNDR/Sectorial/Municipal)'))
projects.to_csv(f"{OUT}/projects.csv",index=False)

# ---------- summary ----------
for t in ['funders','opportunities','project_funding','projects','actions']:
    d=pd.read_csv(f"{OUT}/{t}.csv"); print(f"{t:16} {len(d):5} rows  cols={list(d.columns)}")
print("\nproject_funding by source_label:",pf['source_label'].value_counts().to_dict())
print("projects with >=1 funding line:",int((projects['n_funding_sources']>0).sum()),"of",len(projects))
