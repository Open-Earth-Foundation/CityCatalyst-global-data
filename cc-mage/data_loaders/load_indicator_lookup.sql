SELECT * FROM (
    VALUES 
    ('water resources', 'drought', 'hazard', 'consecutive dry days', 'postive', 'Adapta', ''),
    ('water resources', 'drought', 'hazard', 'standardized precipitation evapotranspiration index', 'positive', 'Adapta', ''),
    ('water resources', 'drought', 'vulnerability', 'inadequate water acesss', 'positive', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/6803/periodos/2022/variaveis/1000381?localidades=N6[all]&classificacao=1821[72153]'),
    ('water resources', 'drought', 'vulnerability', 'income', 'postive', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/1384/periodos/-6/variaveis/1000140?localidades=N6[all]&classificacao=11570[92973,92974,92975,92976,92977,92978,92979,92980]'),
    ('water resources', 'drought', 'vulnerability', 'water security index', 'postiive', 'ANA', 'https://dadosabertos.ana.gov.br/datasets/897b12b3081c49678a1b2161c372b70c_0/about'),
    ('water resources', 'drought', 'exposure', 'population density', 'positive', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/614?localidades=N6[all]'),
    ('water resources', 'drought', 'exposure', 'nutrition and basic medical care', 'positive', 'IPS', '')
) AS t(keyimpact_name, hazard_name, component, indicator_name, relationship, datasoure, url);