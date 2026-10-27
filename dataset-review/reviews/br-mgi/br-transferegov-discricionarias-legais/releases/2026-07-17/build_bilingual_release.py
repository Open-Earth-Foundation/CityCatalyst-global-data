#!/usr/bin/env python3
"""Stream the large proposal-grain working output into the bilingual house schema."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "sample/br_transferegov_proposals_2026-07-17.csv.gz"
OUTPUT = HERE / "sample/br_transferegov_proposals_2026-07-17_bilingual.csv.gz"
MAPPING = HERE / "data/br_transferegov_theme_to_adaptation_actions.csv"

RENAMES = {
    "id_proposta": "proposal_id", "nr_proposta": "proposal_number", "nr_convenio": "agreement_number",
    "uf": "state_code", "cod_ibge": "municipality_ibge_code", "municipio": "municipality_name",
    "cnpj_proponente": "applicant_cnpj", "nome_proponente": "applicant_name",
    "orgao_superior": "superior_federal_body_pt", "orgao_concedente": "granting_body_pt",
    "id_programa": "programme_id", "cod_programa": "programme_code", "nome_programa": "programme_name_pt",
    "orgao_programa": "programme_body_pt", "acao_orcamentaria": "budget_action_code",
    "subtipo_programa": "programme_subtype_pt", "n_programas": "programme_count",
    "subtipo_proposta": "proposal_subtype_pt", "enviada_mandataria": "sent_to_mandatary_pt",
    "item_investimento": "investment_item_pt", "objeto_proposta": "proposal_object_pt",
    "sit_proposta": "proposal_status_pt", "sit_convenio": "agreement_status_pt",
    "situacao_contratacao": "contracting_status_pt", "dt_proposta": "proposal_date",
    "dt_assinatura": "signature_date", "vl_global_prop_cent": "proposal_total_centavos",
    "vl_repasse_prop_cent": "proposal_federal_share_centavos", "vl_contrapartida_prop_cent": "proposal_counterpart_centavos",
    "vl_global_conv_cent": "agreement_total_centavos", "vl_repasse_conv_cent": "agreement_federal_share_centavos",
    "vl_contrapartida_conv_cent": "agreement_counterpart_centavos", "vl_empenho_net_cent": "net_commitment_centavos",
    "vl_empenho_gross_pos_cent": "gross_positive_commitment_centavos", "vl_desembolso_net_cent": "net_disbursement_centavos",
    "vl_pago_net_cent": "net_payment_centavos", "vl_pago_convenente_net_cent": "net_applicant_payment_centavos",
    "n_empenho_events": "commitment_event_count", "n_desembolsos": "disbursement_count", "n_pagamentos": "payment_count",
}

PAIRED = {
    "natureza_juridica": ("applicant_legal_nature", "applicant_legal_nature_pt"),
    "modalidade": ("transfer_modality", "transfer_modality_pt"),
}

LEGAL_NATURE = {
    "Administração Pública Municipal": "Municipal public administration",
    "Administração Pública Estadual ou do Distrito Federal": "State or Federal District public administration",
    "Organização da Sociedade Civil": "Civil-society organisation",
    "Consórcio Público": "Public consortium",
}


def main() -> None:
    with gzip.open(SOURCE, "rt", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        base = []
        for name in reader.fieldnames or []:
            if name in PAIRED:
                base.extend(PAIRED[name])
            else:
                base.append(RENAMES.get(name, name))
        extra = ["programme_name", "investment_item", "proposal_object", "free_text_translation_status"]
        fields = base + extra
        with gzip.open(OUTPUT, "wt", encoding="utf-8", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=fields)
            writer.writeheader()
            count = 0
            for row in reader:
                out = {}
                for key, value in row.items():
                    if key == "natureza_juridica":
                        out["applicant_legal_nature_pt"] = value
                        out["applicant_legal_nature"] = LEGAL_NATURE.get(value, "")
                    elif key == "modalidade":
                        out["transfer_modality_pt"] = value
                        out["transfer_modality"] = ""
                    else:
                        out[RENAMES.get(key, key)] = value
                out.update(programme_name="", investment_item="", proposal_object="", free_text_translation_status="pending_free_text_translation")
                writer.writerow(out)
                count += 1
    assert count == 1_153_701, count

    mappings = [
        {"screen_label": "water_supply", "action_id": "ipcc_0101", "action_name": "Improve urban water management", "mapping_confidence": "medium", "rationale": "Programme/object keyword screen; source has no adaptation taxonomy and proposal matches require adjudication."},
        {"screen_label": "drainage_stormwater", "action_id": "c40_0048", "action_name": "Upgrade urban drainage systems", "mapping_confidence": "medium", "rationale": "Exclude paving-only drainage mentions before accepting proposal matches."},
        {"screen_label": "slope_stabilisation", "action_id": "icare_0184", "action_name": "Upgrade Slope stabilization and drainage", "mapping_confidence": "medium", "rationale": "Theme is close to the action, but each proposal match remains unadjudicated."},
        {"screen_label": "ecosystem_restoration", "action_id": "ipcc_0084", "action_name": "Restore/create natural areas", "mapping_confidence": "medium", "rationale": "Broad restoration language can include non-adaptation activity; adjudication required."},
        {"screen_label": "disaster_risk", "action_id": "icare_0172", "action_name": "Develop and implement the Municipal Risk Reduction Plan (PMRR) and identify population groups vulnerable to climate risks.", "mapping_confidence": "medium", "rationale": "Administrative proposals can fund plans or works; do not attribute amounts until proposal-level review."},
    ]
    MAPPING.parent.mkdir(parents=True, exist_ok=True)
    with MAPPING.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(mappings[0]))
        writer.writeheader(); writer.writerows(mappings)
    print({"rows": count, "output": str(OUTPUT), "mapping_rows": len(mappings)})


if __name__ == "__main__":
    main()

