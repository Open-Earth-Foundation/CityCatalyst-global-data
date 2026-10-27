"""Build the bilingual January-July 2026 civil-defence payment extract.

The source text is retained in paired ``*_pt`` fields. English descriptions are
exact, release-scoped translations of the finite values observed in the source.
Legal entity and place names are preserved rather than translated.
"""

from __future__ import annotations

import glob
import hashlib
import os
import zipfile
from decimal import Decimal

import pandas as pd


RAW_GLOB = "sample/2026*_Transferencias.zip"
OUT = "sample/br_transparencia_transferencias_civil_defence_payments.csv"
TARGET_ORGAN = "53000"
TARGET_ACTIONS = {"22BO", "8348"}

SOURCE_TO_BASE = {
    "ANO / MÊS": "transfer_year_month",
    "TIPO TRANSFERÊNCIA": "transfer_type",
    "TIPO FAVORECIDO": "beneficiary_type",
    "UF": "uf",
    "CÓDIGO MUNICÍPIO SIAFI": "siafi_municipality_code",
    "NOME MUNICÍPIO": "municipality_name",
    "CÓDIGO ÓRGÃO SIAFI": "organ_code",
    "NOME ÓRGÃO": "organ_name",
    "CÓDIGO UNIDADE GESTORA": "managing_unit_code",
    "NOME UNIDADE GESTORA": "managing_unit_name",
    "CÓDIGO FUNÇÃO": "function_code",
    "NOME FUNÇÃO": "function_name",
    "CÓDIGO SUBFUNÇÃO": "subfunction_code",
    "NOME SUBFUNÇÃO": "subfunction_name",
    "CÓDIGO PROGRAMA": "program_code",
    "NOME PROGRAMA": "program_name",
    "AÇÃO": "action_code",
    "NOME AÇÃO": "action_name",
    "LINGUAGEM CIDADÃ": "citizen_language_label",
    "CÓDIGO GRUPO DESPESA": "expense_group_code",
    "NOME GRUPO DESPESA": "expense_group_name",
    "CÓDIGO MODALIDADE APLICAÇÃO DESPESA": "application_modality_code",
    "NOME MODALIDADE APLICAÇÃO DESPESA": "application_modality_name",
    "CÓDIGO ELEMENTO DESPESA": "expense_element_code",
    "NOME ELEMENTO DESPESA": "expense_element_name",
    "CÓDIGO PLANO ORÇAMENTÁRIO": "budget_plan_code",
    "NOME PLANO ORÇAMENTÁRIO": "budget_plan_name",
    "CÓDIGO SUBTÍTULO": "subtitle_code",
    "NOME SUBTÍTULO": "subtitle_name",
    "CÓDIGO LOCALIZADOR": "localizer_code",
    "NOME LOCALIZADOR": "localizer_name",
    "SIGLA LOCALIZADOR": "localizer_acronym",
    "DESCRIÇÃO COMPLEMENTAR LOCALIZADOR": "localizer_complement",
    "CÓDIGO FAVORECIDO": "beneficiary_code",
    "NOME FAVORECIDO": "beneficiary_name",
    "VALOR TRANSFERIDO": "amount_transferred_raw",
}

TRANSLATABLE = {
    "transfer_type",
    "beneficiary_type",
    "organ_name",
    "managing_unit_name",
    "function_name",
    "subfunction_name",
    "program_name",
    "action_name",
    "citizen_language_label",
    "expense_group_name",
    "application_modality_name",
    "expense_element_name",
    "budget_plan_name",
    "subtitle_name",
    "localizer_name",
    "localizer_complement",
}

PROPER_NAMES = {"municipality_name", "beneficiary_name"}

CONTROLLED_TRANSLATIONS = {
    "Legais, Voluntárias e Específicas": "Legal, voluntary and specific transfers",
    "Administração Pública Municipal": "Municipal public administration",
    "Administração Pública Estadual ou do Distrito Federal": "State or Federal District public administration",
    "Administração Pública": "Public administration",
    "Ministério da Integração e do Desenvolvimento Regional - Unidades com vínculo direto": "Ministry of Integration and Regional Development - directly linked units",
    "SECRETARIA NACIONAL PROTECAO E DEFESA CIVIL": "National Secretariat for Civil Protection and Defence",
    "Segurança pública": "Public safety",
    "Defesa civil": "Civil protection and defence",
    "GESTAO DE RISCOS E DE DESASTRES": "Risk and disaster management",
    "ACOES DE PROTECAO E DEFESA CIVIL": "Civil protection and defence actions",
    "APOIO AS ACOES EMERGENCIAIS DE PREVENCAO E MITIGACAO PARA A REDUCAO DE DESASTRES": "Support for emergency prevention and mitigation actions to reduce disasters",
    "Sem informação": "No information",
    "Outras Despesas Correntes": "Other current expenditure",
    "Investimentos": "Investments",
    "Transferências a Municípios": "Transfers to municipalities",
    "Transferências a Estados e ao Distrito Federal": "Transfers to states and the Federal District",
    "Contribuições": "Contributions",
    "Auxílios": "Grants",
    "Múltiplo": "Multiple",
    "ACOES DE RESPOSTA E DE RECUPERACAO DE INFRAESTRUTURA DESTRUIDA POR DESASTRES": "Response actions and recovery of infrastructure destroyed by disasters",
    "APOIO A ACOES EMERGENCIAIS DE PREVENCAO E MITIGACAO PARA REDUCAO DE DESASTRES": "Support for emergency prevention and mitigation actions to reduce disasters",
    "APOIO A OBRAS PREVENTIVAS DE DESASTRES - DESPESAS DIVERSAS": "Support for disaster-prevention works - miscellaneous expenditure",
    "CALAMIDADE PUBLICA - MEDIDA PROVISORIA N. 1.218, DE 11 DE MAIO DE 2024 - ACOES DE PROTECAO E DEFESA CIVIL": "Public calamity - Provisional Measure No. 1,218 of 11 May 2024 - civil protection and defence actions",
    "CALAMIDADE PUBLICA - MEDIDA PROVISORIA N. 1.244 DE 17 DE JULHO DE 2024 - ACOES DE REPOSTA E RECUPERACAO": "Public calamity - Provisional Measure No. 1,244 of 17 July 2024 - response and recovery actions [source says REPOSTA]",
    "CALAMIDADE PUBLICA - MEDIDA PROVISORIA N. 1.265, DE 11 DE OUTUBRO DE 2024 - ACOES DE REPOSTA E RECUPERACAO": "Public calamity - Provisional Measure No. 1,265 of 11 October 2024 - response and recovery actions [source says REPOSTA]",
    "EMERGENCIA CLIMATICA (ADPF N. 743) - MEDIDA PROVISORIA N. 1.268, DE 22 DE OUTUBRO DE 2024 - ACOES DE REPOSTA E RECUPERACAO - AMAZONIA LEGAL": "Climate emergency (ADPF No. 743) - Provisional Measure No. 1,268 of 22 October 2024 - response and recovery actions - Legal Amazon [source says REPOSTA]",
    "MEDIDA PROVISORIA N. 1.102 DE 24 DE FEVEREIRO DE 2022 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,102 of 24 February 2022 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.180, DE 14 DE JULHO DE 2023 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,180 of 14 July 2023 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.188 DE 19 DE SETEMBRO DE 2023 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,188 of 19 September 2023 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.191 DE 25 DE OUTUBRO DE 2023 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,191 of 25 October 2023 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.204, DE 29 DE DEZEMBRO DE 2023 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,204 of 29 December 2023 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.214 DE 29 DE ABRIL DE 2024 - ACOES DE PROTECAO E DEFESA CIVIL": "Provisional Measure No. 1,214 of 29 April 2024 - civil protection and defence actions",
    "MEDIDA PROVISORIA N. 1.279, DE 16 DE DEZEMBRO DE 2024 - ACOES DE REPOSTA E RECUPERACAO - NACIONAL": "Provisional Measure No. 1,279 of 16 December 2024 - response and recovery actions - national [source says REPOSTA]",
    "MEDIDA PROVISORIA N. 1.299 DE 09 DE MAIO DE 2025 - ACOES DE RESPOSTA E RECUPERACAO": "Provisional Measure No. 1,299 of 9 May 2025 - response and recovery actions",
    "MEDIDA PROVISORIA N. XXX, DE XX DE ABRIL DE 2026 - ACOES DE REPOSTA E RECUPERACAO - NACIONAL": "Provisional Measure No. XXX of XX April 2026 - response and recovery actions - national [source placeholder and REPOSTA]",
    "MEDIDA PROVISORIA N. XXX, DE XX DE DEZEMBRO DE 2025 - ACOES DE REPOSTA E RECUPERACAO": "Provisional Measure No. XXX of XX December 2025 - response and recovery actions [source placeholder and REPOSTA]",
    "MEDIDA PROVISORIA N. XXXX, DE XX DE DEZEMBRO DE 2026 - ACOES DE RESPOSTA E RECUPERACAO - ZONA DA MATA/MG": "Provisional Measure No. XXXX of XX December 2026 - response and recovery actions - Zona da Mata/MG [source placeholder]",
    "MEDIDA PROVISORIA N. XXXXX, DE XX DE MAIO DE 2026 - ACOES DE REPOSTA E RECUPERACAO - NACIONAL": "Provisional Measure No. XXXXX of XX May 2026 - response and recovery actions - national [source placeholder and REPOSTA]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NA AMAZONIA LEGAL (C": "Civil protection and defence actions - in the Legal Amazon (C [source truncated]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NACIONAL": "Civil protection and defence actions - national",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NACIONAL (CREDITO EX": "Civil protection and defence actions - national (supplementary cred [source truncated]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NO ESTADO DE MINAS G": "Civil protection and defence actions - in the state of Minas G [source truncated]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NO ESTADO DO RIO GRA": "Civil protection and defence actions - in the state of Rio Gra [source truncated]",
    "APOIO AS ACOES EMERGENCIAIS DE PREVEN - NACIONAL": "Support for emergency prevention actions - national [source truncated]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NA AMAZO": "Civil protection and defence actions - in the Legal Amazo [source truncated]",
    "ACOES DE PROTECAO E DEFESA CIVIL   - NO ESTAD": "Civil protection and defence actions - in the state [source truncated]",
    "APOIO AS ACOES EMERGENCIAIS DE PREVEN - NACIO": "Support for emergency prevention actions - nation [source truncated]",
    "": "",
}


def parse_brl(value: str) -> Decimal:
    return Decimal(value.replace(",", "."))


def load_raw() -> pd.DataFrame:
    frames = []
    for path in sorted(glob.glob(RAW_GLOB)):
        with zipfile.ZipFile(path) as archive:
            members = archive.namelist()
            assert len(members) == 1, f"{path}: expected one member"
            with archive.open(members[0]) as stream:
                frame = pd.read_csv(stream, sep=";", encoding="cp1252", dtype=str, keep_default_na=False)
        frame["source_file"] = os.path.basename(path)
        frames.append(frame)
    assert len(frames) == 7, f"expected seven monthly files, found {len(frames)}"
    return pd.concat(frames, ignore_index=True)


def translate(frame: pd.DataFrame) -> pd.DataFrame:
    output = pd.DataFrame(index=frame.index)
    for source, base in SOURCE_TO_BASE.items():
        values = frame[source]
        if base in TRANSLATABLE:
            missing = sorted(set(values) - set(CONTROLLED_TRANSLATIONS))
            assert not missing, f"untranslated values in {base}: {missing}"
            output[base] = values.map(CONTROLLED_TRANSLATIONS)
            output[f"{base}_pt"] = values
        elif base in PROPER_NAMES:
            output[base] = values
            output[f"{base}_pt"] = values
        else:
            output[base] = values
    output["source_file"] = frame["source_file"]
    output["amount_transferred_brl"] = output["amount_transferred_raw"].map(parse_brl).astype(float)
    code_fields = ["program_code", "expense_group_code", "application_modality_code", "expense_element_code", "budget_plan_code", "subtitle_code", "localizer_code"]
    name_fields_pt = ["program_name_pt", "expense_group_name_pt", "application_modality_name_pt", "expense_element_name_pt", "budget_plan_name_pt", "subtitle_name_pt", "localizer_name_pt"]
    output["is_multiple_classification"] = output[code_fields].isin(["MU", "-14"]).any(axis=1) | output[name_fields_pt].eq("Múltiplo").any(axis=1)
    output["translation_status"] = "complete_exact_release_dictionary"
    output["proper_name_translation_status"] = "not_translated_source_proper_name_preserved"
    return output


def validate(raw: pd.DataFrame, output: pd.DataFrame) -> None:
    assert raw.shape == (1_056_421, 37)
    july = "sample/202607_Transferencias.zip"
    assert hashlib.md5(open(july, "rb").read()).hexdigest() == "14cc4c826bb836ff16aec4f33c3c1ab6"
    assert len(output) == 743
    assert output["action_code"].value_counts().to_dict() == {"22BO": 740, "8348": 3}
    totals = output.groupby("action_code")["amount_transferred_brl"].sum().round(2).to_dict()
    assert totals == {"22BO": 574_570_441.75, "8348": 21_447_873.31}
    assert round(output["amount_transferred_brl"].sum(), 2) == 596_018_315.06
    assert output["beneficiary_code"].str.fullmatch(r"\d{14}").all()
    assert output["is_multiple_classification"].sum() == 38
    assert output["translation_status"].eq("complete_exact_release_dictionary").all()
    for base in TRANSLATABLE | PROPER_NAMES:
        assert f"{base}_pt" in output.columns
    assert output["action_name"].str.contains("Civil|Support", regex=True).all()
    assert output["action_name_pt"].str.contains("ACOES").all()
    assert output["budget_plan_name"].str.strip().ne("").all()
    assert output["budget_plan_name_pt"].str.contains("REPOSTA").any()
    assert not output.duplicated().any()


def main() -> None:
    raw = load_raw()
    target = raw.loc[raw["CÓDIGO ÓRGÃO SIAFI"].eq(TARGET_ORGAN) & raw["AÇÃO"].isin(TARGET_ACTIONS)].reset_index(drop=True)
    output = translate(target)
    validate(raw, output)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    output.to_csv(OUT, index=False, encoding="utf-8")
    reread = pd.read_csv(OUT, dtype=str, keep_default_na=False)
    assert reread.shape == output.shape
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {len(output)} rows x {len(output.columns)} columns; total R$ {output['amount_transferred_brl'].sum():,.2f}; sha256 {digest}")


if __name__ == "__main__":
    main()
