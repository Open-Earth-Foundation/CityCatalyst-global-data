#!/usr/bin/env python3
"""Build deterministic, reviewable matching profiles for every action.

The profiles are derived only from the canonical multilingual action registry.
They are deliberately data rather than prompt prose so both people and local
matchers can inspect the exact terms that define an action's boundary.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


V1 = Path(__file__).resolve().parents[1]
DEFAULT_ACTIONS = V1 / "data" / "registry" / "actions.json"
DEFAULT_OUTPUT = V1 / "data" / "registry" / "action_matching_profiles.json"

STOPWORDS = {
    "a", "al", "and", "as", "by", "con", "como", "de", "del", "el", "en",
    "for", "from", "in", "la", "las", "los", "of", "on", "or", "para", "por",
    "que", "se", "such", "the", "their", "through", "to", "un", "una", "use",
    "y", "e", "o", "its", "this", "these", "will", "city", "ciudad", "promover",
    "implementar", "mejorar", "desarrollar", "establecer", "adoptar", "apoyar",
}

# Human-readable boundaries for the actions represented in the reviewed pilot.
# These are action-level rules (never document IDs or atom IDs) and therefore
# generalise to every policy document in the corpus.
REVIEWED_BOUNDARIES = {
    "icare_0121": {
        "direct_phrases": ["bicicletas compartidas", "bicicletas electricas compartidas", "sistema de bicicletas publicas", "bike sharing"],
        "indirect_phrases": ["bicicletas", "bicicleta", "ciclovias", "ciclovia", "movilidad activa", "modos activos", "ciclos"],
        "exclude_phrases": ["buses electricos", "vehiculos de carga", "flota municipal", "electromovilidad del transporte publico", "transporte publico limpio"],
        "review_note": "Cycling infrastructure is enabling/indirect; electric buses, freight and generic vehicle electrification are different interventions.",
    },
    "c40_0017": {
        "direct_phrases": ["eficiencia energetica en edificios municipales", "edificios municipales", "infraestructura municipal"],
        "direct_requires_any": ["aislamiento", "climatizacion", "iluminacion", "retrofit", "reacondicionamiento", "eficiencia energetica"],
        "indirect_phrases": ["rehabilitacion termica", "acondicionamiento termico", "reacondicionamiento termico", "renovacion energetica"],
        "exclude_phrases": ["industrial", "espacios publicos"],
        "review_note": "Direct evidence needs both an existing municipal-building object and a physical energy-efficiency mechanism.",
    },
    "c40_0023": {
        "direct_phrases": ["buses electricos", "bus electrico", "autobuses electricos", "buses cero emisiones"],
        "indirect_phrases": ["electromovilidad en el transporte publico", "electromovilidad del transporte publico"],
        "exclude_phrases": ["bicicletas", "vehiculos de carga", "flota municipal"],
        "review_note": "Public-transport electromobility is indirect unless buses or bus-fleet deployment are explicit.",
    },
    "c40_0025": {
        "direct_phrases": ["vehiculos de carga electricos", "vehiculos de carga a electricos", "vehiculos de carga", "camiones electricos", "flota de carga"],
        "direct_requires_any": ["electrico", "cero emisiones", "recambio", "renovacion"],
        "exclude_phrases": ["flota municipal", "transporte publico", "buses electricos"],
        "review_note": "The freight object and zero-emission fleet mechanism must both be explicit.",
    },
    "c40_0029": {
        "direct_phrases": ["flota municipal electrica", "flota municipal", "vehiculos municipales electricos", "vehiculos electricos municipales"],
        "direct_requires_any": ["electrico", "electromovilidad", "cero emisiones", "renovacion", "recambio", "incorporacion"],
        "indirect_phrases": ["puntos de carga", "estaciones de carga", "infraestructura de carga", "electrocargadores"],
        "exclude_phrases": ["vehiculos de carga", "buses electricos"],
        "review_note": "Charging infrastructure is enabling; direct evidence electrifies vehicles owned or operated by the municipality.",
    },
    "icare_0012": {
        "direct_phrases": ["paneles solares en edificios municipales", "paneles solares fotovoltaicos en edificios municipales", "energia solar en edificios municipales", "solar municipal"],
        "exclude_phrases": ["agrivolta", "viviendas", "residencial"],
        "review_note": "Solar technology must be installed on a municipal facility or public asset.",
    },
    "icare_0033": {"direct_phrases": ["biodigestores", "biodigestor"], "review_note": "Biodigester implementation is the distinctive mechanism."},
    "icare_0040": {
        "direct_phrases": ["alumbrado publico", "luminarias publicas", "iluminacion publica"],
        "direct_requires_any": ["led", "solar", "eficiente", "recambio", "reemplazo"],
        "review_note": "Direct evidence needs public/street lighting plus an efficient or solar replacement mechanism.",
    },
    "icare_0110": {
        "direct_phrases": ["residuos de construccion y demolicion", "residuos construccion demolicion", "rcd"],
        "contextual_phrases": ["materiales sustentables", "materiales sostenibles"],
        "review_note": "Construction circularity is contextual unless construction/demolition waste management is explicit.",
    },
    "ipcc_0053": {"direct_phrases": ["reforestacion", "forestacion", "restauracion forestal", "restauracion de bosques"], "review_note": "Forest establishment or recovery is direct; emissions accounting alone is excluded."},
    "ipcc_0057": {
        "direct_phrases": ["restauracion de turberas", "restaurar turberas", "rehumectacion de turberas"],
        "contextual_phrases": ["turberas", "turbera"],
        "exclude_phrases": ["humedales urbanos"],
        "review_note": "General wetlands are not peatlands; peatland risk/context without restoration is contextual.",
    },
    "ipcc_0062": {"direct_phrases": ["biochar", "biocarbon", "biocarbono"], "review_note": "Soil carbon, reforestation and biodigesters are different mechanisms."},
    "ipcc_0070": {"direct_phrases": ["perdida de alimentos", "desperdicio de alimentos", "perdidas y desperdicios de alimentos", "residuos alimentarios"], "review_note": "Evidence must specifically prevent or reduce food loss/waste."},
    "ipcc_0105": {
        "direct_phrases": ["redistribucion del espacio vial", "reasignacion del espacio vial", "reconversion del espacio vial"],
        "indirect_phrases": ["ciclovias", "ciclovia", "infraestructura ciclista", "movilidad activa", "peatones y ciclistas"],
        "review_note": "Walking/cycling infrastructure is indirect unless existing road space is explicitly reallocated.",
    },
    "icare_0137": {"direct_phrases": ["iluminacion led", "luminarias led", "alumbrado led", "alumbrado publico"], "direct_requires_any": ["led"], "review_note": "Direct evidence replaces public-space lighting with LED technology."},
    "icare_0139": {"direct_phrases": ["tarificacion por congestion", "cobro por congestion", "restriccion de vehiculos contaminantes", "zonas de bajas emisiones"], "review_note": "Electrification and modal shift are not pricing or access restrictions."},
    "c40_0037": {"direct_phrases": ["separacion en origen", "residuos en origen", "recoleccion segregada", "recogida selectiva", "reciclaje domiciliario", "segregacion de residuos"], "review_note": "Direct evidence separates collection streams for households or businesses."},
    "c40_0042": {
        "direct_phrases": ["ampliacion de areas verdes urbanas", "aumentar las areas verdes urbanas", "creacion de parques urbanos", "nuevos parques urbanos", "plantacion de arbolado urbano", "incremento del arbolado urbano", "corredores verdes"],
        "contextual_phrases": ["areas verdes urbanas", "espacios verdes urbanos", "parques urbanos", "arbolado urbano"],
        "exclude_phrases": ["restauracion forestal", "plantaciones forestales"],
        "review_note": "Forest restoration is not urban/peri-urban green-space expansion without an urban application context.",
    },
}

# Second-pass review of the remaining catalogue. These rules encode the
# distinctive intervention object/mechanism in Spanish policy terminology.
# Broad sector phrases are placed in indirect/contextual lists or omitted.
REMAINING_REVIEWED_BOUNDARIES = {
    "icare_0001": {"direct_phrases": ["recuperacion de calor", "calor residual", "recuperacion de energia residual"], "review_note": "Generic industrial efficiency is not heat/energy recovery."},
    "icare_0002": {"direct_phrases": ["etiquetado energetico de edificios", "calificacion energetica de edificios", "programa de etiquetado de edificios"], "contextual_phrases": ["certificacion energetica de edificios", "certificacion iso 50001 en edificios"], "review_note": "Requires a building energy label/rating programme, not a general efficiency certification."},
    "icare_0006": {"direct_phrases": ["microred", "micro red"], "direct_requires_any": ["solar", "fotovolta*", "bateria", "almacenamiento"], "indirect_phrases": ["almacenamiento distribuido", "generacion distribuida"], "review_note": "Direct evidence combines a microgrid with renewable generation or storage."},
    "icare_0008": {"direct_phrases": ["red inteligente", "redes inteligentes", "smart grid", "almacenamiento distribuido"], "direct_requires_any": ["electric*", "energia", "bateria", "municip*"], "review_note": "Renewable generation alone is not smart-grid/storage integration."},
    "icare_0009": {"direct_phrases": ["cogeneracion", "cogeneracion industrial"], "review_note": "Generic industrial energy efficiency is not cogeneration."},
    "icare_0010": {"direct_phrases": ["energia neta cero", "edificios net zero", "edificios carbono neutral", "certificacion de edificios verdes", "certificacion leed"], "contextual_phrases": ["certificacion energetica de edificios"], "review_note": "Direct evidence requires net-zero/green-building certification, not ordinary retrofit."},
    "icare_0015": {"direct_phrases": ["microhidro", "micro hidro", "minihidro", "mini hidro", "pequena hidroelectric", "energia de biomasa", "generacion con biomasa"], "contextual_phrases": ["biomasa forestal"], "review_note": "Generic renewables do not establish small hydro or biomass generation."},
    "icare_0016": {"direct_phrases": ["solar termica para agua caliente", "colectores solares termicos para agua caliente", "bombas de calor para agua caliente", "bomba de calor para agua caliente"], "indirect_phrases": ["energia solar termica", "bombas de calor", "bomba de calor"], "review_note": "Solar PV is different; solar thermal/heat pumps without a water-heating application are indirect."},
    "icare_0023": {"direct_phrases": ["subestacion electrica", "subestaciones electricas"], "direct_requires_any": ["moderniz*", "manteni*", "mejor*", "ampli*", "renov*"], "review_note": "Electric networks or chargers without substation works are excluded."},
    "icare_0024": {"direct_phrases": ["energia renovable para bombeo", "energia solar para bombeo", "paneles fotovoltaicos para alimentar energeticamente los sistemas de agua", "energia renovable en plantas de tratamiento de agua"], "review_note": "Requires renewable power applied to municipal water treatment, pumping, or distribution."},
    "icare_0025": {"direct_phrases": ["viviendas vulnerables", "viviendas precarias", "campamentos", "asentamientos informales", "vivienda social"], "direct_requires_any": ["eficiencia energetica", "aislamiento", "confort termico", "resiliencia climatica", "acondicionamiento termico"], "indirect_phrases": ["subsidio de acondicionamiento termico"], "review_note": "Both vulnerable/low-income housing and an efficiency/resilience intervention are required."},
    "icare_0026": {"direct_phrases": ["tarifa horaria", "tarifas horarias", "tarifa por horario", "tarifa de tiempo de uso"], "review_note": "Demand management without time-varying electricity pricing is not direct."},
    "icare_0027": {"direct_phrases": ["financiamiento de proyectos de energia renovable", "fondo para energias renovables", "subsidios para energias renovables", "creditos para energias renovables"], "indirect_phrases": ["incentivos para energias renovables"], "review_note": "Requires a financing mechanism tied to local renewable projects."},
    "icare_0028": {"direct_phrases": ["ventilacion natural", "sombreamiento natural", "diseno pasivo", "enfriamiento pasivo", "refrigeracion pasiva"], "indirect_phrases": ["techos verdes", "fachadas verdes"], "review_note": "Green roofs/facades are enabling unless passive cooling is explicit."},
    "icare_0031": {"direct_phrases": ["biogas en plantas de tratamiento de aguas", "biogas en ptas", "captura de biogas en plantas de tratamiento", "biogas de lodos"], "indirect_phrases": ["biogas a partir de residuos organicos"], "review_note": "Biogas from landfill/organic waste is not wastewater-treatment biogas."},
    "icare_0034": {"direct_phrases": ["suministro de combustible industrial", "inyeccion de carbon pulverizado", "combustible para hornos industriales"], "review_note": "Efficient residential heating and generic industrial fuel switching are different interventions."},
    "icare_0035": {"direct_phrases": ["eficiencia energetica en procesos industriales", "eficiencia energetica industrial", "sistemas de gestion de la energia a nivel industrial"], "contextual_phrases": ["ley de eficiencia energetica"], "review_note": "Direct evidence implements industrial process efficiency."},
    "icare_0045": {"direct_phrases": ["agricultura regenerativa", "agricultura organica", "agricultura agroecologica", "produccion agroecologica", "manejo regenerativo de suelos"], "review_note": "General sustainable agriculture is indirect unless an organic/regenerative/agroecological practice is named."},
    "icare_0049": {"direct_phrases": ["hub de energia renovable", "polo de energia renovable", "centro regional de energia renovable"], "review_note": "Individual renewable projects do not establish a regional production hub."},
    "icare_0050": {"direct_phrases": ["agroforesteria", "sistemas agroforestales", "sistemas de agroforesteria"], "review_note": "Reforestation alone is not agroforestry."},
    "icare_0053": {"direct_phrases": ["cooperativas de recicladores", "asociaciones de recicladores", "recicladores de base"], "direct_requires_any": ["cooperativa", "asociacion", "formaliz", "fortalec", "organicos", "empresa"], "contextual_phrases": ["recicladores de base"], "review_note": "Requires organization/formalization of waste pickers or expansion into organics."},
    "icare_0064": {"direct_phrases": ["estrategia de residuos organicos", "plan de gestion de residuos organicos", "programa de gestion de residuos organicos"], "indirect_phrases": ["compostaje", "tratamiento de residuos organicos"], "review_note": "A single composting activity enables but is not an integrated strategy."},
    "icare_0069": {"direct_phrases": ["zonificacion agroclimatica", "mapa agroclimatico", "cartografia agroclimatica", "zonificacion ecologica"], "review_note": "General risk mapping is not ecological/agroclimatic zoning."},
    "icare_0071": {"direct_phrases": ["eficiencia de hornos industriales", "hornos y calderas industriales", "hornos industriales eficientes", "eficiencia de hornos y secadores"], "review_note": "Generic process efficiency is not furnace/kiln efficiency."},
    "icare_0072": {"direct_phrases": ["redes de intercambiadores de calor", "intercambiadores de calor", "bombas de calor de alta temperatura", "reutilizacion de calor residual"], "review_note": "Requires recovery/reuse through heat exchangers or heat pumps."},
    "icare_0074": {"direct_phrases": ["tecnologias de eficiencia energetica industrial", "tecnologias eficientes en procesos industriales", "eficiencia energetica en la mineria", "sistemas de gestion de la energia a nivel industrial"], "review_note": "Broad productive-sector technology without energy efficiency is excluded."},
    "icare_0076": {"direct_phrases": ["electrificacion de procesos industriales", "electrificar procesos industriales", "electrificacion industrial"], "direct_requires_any": ["renovable", "baja emision", "carbono", "hidrogeno", "electric"], "review_note": "General renewable power or electromobility is not industrial-process electrification."},
    "icare_0078": {"direct_phrases": ["descarbonizacion de materias primas", "materias primas bajas en carbono", "insumos industriales bajos en carbono", "captura y utilizacion de carbono"], "review_note": "Fuel switching alone is not feedstock decarbonization."},
    "icare_0079": {"direct_phrases": ["captura y utilizacion de carbono", "captura y uso de carbono", "captura utilizacion de co2", "ccu"], "review_note": "Carbon storage without utilization is a different intervention."},
    "icare_0082": {"direct_phrases": ["captura y almacenamiento de carbono", "almacenamiento geologico de carbono", "captura almacenamiento de co2"], "review_note": "The acronym CCS is excluded because Chilean policies also use it for climate councils; the full geological-storage mechanism is required."},
    "icare_0099": {"direct_phrases": ["certificacion agroecologica", "certificaciones agroecologicas", "sello agroecologico"], "review_note": "Agroecological production without certification participation is indirect."},
    "icare_0101": {"direct_phrases": ["maquinaria agricola electrica", "maquinaria agricola cero emisiones", "tractores electricos", "maquinaria agricola solar"], "review_note": "Electric municipal vehicles are not agricultural machinery."},
    "icare_0104": {"direct_phrases": ["sistema hibrido solar eolico", "sistemas hibridos solar eolica", "generacion hibrida solar eolica"], "review_note": "Separate solar or wind deployment is not a hybrid system."},
    "icare_0105": {"direct_phrases": ["perdidas tecnicas de distribucion", "reducir las perdidas electricas", "reduccion de perdidas electricas", "perdidas en redes electricas"], "contextual_phrases": ["perdidas electricas"], "review_note": "Grid expansion without technical-loss reduction is excluded."},
    "icare_0111": {"direct_phrases": ["responsabilidad extendida del productor", "fortalecer los sistemas rep", "implementacion de sistemas rep"], "contextual_phrases": ["ley rep", "sistemas rep"], "review_note": "References to the EPR law are contextual unless the policy implements or strengthens the system."},
    "icare_0117": {"direct_phrases": ["mejorar el transporte publico", "fortalecer el transporte publico", "aumentar la cobertura del transporte publico", "mejoras al transporte publico", "sistema integrado de transporte publico"], "indirect_phrases": ["electromovilidad en el transporte publico", "buses electricos"], "review_note": "Fleet technology is enabling unless service quality and modal shift are addressed."},
    "icare_0120": {"direct_phrases": ["criterios de eficiencia energetica en compras publicas", "eficiencia energetica en la contratacion publica", "eficiencia energetica en licitaciones", "compras publicas energeticamente eficientes"], "contextual_phrases": ["compras publicas sustentables"], "review_note": "Sustainable procurement is contextual unless energy-efficiency criteria are explicit."},
    "icare_0122": {"direct_phrases": ["ecoparque", "eco parque", "parque de reciclaje"], "direct_requires_any": ["residu", "recicl", "tratamiento", "compost"], "review_note": "Ordinary parks are not waste-treatment eco-parks."},
    "icare_0127": {"direct_phrases": ["regularizacion ambiental de predios rurales", "registro ambiental rural", "catastro ambiental de predios rurales"], "review_note": "Land-use regularization without the rural environmental registry is not direct."},
    "icare_0128": {"direct_phrases": ["pago por servicios ambientales", "pagos por servicios ecosistemicos", "programa municipal de servicios ambientales"], "indirect_phrases": ["incentivos para la conservacion"], "review_note": "General conservation finance is indirect unless a PES mechanism is named."},
    "icare_0131": {"direct_phrases": ["compras publicas de productos agroecologicos", "adquisicion publica de alimentos agroecologicos", "compras publicas de alimentos locales"], "direct_requires_any": ["agroecolog", "local", "sostenibl"], "review_note": "Requires public procurement of local/agroecological food."},
    "icare_0132": {"direct_phrases": ["circuitos cortos de comercializacion", "cadenas cortas agroalimentarias", "produccion agroecologica local", "ferias agroecologicas"], "review_note": "General local commerce is not an agroecological short supply chain."},
    "c40_0010": {"direct_phrases": ["estandares de eficiencia energetica para viviendas nuevas", "normas de eficiencia energetica para nuevas viviendas", "reglamentacion termica de viviendas nuevas", "implementacion de la actualizacion de la reglamentacion termica", "reduccion del consumo de energia en un 20 en las edificaciones nuevas"], "contextual_phrases": ["reglamentacion termica"], "indirect_phrases": ["calificacion energetica de viviendas", "estudios para la futura actualizacion de la reglamentacion termica"], "review_note": "Retrofits and voluntary labels are not mandatory standards for new housing."},
    "c40_0012": {"direct_phrases": ["estandares de eficiencia energetica para edificios publicos", "criterios de eficiencia energetica para edificacion publica", "edificacion publica sostenible"], "direct_requires_any": ["estandar", "criteri", "norma", "requisito", "sostenible"], "review_note": "Physical retrofit is different from standards for new institutional buildings."},
    "c40_0013": {"direct_phrases": ["estandares de eficiencia para edificios industriales", "normas de eficiencia energetica industrial para edificaciones", "certificacion de edificios industriales"], "review_note": "Process efficiency is not an industrial-building standard."},
    "c40_0015": {"direct_phrases": ["acondicionamiento termico de viviendas", "reacondicionamiento termico de viviendas", "eficiencia energetica en viviendas existentes", "aislamiento termico de viviendas"], "review_note": "New-building standards and municipal retrofits are different objects."},
    "c40_0016": {"direct_phrases": ["eficiencia energetica en edificios comerciales", "eficiencia energetica en edificios publicos", "medidas de eficiencia energetica en los edificios publicos", "reacondicionamiento de edificios no residenciales", "retrofit de edificios comerciales", "eficiencia energetica en edificios institucionales"], "direct_requires_any": ["existente", "aislamiento", "climatizacion", "iluminacion", "reacondicion*", "mejor*", "implement*", "eficiencia energetica"], "review_note": "Municipal-only and new-building standards are distinct."},
    "c40_0018": {"direct_phrases": ["eficiencia energetica en infraestructura industrial existente", "optimizacion energetica de instalaciones industriales", "sistemas de gestion de la energia"], "direct_requires_any": ["industrial", "industria"], "review_note": "Requires existing industrial infrastructure, not buildings or industry context generally."},
    "c40_0034": {"direct_phrases": ["prohibicion de plasticos de un solo uso", "prohibiciones como plasticos de un solo uso", "prohibir plasticos de un solo uso", "restriccion de plasticos de un solo uso", "ley de plasticos de un solo uso", "implementacion de la ley de plasticos de un solo uso", "prohibicion de materiales no reciclables"], "contextual_phrases": ["reduccion del consumo de papel y plasticos de un solo uso"], "review_note": "Recycling campaigns are not material bans."},
    "c40_0035": {"direct_phrases": ["plan de gestion de residuos", "estrategia de gestion de residuos", "optimizar la gestion de residuos", "mejorar el sistema de gestion de residuos"], "indirect_phrases": ["reciclaje", "compostaje"], "review_note": "Single-stream recycling/composting is enabling, not system optimization."},
    "c40_0036": {"direct_phrases": ["relleno sanitario con captura de biogas", "captura de biogas en rellenos sanitarios", "captura de metano en rellenos sanitarios", "captura y quema de biogas en rellenos sanitarios"], "contextual_phrases": ["relleno sanitario"], "review_note": "Landfill management without an explicit engineered gas-capture mechanism is contextual."},
    "c40_0040": {"direct_phrases": ["tarifa por volumen de residuos", "pago por generacion de residuos", "paga segun lo que botas", "cobro por volumen de residuos"], "review_note": "Ordinary collection fees are not volume-based pricing."},
    "c40_0071": {"direct_phrases": ["cocinas de induccion", "cocinas electricas eficientes", "electrificacion de la coccion", "sustitucion de lena para cocinar"], "review_note": "Heating electrification is not clean cooking."},
    "ipcc_0001": {"direct_phrases": ["desarrollo orientado al transporte", "desarrollo urbano orientado al transporte", "ciudad compacta", "densificacion en torno al transporte publico"], "indirect_phrases": ["uso mixto del suelo", "planificacion urbana compacta"], "review_note": "Transit investment alone is not compact/TOD urban form."},
    "ipcc_0023": {"direct_phrases": ["aligeramiento de productos", "productos livianos", "materiales ligeros", "reduccion de peso de productos"], "review_note": "Material recycling is not lightweight product design."},
    "ipcc_0024": {"direct_phrases": ["eficiencia en el uso de materiales en produccion", "eficiencia material en procesos productivos", "reduccion de mermas de materiales"], "review_note": "Waste collection is downstream and not production material utilization."},
    "ipcc_0025": {"direct_phrases": ["diseno para la reutilizacion", "diseno para el reciclaje", "diseno para la reparacion", "diseno para el desmontaje", "diseno para la recuperacion"], "review_note": "Reuse/recycling programmes do not necessarily change product design."},
    "ipcc_0026": {"direct_phrases": ["materias primas alternativas en la industria", "insumos alternativos en la produccion industrial", "sustitucion de clinker", "escoria de alto horno", "cenizas volantes", "materiales cementicios suplementarios"], "review_note": "Alternative fuels and recycled consumer products are not industrial feedstock substitution."},
    "ipcc_0028": {"direct_phrases": ["cambio de comportamiento para reducir residuos", "prevencion de residuos mediante cambios de habitos", "consumo responsable para reducir residuos", "campanas de sensibilizacion masivas y capacitacion a la comunidad educativa en habitos de consumo", "habitos de consumo minimizacion del desperdicio de alimentos"], "indirect_phrases": ["campana de reduccion de residuos", "educacion sobre residuos"], "review_note": "Treatment infrastructure is not behavioural waste prevention."},
    "ipcc_0031": {"direct_phrases": ["productos compartidos", "sistemas de uso compartido", "plataformas de intercambio de productos", "intercambio y prolongacion del ciclo de vida de productos", "economia del compartir"], "review_note": "Bike sharing is transport-specific and may be contextual, not generic product-service policy."},
    "ipcc_0033": {"direct_phrases": ["mantenimiento para extender la vida util", "reparacion para prolongar la vida util", "extension de vida util de productos", "reutilizacion reparacion intercambio y prolongacion del ciclo de vida de productos", "mantenimiento de infraestructura existente"], "review_note": "Recycling after disposal is not product-life extension."},
    "ipcc_0034": {"direct_phrases": ["suficiencia en el consumo", "reduccion del consumo de bienes", "reducir el consumo de productos", "patrones de consumo sostenible", "consumo responsable de bienes"], "contextual_phrases": ["educacion para el consumo sostenible", "consumo sostenible"], "review_note": "Water and energy conservation are different actions; evidence must address product/material consumption or sufficiency."},
    "ipcc_0037": {"direct_phrases": ["materiales carbono neutral", "materiales cero emisiones", "materiales de construccion bajos en carbono", "cadena de suministro net zero"], "indirect_phrases": ["utilizacion de materiales reciclados", "materiales reciclados o de origen sostenible"], "review_note": "Sustainable materials without a net-zero supply-chain objective are indirect."},
    "ipcc_0038": {"direct_phrases": ["energia solar en industrias", "paneles solares en instalaciones industriales", "fotovoltaica en plantas industriales"], "review_note": "Municipal/residential solar uses the same technology on the wrong asset."},
    "ipcc_0039": {"direct_phrases": ["sustitucion de materiales convencionales", "reemplazo de materiales tradicionales", "materiales alternativos sostenibles", "materiales de construccion con bajo impacto ambiental", "bioplasticos"], "review_note": "Recycling alone is not material substitution in product design."},
    "ipcc_0040": {"direct_phrases": ["acuerdo publico privado para reducir emisiones industriales", "colaboracion entre industria y gobierno", "alianza publico privada con la industria"], "direct_requires_any": ["emision*", "descarbon*", "carbono", "climat*"], "indirect_phrases": ["acuerdo de produccion limpia en el sector industrial", "acuerdos de produccion limpia en comercios"], "review_note": "Industry emissions action without government-industry collaboration is not direct."},
    "ipcc_0041": {"direct_phrases": ["investigacion en tecnologias de manufactura carbono neutral", "investigacion de tecnologias industriales bajas en carbono", "i d para descarbonizacion industrial"], "indirect_phrases": ["investigacion y desarrollo en tecnologias"], "review_note": "General technology R&D, including electromobility, is indirect."},
    "ipcc_0042": {"direct_phrases": ["meta de reduccion de emisiones industriales", "objetivo de descarbonizacion industrial", "metas para el sector industrial"], "direct_requires_any": ["emision", "carbono", "descarbon", "gei"], "review_note": "Industrial inventory shares and economy-wide targets are not sector reduction targets."},
    "ipcc_0043": {"direct_phrases": ["hidrogeno verde en procesos industriales", "combustibles cero emisiones para la industria", "biogas en procesos industriales", "combustibles renovables en la industria"], "indirect_phrases": ["fomento al uso de hidrogeno verde"], "review_note": "Hydrogen promotion is indirect unless industrial process use is explicit."},
    "ipcc_0045": {"direct_phrases": ["energias renovables en la industria", "energia renovable para procesos industriales", "descarbonizacion energetica industrial"], "indirect_phrases": ["reduccion de combustibles fosiles en la industria"], "review_note": "Renewables in other sectors or generic industrial fuel reduction are not direct."},
    "ipcc_0049": {"direct_phrases": ["politica de economia circular", "plan de economia circular", "estrategia de economia circular", "modelo de economia circular"], "indirect_phrases": ["reciclaje", "reutilizacion"], "review_note": "Individual recycling measures enable but do not constitute a circular-economy policy."},
    "ipcc_0050": {"direct_phrases": ["incentivo tributario para tecnologias limpias", "beneficio tributario para tecnologias limpias", "exencion fiscal para tecnologias limpias", "credito tributario verde"], "review_note": "Public expenditure and grants are not tax incentives."},
    "ipcc_0052": {"direct_phrases": ["reducir la deforestacion", "reducir la degradacion del bosque", "evitar la deforestacion", "prevencion de la deforestacion"], "contextual_phrases": ["deforestacion y degradacion", "perdida de bosques"], "review_note": "Forest restoration is a separate action; risk/inventory statements are contextual."},
    "ipcc_0054": {"direct_phrases": ["manejo forestal sostenible", "manejo sustentable del bosque", "gestion forestal sostenible", "practicas silviculturales sostenibles"], "review_note": "Conservation, reforestation and agroforestry are distinct unless management of existing forests is explicit."},
    "ipcc_0055": {"direct_phrases": ["manejo del fuego", "gestion de incendios forestales", "prevencion de incendios forestales", "quemas prescritas", "cortafuegos"], "contextual_phrases": ["incendios forestales"], "review_note": "Wildfire risk alone is contextual; direct evidence implements fire management."},
    "ipcc_0056": {"direct_phrases": ["proteccion de pastizales", "evitar la conversion de pastizales", "manejo sostenible de pastizales", "conservacion de sabanas"], "contextual_phrases": ["emisiones de pastizales", "degradacion de pastizales"], "review_note": "General soil management is not grassland/savanna conversion prevention."},
    "ipcc_0060": {"direct_phrases": ["restauracion de humedales costeros", "proteccion de humedales costeros", "proteger humedales costeros", "restauracion de manglares", "restauracion de marismas", "restauracion de pastos marinos"], "contextual_phrases": ["humedales costeros"], "review_note": "Urban/inland wetlands are not coastal wetlands."},
    "ipcc_0064": {"direct_phrases": ["reducir la fermentacion enterica", "reduccion de metano enterico", "aditivos alimentarios para ganado", "inhibidores de metano en ganado"], "contextual_phrases": ["fermentacion enterica"], "review_note": "Livestock methane inventories are contextual unless a direct enteric intervention is specified."},
    "ipcc_0067": {"direct_phrases": ["mejorar el manejo de estiercol", "tratamiento de estiercol", "reduccion de emisiones del estiercol", "fertilizacion nitrogenada eficiente", "manejo mejorado de nutrientes de cultivos"], "contextual_phrases": ["manejo de estiercol", "gestion del estiercol", "emisiones por manejo de estiercol"], "review_note": "Inventory descriptions are contextual; only improved manure/nutrient practices are direct."},
    "ipcc_0068": {"direct_phrases": ["bioenergia con captura de carbono", "beccs", "biomasa con captura y almacenamiento de carbono"], "review_note": "Biogas capture or bioenergy without carbon storage is not BECCS."},
    "ipcc_0069": {"direct_phrases": ["dietas saludables y sostenibles", "alimentacion saludable y sostenible", "reduccion del consumo de carne", "dietas bajas en carbono"], "review_note": "Sustainable agriculture and public food procurement do not necessarily change diets."},
    "ipcc_0071": {"direct_phrases": ["productos de madera sostenible", "madera certificada", "madera como sustituto del hormigon", "uso sostenible de la madera"], "review_note": "Sustainable procurement/materials generally are not wood-product substitution."},
    "ipcc_0074": {"direct_phrases": ["forma urbana compacta", "ciudad compacta", "densificacion urbana", "planificacion espacial compacta"], "review_note": "District heating and ordinary spatial planning are not compact urban form."},
    "ipcc_0076": {"direct_phrases": ["auditorias energeticas en industrias", "auditoria energetica industrial", "auditorias energeticas en plantas industriales"], "indirect_phrases": ["sistemas de gestion de la energia sge a nivel industrial", "sistemas de gestion de la energia a nivel industrial"], "review_note": "Building audits are distinct; industrial energy-management systems are an indirect enabling measure."},
}

REVIEWED_BOUNDARIES.update(REMAINING_REVIEWED_BOUNDARIES)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def tokens(text: str) -> list[str]:
    return [t for t in normalize(text).split() if len(t) >= 3 and t not in STOPWORDS]


def phrases(text: str, min_n: int = 1, max_n: int = 3) -> list[str]:
    toks = tokens(text)
    out: list[str] = []
    for n in range(min_n, max_n + 1):
        out.extend(" ".join(toks[i:i+n]) for i in range(len(toks) - n + 1))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actions", type=Path, default=DEFAULT_ACTIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    actions = json.loads(args.actions.read_text(encoding="utf-8"))
    document_frequency: Counter[str] = Counter()
    action_phrases: dict[str, set[str]] = {}
    for action in actions:
        fields = [action.get("actionName", ""), action.get("description", "")]
        fields += list((action.get("name_i18n") or {}).values())
        fields += list((action.get("description_i18n") or {}).values())
        ps = set(phrases(" ".join(v for v in fields if v)))
        action_phrases[action["actionId"]] = ps
        document_frequency.update(ps)

    profiles = []
    n_actions = len(actions)
    for action in actions:
        aid = action["actionId"]
        names = action.get("name_i18n") or {}
        descriptions = action.get("description_i18n") or {}
        title_text = " ".join([action.get("actionName", ""), *names.values()])
        title_terms = set(phrases(title_text))
        candidates = action_phrases[aid]
        # Multiword phrases and rare single words carry the identity. Generic
        # climate/action verbs are removed above and cannot create a match.
        ranked = sorted(
            candidates,
            key=lambda p: (
                len(p.split()),
                (n_actions + 1) / (document_frequency[p] + 1),
                p in title_terms,
                len(p),
            ),
            reverse=True,
        )
        anchors = [
            p for p in ranked
            if (len(p.split()) >= 2 and document_frequency[p] <= 8)
            or (len(p.split()) == 1 and document_frequency[p] <= 3)
        ][:36]
        title_anchors = [p for p in ranked if p in title_terms and document_frequency[p] <= 12][:16]
        reviewed = REVIEWED_BOUNDARIES.get(aid)
        profiles.append({
            "action_id": aid,
            "action_name": action.get("actionName", ""),
            "action_type": action.get("action_type"),
            "identity": {
                "names": {"en": action.get("actionName", ""), **names},
                "descriptions": {"en": action.get("description", ""), **descriptions},
                "intervention_summary": action.get("intervention_summary_i18n") or {},
                "outcome_summary": action.get("outcome_summary_i18n") or {},
            },
            "matching_boundary": {
                "direct_rule": "The policy atom implements or explicitly targets the same intervention object and mechanism.",
                "indirect_rule": "The atom is a concrete prerequisite or enabling measure for this action but does not implement the same intervention.",
                "contextual_rule": "The atom describes the same narrowly defined problem or sector context without an enabling or implementation measure.",
                "exclude_rule": "Shared sector, technology, outcome, or climate language alone is not a match.",
            },
            "title_anchors": title_anchors,
            "distinctive_anchors": anchors,
            "reviewed_rules": reviewed or {},
            "profile_status": "pilot_reviewed" if reviewed else "machine_generated_review_required",
        })

    payload = {
        "schema_version": "1.0.0",
        "profile_method": "deterministic multilingual distinctive-phrase extraction",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "action_count": len(profiles),
        "profiles": profiles,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(profiles)} profiles to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
