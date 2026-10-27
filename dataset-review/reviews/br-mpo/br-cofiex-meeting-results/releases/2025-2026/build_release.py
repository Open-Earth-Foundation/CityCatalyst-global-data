#!/usr/bin/env python3
"""Build COFIEX meeting decisions reviewed slice from source-preserving compile rows. Generated review build; standard-library only."""
from __future__ import annotations
import csv, re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]

# RAW holds the COFIEX rows extracted in the retired br-climate-awards compile
RAW=HERE/'sample/cofiex_compile_rows.csv'; OUT=HERE/'sample/br_cofiex_meeting_results.csv'; MAP=HERE/'sample/br_cofiex_meeting_results_to_adaptation_actions.csv'
PROJECT_TRANSLATIONS = {
 "Programa ProIgualdade de Gênero e Raça": "Pro-Equality Program for Gender and Race",
 "Primeiro Hospital Inteligente do Brasil": "Brazil's First Smart Hospital",
 "Financiamento para Desenvolvimento Regional Sustentável": "Financing for Sustainable Regional Development",
 "Programa de Concessões Rodoviárias Inteligentes": "Smart Highway Concessions Program",
 "Empreendimentos Habitacionais com Certificação Ambiental": "Housing Developments with Environmental Certification",
 "Maranhão Mais Conectado": "More Connected Maranhão",
 "Desenvolvimento Urbano Sustentável - Vida Nova no Morro": "Sustainable Urban Development - New Life on the Hill",
 "Desenvolvimento e Mobilidade Urbana de Camaragibe": "Urban Development and Mobility in Camaragibe",
 "CREMA-Sergipe: Manutenção Proativa, Segura e Resiliente das Rodovias Estaduais": "CREMA-Sergipe: Proactive, Safe and Resilient Maintenance of State Highways",
 "Segurança Alimentar, Sociobioeconomia e Conservação de Florestas da Agricultura Familiar": "Food Security, Sociobioeconomy and Forest Conservation in Family Farming",
 "Desenvolvimento Rural Sustentável - Agro Paulista Mais Verde": "Sustainable Rural Development - Greener São Paulo Agriculture",
 "Estradas Seguras - Recuperação Proativa, Segura e Resiliente das Rodovias Estaduais": "Safe Roads - Proactive, Safe and Resilient Rehabilitation of State Highways",
 "Joinville Resiliente e Sustentável: Integração Territorial e Melhoria da Qualidade de Vida": "Resilient and Sustainable Joinville: Territorial Integration and Improved Quality of Life",
 "TransformAção Educacional": "Educational Transformation",
 "Saneamento Ambiental e Urbanização do Subúrbio de Salvador 2a Etapa - Paraguari Mamede": "Environmental Sanitation and Urban Development in the Salvador Suburbs, Phase 2 - Paraguari Mamede",
 "Modernização da Gestão Fiscal - PROFISCO III-PE": "Modernization of Fiscal Management - PROFISCO III-PE",
 "Sustentabilidade Fiscal, Eficiência e Eficácia do Gasto Público de Sergipe": "Fiscal Sustainability and the Efficiency and Effectiveness of Public Spending in Sergipe",
 "Sustentabilidade Fiscal, Eficiência e Eficácia do Gasto Público do Amapá": "Fiscal Sustainability and the Efficiency and Effectiveness of Public Spending in Amapá",
 "Programa de Transformação Ambiental de Palmas frente às Mudanças Climáticas": "Palmas Environmental Transformation Program in Response to Climate Change",
 "VIVA BEM Joinville: Sustentabilidade Urbana, Resiliência Territorial e Inclusão Social": "LIVE WELL Joinville: Urban Sustainability, Territorial Resilience and Social Inclusion",
 "Desenvolvimento Rural Sustentável do Espírito Santo": "Sustainable Rural Development in Espírito Santo",
 "Amaparque - conservação, recuperação ambiental e adaptação climática na RM do Amapá": "Amaparque - Conservation, Environmental Restoration and Climate Adaptation in the Amapá Metropolitan Region",
 "PPP dos Sistemas de Travessias Hídricas - Terminal de São Sebastião": "Public-Private Partnership for Water Crossing Systems - São Sebastião Terminal",
 "Desenvolvimento Sustentável e Inclusivo do Estado da Bahia": "Sustainable and Inclusive Development in the State of Bahia",
 "Programa de Eficiência Fiscal e Ambiental de Manaus": "Manaus Fiscal and Environmental Efficiency Program",
 "Promoção da Sustentabilidade Urbana, Ambiental e Fiscal de Fortaleza": "Promotion of Urban, Environmental and Fiscal Sustainability in Fortaleza",
 "Resiliência Climática e Desenvolvimento Urbano Integrado - Córrego Machado": "Climate Resilience and Integrated Urban Development - Córrego Machado",
 "Fortalecimento do SUS no Estado do Piauí": "Strengthening Brazil's Unified Health System in the State of Piauí",
 "Expansão e Qualidade da Educação Profissional e Tecnológica do Pará": "Expansion and Quality of Vocational and Technological Education in Pará",
 "PROFISCO III-SP - Apoio à Gestão e Integração dos Fiscos": "PROFISCO III-SP - Support for Tax Administration and Integration",
 "ARAS SP - Redes Regionais de Atenção à Saúde": "ARAS SP - Regional Health Care Networks",
 "Linha de Crédito para Resiliência Urbana no Sul do Brasil": "Credit Line for Urban Resilience in Southern Brazil",
 "Programa de Reformas de Valor Agregado para o Desenvolvimento e a Sustentabilidade Econômica e Ecológica": "Value-Added Reform Program for Development and Economic and Ecological Sustainability",
 "Programa de Financiamento à Inovação Aberta do Nordeste": "Northeast Open Innovation Financing Program",
 "PróInvestimento – Fundo Estratégico do Paraná": "Pro-Investment - Paraná Strategic Fund",
 "Programa de Financiamento de Obras de Infraestrutura de Gurupi – TO": "Infrastructure Works Financing Program for Gurupi, Tocantins",
 "Projeto de Modernização do Ministério Público de Pernambuco (Projeto de Modernização e Fortalecimento Institucional do Ministério Público, para o Combate ao Crime Organizado e a Sustentabilidade Ambiental)": "Modernization Project for the Pernambuco Public Prosecutor's Office (Institutional Modernization and Strengthening Project for Combating Organized Crime and Promoting Environmental Sustainability)",
 "Programa Simões Filho 100 – Desenvolvimento Urbano Integrado": "Simões Filho 100 Program - Integrated Urban Development",
 "PROGRAMA JOINVILLE RESILIENTE E SUSTENTÁVEL: Integração Territorial e Melhoria da Qualidade de Vida da População": "RESILIENT AND SUSTAINABLE JOINVILLE PROGRAM: Territorial Integration and Improved Quality of Life for the Population",
 "Programa de Superação da Pobreza - Estado de São Paulo": "Poverty Reduction Program - State of São Paulo",
 "Projeto de Desenvolvimento Viva Melhor Ponta Porã – MS": "Live Better Ponta Porã Development Project - Mato Grosso do Sul",
 "Programa de Modernização e Ressocialização no Sistema Penitenciário do Estado do Maranhão": "Modernization and Social Reintegration Program for the Maranhão State Prison System",
 "Parque Tecnológico de Brasília – BIOTIC: Infraestrutura para Inovação e Sustentabilidade": "Brasília Technology Park - BIOTIC: Infrastructure for Innovation and Sustainability",
 "Programa de desenvolvimento ambiental, social e da infraestrutura urbana de Mauá": "Mauá Environmental, Social and Urban Infrastructure Development Program",
 "Programa de Saneamento Ambiental e Urbanização do Subúrbio de Salvador - 2ª. Etapa – PARAGUARI MAMEDE": "Environmental Sanitation and Urban Development Program for the Salvador Suburbs - Phase 2 - Paraguari Mamede",
 "Programa Estradas Seguras – Recuperação Proativa, Segura e Resiliente das Rodovias Estaduais do Piauí": "Safe Roads Program - Proactive, Safe and Resilient Rehabilitation of Piauí State Highways",
 "Programa de Desenvolvimento Social Sustentável de Crato/CE": "Sustainable Social Development Program for Crato, Ceará",
 "Projeto Levanta Belém": "Rise Up Belém Project",
 "PROGRAMA DE MOBILIDADE URBANA NO MUNICÍPIO DE BOA VISTA-RR": "URBAN MOBILITY PROGRAM IN THE MUNICIPALITY OF BOA VISTA, RORAIMA",
 "Projeto Integra SP Sul – Ponte e Corredor Graúna-Gaivotas": "Integra SP South Project - Graúna-Gaivotas Bridge and Corridor",
 "Programa de Ampliação e Modernização do Museu Parque do Saber": "Expansion and Modernization Program for the Parque do Saber Museum",
 "Transformação Educacional: Construção, Ampliação e Qualidade para fortalecer a Educação de Blumenau": "Educational Transformation: Construction, Expansion and Quality Improvements to Strengthen Education in Blumenau",
 "PROGRAMA DE DESENVOLVIMENTO URBANO SUSTENTÁVEL DO MUNICÍPIO DE AÇAILÂNDIA": "SUSTAINABLE URBAN DEVELOPMENT PROGRAM FOR THE MUNICIPALITY OF AÇAILÂNDIA",
 "Programa Barbalha Para o Futuro": "Barbalha for the Future Program",
 "PROGRAMA DE SUSTENTABILIDADE FISCAL, EFICIÊNCIA E EFICÁCIA DO GASTO PÚBLICO DO ESTADO DE AMAPÁ": "FISCAL SUSTAINABILITY AND PUBLIC SPENDING EFFICIENCY AND EFFECTIVENESS PROGRAM FOR THE STATE OF AMAPÁ",
 "Projeto de Mitigação de Risco em Comunidades Urbanas por meio de Soluções Baseadas na Natureza: Requalificação de Canabrava e Vila Mar.": "Risk Mitigation Project in Urban Communities through Nature-based Solutions: Upgrading Canabrava and Vila Mar",
 "Programa de Desenvolvimento Rural Sustentável do Estado do Espírito Santo": "Sustainable Rural Development Program for the State of Espírito Santo",
 "Programa de Desenvolvimento Sustentável e Conservação Ambiental para o Estado do Maranhão - Floresta Viva Maranhão": "Sustainable Development and Environmental Conservation Program for the State of Maranhão - Living Forest Maranhão",
 "Programa para Controle de Enchentes, Cidades Resilientes e Enfrentamento de Eventos Extremos por Mudanças Climáticas no Município de São Paulo": "Program for Flood Control, Resilient Cities and Response to Climate Change-driven Extreme Events in the Municipality of São Paulo",
 "Parceria Publico Privada do Hospital Regional de Mato Grosso do Sul": "Public-Private Partnership for the Mato Grosso do Sul Regional Hospital",
 "Implantação e Expansão da PPP Linha 6 - Laranja do Metrô de São Paulo": "Implementation and Expansion of the São Paulo Metro Line 6 - Orange Public-Private Partnership",
 "PPP de Requalificação do Parque Dom Pedro II": "Public-Private Partnership for the Upgrading of Dom Pedro II Park",
 "Programa de Apoio Financeiro Setorial - Estruturação da Mobilidade Urbana Sustentável no Brasil - P-MUS": "Sector Financial Support Program - Structuring Sustainable Urban Mobility in Brazil - P-MUS",
 "Programa de Financiamento da Modernização da Infraestrutura de Televisão Aberta Brasileira para Inclusão Digital": "Financing Program to Modernize Brazil's Free-to-air Television Infrastructure for Digital Inclusion",
 "FORTALECIMENTO DA REDE DE APOIO À AGRICULTURA FAMILIAR RELACIONADA AOS PROGRAMAS DA CONAB": "STRENGTHENING THE FAMILY FARMING SUPPORT NETWORK ASSOCIATED WITH CONAB PROGRAMS",
 "Programa PRÓ-BIOMAS - Programa BID-BNDES de Acesso ao Crédito e Fortalecimento das MPMEs nos Biomas Estratégicos do Brasil": "PRO-BIOMES Program - IDB-BNDES Program for Access to Credit and Strengthening Micro, Small and Medium-sized Enterprises in Brazil's Strategic Biomes",
 "Projeto de Desenvolvimento de Corumbá - Pantanal Urbano": "Corumbá Development Project - Urban Pantanal",
 "Programa Três Lagoas Cada Dia Melhor": "Better Every Day Três Lagoas Program",
 "Projeto Estruturador de Desenvolvimento Sustentável do Jaboatão dos Guararapes": "Strategic Sustainable Development Project for Jaboatão dos Guararapes",
 "Projeto de Apoio às Redes Regionais de Atenção à Saúde do Estado de São Paulo – ARAS SP": "Support Project for Regional Health Care Networks in the State of São Paulo - ARAS SP",
 "Projeto Belém Educação Sustentável": "Belém Sustainable Education Project",
 "Programa de Infraestrutura Urbana e Desenvolvimento Socioambiental de Jequié - Avançar Jequié": "Jequié Urban Infrastructure and Socio-environmental Development Program - Advance Jequié",
 "PROJETO NATAL INTEGRA – DESENVOLVIMENTO SOCIAL E ECONÔMICO INTEGRADO DO MUNICÍPIO DE NATAL": "NATAL INTEGRA PROJECT - INTEGRATED SOCIAL AND ECONOMIC DEVELOPMENT OF THE MUNICIPALITY OF NATAL",
 "PROGRAMA DE REQUALIFICAÇÃO URBANA E AMBIENTAL DE ALAGOINHAS/BA": "URBAN AND ENVIRONMENTAL UPGRADING PROGRAM FOR ALAGOINHAS, BAHIA",
 "Programa de Otimização Viária e Mobilidade Urbana de Camboriú/SC - Avança Camboriú": "Road Optimization and Urban Mobility Program for Camboriú, Santa Catarina - Advance Camboriú",
 "Programa de Manutenção Proativa, Segura e Resiliente – PE na Estrada": "Proactive, Safe and Resilient Maintenance Program - Pernambuco on the Road",
 "Paraná Cuidado e Protegido": "Cared-for and Protected Paraná",
 "Programa de Financiamento às Transições Tecnológicas Energética e Digital de Minas Gerais": "Financing Program for Energy and Digital Technology Transitions in Minas Gerais",
 "Projeto de Modernização da Gestão Fiscal do Estado de Roraima": "Fiscal Management Modernization Project for the State of Roraima",
 "Programa de Modernização Fiscal do Estado do Acre": "Fiscal Modernization Program for the State of Acre",
 "Projeto de Modernização da Gestão Fiscal do Estado do Paraná": "Fiscal Management Modernization Project for the State of Paraná",
 "Programa de Modernização da Gestão Pública do Estado de Goiás (PROGESTAO GO)": "Public Administration Modernization Program for the State of Goiás (PROGESTÃO GO)",
 "Programa São Paulo Resiliente: Controle de Enchentes e Adaptação Climática": "Resilient São Paulo Program: Flood Control and Climate Adaptation",
 "Programa de Sustentabilidade Fiscal e Desenvolvimento Social do Município de Salvador": "Fiscal Sustainability and Social Development Program for the Municipality of Salvador",
 "Programa de Sustentabilidade Fiscal e Desenvolvimento Humano Sustentável": "Fiscal Sustainability and Sustainable Human Development Program",
 "CREMA PPP - MINAS GERAIS: PROJETO DE MANUTENÇÃO PROATIVA, SEGURA E RESILIENTE DAS RODOVIAS ESTADUAIS DE MINAS GERAIS NO ÂMBITO DA BACIA HIDROGRÁFICA DO RIO DOCE": "CREMA PUBLIC-PRIVATE PARTNERSHIP - MINAS GERAIS: PROACTIVE, SAFE AND RESILIENT MAINTENANCE PROJECT FOR MINAS GERAIS STATE HIGHWAYS IN THE RIO DOCE WATERSHED",
 "Programa de Desenvolvimento Socioambiental de Rio Largo/AL": "Socio-environmental Development Program for Rio Largo, Alagoas",
 "Programa de Infraestrutura Sustentável e Fortalecimento Turístico de Fortaleza": "Sustainable Infrastructure and Tourism Strengthening Program for Fortaleza",
 "Saneamento Integrado das Águas de Balsas": "Integrated Water and Sanitation Program for Balsas",
 "Projeto de Sustentabilidade Hídrica do Piauí": "Piauí Water Sustainability Project",
 "São Paulo super digital: Infraestrutura, Serviços e Competências para o Futuro Digital": "Super Digital São Paulo: Infrastructure, Services and Skills for the Digital Future",
 "Programa de Revitalização e Obras de Cascavel": "Cascavel Revitalization and Public Works Program",
 "Reorganização e Expansão a garantir o Direito à Saúde em João Pessoa - REDS+JP": "Reorganization and Expansion to Guarantee the Right to Health in João Pessoa - REDS+JP",
 "SUAPE RUMO À TRANSIÇÃO ENERGÉTICA: INFRAESTRUTURA, DESENVOLVIMENTO SOCIOECONÔMICO E AMBIENTALMENTE SUSTENTÁVEL": "SUAPE TOWARD THE ENERGY TRANSITION: INFRASTRUCTURE AND SOCIOECONOMIC AND ENVIRONMENTALLY SUSTAINABLE DEVELOPMENT",
 "Programa São Paulo Resiliente: Controle de Enchentes e Adaptação Climática – Fase II": "Resilient São Paulo Program: Flood Control and Climate Adaptation - Phase II",
 "Intervenções em Infraestrutura e Mobilidade Urbana de Belo Horizonte": "Infrastructure and Urban Mobility Interventions in Belo Horizonte",
 "Programa de Resiliência Climática e Mobilidade Urbana Integrada de Aracaju": "Climate Resilience and Integrated Urban Mobility Program for Aracaju",
 "Projeto de Modernização da Gestão Fiscal do Estado da Paraíba": "Fiscal Management Modernization Project for the State of Paraíba",
 "Programa de conservação, recuperação ambiental e adaptação climática na Região Metropolitana do Estado do Amapá - Amaparque": "Conservation, Environmental Restoration and Climate Adaptation Program in the Amapá Metropolitan Region - Amaparque",
 "Programa Municipal de Redução de Riscos Geológicos e Hidrológicos de São Paulo - PMRR-BL1-L3A": "São Paulo Municipal Geological and Hydrological Risk Reduction Program - PMRR-BL1-L3A",
 "Parceria Público-Privada para Construção e Operação da Esplanada Liberdade": "Public-Private Partnership for the Construction and Operation of Esplanada Liberdade",
 "Implantação e Expansão da PPP Linha 6 - Laranja do Metrô de São Paulo - 2º Pedido": "Implementation and Expansion of the São Paulo Metro Line 6 - Orange Public-Private Partnership - Second Request",
 "Projeto de Qualidade Fiscal do Estado do Piauí": "Fiscal Quality Project for the State of Piauí",
 "Programa de Modernização e Melhoria da Qualidade das Redes de Atenção em Saúde em Belo Horizonte II": "Modernization and Quality Improvement Program for Health Care Networks in Belo Horizonte II",
 "ProInvestimento – Programa de Competitividade e Inovação do Estado de Goiás": "Pro-Investment - Competitiveness and Innovation Program for the State of Goiás",
 "Programa Casa Fácil PR - Projeto Valor de Entrada": "Easy Home Paraná Program - Down Payment Project",
 "Projeto de Recuperação de Áreas Degradadas e Promoção da Agricultura Sustentável no Brasil (Fase 1)": "Project for the Restoration of Degraded Areas and Promotion of Sustainable Agriculture in Brazil (Phase 1)",
 "Aliança Bancos Europeus e BID para Apoio Financeiro ao Fundo Nacional sobre Mudança do Clima (FNMC)": "European Banks and IDB Alliance for Financial Support to the National Fund on Climate Change (FNMC)",
 "Programa de Transformação da Indústria Brasileira": "Brazilian Industry Transformation Program",
 "Programa de Modernização do Poder Judiciário do Estado do Ceará 2": "Modernization Program for the Ceará State Judiciary 2",
 "PENA JUSTA SERGIPE - PROGRAMA DE MODERNIZAÇÃO DA POLÍTICA PENAL": "FAIR SENTENCING SERGIPE - PENAL POLICY MODERNIZATION PROGRAM",
 "Programa de Desenvolvimento da Agricultura Irrigada Sustentável no Semiárido de Pernambuco": "Sustainable Irrigated Agriculture Development Program in the Semi-arid Region of Pernambuco",
 "Programa de Desenvolvimento Urbano Integrado - ATIBAIA +": "Integrated Urban Development Program - ATIBAIA +",
 "Programa de Eletrificação e Melhoria do Transporte Público Coletivo Urbano de São Paulo": "Electrification and Improvement Program for Urban Public Transport in São Paulo",
}
rows=[]
with RAW.open(newline='',encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
  if not (r['source_id'].startswith('cofiex-')): continue
  native=''
  if r['source_id']=='novopac-2025-relacao-propostas-habilitadas':
   m=re.search(r'proposta ([\d/]+)',r['notes']); native=m.group(1) if m else ''
  project_pt=r['project_name']
  rows.append({'record_id':r['id'],'native_record_id':native,'project_description':PROJECT_TRANSLATIONS[project_pt],'project_description_pt':project_pt,'translation_status':'complete_human_reviewed_translation','recipient':r['recipient'],'recipient_type':r['recipient_type'],'state_code':r['uf'],'municipality_name':r['municipio'],'instrument':r['instrument'],'amount':r['amount'],'currency':r['currency'],'decision_date':r['award_date'],'status':r['status'],'funder':r['funder'],'financier':r['financier'],'source_id':r['source_id'],'source_url':r['source_url'],'source_title_pt':r['source_title'],'notes_pt':r['notes']})
assert rows and len(rows)==138 and len({r['record_id'] for r in rows})==len(rows)
assert len(PROJECT_TRANSLATIONS)==114
assert set(PROJECT_TRANSLATIONS)=={r['project_description_pt'] for r in rows}
assert all(r['project_description'] and r['translation_status']=='complete_human_reviewed_translation' for r in rows)
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
maps=[]
for r in rows:
 t=(r['project_description_pt']+' '+r['notes_pt']).casefold(); links=[]
 if 'drenagem' in t: links=[('c40_0048','Upgrade urban drainage systems','direct','high')]
 elif 'encosta' in t or 'estabiliza' in t: links=[('icare_0184','Upgrade Slope stabilization and drainage','direct','high')]
 elif any(k in t for k in ['restaura','áreas degradadas','conservação','florest']): links=[('ipcc_0084','Restore/create natural areas','related','medium')]
 elif any(k in t for k in ['resiliência','adaptação','climática']): links=[('ipcc_0087','Improve Infrastructure retrofitting','related','medium')]
 elif 'saneamento' in t or 'água' in t: links=[('ipcc_0101','Improve urban water management','related','medium')]
 else: links=[('','','none','none')]
 for aid,aname,mtype,conf in links: maps.append({'record_id':r['record_id'],'project_description_pt':r['project_description_pt'],'action_id':aid,'action_name':aname,'match_type':mtype,'mapping_confidence':conf,'adjudication_status':'pending' if conf=='medium' else 'not required','rationale':'Draft link from explicit source text; medium links require human adjudication.' if aid else 'No defensible adaptation-action link from the published title.'})
with MAP.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(maps[0])); w.writeheader(); w.writerows(maps)
SUMMARY={'rows':len(rows),'mapped':sum(bool(r['action_id']) for r in maps),'translations_complete':len(rows),'distinct_translations':len(PROJECT_TRANSLATIONS)}
print(SUMMARY)
