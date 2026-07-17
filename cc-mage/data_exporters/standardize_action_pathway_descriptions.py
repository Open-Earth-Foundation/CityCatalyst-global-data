"""
Data exporter that standardizes action_pathway descriptions by removing
geography-specific references (particularly Brazil-specific content).

This block updates:
- icare_0002: Energy labeling programs (removed "Brazilian")
- ipcc_0039: Sustainable materials (removed Brazil bioeconomy specifics)
- c40_0015: Building retrofits (removed PROCEL reference)

All updates apply to all languages (en, es, pt).
"""

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def standardize_action_descriptions(**kwargs) -> None:
    """
    Update modelled.action_pathway to have geographically neutral descriptions.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    # SQL updates for each action
    update_queries = [
        # icare_0002: Generic energy labeling program (all languages)
        """
        UPDATE modelled.action_pathway 
        SET name_i18n = jsonb_build_object(
          'en', 'Promote and expand energy labeling programs for buildings',
          'es', 'Promover y ampliar los programas de etiquetado energético para edificios',
          'pt', 'Promover e expandir programas de etiquetagem energética para edifícios'
        ),
        description_i18n = jsonb_build_object(
          'en', 'The city will encourage the adoption and enforcement of an Energy Labeling Program for Buildings to improve energy efficiency and reduce emissions from the building sector. The program evaluates and certifies buildings based on their energy performance, covering aspects such as thermal efficiency, lighting, and HVAC systems. Actions may include incentivizing developers and property owners to seek certification, integrating energy performance criteria into municipal building codes, and raising public awareness of the benefits of energy-efficient construction and renovation.',
          'es', 'La ciudad fomentará la adopción y aplicación de un Programa de Etiquetado Energético para Edificios con el fin de mejorar la eficiencia energética y reducir las emisiones del sector de la construcción. El programa evalúa y certifica los edificios según su desempeño energético, abarcando aspectos como la eficiencia térmica, la iluminación y los sistemas HVAC. Las acciones pueden incluir incentivar a desarrolladores y propietarios a buscar la certificación, integrar criterios de desempeño energético en los códigos de edificación municipales y aumentar la concienciación pública sobre los beneficios de la construcción y renovación energéticamente eficiente.',
          'pt', 'A cidade irá incentivar a adoção e a aplicação de um Programa de Etiquetagem de Edificações para melhorar a eficiência energética e reduzir as emissões do setor de edificações. O programa avalia e certifica edifícios com base em seu desempenho energético, abrangendo aspectos como eficiência térmica, iluminação e sistemas de HVAC. As ações podem incluir o incentivo a incorporadores e proprietários de imóveis para buscar a certificação, a integração de critérios de desempenho energético nos códigos de obras municipais e o aumento da conscientização pública sobre os benefícios da construção e renovação energeticamente eficientes.'
        )
        WHERE src_action_id = 'icare_0002';
        """,
        
        # ipcc_0039: Generic bioeconomy materials (all languages)
        """
        UPDATE modelled.action_pathway 
        SET name_i18n = jsonb_build_object(
          'en', 'Promote the substitution of traditional materials with sustainable alternatives',
          'es', 'Promover la sustitución de materiales tradicionales por alternativas sostenibles',
          'pt', 'Promover a substituição de materiais tradicionais por alternativas sustentáveis'
        ),
        description_i18n = jsonb_build_object(
          'en', 'Stimulate the replacement of conventional materials in consumer goods with sustainable alternatives from local bioeconomy resources, such as bio-based plastics, high-quality recycled polymers, and biotextiles made from biomass fibers or agricultural waste.',
          'es', 'Estimular la sustitución de materiales convencionales en bienes de consumo por alternativas sostenibles provenientes de recursos locales de la bioeconomía, como bioplásticos, polímeros reciclados de alta calidad y biotextiles elaborados a partir de fibras de biomasa o residuos agrícolas.',
          'pt', 'Estimular a substituição de materiais convencionais em bens de consumo por alternativas sustentáveis da bioeconomia local, como bioplásticos, polímeros reciclados de alta qualidade e biotêxteis feitos de fibras de biomassa ou resíduos agrícolas.'
        )
        WHERE src_action_id = 'ipcc_0039';
        """,
        
        # c40_0015: Remove PROCEL reference (all languages)
        """
        UPDATE modelled.action_pathway 
        SET description_i18n = jsonb_build_object(
          'en', 'The city supports retrofitting existing residential buildings to improve energy efficiency and reduce emissions. Key interventions include replacing inefficient refrigerators, air conditioners, and lighting with high-efficiency models, sealing windows and doors to reduce air leakage, and improving indoor comfort through natural ventilation and shading. Municipalities can facilitate access to financing programs, bulk procurement, and technical assistance for households to adopt upgrades. Retrofits should prioritize passive cooling strategies (shading, ventilation) before installing high-efficiency cooling technologies using low-GWP refrigerants.',
          'es', 'La ciudad apoya la modernización de edificios residenciales existentes para mejorar la eficiencia energética y reducir las emisiones. Las intervenciones clave incluyen reemplazar refrigeradores, aires acondicionados y sistemas de iluminación ineficientes por modelos de alta eficiencia, sellar ventanas y puertas para reducir fugas de aire, y mejorar el confort interior mediante ventilación natural y sombreado. Los municipios pueden facilitar el acceso a programas de financiamiento, compras en volumen y asistencia técnica para que los hogares adopten estas mejoras. Las modernizaciones deben priorizar estrategias de enfriamiento pasivo (sombreado, ventilación) antes de instalar tecnologías de enfriamiento de alta eficiencia que utilicen refrigerantes de bajo GWP.',
          'pt', 'A cidade apoia a requalificação de edifícios residenciais existentes para melhorar a eficiência energética e reduzir emissões. As principais intervenções incluem substituir geladeiras, aparelhos de ar-condicionado e iluminação ineficientes por modelos de alta eficiência, vedar janelas e portas para reduzir infiltrações de ar e melhorar o conforto interno por meio de ventilação natural e sombreamento. Os municípios podem facilitar o acesso a programas de financiamento, compras em volume e assistência técnica para que as famílias adotem essas melhorias. As requalificações devem priorizar estratégias de resfriamento passivo (sombreamento, ventilação) antes de instalar tecnologias de resfriamento de alta eficiência com refrigerantes de baixo GWP.'
        )
        WHERE src_action_id = 'c40_0015';
        """
    ]
    
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        for query in update_queries:
            result = loader.execute(query)
            print(f"✓ Updated action descriptions in modelled.action_pathway")
    
    print("Standardization complete: 3 actions updated to use geographically neutral descriptions")
