#!/usr/bin/env python3
"""Build the bilingual Novo PAC drainage and slope-containment review release."""

from __future__ import annotations

import csv
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RAW = HERE / "sample/novopac_compile_rows.csv"  # Novo PAC rows extracted in the retired br-climate-awards compile
OUT = HERE / "sample/br_novopac_drainage_slopes.csv"
MAP = HERE / "sample/br_novopac_drainage_slopes_to_adaptation_actions.csv"

CUSTOM_TRANSLATIONS = {
    "Novo PAC 2025 total (agregado nacional)": "Novo PAC 2025 total (national aggregate)",
    "Novo PAC 2025 drenagem (agregado nacional)": "Novo PAC 2025 drainage (national aggregate)",
    "Novo PAC 2025 contencao-encostas (agregado nacional)": "Novo PAC 2025 slope containment (national aggregate)",
    "Sistema de Macrodrenagem na sede do município de Coruripe": "Stormwater macrodrainage system in the municipal seat of Coruripe",
    "Sistema de Macrodrenagem da bacia do Córrego Embira": "Stormwater macrodrainage system for the Córrego Embira basin",
    "Sistema de Macrodrenagem dos cursos d' água da Av. Várzea da Palma e da Av. Central": "Stormwater macrodrainage system for the waterways along Avenida Várzea da Palma and Avenida Central",
    "Projeto de Macrodrenagem na bacia do Córrego dos Pintos.": "Macrodrainage project for the Córrego dos Pintos basin",
    "Sistema de Macrodrenagem nos bairros Conjunto Lagoa / Paquetá": "Macrodrainage system in the Conjunto Lagoa and Paquetá neighbourhoods",
    "Projeto de Macrodrenagem na bacia dos Córregos Vilarinho e do Nado": "Macrodrainage project for the Córrego Vilarinho and Córrego do Nado basins",
    "Execução de rede de drenagem pluvial na sub-bacia denominada Geraldo Abrão, no bairro Granada na cidade Uberlândia.": "Construction of a stormwater drainage network in the Geraldo Abrão sub-basin, in the Granada neighbourhood of Uberlândia",
    "Implantação de 3 reservatórios de detenção ao longo do Córrego Lagoinha, localizados a montante das Ruas Jaime de Barros, Vasco Mascia e Benjamin Alves Santos, em Uberlândia/MG": "Construction of three detention reservoirs along Córrego Lagoinha, upstream of Rua Jaime de Barros, Rua Vasco Mascia and Rua Benjamin Alves Santos, in Uberlândia, Minas Gerais",
    "Execução de redes de drenagem pluvial em 8 sub-bacias do Córrego Lagoinha, abrangendo áreas críticas nos bairros Santa Mônica, Santa Luzia, Pampulha e Carajás, em Uberlândia/MG.": "Construction of stormwater drainage networks in eight Córrego Lagoinha sub-basins, covering critical areas in the Santa Mônica, Santa Luzia, Pampulha and Carajás neighbourhoods of Uberlândia, Minas Gerais",
    "Execução de redes de infraestrutura de drenagem pluvial no Loteamento Maná, bairro Morumbi, Uberlândia/MG.": "Construction of stormwater drainage infrastructure networks in the Maná subdivision, Morumbi neighbourhood, Uberlândia, Minas Gerais",
    "Execução de redes de infraestrutura de drenagem pluvial no Loteamento Zaire Rezende, no bairro Morumbi, em Uberlândia/MG.": "Construction of stormwater drainage infrastructure networks in the Zaire Rezende subdivision, Morumbi neighbourhood, Uberlândia, Minas Gerais",
    "Implantação de 2 reservatórios de detenção ao longo do Córrego Mogi, localizados a montante da Alameda Padre Manoel e Avenida Antônio Francisco, em Uberlândia/MG.": "Construction of two detention reservoirs along Córrego Mogi, upstream of Alameda Padre Manoel and Avenida Antônio Francisco, in Uberlândia, Minas Gerais",
    "Projeto de Macrodrenagem do Canal Real Estrela e Michele Carrara": "Macrodrainage project for Canal Real Estrela and Canal Michele Carrara",
    "Projeto de Macrodrenagem do Canal Calombé": "Macrodrainage project for Canal Calombé",
    "Projeto de Macrodrenagem do Canal Marilândia": "Macrodrainage project for Canal Marilândia",
    "Projeto de Macrodrenagem do Canal Jacque de Molay": "Macrodrainage project for Canal Jacque de Molay",
    "Sistema de Macrodrenagem na sede do Município de Lages": "Stormwater macrodrainage system in the municipal seat of Lages",
    "Sistema de Macrodrenagem da bacia do Córrego Pedrinhas": "Stormwater macrodrainage system for the Córrego Pedrinhas basin",
    "Readequação do sistema de intercepção da drenagem da orla da praia, entre os bairros Canto do Forte e Mirim.": "Upgrade of the beachfront drainage interception system between the Canto do Forte and Mirim neighbourhoods",
    "Readequação hidráulica do canal Praião": "Hydraulic upgrade of Canal Praião",
    "Readequação hidráulica do canal São Salvador": "Hydraulic upgrade of Canal São Salvador",
    "Implantação de galerias de drenagem nas Vilas Brasília e Costa do Sol, bacia do córrego Tijuco Preto": "Construction of stormwater drains in Vila Brasília and Costa do Sol, in the Córrego Tijuco Preto basin",
}

SOURCE_TITLE_TRANSLATIONS = {
    "Novo PAC viabiliza R$ 11,7 bilhões drenagem e contenção de encostas": "Novo PAC unlocks R$11.7 billion for drainage and slope-containment works",
    "MCidades — Seleção Novo PAC Contenção de Encostas e Drenagem (relação de propostas habilitadas)": "Ministry of Cities — Novo PAC Slope-Containment and Drainage Selection (list of eligible proposals)",
}


def translate_description(text: str) -> tuple[str, str]:
    """Return reviewed English text while preserving every proper place/entity name."""
    if text in CUSTOM_TRANSLATIONS:
        return CUSTOM_TRANSLATIONS[text], "reviewed_exact_translation"
    match = re.fullmatch(r"Novo PAC 2025 drenagem — Estado (?:Do|Da|De) (.+)", text)
    if match:
        return f"Novo PAC 2025 drainage — State of {match.group(1)}", "reviewed_template_translation_proper_name_preserved"
    match = re.fullmatch(r"Novo PAC 2025 drenagem — Munic[ií]pio (?:De|Do) (.+)", text)
    if match:
        return f"Novo PAC 2025 drainage — Municipality of {match.group(1)}", "reviewed_template_translation_proper_name_preserved"
    match = re.fullmatch(r"Novo PAC 2025 drenagem — (Consorcio .+)", text)
    if match:
        return f"Novo PAC 2025 drainage — {match.group(1)}", "reviewed_template_translation_proper_legal_name_preserved"
    match = re.fullmatch(r"Novo PAC 2025 encostas — (.+)", text)
    if match:
        return f"Novo PAC 2025 slope containment — {match.group(1)}", "reviewed_template_translation_proper_name_preserved"
    raise AssertionError(f"Unreviewed project-description translation: {text!r}")


def translate_note(text: str, project_description: str, project_description_pt: str) -> tuple[str, str]:
    controls = {
        "235 municípios, 26 estados. Control total.": "235 municipalities, 26 states. Control total.",
        "174 municípios (drenagem urbana). Control total.": "174 municipalities (urban drainage). Control total.",
        "102 municípios (contenção de encostas). Control total.": "102 municipalities (slope containment). Control total.",
    }
    if text in controls:
        return controls[text], "reviewed_exact_translation"
    match = re.fullmatch(
        r"\[(drenagem|encostas)/(OGU|FGTS|FGTS-fin)\] proposta ([\d/]+)\."
        r"(?: objeto: (.*?))? Reconciled to eixo control totals "
        r"\(drenagem R\$10\.3bn/174; encostas >R\$1\.4bn/102; total R\$11\.7bn/235mun/26UF\)\.",
        text,
    )
    if not match:
        raise AssertionError(f"Unreviewed note translation: {text!r}")
    theme, channel, proposal_id, source_object = match.groups()
    if source_object:
        assert source_object == project_description_pt
    theme_en = "drainage" if theme == "drenagem" else "slope-containment"
    result = f"[{theme_en}/{channel}] proposal {proposal_id}."
    if source_object:
        result += f" project description: {project_description}"
    result += " Reconciled to programme-axis control totals (drainage R$10.3bn/174; slope containment >R$1.4bn/102; total R$11.7bn/235 municipalities/26 UFs)."
    return result, "reviewed_structured_translation_proper_names_preserved"


rows = []
with RAW.open(newline="", encoding="utf-8-sig") as source:
    for raw in csv.DictReader(source):
        if raw["source_id"] not in {
            "novopac-2025-relacao-propostas-habilitadas",
            "novopac-2025-drenagem-encostas-release",
        }:
            continue
        native = ""
        if raw["source_id"] == "novopac-2025-relacao-propostas-habilitadas":
            match = re.search(r"proposta ([\d/]+)", raw["notes"])
            native = match.group(1) if match else ""
        description, translation_status = translate_description(raw["project_name"])
        notes, notes_status = translate_note(raw["notes"], description, raw["project_name"])
        source_title = SOURCE_TITLE_TRANSLATIONS[raw["source_title"]]
        rows.append(
            {
                "record_id": raw["id"],
                "native_record_id": native,
                "project_description": description,
                "project_description_pt": raw["project_name"],
                "translation_status": translation_status,
                "proper_name_translation_status": "not_translated_source_proper_names_preserved",
                "recipient": raw["recipient"],
                "recipient_type": raw["recipient_type"],
                "state_code": raw["uf"],
                "municipality_name": raw["municipio"],
                "instrument": raw["instrument"],
                "amount": raw["amount"],
                "currency": raw["currency"],
                "decision_date": raw["award_date"],
                "status": raw["status"],
                "funder": raw["funder"],
                "financier": raw["financier"],
                "source_id": raw["source_id"],
                "source_url": raw["source_url"],
                "source_title": source_title,
                "source_title_pt": raw["source_title"],
                "source_title_translation_status": "reviewed_exact_translation",
                "notes": notes,
                "notes_pt": raw["notes"],
                "notes_translation_status": notes_status,
            }
        )

assert len(rows) == 318
assert len({row["record_id"] for row in rows}) == 318
assert len({row["project_description_pt"] for row in rows}) == 279
assert len({row["project_description"] for row in rows}) == 279
assert all(row["project_description"] and row["project_description_pt"] for row in rows)
assert all(row["source_title"] and row["source_title_pt"] for row in rows)
assert all(row["notes"] and row["notes_pt"] for row in rows)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

# Mapping logic is intentionally unchanged; it continues to use Portuguese source text.
maps = []
for row in rows:
    text = (row["project_description_pt"] + " " + row["notes_pt"]).casefold()
    if "drenagem" in text:
        links = [("c40_0048", "Upgrade urban drainage systems", "direct", "high")]
    elif "encosta" in text or "estabiliza" in text:
        links = [("icare_0184", "Upgrade Slope stabilization and drainage", "direct", "high")]
    elif any(term in text for term in ["restaura", "áreas degradadas", "conservação", "florest"]):
        links = [("ipcc_0084", "Restore/create natural areas", "related", "medium")]
    elif any(term in text for term in ["resiliência", "adaptação", "climática"]):
        links = [("ipcc_0087", "Improve Infrastructure retrofitting", "related", "medium")]
    elif "saneamento" in text or "água" in text:
        links = [("ipcc_0101", "Improve urban water management", "related", "medium")]
    else:
        links = [("", "", "none", "none")]
    for action_id, action_name, match_type, confidence in links:
        maps.append(
            {
                "record_id": row["record_id"],
                "project_description_pt": row["project_description_pt"],
                "action_id": action_id,
                "action_name": action_name,
                "match_type": match_type,
                "mapping_confidence": confidence,
                "adjudication_status": "pending" if confidence == "medium" else "not required",
                "rationale": "Draft link from explicit source text; medium links require human adjudication." if action_id else "No defensible adaptation-action link from the published title.",
            }
        )

with MAP.open("w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=list(maps[0]))
    writer.writeheader()
    writer.writerows(maps)

SUMMARY = {
    "rows": len(rows),
    "distinct_project_descriptions": len({row["project_description_pt"] for row in rows}),
    "mapped": sum(bool(row["action_id"]) for row in maps),
    "translations_pending": sum(row["translation_status"].startswith("pending") for row in rows),
}
print(SUMMARY)
