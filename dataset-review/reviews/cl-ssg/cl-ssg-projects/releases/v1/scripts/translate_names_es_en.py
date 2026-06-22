#!/usr/bin/env python3
"""Translate BIP (cl-ssg-projects) project names ES->EN.

These are highly templated Chilean SNI/BIP public-works titles. Strategy:
  1. clean: ftfy mojibake repair + strip the "Año y Etapa a Financiar:" admin suffix.
  2. phrase-level glossary (longest-match first) for the domain vocabulary.
  3. token-level glossary for remaining function words / nouns.
  4. unknown tokens (place names, sectors) -> Title Case passthrough.
Output: a CSV keyed on codigo_bip (robust to later text edits) plus a JSON
{cleaned_es: en} review map. A separate step folds nombre_en into the review CSV.
"""
import csv, json, re, sys
import ftfy

SRC = "data/derived/projects_profiled.csv"
OUT = "data/derived"

def clean(s):
    t = ftfy.fix_text(s or "")
    t = re.sub(r"\s*A[ñn]o y Etapa a Financiar:.*$", "", t, flags=re.IGNORECASE).strip()
    t = re.sub(r"\s+(\d{4})-(EJECUCION|DISE[ÑN]O|PERFIL|PREFACTIBILIDAD|FACTIBILIDAD)$", "", t).strip()
    t = t.strip(" Ã").strip()
    return re.sub(r"\s{2,}", " ", t).strip()

# ---- phrase glossary (lowercased keys, matched longest-first, accent-insensitive) ----
PHRASES = {
    # region names (proper, English word order)
    "region metropolitana": "Metropolitan Region",
    "region del biobio": "Biobio Region", "region del bio bio": "Biobio Region",
    "region del bio-bio": "Biobio Region", "regiones del biobio": "Biobio Region",
    "region de los lagos": "Los Lagos Region", "region de los rios": "Los Rios Region",
    "region de coquimbo": "Coquimbo Region", "region de valparaiso": "Valparaiso Region",
    "region de la araucania": "Araucania Region", "region de atacama": "Atacama Region",
    "region del maule": "Maule Region", "region de tarapaca": "Tarapaca Region",
    "region de antofagasta": "Antofagasta Region", "region de aysen": "Aysen Region",
    "region de arica y parinacota": "Arica y Parinacota Region",
    "region de magallanes": "Magallanes Region", "region de nuble": "Nuble Region",
    "region de ohiggins": "O'Higgins Region", "region del libertador": "O'Higgins Region",
    "control aluvional y crecidas liquidas": "debris-flow and flash-flood control",
    "plan de cierre vertedero": "landfill-closure plan",
    "corredor transporte publico": "public-transport corridor",
    "corredor transp. publico": "public-transport corridor",
    "muros de contencion": "retaining walls", "muro de contencion": "retaining wall",
    "muro contencion": "retaining wall",
    "valorizacion de residuos": "waste recovery",
    "medidas eficiencia energetica": "energy-efficiency measures",
    "transferencia tecnologica": "Technology transfer:",
    "calidad del aire": "air quality", "calidad de aire": "air quality",
    "energia eolica": "wind energy", "energia solar": "solar energy",
    "estanque de retencion": "retention tank", "estanque retencion": "retention tank",
    "empalmes de respaldo": "backup connections",
    "infraestructura ferroviaria asociada": "associated railway infrastructure",
    # waste
    "residuos solidos domiciliarios y asimilables": "household and similar solid waste",
    "residuos solidos domiciliarios": "household solid waste",
    "residuos solidos": "solid waste",
    "rsd y a": "household and similar solid waste",
    "rsd y asimilable": "household and similar solid waste",
    "rsd y asimilables": "household and similar solid waste",
    "rsd": "household solid waste",
    "res. sol. org. dom.": "household organic solid waste",
    "residuos vegetales": "green (plant) waste",
    "camion recolector de basura": "garbage collection truck",
    "camion recolector de rsd": "household-waste collection truck",
    "camion recolector": "collection truck",
    "camiones recolectores de rsd": "household-waste collection trucks",
    "camiones recolectores": "collection trucks",
    "camiones sistema de recoleccion rsd": "household-waste collection trucks",
    "recoleccion rsd": "household-waste collection",
    "recoleccion de basura": "garbage collection",
    "contenedores de basura": "waste containers",
    "contenedores de rsd": "household-waste containers",
    "contenedores para manejo de rsd": "household-waste management containers",
    "contenedores para residuos solidos": "solid-waste containers",
    "contenedores para recoleccion de basura": "garbage-collection containers",
    "contenedores": "containers",
    "alzacontenedor": "container lifter",
    "centro de gestion de residuos solidos": "solid-waste management center",
    "centro de gestion residuos solidos": "solid-waste management center",
    "centro gestion de residuos solidos": "solid-waste management center",
    "centro de manejo de residuos solidos": "solid-waste management center",
    "centro manejo residuos solidos": "solid-waste management center",
    "centro de tratamiento y disposicion final": "treatment and final-disposal center",
    "centro de tratamiento integral residuos solidos": "integrated solid-waste treatment center",
    "centro tratamiento integral residuos solidos": "integrated solid-waste treatment center",
    "centro tratamiento intermedio rsd": "household-waste intermediate treatment center",
    "centro de valorizacion de residuos": "waste recovery center",
    "centro de reciclaje comunal": "municipal recycling center",
    "centro de reciclaje": "recycling center",
    "manejo de residuos solidos": "solid-waste management",
    "gestion de residuos solidos": "solid-waste management",
    "gestion integral de residuos": "integrated waste management",
    "planta de compostaje y lombricultura": "composting and vermiculture plant",
    "bioplanta de compostaje y lombricultura": "composting and vermiculture bioplant",
    "compostaje": "composting",
    "reciclaje": "recycling",
    "relleno sanitario": "sanitary landfill",
    "equipo para reciclaje": "recycling equipment",
    "vehiculos y contenedores para reciclaje": "recycling vehicles and containers",
    # lighting / solar
    "luminarias alta eficiencia tipo led": "high-efficiency LED streetlights",
    "luminarias fotovoltaicas": "photovoltaic streetlights",
    "luminarias solares": "solar streetlights",
    "luminaras solares": "solar streetlights",
    "luminarias led": "LED streetlights",
    "luminarias": "streetlights",
    "alumbrado publico solar": "solar public lighting",
    "alumbrado publico led": "LED public lighting",
    "alumbrado publico": "public lighting",
    "alumbrado peatonal de eficiencia energetica": "energy-efficient pedestrian lighting",
    "alumbrado peatonal": "pedestrian lighting",
    "alumbrado fotovoltaico": "photovoltaic lighting",
    "alumbrado solar vial": "solar road lighting",
    "alumbrado vial solar": "solar road lighting",
    "alumbrado solar": "solar lighting",
    "alumbrado y planta solar con conexion a red": "lighting and grid-connected solar plant",
    "postes solares": "solar poles",
    "paneles fotovoltaicos": "photovoltaic panels",
    "panel fotovoltaico": "photovoltaic panel",
    "sistema fotovoltaico": "photovoltaic system",
    "planta solar con conexion a red": "grid-connected solar plant",
    "con conexion a red": "grid-connected",
    "vias de evacuacion": "evacuation routes",
    "ernc": "non-conventional renewable energy (NCRE)",
    # water / sanitation
    "agua potable rural": "rural drinking water",
    "agua potable": "drinking water",
    "casetas sanitarias": "sanitation units",
    "soluciones sanitarias": "sanitation solutions",
    "soluc. sanitarias": "sanitation solutions",
    "infraestructuras sanitarias": "sanitation infrastructure",
    "alcantarillado y extension de redes de agua potable": "sewerage and drinking-water network extension",
    "alcantarillado de aguas lluvias": "stormwater drainage system",
    "alcantarillado": "sewerage",
    "aguas lluvias": "stormwater",
    "colectores primarios de aguas lluvias": "primary stormwater collectors",
    "colectores de aguas lluvias": "stormwater collectors",
    "colector de aguas lluvias": "stormwater collector",
    "red primaria de aguas lluvias": "primary stormwater network",
    "red primaria de evacuacion y drenaje de aguas lluvias": "primary stormwater drainage network",
    "red secundaria de aguas lluvias": "secondary stormwater network",
    "redes secundarias de aguas lluvias": "secondary stormwater networks",
    "redes secundarias": "secondary networks",
    "sistemas secundarios de aguas lluvias": "secondary stormwater systems",
    "sistema de aguas lluvias": "stormwater system",
    "sistemas de aguas lluvias": "stormwater systems",
    "obras de control aluvional": "debris-flow control works",
    "control aluvional": "debris-flow control",
    "obras por sequia": "drought-relief works",
    "obras de regadio": "irrigation works",
    "obras de riego": "irrigation works",
    "gestion de recursos hidricos": "water-resources management",
    "uso eficiente del recurso hidrico": "efficient water use",
    "recurso hidrico": "water resources",
    "drenaje": "drainage",
    "drenajes": "drainage",
    # rivers
    "riberas de cauces naturales": "banks of natural watercourses",
    "riberas cauces naturales": "banks of natural watercourses",
    "riberas de varios cauces": "banks of several watercourses",
    "riberas": "riverbanks",
    "cauces naturales": "natural watercourses",
    "defensas fluviales": "river flood defenses",
    "ribera sur": "south bank",
    # transport / rail
    "transporte publico": "public transport",
    "material rodante": "rolling stock",
    "via ferrea": "railway",
    "vias ferrea": "railway",
    "infraestructura ferroviaria": "railway infrastructure",
    "servicio ferroviario": "rail service",
    "equipos ferroviarios menores": "minor railway equipment",
    "paradas ferroviarias": "railway stops",
    "ferrocarril de arica a la paz": "Arica-La Paz Railway",
    "red neumatica": "pneumatic (tube) network",
    "pantallas de acceso": "platform screen doors",
    "estaciones de metro": "metro stations",
    "estacion": "station",
    "ascensores": "elevators",
    "coches": "rail cars",
    "terminales de buses": "bus terminals",
    "refugios para el transporte publico": "public-transport shelters",
    "seguridad vial": "road safety",
    "conservacion vial": "road maintenance",
    "ciclo via": "bike path",
    "ciclovias": "bike paths",
    "ciclovia": "bike path",
    "ciclov": "bike path",
    "caminos de uso publico": "public-use roads",
    "cam. de uso pub.": "public-use roads",
    "av. del tren": "Av. del Tren",
    "movilidad activa": "active mobility",
    # green space / parks
    "areas verdes": "green areas",
    "area verde": "green area",
    "parque urbano": "urban park",
    "parque fluvial": "riverside park",
    "espacios publicos": "public spaces",
    "muros de contencion": "retaining walls",
    "control erosion": "erosion control",
    "infraestructura verde urbana": "urban green infrastructure",
    # forestry / agri
    "incendios forestales": "forest fires",
    "combate de incendios forestales": "forest-fire fighting",
    "cambio climatico": "climate change",
    "pequena agricultura": "small-scale agriculture",
    "productos agropecuarios": "agricultural products",
    "sello de origen": "origin label",
    "sostenibilidad energetica": "energy sustainability",
    "eficiencia energetica": "energy efficiency",
    "obra mitigacion riesgo": "risk-mitigation works",
    # generic
    "varios sectores": "various sectors",
    "diversos sectores": "various sectors",
    "varias comunas": "several communes",
    "diversas comunas": "several communes",
    "sectores rurales": "rural sectors",
    "sector rural": "rural sector",
    "sector urbano": "urban sector",
    "sectores urbanos": "urban sectors",
    "alta eficiencia": "high efficiency",
    "alto estandar": "high standard",
    "corto plazo": "short-term",
    "mantencion": "maintenance",
    "rehabilitacion": "rehabilitation",
    "rehabilit.": "rehabilitation",
    "infraest.": "infrastructure",
    "infraestructura": "infrastructure",
    "maquinaria": "machinery",
    "excavadora": "excavator",
    "habilitacion": "fitting-out",
    "urbanizacion": "urbanization",
    "abastecimiento y gestion de contratos": "procurement and contract management",
    "control de gestion": "management control",
    "sistema de comunicaciones": "communications system",
    "sistema radiocomunicaciones": "radio-communications system",
    "sistemas de seguridad": "security systems",
    "maquinas de autoservicio": "self-service machines",
    "maquina registradora geometria": "track-geometry recording machine",
    "equipos aire acondicionado": "air-conditioning equipment",
    "equipos aire acond.": "air-conditioning equipment",
    "locales tecnicos": "technical rooms",
    "equipamiento": "equipment",
}

# leading action verbs -> English noun; an "of" is inserted after them automatically
VERBS = {
    "adquisicion": "Acquisition", "construccion": "Construction",
    "conservacion": "Maintenance", "ampliacion": "Expansion",
    "reposicion": "Replacement", "mejoramiento": "Improvement",
    "capacitacion": "Training in", "instalacion": "Installation",
    "implementacion": "Implementation", "implantacion": "Implementation",
    "operacion": "Operation", "reparacion": "Repair", "habilitacion": "Fitting-out",
    "normalizacion": "Normalization", "renovacion": "Renewal",
    "transferencia": "Transfer", "saneamiento": "Sanitation", "extension": "Extension",
    "difusion": "Outreach on", "construccon": "Construction",
    "electrificacion": "Electrification", "diseno": "Design", "actualizacion": "Update",
}
# ---- single-token glossary ----
WORDS = {
    "y": "and", "e": "and", "de": "of", "del": "of the", "la": "", "las": "",
    "el": "", "los": "", "en": "in", "para": "for", "por": "for", "con": "with",
    "a": "to", "otros": "others", "otras": "others", "servicio": "service",
    "servicios": "services", "localidad": "locality", "parcial": "partial",
    "soluciones": "solutions", "solucion": "solution", "sistema": "system",
    "sitema": "system", "sist.": "system", "acceso": "access", "interceptor": "interceptor",
    "colector": "collector", "colectores": "collectors", "tren": "train", "tierra": "ground",
    "sanitaria": "sanitary", "sanitario": "sanitary", "sanitarias": "sanitation",
    "vecinal": "neighborhood", "unidad": "unit", "interconexion": "interconnection",
    "proyecto": "project", "proyectos": "projects", "muro": "wall", "muros": "walls",
    "cuenca": "basin", "vertedero": "landfill", "cierre": "closure", "plan": "plan",
    "medidas": "measures", "aplicacion": "application", "eje": "axis", "ejes": "axes",
    "corredor": "corridor", "agentes": "agents", "poblacion": "neighborhood",
    "pob.": "neighborhood", "pob": "neighborhood", "villa": "Villa", "barrio": "neighborhood",
    "contencion": "retaining", "interceptor": "interceptor", "transp.": "transport",
    "desvios": "detours", "desvio": "detour", "estanque": "tank", "retencion": "retention",
    "tecnologica": "technological", "tecnologico": "technological", "mediante": "via",
    "segunda": "second", "primera": "first", "tercera": "third", "sobre": "on",
    "asociada": "associated", "asociado": "associated", "seccion": "section",
    "calidad": "quality", "aire": "air", "energia": "energy", "eolica": "wind",
    "desarrollo": "development", "empalmes": "connections", "respaldo": "backup",
    "anos": "", "ano": "", "segurid": "safety", "seguridad": "safety", "chilena": "Chilean",
    "sist.": "system", "sist": "system", "evacuacion": "evacuation", "mejorar": "improve",
    "iluminacion": "lighting", "zona": "Zone", "abatimiento": "abatement",
    "emisiones": "emissions", "atmosfericas": "atmospheric", "asistencia": "assistance",
    "plataforma": "platform", "relojes": "clocks", "alcantar": "sewerage", "tecnol.": "technology",
    "comuna": "Commune", "sector": "Sector", "sectores": "Sectors",
    "region": "Region", "provincia": "Province", "calle": "Street", "avenida": "Avenue",
    "ruta": "Route", "etapa": "Stage", "fase": "Phase", "varios": "various",
    "varias": "several", "diversos": "various", "diversas": "various",
    "rural": "rural", "rurales": "rural", "urbano": "urban", "urbana": "urban",
    "solar": "solar", "solares": "solar", "fotovoltaico": "photovoltaic",
    "fotovoltaicos": "photovoltaic", "fotovoltaicas": "photovoltaic",
    "puente": "Bridge", "puentes": "bridges", "canal": "Canal", "canales": "canals",
    "taludes": "slopes", "vehiculos": "vehicles", "camiones": "trucks",
    "camion": "truck", "bascula": "weighbridge", "basura": "garbage",
    "sistema": "System", "sistemas": "systems", "red": "Network", "redes": "networks",
    "obras": "works", "obra": "works", "centro": "Center", "planta": "Plant",
    "panel": "panel", "paneles": "panels", "postes": "poles", "vial": "road",
    "vias": "roads", "via": "road", "caminos": "roads", "camino": "road",
    "seguridad": "safety", "drenaje": "drainage", "drenajes": "drainage",
    "primaria": "primary", "secundaria": "secondary", "secundarias": "secondary",
    "primarios": "primary", "naturales": "natural", "natural": "natural",
    "metalicos": "steel", "anticorrosiva": "anti-corrosion", "proteccion": "protection",
    "verde": "green", "verdes": "green", "area": "area", "areas": "areas",
    "espacios": "spaces", "publicos": "public", "publico": "public",
    "comunal": "municipal", "domiciliarios": "household", "solidos": "solid",
    "tratamiento": "treatment", "valorizacion": "recovery", "manejo": "management",
    "gestion": "management", "integral": "integrated", "intermedio": "intermediate",
    "disposicion": "disposal", "final": "final", "sanitario": "sanitary",
    "sanitarias": "sanitation", "sanitarias.": "sanitation", "potable": "drinking",
    "agua": "water", "aguas": "waters", "lluvias": "rain", "riego": "irrigation",
    "regadio": "irrigation", "sequia": "drought", "fluviales": "river",
    "fluvial": "river", "cauces": "watercourses", "cauce": "watercourse",
    "riberas": "riverbanks", "ribera": "bank", "defensas": "defenses",
    "ferroviaria": "railway", "ferroviario": "railway", "ferroviarios": "railway",
    "rieles": "rails", "estaciones": "stations", "estacion": "Station",
    "buses": "buses", "terminales": "terminals", "refugios": "shelters",
    "pasajeros": "passengers", "transporte": "transport", "movilidad": "mobility",
    "energetica": "energy", "energetico": "energy", "eficiencia": "efficiency",
    "climatico": "climate", "climatica": "climate", "forestales": "forest",
    "incendios": "fires", "agricultura": "agriculture", "agropecuarios": "agricultural",
    "compostaje": "composting", "reciclaje": "recycling", "contenedores": "containers",
    "luminarias": "streetlights", "alumbrado": "lighting", "peatonal": "pedestrian",
    "ascensores": "elevators", "equipos": "equipment", "equipo": "equipment",
    "equipamiento": "equipment", "maquinaria": "machinery", "excavadora": "excavator",
    "innovacion": "innovation", "uso": "use", "eficiente": "efficient",
    "hidrico": "water", "hidricos": "water", "recursos": "resources",
    "recurso": "resource", "control": "control", "erosion": "erosion",
    "mitigacion": "mitigation", "riesgo": "risk", "muros": "walls",
    "contencion": "retaining", "parque": "Park", "parques": "parks",
    "oficinas": "offices", "habilitacion": "fitting-out", "mantencion": "maintenance",
    "mantenimiento": "maintenance", "mayor": "major", "operacional": "operational",
    "norte": "North", "sur": "South", "centro": "Center", "oriente": "East",
    "poniente": "West", "alto": "Upper", "bajo": "Lower",
}

# acronyms / proper tokens kept verbatim (upper)
KEEP_UPPER = {"RSD", "RSD Y A", "APR", "LED", "ERNC", "ERP", "SAP", "RE-FX", "EFE",
              "METRO", "MERVAL", "RM", "RMS", "VR", "ZOFRI", "CCBB", "CPIF", "FCALP",
              "S.A.", "S.A", "TETRA", "FF", "PMS", "AYP", "CRC", "TT", "II", "III",
              "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV",
              "XV", "PLC", "TCO", "SAGR", "AGR"}

import unicodedata
def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def title_token(tok):
    # place names / unknowns -> Title Case, keep acronyms
    if tok.upper() in KEEP_UPPER or (tok.isupper() and len(tok) <= 4):
        return tok.upper()
    return tok.capitalize()

def translate(name):
    s = name
    low = " " + deacc(s).lower() + " "
    # phrase pass (longest first)
    repl = {}
    for i, (k, v) in enumerate(sorted(PHRASES.items(), key=lambda kv: -len(kv[0]))):
        pat = r"(?<![a-z])" + re.escape(k).replace("\\ ", r"\s+") + r"(?![a-z])"
        m = re.search(pat, low)
        if m:
            token = f" \x00{i}\x00 "
            low = re.sub(pat, token, low)
            repl[str(i)] = v
    toks = low.split()
    # leading action verb -> noun + "of"
    out = []
    if toks:
        first = deacc(toks[0]).lower()
        if first in VERBS:
            verb = VERBS[first]
            out.append(verb)
            if not verb.endswith("in"):  # "Training in" already has connector
                out.append("of")
            toks = toks[1:]
            # the verb's "of" subsumes a following Spanish "de"
            if toks and deacc(toks[0]).lower() in ("de", "del"):
                toks = toks[1:]
    for tok in toks:
        if tok.startswith("\x00"):
            out.append(repl[tok.strip("\x00")]); continue
        # split off surrounding punctuation so "otros," -> "others,"
        m = re.match(r"^([(\"']*)(.*?)([)\"',.:;]*)$", tok)
        pre, core, post = m.group(1), m.group(2), m.group(3)
        base = deacc(core).lower()
        if base in WORDS:
            w = WORDS[base]
            out.append(f"{pre}{w}{post}" if w else post)
        elif base in VERBS:  # verb appearing mid-title (e.g. "y reposicion")
            out.append(f"{pre}{VERBS[base]}{post}")
        else:
            out.append(f"{pre}{title_token(core)}{post}")
    txt = " ".join(out)
    # cleanups
    txt = re.sub(r"\bof of\b", "of", txt)
    txt = re.sub(r"\bof the of\b", "of the", txt)
    txt = re.sub(r"\bof and\b", "and", txt)
    txt = re.sub(r"\bof in\b", "in", txt)
    txt = re.sub(r"\b(in|for|of|with|and) (the )?(,|$)", r"\3", txt)  # dangling connectors
    txt = re.sub(r"\s+([,.;:])", r"\1", txt)
    txt = re.sub(r"\s{2,}", " ", txt).strip(" ,.;-")
    return txt[:1].upper() + txt[1:] if txt else txt

if __name__ == "__main__":
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    seen = {}
    out_rows = []
    for r in rows:
        es = clean(r["nombre"])
        en = translate(es)
        out_rows.append({"codigo_bip": r["codigo_bip"], "nombre_es_clean": es, "nombre_en": en})
        seen[es] = en
    with open(f"{OUT}/nombre_en.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["codigo_bip", "nombre_es_clean", "nombre_en"])
        w.writeheader(); w.writerows(out_rows)
    json.dump(seen, open(f"{OUT}/nombre_en_review.json", "w"), ensure_ascii=False, indent=1)
    print(f"translated {len(out_rows)} rows / {len(seen)} distinct names")
    # sample for review
    for es in list(seen)[:40]:
        print(f"  {es[:55]:55s} -> {seen[es]}")
