#!/usr/bin/env python3
"""Build the FNMC 2025-11 cleaned release and draft action mapping. Generated review build; standard-library only."""
from __future__ import annotations
import csv, re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]

RAW=HERE/'sample/projetos-fnmc-2011-a-2025-dados-abertos.csv'
OUT=HERE/'data/br_fnmc_projects.csv'; MAP=HERE/'data/br_fnmc_projects_to_adaptation_actions.csv'
NBSP = '\xa0'
def money(x): return f"{float(x.replace('R$','').replace(NBSP,'').strip().replace('.','').replace(',','.')):.2f}" if x.strip() else ''
def date(x):
 d,m,y=x.strip().split('/'); y=('20'+y) if len(y)==2 else y; return f'{y}-{int(m):02d}-{int(d):02d}'
area_en={'Adaptação':'Adaptation','Educação, capacitação, treinamento e mobilização':'Education, training and mobilisation','Recuperação de áreas degradadas e restauração florestal':'Recovery of degraded areas and forest restoration','Sistemas Agroflorestais':'Agroforestry systems','Desenvolvimento e difusão de tecnologia':'Technology development and dissemination','Ciência e tecnologia':'Science and technology','Apoio às cadeias produtivas sustentáveis':'Support for sustainable value chains','Redução de emissões de gases de efeito estufa':'Reduction of greenhouse-gas emissions'}
type_en={'Estadual':'State government','Federal':'Federal government','Municipal':'Municipal government','OSC':'Civil-society organisation'}
project_name_en=[
'Implementation of Sustainable Agrobiodiversity Management Modules to Combat Desertification in the Pernambuco Semi-Arid Region',
'Technology Transfer: Implementation of Mobile Solar Dryer Technology Demonstration Units in Campo Maior and Coivaras',
'Restoration of Land Degraded by Desertification in the Brum Stream Sub-basin in Jaguaribe, Ceará',
'Integrated Assessment of the Vulnerability of Urban Settlements on the Northern Coast of Rio Grande do Sul to Sea-Level Rise',
'Support for Implementing the Brazilian Coast Monitoring System (SiMCosta)',
'Restoration of Areas Degraded by Bauxite Mining in Barro Alto',
'Sergipe Combating Desertification in Settlements and Communities through Social Mechanisms and Technologies',
'Dissemination of Technologies and Integrated, Sustainable Multiple Use of Natural Resources to Improve Water, Food and Energy Security and Coexistence with the Semi-Arid Climate',
'Life in Support of Conservation and Reforestation: Implementation of 11 Seedling Nurseries',
'Sustainable Development of the Mandacaru Settlement through Integrated Technologies for Coexistence with the Semi-Arid Climate and Natural Resource Conservation',
'Adaptation of INPE’s Cuiabá Satellite Data Reception Station for Direct Reception of UK-DMC Data and One Year of Data Acquisition',
'Strategic Fisheries and Aquaculture Plan for Climate Change',
'Prototype for Carbon Sequestration through Degraded-Land Restoration and Community Development',
'Identification and Mapping of Vulnerable Areas and Potential Climate-Change Risks in the Pernambuco Coastal Zone',
'Methodology for Quantifying Coastal Risks and Projecting Future Shorelines to Support Studies and Adaptation on Northern Santa Catarina Island and Surrounding Areas',
'Implementation of a Biomass Production Unit',
'Development of Outreach and Training Materials for the Low-Carbon Agriculture Plan (ABC Plan)',
'Land of Lives: Agroforestry Systems to Combat Desertification and Adapt to Climate Change in the Semi-Arid Region',
'Assessment of Recruitment Rates and Reproductive Potential of Rocky-Shore Intertidal Invertebrates in Response to Abrupt Storm- and Wave-Driven Sea-Level Changes',
'Strengthening the National Solid Waste Policy through the Public-Interest Campaign “Separate Your Waste and Get It Right”',
'Expansion of the Adapta Sertão Network to the Fourteen Municipalities of the Jacuípe Basin Territory in Semi-Arid Bahia as a Climate-Adaptation and Food-Security Strategy for Family Farmers',
'Conservation, Restoration and Sustainable Economic Use of Biodiversity for Raw-Material and Bioproduct Production in Municipalities of the Rio Grande do Norte Caatinga',
'Support for Implementing the Natural-Disaster Monitoring and Warning System',
'Greenhouse-Gas Monitoring System for Forests and Agriculture',
'Living Backlands: Knowledge and Work in the Caatinga',
'Strengthening Climate-Adaptation Strategies with Agroextractivist Communities in the Cerrado of Northern Minas Gerais',
'Validation of Climate-Change Effects on Biodiversity through In-Situ Monitoring in Protected Areas',
'Development of an Evidence Base for the Adaptation Component of the National Climate Change Plan',
'Joint Operation of the National Forest Development Fund and the National Climate Change Fund',
'Acquisition of High-Resolution Satellite Imagery by MMA to Structure Image-Based Information Systems for Program and Project Implementation',
'Support for the Brazilian Panel on Climate Change',
'Araripe Sustainable Development Foundation: National Meeting for Collective Development of Knowledge and Strategies to Prevent and Combat Desertification and Live with Semi-Arid Conditions',
'Greenhouse-Gas Emissions Management for the Confederations Cup and World Cup',
'Assessment of the Impacts of Global Climate-Change Projections on Cerrado Water Resources',
'Joint Operation of the National Forest Development Fund and the National Climate Change Fund',
'Enteric Methane Emissions in Integrated Production Systems in Mato Grosso and São Paulo',
'Preparation of Territorial and Environmental Management Plans for Indigenous Lands',
'Support for Sustainable Coexistence with Semi-Arid Conditions by Expanding Knowledge for Climate Adaptation and Mitigation, Drought Response and Desertification Control',
'Strategic Plan to Recover Historical Meteorological Data and Convert It to Digital Format',
'Support for Collecting and Providing Meteorological and Oceanographic Data for Brazilian Ocean Areas through the Acquisition of Ocean Meteorological Buoys',
'Development of Population Vulnerability Indicators to Inform Climate-Change Adaptation Actions in Brazil',
'Development of Technical and Institutional Capacity for Local Partnerships in River Basins',
'Solar-Energy Use by Artisanal Fishers in the Ribeira Valley, São Paulo',
'Refazenda Cantareira Project',
'Indigenous Fire: Climate-Adapted Management Alternatives for Forest Conservation in Xingu Indigenous Park',
'Solar-Thermal Energy Use and Energy Self-Sufficiency in Restinga de Cabedelo National Forest',
'Energy Efficiency and Sustainable Biomass Use in the Ceramics and Gypsum Industries of Northeast Brazil',
'Forest Restoration of Permanent Preservation Areas in the Peixe River Sub-basin',
'Forest Restoration of Permanent Preservation Areas Contributing to the Water Supply of the Salvador Metropolitan Region',
'Forest Restoration around Springs and Along Watercourses in Permanent Preservation Areas of the Jucu River Basin',
'Maintenance and Expansion of an Observational System Comprising Fixed, Floating and Orbital Platforms',
'Forest Restoration of Permanent Preservation Areas Contributing to the Water Supply of the Natal Metropolitan Region',
'Forest Restoration of Permanent Preservation Areas Contributing to the Water Supply of the Porto Alegre Metropolitan Region',
'Planning and Delivery of Socio-environmental Initiatives to Reduce Climate-Change Vulnerability in Urban Areas of Jaçanã, Rio Grande do Norte',
'Implementation of Greywater Reuse Systems for Agroecological Production, Consumption, Family and School Markets, and Reduced Local Climate-Change Vulnerability',
'Restoration of Pedrinhas Lagoon and Its Permanent Preservation Area and Establishment of a Community Organic Garden in Urban Propriá, Sergipe',
'Reduction of Climate-Change Vulnerability in Urban Areas of Caruaru, Pernambuco',
'Restoration of the Lagamar Permanent Preservation Area in Várzea, Itarema, Ceará, to Reduce Urban Climate-Change Vulnerability',
'Socio-environmental Initiatives to Reduce Climate-Change Vulnerability in Urban Areas of Teixeira de Freitas, Bahia',
'Restoration of the Verruga River Permanent Preservation Area',
'Implementation of Socio-environmental Initiatives to Reduce Climate-Change Vulnerability in an Urban Area',
'Concrete Actions to Close Open Dumps in Rondônia',
'Implementation of Bem-Te-Vi Urban Park in Fagundes Varela, Rio Grande do Sul',
'Strengthening Osasco’s Sustainable Development and Climate Adaptability through Expanded Green Areas, Green-Infrastructure Feasibility Studies and the City’s First Greenhouse-Gas Inventory',
'Strengthening the Pajeú Women Producers Network through Training and Implementation of Agroforestry Systems and Technologies for Coexistence with the Semi-Arid Climate',
'Creation of Demonstration Multifunctional Landscapes for Climate Mitigation, Biodiversity and Native-Ecosystem Conservation, and More Resilient Production Systems in Municipalities at Risk of Desertification in Espírito Santo',
'Sustainable Natural-Resource Management in Traditional Agropastoral and Extractivist Communities of the Caatinga',
'Strengthening Political Organisation and Implementing River-Basin Revitalisation and Conservation Initiatives in the Pajeú Basin',
'Development of Participatory Mechanisms to Mitigate Climate-Related Risks and Vulnerabilities in Itarema and Acaraú',
'Promotion and Dissemination of Good Practices for Living with the Semi-Arid Climate among Family-Farming and Quilombola Communities in Areas Susceptible to Desertification in Alagoas',
'Implementation of the Sustainable Development and Climate Resilience Project in the Pajeú River Basin',
'Agro-Producers Network: Training, Technical Assistance and Rural Extension for Traditional Communities and Family Farmers to Promote Climate-Resilient and Adapted Systems',
'Sustainable Territorial and Environmental Management in Carrasco Quilombo through Meliponiculture, Biodiversity Conservation, Environmental Education and Agroecological Practices',
'Food in the Semi-Arid Region: Agroecological Resilience in the Ceará Backlands through Educational Experimentation Integrated with Food Production and Participatory Agroecology',
'Community Risk Management and Climate-Crisis Adaptation Plans for Parati Mirim Indigenous Land, Tekoa Itax? Mirim and the Ponta Negra Caiçara Community in Paraty, Rio de Janeiro',
'Implementation of the Redesnoes Parcs Sagarana Grande Sertão Veredas Network to Prepare Farmers and Traditional Riverside Communities for Ongoing Climate Change',
'Cerrado Resilience: Food and Climate Project, Implementing Socio-environmental Initiatives and Management Instruments to Reduce Climate Vulnerability through Sustainable Biodiversity Use',
'Implementation of the Mata do Pau-Ferro–Açude Pitombeira Protected-Area Ecological Corridor to Address Desertification Edge Effects and Water Insecurity in the Mamanguape River Basin',
'Development of Inclusive Climate-Adaptation Initiatives Using Nature-Based Solutions in Recife’s Cajueiro Macro-area',
'Development of Inclusive Climate-Adaptation Initiatives Using Nature-Based Solutions in Contagem’s Nascentes Imperiais Macro-area',
'Development of Inclusive Climate-Adaptation Initiatives Using Nature-Based Solutions in Eastern Diadema',
'Development of Inclusive Climate-Adaptation Initiatives Using Nature-Based Solutions in the Parque da Barragem Macro-area of Águas Lindas de Goiás',
]
assert len(project_name_en)==82
rows=[]
with RAW.open(newline='',encoding='cp1252') as f:
 for c in csv.reader(f,delimiter=';'):
  c=[x.strip() for x in c]
  if not c or not c[0] or c[0]=='Ano': continue
  ano,instr,proc,name,executor,uf,biome,area,typ,start,end=c[:11]
  vals=c[11:16]
  row_index=len(rows)
  rows.append({'record_id':f"fnmc-{row_index+1:03d}",'year':ano,'transfer_instrument_id':instr,'process_id':proc,'project_name':project_name_en[row_index],'project_name_pt':re.sub(r'\s+',' ',name),'translation_status':'reviewed_english_translation','executing_institution':executor,'state_code':uf,'biome_pt':biome,'activity_area':area_en.get(area,''),'activity_area_pt':area,'institution_type':type_en.get(typ,''),'institution_type_pt':typ,'agreement_start_date':date(start),'agreement_end_date':date(end),'fnmc_committed_amount_brl':money(vals[0]),'counterpart_amount_brl':money(vals[1]),'total_project_amount_brl':money(vals[2]),'transferred_amount_brl':money(vals[3]),'not_transferred_amount_brl':money(vals[4]),'source_url':'https://dados.mma.gov.br/dataset/32b154de-d5eb-43de-9a72-7da0dca3d259'})
assert len(rows)==82 and len({r['record_id'] for r in rows})==82
assert len({r['project_name_pt'] for r in rows})==81
assert all(r['project_name'] and r['translation_status']=='reviewed_english_translation' for r in rows)
assert rows[28]['project_name']==rows[34]['project_name'] and rows[28]['project_name_pt']==rows[34]['project_name_pt']
assert round(sum(float(r['fnmc_committed_amount_brl']) for r in rows),2)==152850266.43
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
maps=[]
for r in rows:
 t=(r['project_name_pt']+' '+r['activity_area_pt']).casefold(); links=[]
 if any(k in t for k in ['drenagem','enchente','inundação']): links=[('c40_0048','Upgrade urban drainage systems','direct','high')]
 elif any(k in t for k in ['restauração','recuperação de áreas degradadas','reflorest']): links=[('ipcc_0084','Restore/create natural areas','direct','high')]
 elif any(k in t for k in ['agroflorest','agricultura','produção sustentável']): links=[('ipcc_0096','Strengthen climate resilience in farming and fisheries','component','medium')]
 elif 'adaptação' in t or 'resiliência' in t: links=[('ipcc_0086','Implement ecosystem‑based adaptation measures','related','medium')]
 elif 'educação' in t or 'capacita' in t: links=[('icare_0165','Develop an Environmental Education Plan','enabling','medium')]
 else: links=[('','','none','none')]
 for aid,aname,mtype,conf in links: maps.append({'record_id':r['record_id'],'transfer_instrument_id':r['transfer_instrument_id'],'project_name_pt':r['project_name_pt'],'action_id':aid,'action_name':aname,'match_type':mtype,'mapping_confidence':conf,'adjudication_status':'pending' if conf=='medium' else 'not required','rationale':'Keyword-based draft from the source project name and activity area; human adjudication required for medium links.' if aid else 'No defensible adaptation-action link from the available source text.'})
with MAP.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(maps[0])); w.writeheader(); w.writerows(maps)
SUMMARY={'rows':len(rows),'committed_brl':sum(float(r['fnmc_committed_amount_brl']) for r in rows),'mapped':sum(bool(r['action_id']) for r in maps),'translations_reviewed':len(rows),'translations_pending':0}
print(SUMMARY)
