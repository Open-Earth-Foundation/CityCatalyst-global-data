#!/usr/bin/env python3
"""Build the FNMA 2025-03 review release from the canonical MMA CSV.

The script uses only the Python standard library so it can be rerun without a
notebook kernel. It preserves publisher defects as flags and never fabricates
translations for Portuguese free text.
"""
from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RAW = HERE / "sample/projetos-fnma-1990-a-2024-dados-abertos-2025.csv"
ACTION_BANK = ROOT / "dataset-review/reviews/br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv"
OUTPUT = HERE / "data/br_fnma_transfer_instruments.csv"
MAPPING = HERE / "data/br_fnma_transfer_instruments_to_adaptation_actions.csv"
SOURCE_URL = "https://dados.mma.gov.br/dataset/fundo-nacional-do-meio-ambiente"


THEME_EN = {
    "Amazônia Sustentável": "Sustainable Amazon",
    "Conservação e Manejo da Biodiversidade": "Biodiversity conservation and management",
    "Educação Ambiental": "Environmental education",
    "Gestão de Áreas Protegidas": "Protected-area management",
    "Gestão Integrada de Resíduos Sólidos": "Integrated solid-waste management",
    "Meio Ambiente Urbano": "Urban environment",
    "Planejamento e Gestão Territorial": "Territorial planning and management",
    "Qualidade Ambiental": "Environmental quality",
    "Resíduos Sólidos": "Solid waste",
    "Sociedades Sustentáveis": "Sustainable societies",
    "Uso Sustentável dos Recursos Pesqueiros": "Sustainable use of fishery resources",
    "Água e Floresta": "Water and forests",
    "ANULADO": "Cancelled (publisher value in theme field)",
}
REGION_EN = {
    "Centro-Oeste": "Central-West",
    "Nordeste": "Northeast",
    "Norte": "North",
    "Sudeste": "Southeast",
    "Sul": "South",
}
SPHERE_EN = {
    "Federal": "Federal government",
    "Estadual": "State government",
    "Municipal": "Municipal government",
    "OSC": "Civil-society organisation",
}
SELECTION_EN = {
    "Demanda Espontânea (DE)": "Unsolicited demand",
    "Demanda Induzida (DI)": "Call-based selection",
}
BIOME_EN = {
    "Amazônia": "Amazon",
    "Caatinga": "Caatinga",
    "Cerrado": "Cerrado",
    "Mata Atlântica": "Atlantic Forest",
    "Pampa": "Pampa",
    "Pantanal": "Pantanal",
    "Marinho Costeiro": "Coastal and marine",
    "Costeiro Marinho": "Coastal and marine",
    "Zona Costeira e Marinha": "Coastal and marine zone",
    "Marítimo": "Marine",
    "Orla": "Coastline",
    "Mata Atlântica / Cerrado": "Atlantic Forest / Cerrado",
    "Cerrado / Caatinga": "Cerrado / Caatinga",
    "Mata Atlântica / Caatinga": "Atlantic Forest / Caatinga",
    "Cerrado / Amazônia": "Cerrado / Amazon",
    "Mata Atlântica e Pampa": "Atlantic Forest and Pampa",
    "Todos": "All",
}
MONTHS_PT = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}
TARGETS = {
    "icare_0165": "Develop an environmental education and climate awareness plan",
    "icare_0162": "Strengthen programs for control and conservation of protected areas",
    "new0002": "Strengthen context-sensitive selective waste collection to reduce health risks",
    "ipcc_0084": "Restore and create natural areas through ecosystem-based measures",
    "ipcc_0085": "Reduce pressures on ecosystems to build resilience",
    "ipcc_0089": "Map climate-risk areas and redirect development through land-use planning and regulation",
    "ipcc_0096": "Strengthen climate resilience in agriculture and livestock systems",
    "ipcc_0099": "Protect and enhance water sources and watersheds",
    "icare_0182": "Develop an urban afforestation plan",
    "icare_0186": "Implement integrated coastal zone management",
}

# Audited scope: every duplicated title in this frozen release. Singleton titles
# remain pending rather than being machine-translated or copied into English.
PROJECT_TITLE_EN = {
    "Formação de Agentes Populares de Educação Ambiental na Agricultura Familiar": "Training community environmental-education facilitators in family farming",
    "Educação Ambiental": "Environmental education",
    "Plano de Gerenciamento Integrado de Resíduos Sólidos": "Integrated solid-waste management plan",
    "Inventário Estadual de Resíduos Sólidos Industriais": "State inventory of industrial solid waste",
    "Gerenciamento Integrado de Resíduos Sólidos": "Integrated solid-waste management",
    "Construção da Agenda 21 Local": "Development of the Local Agenda 21",
    "Saúde e Alegria (Continuação)": "Saúde e Alegria (continuation)",
    "Um Caminho para Gaia": "A Path to Gaia",
    "Recuperação de Animais": "Wildlife rescue and rehabilitation",
    "Recuperação de Matas Ciliares": "Riparian-forest restoration",
    "Diagnóstico de Agroecossistemas": "Agroecosystem assessment",
    "Arte e Educação Ambiental": "Art and environmental education",
    "Aterro Sanitário": "Sanitary landfill",
    "Coleta Seletiva de Lixo": "Separate waste collection",
    "Cidade Ecológica": "Ecological City",
    "Peixes Migratórios": "Migratory fish",
    "Educação não Formal": "Non-formal education",
    "Brasil Alternativo": "Alternative Brazil",
    "Mapeamento de Biótopos": "Biotope mapping",
    "Recuperação de Áreas Degradadas": "Restoration of degraded areas",
    "Plano de Gestão Integrada de Resíduos Sólidos": "Integrated solid-waste management plan",
    "Gestão Integrada de Resíduos Sólidos Urbanos": "Integrated municipal solid-waste management",
    "Plano de Gerenciamento Integrado de Resíduos Sólidos Urbanos": "Integrated municipal solid-waste management plan",
    "Manejo Sustentado de Quelônios da Amazônia": "Sustainable management of Amazonian turtles",
    "Implementação da Unidade de Resgate e Reabilitação do Peixe-Boi Marinho": "Establishment of the marine-manatee rescue and rehabilitation unit",
    "Elaboração dos Planos de Utilização das Unidades de Produção": "Preparation of utilization plans for production units",
    "Ações Educativas para Gestão dos Resíduos Sólidos Urbanos": "Educational activities for municipal solid-waste management",
}

ORIGIN_CALL_EN = {
    "EDITAL FNMA 04/2005 – Apoio à Criação e Fortalecimento de Fundos Socioambientais Públicos": "FNMA Call 04/2005 — Support for creating and strengthening public socio-environmental funds",
    "Edital 01/2012 - Elaboração de Planos Estaduais de Recursos Hídricos na Amazônia Legal": "Call 01/2012 — Preparation of state water-resources plans in the Legal Amazon",
    "Edital 01/2013 - Formação de Agentes Populares de Educação Ambiental na Agricultura Familiar": "Call 01/2013 — Training community environmental-education facilitators in family farming",
    "Edital 01/2015 - Recuperação de Áreas de Preservação Permanente para produção de Água": "Call 01/2015 — Restoration of permanent preservation areas for water production",
    "Edital 02/2013 - Apoio ao Cumprimento da Nova Lei Florestal por meio do Fortalecimento da Produção e Oferta de Sementes e Mudas Nativas": "Call 02/2013 — Support for compliance with the new Forest Law by strengthening the production and supply of native seeds and seedlings",
    "Edital FNMA 01/2002 Assistência Técnica e Extensão Florestal aos Agricultores Familiares da Mata Atlântica": "FNMA Call 01/2002 — Technical assistance and forestry extension for family farmers in the Atlantic Forest",
    "Edital FNMA 01/2003 Manejo de Espécies da Fauna Ameaçadas de Extinção": "FNMA Call 01/2003 — Management of threatened wildlife species",
    "Edital FNMA 01/2004 Formação de Agentes Multidisciplinares e Assessoria Técnica e Extensão Florestal aos Agricultores Familiares do Bioma Caatinga": "FNMA Call 01/2004 — Training multidisciplinary facilitators and providing technical assistance and forestry extension to family farmers in the Caatinga biome",
    "Edital FNMA 01/2005 Mosaicos de Áreas Protegidas: Uma Estratégia de Desenvolvimento Territorial com Base Conservacionista.": "FNMA Call 01/2005 — Protected-area mosaics: a conservation-based territorial-development strategy",
    "Edital FNMA 01/2006 Formação de Agentes Multiplicadores, Assistência Técnica e Extensão Rural em Atividades Florestais aos Agricultores Familiares no Bioma Amazônia": "FNMA Call 01/2006 — Training facilitators and providing technical assistance and rural extension in forestry activities for family farmers in the Amazon biome",
    "Edital FNMA 02/2002 Gestão Participativa do Uso dos Recursos Pesqueiros nas Zonas Costeira e Marinha": "FNMA Call 02/2002 — Participatory management of fishery-resource use in coastal and marine zones",
    "Edital FNMA 02/2003 Agenda 21": "FNMA Call 02/2003 — Agenda 21",
    "Edital FNMA 02/2004 Formação de Agentes Multiplicadores, Assistência Técnica e Extensão Rural em Atividades Florestais aos Agricultores Familiares no Bioma Cerrado": "FNMA Call 02/2004 — Training facilitators and providing technical assistance and rural extension in forestry activities for family farmers in the Cerrado biome",
    "Edital FNMA 02/2005 Recuperação e proteção das nascentes e áreas que margeiam os corpos d'água": "FNMA Call 02/2005 — Restoration and protection of springs and riparian areas",
    "Edital FNMA 03/2001 Unidades de Conservação": "FNMA Call 03/2001 — Protected areas",
    "Edital FNMA 03/2002 Gestão e Manejo Comunitário dos Recursos Florestais e Pesqueiros na Amazônia Legal": "FNMA Call 03/2002 — Community management of forest and fishery resources in the Legal Amazon",
    "Edital FNMA 03/2003 Fortalecimento da Gestão Participativa em Unidades de Conservação de Uso Sustentável.": "FNMA Call 03/2003 — Strengthening participatory management in sustainable-use protected areas",
    "Edital FNMA 03/2005 Apoio ao fortalecimento da gestão ambiental e do ordenamento territorial dos municípios localizados na área de influência da rodovia BR 163/trecho Cuiabá-Santarém.": "FNMA Call 03/2005 — Support for strengthening environmental management and territorial planning in municipalities influenced by the Cuiabá–Santarém section of highway BR-163",
    "Edital FNMA 04/2001 Manejo de Espécies Ameaçadas de Extinção": "FNMA Call 04/2001 — Management of threatened species",
    "Edital FNMA 04/2003 Programa de apoio às organizações de materiais recicláveis nas regiões metropolitanas e capitais": "FNMA Call 04/2003 — Support programme for recyclable-material organizations in metropolitan regions and state capitals",
    "Edital FNMA 04/2005 Apoio à Criação e ao Fortalecimento de Fundos Socioambientais Públicos": "FNMA Call 04/2005 — Support for creating and strengthening public socio-environmental funds",
    "Edital FNMA 05/2003 Fortalecimento da Gestão Ambiental nos Municípios da Amazônia Legal.": "FNMA Call 05/2003 — Strengthening environmental management in Legal Amazon municipalities",
    "Edital FNMA 05/2005 Coletivos Educadores para Territórios Sustentáveis": "FNMA Call 05/2005 — Educator collectives for sustainable territories",
    "Edital FNMA 06/2000 Fomento a Projetos de Gestão Integrada de Resíduos Sólidos Urbanos": "FNMA Call 06/2000 — Support for integrated municipal solid-waste management projects",
    "Edital FNMA 06/2001 Gestão Ambiental em Terras Indígenas": "FNMA Call 06/2001 — Environmental management in Indigenous lands",
    "Edital FNMA 07/2005 Fomento a projetos de gestão integrada de resíduos sólidos urbanos na bacia do rio São Francisco": "FNMA Call 07/2005 — Support for integrated municipal solid-waste management projects in the São Francisco River basin",
    "Edital FNMA 1/2024 - Apoio às Cooperativas e Associações de Catadoras e Catadores de Materiais Reutilizáveis e Recicláveis": "FNMA Call 1/2024 — Support for cooperatives and associations of collectors of reusable and recyclable materials",
    "Edital FNMA 10/2001 Apoio à Gestão Integrada em Unidades de Conservação": "FNMA Call 10/2001 — Support for integrated management in protected areas",
    "Edital FNMA 11/2001 Difusão e Capacitação em Sistemas Agroflorestais": "FNMA Call 11/2001 — Outreach and training in agroforestry systems",
    "Edital FNMA 12/2001 Fomento a Projetos de Gestão Integrada de Resíduos Sólidos Urbanos": "FNMA Call 12/2001 — Support for integrated municipal solid-waste management projects",
    "Edital FNMA 2/2023 - Centros de Educação e Cooperação Socioambiental": "FNMA Call 2/2023 — Socio-environmental education and cooperation centres",
    "Edital FNMA Nº 01/2003 Manejo de Espécies da Fauna Ameaçadas de Extinção, Visando à Conservação da Diversidade Biológica Brasileira": "FNMA Call 01/2003 — Management of threatened wildlife species to conserve Brazilian biological diversity",
    "Edital FNMA Nº 05/2001 Fomento a Projetos de Gestão Integrada de Resíduos Sólidos Urbanos": "FNMA Call 05/2001 — Support for integrated municipal solid-waste management projects",
    "Edital FNMA Nº 08/2001 Combate à Desertificação": "FNMA Call 08/2001 — Combating desertification",
    "Edital FNMA Nº 09/2001 Mudanças Climáticas": "FNMA Call 09/2001 — Climate change",
    "Edital FNMA/FNMC 01/2018 - Iniciativas socioambientais para redução de vulnerabilidade à mudança do clima em àreas urbanas": "FNMA/FNMC Call 01/2018 — Socio-environmental initiatives to reduce climate-change vulnerability in urban areas",
    "Edital FNMC 1/2023 - Iniciativas Socioambientais para Redução de Vulnerabilidade à Mudança do Clima em Áreas Urbanas e Rurais": "FNMC Call 1/2023 — Socio-environmental initiatives to reduce climate-change vulnerability in urban and rural areas",
    "Termo de Referência FNMA 01/2007 Recuperação e Conservação da Sub-bacia do Rio Taquari (MT/MS)": "FNMA Terms of Reference 01/2007 — Restoration and conservation of the Taquari River sub-basin (Mato Grosso/Mato Grosso do Sul)",
    "Termo de Referência FNMA 02/2004 Implantação de \"Centros Irradiadores de Manejo da Agrobiodiversidade - CIMAs\", em Áreas de Assentamentos de Reforma Agrária": "FNMA Terms of Reference 02/2004 — Establishment of Agrobiodiversity Management Outreach Centres (CIMAs) in agrarian-reform settlements",
    "Termo de Referência FNMA 02/2007 - Recuperação Ambiental da Bacia do Rio dos Sinos": "FNMA Terms of Reference 02/2007 — Environmental restoration of the Rio dos Sinos basin",
    "Termo de Referência FNMA 03/2007 Estratégia Integrada de Conservação e Manejo da Biodiversidade para o Estado da Bahia": "FNMA Terms of Reference 03/2007 — Integrated biodiversity conservation and management strategy for the State of Bahia",
    "Termo de Referência FNMA 04/2004 Plano Nacional de Prevenção, Preparação e Resposta Rápida a Emergências Ambientais com Produtos Químicos Perigosos (P2R2) - Mapeamento de Áreas de Risco": "FNMA Terms of Reference 04/2004 — National plan for preventing, preparing for and rapidly responding to environmental emergencies involving hazardous chemicals (P2R2): risk-area mapping",
    "Termo de Referência FNMA 05/2004 Elaboração de Planos Estaduais de Recursos Hídricos": "FNMA Terms of Reference 05/2004 — Preparation of state water-resources plans",
    "Termo de Referência Nº 01/2004 Proambiente": "Terms of Reference 01/2004 — Proambiente",
    "Termo de Referência Nº 01/2005 Apoio a Iniciativas de Implementação de Mecanismos de Desenvolvimento Limpo - MDL na Caatinga": "Terms of Reference 01/2005 — Support for Clean Development Mechanism (CDM) implementation initiatives in the Caatinga",
    "Uso Sustentável dos Recursos Pesqueiros": "Sustainable use of fishery resources",
}


def clean_text(value: str) -> str:
    """Trim Unicode whitespace and collapse embedded whitespace in descriptions."""
    return re.sub(r"\s+", " ", value.replace("\ufeff", "").replace("\xa0", " ")).strip()


def money(value: str) -> str:
    text = clean_text(value).replace("R$", "").replace(".", "").replace(",", ".")
    return f"{Decimal(text):.2f}" if text else ""


def parse_date(value: str) -> tuple[str, str]:
    """Return ISO date and status while retaining the source text elsewhere."""
    text = clean_text(value)
    if not text:
        return "", "missing"
    if text.casefold() == "anulado":
        return "", "cancelled_marker"
    parts = text.split("/")
    try:
        if len(parts) == 3 and parts[1].casefold()[:3] in MONTHS_PT:
            day = int(parts[0])
            month = MONTHS_PT[parts[1].casefold()[:3]]
            year = int(parts[2]) + (2000 if len(parts[2]) == 2 else 0)
            return datetime(year, month, day).date().isoformat(), "parsed"
        day, month, year = (int(part) for part in parts)
        if year < 100:
            year += 2000 if year < 50 else 1900
        return datetime(year, month, day).date().isoformat(), "parsed"
    except (ValueError, TypeError):
        return "", "invalid_source_value"


def load_source(path: Path = RAW) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    if not rows:
        raise ValueError("FNMA source is empty")
    return rows


def stable_id(source: dict[str, str]) -> str:
    identity = "|".join(clean_text(source[key]) for key in (
        "Ano", " Nº  Interno", "Instituição Executora", "Título do Projeto", "Recursos do FNMA (R$)"
    ))
    return "fnma-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


def clean_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    for source_row_number, source in enumerate(source_rows, start=2):
        theme_pt = clean_text(source["Tema"])
        project_pt = clean_text(source["Título do Projeto"])
        call_pt = clean_text(source["Edital ou Termo de Referência de Origem do Projeto"])
        biome_pt = clean_text(source["Bioma"])
        signature_date, signature_status = parse_date(source["Data Assinatura"])
        gazette_date, gazette_status = parse_date(source["Data de Publicação no DOU"])
        end_date, end_status = parse_date(source["Data de Fim da Vigência"])
        fnma = money(source["Recursos do FNMA (R$)"])
        counterpart = money(source["Recursos de CP (R$)"])
        total = money(source["Valor Total do Projeto (R$)"])
        difference = Decimal(fnma) + Decimal(counterpart) - Decimal(total)
        cancelled = theme_pt == "ANULADO" or end_status == "cancelled_marker"
        project_en = PROJECT_TITLE_EN.get(project_pt, "")
        call_en = ORIGIN_CALL_EN.get(call_pt, "") if call_pt else ""
        cleaned.append({
            "record_id": stable_id(source),
            "source_row_number": str(source_row_number),
            "year": clean_text(source["Ano"]),
            "transfer_instrument_id": clean_text(source["Nº do Instrumento de Repasse"]),
            "internal_instrument_id": clean_text(source[" Nº  Interno"]),
            "theme": THEME_EN[theme_pt],
            "theme_pt": theme_pt,
            "executing_institution_name": clean_text(source["Instituição Executora"]),
            "project_title": project_en,
            "project_title_pt": project_pt,
            "project_title_translation_status": "reviewed_exact_translation" if project_en else "pending_free_text_translation",
            "state_code": clean_text(source["UF"]),
            "region": REGION_EN[clean_text(source["Região Geográfica"])],
            "region_pt": clean_text(source["Região Geográfica"]),
            "executing_institution_city_name": clean_text(source["Cidade da Instituição Executora"]),
            "biome": BIOME_EN.get(biome_pt, ""),
            "biome_pt": biome_pt,
            "institutional_sphere": SPHERE_EN[clean_text(source["Esfera Institucional"])],
            "institutional_sphere_pt": clean_text(source["Esfera Institucional"]),
            "signature_date": signature_date,
            "signature_date_source": clean_text(source["Data Assinatura"]),
            "gazette_publication_date": gazette_date,
            "gazette_publication_date_source": clean_text(source["Data de Publicação no DOU"]),
            "agreement_end_date": end_date,
            "agreement_end_date_source": clean_text(source["Data de Fim da Vigência"]),
            "date_parse_status": f"signature:{signature_status};gazette:{gazette_status};end:{end_status}",
            "fnma_planned_transfer_amount_brl": fnma,
            "counterpart_planned_amount_brl": counterpart,
            "total_planned_project_amount_brl": total,
            "amount_reconciliation_difference_brl": f"{difference:.2f}",
            "selection_type": SELECTION_EN[clean_text(source["Tipo de Seleção do Projeto"])],
            "selection_type_pt": clean_text(source["Tipo de Seleção do Projeto"]),
            "origin_call_name": call_en,
            "origin_call_name_pt": call_pt,
            "origin_call_translation_status": "reviewed_exact_translation" if call_pt else "not_applicable_missing_source",
            "translation_status": "reviewed_exact_translation" if project_en else "pending_free_text_translation",
            "proper_name_translation_status": "not_translated_source_proper_names_preserved",
            "record_status": "cancelled" if cancelled else "not_stated",
            "funding_stage": "signed_transfer_instrument",
            "source_url": SOURCE_URL,
        })
    return cleaned


def validate_rows(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 1495
    assert len({row["record_id"] for row in rows}) == len(rows)
    assert {row["year"] for row in rows} == {
        "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999",
        "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2010", "2011",
        "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2020", "2023", "2024",
    }
    assert sum(row["record_status"] == "cancelled" for row in rows) == 13
    assert sum(Decimal(row["fnma_planned_transfer_amount_brl"]) for row in rows) == Decimal("313760048.78")
    assert sum(Decimal(row["counterpart_planned_amount_brl"]) for row in rows) == Decimal("97742203.92")
    assert sum(Decimal(row["total_planned_project_amount_brl"]) for row in rows) == Decimal("411707559.03")
    mismatches = [row for row in rows if abs(Decimal(row["amount_reconciliation_difference_brl"])) > Decimal("0.01")]
    assert len(mismatches) == 1
    assert mismatches[0]["source_row_number"] == "1435"
    assert len(PROJECT_TITLE_EN) == 27
    assert len({row["project_title_pt"] for row in rows}) == 1448
    assert sum(bool(row["project_title"]) for row in rows) == 74
    assert len({row["project_title_pt"] for row in rows if row["project_title"]}) == 27
    assert sum(row["translation_status"] == "pending_free_text_translation" for row in rows) == 1421
    assert len(ORIGIN_CALL_EN) == 46
    assert {row["origin_call_name_pt"] for row in rows if row["origin_call_name_pt"]} == set(ORIGIN_CALL_EN)
    assert sum(bool(row["origin_call_name"]) for row in rows) == 531
    assert all(row["origin_call_name"] for row in rows if row["origin_call_name_pt"])
    assert all(not row["biome_pt"] or row["biome"] for row in rows)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def action_bank_targets(path: Path = ACTION_BANK) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        raw = list(csv.reader(handle))
    return {row[0]: row[1] for row in raw[2:] if len(row) > 1 and row[0]}


def draft_link(row: dict[str, str]) -> tuple[str, str, str, str]:
    """Return target, role, confidence and rationale; at most one link per source row."""
    if row["record_status"] == "cancelled":
        return "", "none", "none", "Cancelled source record; no current action evidence is claimed."
    text = f'{row["project_title_pt"]} {row["theme_pt"]}'.casefold()
    if re.search(r"arboriza|arborização urbana", text):
        return "icare_0182", "direct", "high", "The project title explicitly describes urban tree planting."
    if re.search(r"restaura|refloresta|recupera.+(?:mata|floresta|vegetação|área degradada)|mata ciliar", text):
        return "ipcc_0084", "direct", "high", "The project title explicitly describes ecosystem restoration or recovery."
    if re.search(r"bacia|nascentes?|mananciais?|recursos hídricos", text) and re.search(r"prote|recuper|conserv|manejo|gestão", text):
        return "ipcc_0099", "direct", "high", "The title describes protection or management of water sources or watersheds."
    if re.search(r"zoneamento|ordenamento territorial|plano diretor|mapeamento de risco", text):
        return "ipcc_0089", "component", "medium", "The territorial-planning output may enable risk-aware land-use decisions; climate-risk intent needs adjudication."
    if re.search(r"agroecolog|agroflorest|agricultura sustentável", text):
        return "ipcc_0096", "component", "medium", "The project supports resilient production practices, but adaptation intent is not explicit."
    if re.search(r"gestão costeira|gerenciamento costeiro|zona costeira", text):
        return "icare_0186", "component", "medium", "The project concerns coastal-zone management; the climate-resilience link needs adjudication."
    if row["theme_pt"] == "Educação Ambiental":
        return "icare_0165", "enabling", "medium", "Environmental education is an enabling instrument; climate-awareness relevance is not explicit in most titles."
    if row["theme_pt"] == "Gestão de Áreas Protegidas":
        return "icare_0162", "component", "medium", "The publisher theme indicates protected-area management, but project scope varies."
    if row["theme_pt"] in {"Gestão Integrada de Resíduos Sólidos", "Resíduos Sólidos"}:
        return "new0002", "component", "medium", "The source concerns solid-waste management; selective-collection and health-risk scope needs record-level adjudication."
    if row["theme_pt"] == "Conservação e Manejo da Biodiversidade":
        return "ipcc_0085", "related", "medium", "Biodiversity conservation may reduce ecosystem pressure, but the adaptation pathway is not explicit."
    return "", "none", "none", "No defensible link to a current adaptation action from the available title and controlled theme."


def build_mapping(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    bank = action_bank_targets()
    for target_id, target_name in TARGETS.items():
        assert bank.get(target_id) == target_name, (target_id, bank.get(target_id), target_name)
    mappings: list[dict[str, str]] = []
    for row in rows:
        action_id, match_type, confidence, rationale = draft_link(row)
        mappings.append({
            "record_id": row["record_id"],
            "internal_instrument_id": row["internal_instrument_id"],
            "project_title_pt": row["project_title_pt"],
            "action_id": action_id,
            "action_name": TARGETS.get(action_id, ""),
            "match_type": match_type,
            "mapping_confidence": confidence,
            "adjudication_status": "pending" if confidence == "medium" else "not_required",
            "rationale": rationale,
        })
    assert len(mappings) == len(rows)
    assert len({row["record_id"] for row in mappings}) == len(rows)
    assert all(not row["action_id"] or row["action_id"] in bank for row in mappings)
    return mappings


def export_release(rows: list[dict[str, str]], mappings: list[dict[str, str]]) -> None:
    write_csv(OUTPUT, rows)
    write_csv(MAPPING, mappings)


def main() -> None:
    source = load_source()
    rows = clean_rows(source)
    validate_rows(rows)
    mappings = build_mapping(rows)
    export_release(rows, mappings)
    print({
        "records": len(rows),
        "cancelled": sum(row["record_status"] == "cancelled" for row in rows),
        "project_title_translated_rows": sum(bool(row["project_title"]) for row in rows),
        "project_title_distinct_translated": len({row["project_title_pt"] for row in rows if row["project_title"]}),
        "project_title_distinct_pending": len({row["project_title_pt"] for row in rows if not row["project_title"]}),
        "origin_call_translated_rows": sum(bool(row["origin_call_name"]) for row in rows),
        "mapping_confidence": dict(Counter(row["mapping_confidence"] for row in mappings)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "mapping": str(MAPPING.relative_to(ROOT)),
    })


if __name__ == "__main__":
    main()
