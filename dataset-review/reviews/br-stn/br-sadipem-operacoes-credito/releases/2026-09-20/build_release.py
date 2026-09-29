#!/usr/bin/env python3
"""Build the SADIPEM 2026-09-20 cleaned release and purpose mapping. Generated review build; standard-library only."""
from __future__ import annotations
import csv, gzip, io, re
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]

RAW=HERE/'sample/sadipemconsultapublicageralbatch20092026.csv'; OUT=HERE/'data/br_sadipem_credit_operations.csv.gz'; MAP=HERE/'data/br_sadipem_purposes_to_adaptation_actions.csv'
purpose_en={'Saneamento básico':'Basic sanitation','Saneamento para Todos':'Sanitation for All','Desenvolvimento sustentável':'Sustainable development','Preservação e recuperação ambiental':'Environmental preservation and recovery','Infraestrutura':'Infrastructure','Mobilidade urbana':'Urban mobility','Gestão de recursos hídricos':'Water-resources management'}
party_en={'Município':'Municipality','Estado':'State','Empresa Estatal':'State-owned company'}
operation_en={
 'Operação Contratual Interna':'Domestic contractual operation',
 'Operação Contratual Interna (com garantia da União)':'Domestic contractual operation (with Union guarantee)',
 'Operação Contratual Externa':'External contractual operation',
 'Operação Contratual Externa (com garantia da União)':'External contractual operation (with Union guarantee)',
 'Concessão de garantia':'Granting of a guarantee',
 'Emissão de Títulos Públicos':'Public bond issuance',
}
creditor_type_en={
 'Instituição Financeira Nacional':'Domestic financial institution',
 'Instituição Financeira Internacional':'International financial institution',
 'Empresa Estatal':'State-owned company',
 'Empresa Não Estatal':'Non-state-owned company',
 'Outras':'Other',
 'União':'Federal Union',
 'Outro - Pessoa Física':'Other — individual',
}
currency_en={'Real':'BRL','Dólar dos EUA':'USD','Euro':'EUR','Iene':'JPY','Direito Especial - SDR':'SDR'}
status_en={
 'Deferido':'Granted',
 'Deferido (PVL-IF)':'Granted (PVL-IF)',
 'Arquivado':'Archived',
 'Devolvido':'Returned',
 'Encaminhado à PGFN com manifestação técnica favorável':'Referred to PGFN with a favourable technical opinion',
 'Arquivado por decurso de prazo':'Archived after expiry of the deadline',
 'Regularizado':'Regularized',
 'Arquivado a pedido':'Archived at the applicant’s request',
 'Em retificação pelo interessado':'Under correction by the applicant',
 'Indeferido':'Denied',
 'Em retificação pelo interessado (PVL-IF)':'Under correction by the applicant (PVL-IF)',
 'Arquivado a pedido (PVL-IF)':'Archived at the applicant’s request (PVL-IF)',
 'Arquivado por decurso de prazo (PVL-IF)':'Archived after expiry of the deadline (PVL-IF)',
 'Em retificação pelo credor (PVL-IF)':'Under correction by the creditor (PVL-IF)',
 'Encaminhado à PGFN (decisão judicial)':'Referred to PGFN (court decision)',
 'Cancelado':'Cancelled',
 'Em análise':'Under review',
 'Em retificação pelo credor':'Under correction by the creditor',
 'Pendente de regularização':'Pending regularization',
 'Arquivado pela STN':'Archived by the National Treasury',
 'Deferido (decisão judicial)':'Granted (court decision)',
 'Em análise (PVL-IF)':'Under review (PVL-IF)',
 'Assinado pelo interessado (retificação)':'Signed by the applicant (correction)',
 'Enviado à instituição financeira (PVL-IF)':'Sent to the financial institution (PVL-IF)',
 'Pendente de distribuição (PVL-IF)':'Pending assignment (PVL-IF)',
 'Regular por decisão judicial':'Regular by court decision',
 'Indeferido (PVL-IF)':'Denied (PVL-IF)',
 'PVL cancelado':'PVL cancelled',
}
analysed_by_en={'STN':'National Treasury','Instituição Financeira':'Financial institution'}
def number(x): return x.replace('.','').replace(',','.')
def date(x): d,m,y=x.split('/'); return f'{y}-{m}-{d}'
rows=[]
with RAW.open(newline='',encoding='latin-1') as f:
 for r in csv.DictReader(f,delimiter=';'):
  p=r['Finalidade']; op=r['Tipo de operação']; typ=r['Tipo de interessado']
  desc_pt=f"{p} — {r['Interessado']}/{r['UF']}"
  desc=f"{purpose_en.get(p,p)} — {r['Interessado']}/{r['UF']}" if p in purpose_en else ''
  rows.append({'interested_party':r['Interessado'],'state_code':r['UF'],'interested_party_type':party_en[typ],'interested_party_type_pt':typ,'operation_type':operation_en[op],'operation_type_pt':op,'purpose':purpose_en.get(p,''),'purpose_pt':p,'project_description':desc,'project_description_pt':desc_pt,'translation_status':'translated_by_controlled_value' if desc else 'pending_free_text_translation','controlled_translation_status':'complete_exact_release_dictionary','creditor_type':creditor_type_en[r['Tipo de credor']],'creditor_type_pt':r['Tipo de credor'],'creditor':r['Credor'],'currency':currency_en[r['Moeda']],'currency_pt':r['Moeda'],'amount':number(r['Valor']),'pvl_number':r['Número do Processo/PVL'],'ibge_code':r['Código IBGE'],'status':status_en[r['Status']],'status_pt':r['Status'],'status_date':date(r['Data']),'analysed_by':analysed_by_en[r['Analisado por']],'analysed_by_pt':r['Analisado por'],'proper_name_translation_status':'not_translated_source_proper_names_preserved','source_url':'https://www.tesourotransparente.gov.br/ckan/dataset/operacoes-copem'})
assert len(rows)==28402 and len({r['pvl_number'] for r in rows})==len(rows)
assert {r['interested_party_type_pt'] for r in rows}==set(party_en)
assert {r['operation_type_pt'] for r in rows}==set(operation_en)
assert {r['creditor_type_pt'] for r in rows}==set(creditor_type_en)
assert {r['currency_pt'] for r in rows}==set(currency_en)
assert {r['status_pt'] for r in rows}==set(status_en)
assert {r['analysed_by_pt'] for r in rows}==set(analysed_by_en)
assert all(r['controlled_translation_status']=='complete_exact_release_dictionary' for r in rows)
OUT.parent.mkdir(parents=True,exist_ok=True)
with gzip.GzipFile(OUT,'wb',mtime=0) as gz, io.TextIOWrapper(gz,newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
maps=[]
for p in sorted({r['purpose_pt'] for r in rows}):
 t=p.casefold(); links=[]
 if 'saneamento' in t: links=[('ipcc_0101','Improve urban water management','related','medium')]
 elif 'recurso' in t and 'hídr' in t: links=[('c40_0056','Improve Watershed Protection and Management','related','medium')]
 elif 'preservação' in t or 'recuperação ambiental' in t: links=[('ipcc_0084','Restore/create natural areas','related','medium')]
 else: links=[('','','none','none')]
 for aid,aname,mtype,conf in links: maps.append({'purpose_pt':p,'purpose':purpose_en.get(p,''),'action_id':aid,'action_name':aname,'match_type':mtype,'mapping_confidence':conf,'adjudication_status':'pending' if conf=='medium' else 'not required','rationale':'Purpose-level link only; SADIPEM publishes no project object, so no amount is attributed to the action.' if aid else 'The broad credit purpose does not identify a defensible adaptation action.'})
with MAP.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(maps[0])); w.writeheader(); w.writerows(maps)
SUMMARY={'rows':len(rows),'purposes':len(maps),'purpose_translations_complete':sum(bool(r['purpose']) for r in rows),'purpose_translations_pending':sum(not bool(r['purpose']) for r in rows),'controlled_translations_complete':sum(r['controlled_translation_status']=='complete_exact_release_dictionary' for r in rows),'mapped_purposes':sum(bool(r['action_id']) for r in maps)}
print(SUMMARY)
