SELECT * FROM (
    VALUES 
    ('inadequate water access', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/6803/periodos/2022/variaveis/1000381?localidades=N6[all]&classificacao=1821[72153]'),
    ('income', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/1384/periodos/-6/variaveis/1000140?localidades=N6[all]&classificacao=11570[92973,92974,92975,92976,92977,92978,92979,92980]'),
    ('population density', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/614?localidades=N6[all]'),
    -- ('percentage of the population older than 60', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/6740/periodos/2022/variaveis/1009459?localidades=N6[all]&classificacao=297[72205]%7C86[95251]%7C287[100362]'),
    -- ('percentage of the population younger than 5', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/9847/periodos/2022/variaveis/9175?localidades=N6[all]&classificacao=1714[60024]|2661[32776]'),
    ('municipal agricultural area','IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/5457/periodos/2023/variaveis/1008331|1000216|1000215?localidades=N6[all]&classificacao=782[0]'),
    -- ('total gdp', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/-1/variaveis/37?localidades=N6[all]'),
    ('agriculture gdp', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/-1/variaveis/513?localidades=N6[all]'),
    ('inadequate sanitation', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/6805/periodos/-1/variaveis/1000381?localidades=N6[all]&classificacao=11558[72113,92858,72114,92861]'),
    ('waste collection', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/6892/periodos/-1/variaveis/1000381?localidades=N6[all]&classificacao=67[72122,72123,72124,1091]'),
    ('industry gdp', 'IBGE', 'https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/-1/variaveis/517?localidades=N6')
) AS t(indicator_name, datasoure, url);