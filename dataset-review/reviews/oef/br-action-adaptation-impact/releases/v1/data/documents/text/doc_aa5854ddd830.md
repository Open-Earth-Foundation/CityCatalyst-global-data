# Teórico-metodológico para avaliação do risco de impacto das mudanças climáticas em Setores Estratégicos — Recursos Hídricos

- Candidate document ID: `doc_aa5854ddd830`
- Workbook source IDs: WR_SRC_001
- Candidate sectors: Water resources
- Source PDF: `working/raw/doc_aa5854ddd830.pdf`
- SHA-256: `8bdccf4c932c39ae31ae1404f4483ba8dde337e17f850236034a985273fa5e71`
- Physical PDF pages: 70
- Extraction: Poppler pdftotext 25.09.1 (-layout)

> Page headings below use the 1-based physical PDF page number. Text order follows Poppler's layout-preserving extraction and has not been substantively edited.

---

## PDF page 1

Teórico-metodológico para avaliação do
        risco de impacto das mudanças
    climáticas em Setores Estratégicos


                             RECURSOS HÍDRICOS


          2025

## PDF page 2

                P70 Teórico-metodológico para avaliação do risco de impacto das mudanças
                climáticas em Setores Estratégicos - Recursos Hídricos / Instituto Nacional
                de Pesquisas Espaciais. – São José dos Campos: INPE, 2025.
                70 p.: il.


             1. Plataforma AdaptaBrasil. 2. Mudanças climáticas. 3. Risco climatico


                                                                        CDU: 551.583(07)


Data de revisão do documento: 18 de agosto de 2025.

## PDF page 3

 SUMÁRIO

1.            RISCO DE IMPACTO DAS MUDANÇAS CLIMÁTICAS ................ 5
     1.1. Risco de Impacto em Cascata ou Risco Encadeado ....................................................8
2.            DELIMITANDO O SETOR ESTRATEGICO RECURSOS HÍDRICOS ............ 11
     2.1. Caracterização do risco de escassez hídrica .............................................................. 14
     2.2. Caracterização do risco de estresse hídrico ............................................................... 16
3.            ÍNDICES E INDICADORES: PERSPECTIVAS TEÓRICAS............................... 18
4.  ÍNDICE DE RISCO DE IMPACTO ÀS MUDANÇAS CLIMÁTICAS PARA
RECURSOS HÍDRICOS ....................................................................................................... 20
     4.1. Ameaça de escassez hídrica ........................................................................................ 24
              4.1.1. Construção da ameaça de risco de escassez hídrica ............................................... 25
              4.1.2. Modelagem hidrológica 26
              4.1.3. Representação municipal da escassez hídrica 30
              4.1.4. Associação da ottobacia nos municípios 32
              4.1.5. Agregação dos valores brutos da ottobacia nos municípios 33
     4.2. Risco de estresse hídrico .......................................................................................... 34
              4.2.1. Identificação e pré-seleção dos indicadores candidatos ................................... 35
              4.2.2. Construção numérica e seleção dos indicadores .................................................. 36
              4.2.3. Cálculo dos demais níveis hierárquicos .................................................................... 43
     4.3. Cálculo dos fatores influenciadores ........................................................................ 49
      4.3.1. Cálculo da contribuição dos indicadores simples aos Índices de Risco de
Impacto (Nível 1 para Nível 5) ................................................................................................................. 49
       4.3.2. Cálculo da contribuição dos indicadores simples às dimensões associadas
(Nível 1 para Nível 4) .................................................................................................................................... 55
            4.3.3. Cálculo da contribuição dos indicadores simples às subdimensões da
vulnerabilidade a que estão associadas (Nível 1 para Nível
3) ....................................................................................................... .................................................................... 56
            4.3.4. Cálculo da contribuição dos indicadores simples aos indicadores temáticos a
que estão associadas (Nível 1 para Nível
2) ....................................................................................................... .................................................................... 57
              REFEREENCIAS BIBLIOGRAFICAS ................................................................. 59
              APÊNDICE A ............................................................................................................ 68

## PDF page 4

Resumo
O Sistema de Informações e Análises sobre Impactos das Mudanças do Clima (AdaptaBrasil) foi
instituído pelo Ministério da Ciência, Tecnologia e Inovações, por meio da Portaria nº 3.896, de
16 de outubro de 2020, tem como objetivo consolidar, integrar e disseminar informações que
possibilitem o avanço das análises dos impactos da mudança do clima, observados e projetados
no território nacional, dando subsídios às autoridades competentes pelas ações de adaptação.
       O AdaptaBrasil MCTI é desenvolvido por meio de uma cooperação entre o Instituto
Nacional de Pesquisas Espaciais (INPE), a Rede Nacional de Pesquisa e Ensino (RNP) e o
Ministério de Ciência, Tecnologia e Inovação (MCTI). Sua construção envolve especialistas e
atores nacionais e internacionais que trazem, através de um arcabouço científico metodológico,
dados e informações relevantes à sociedade no contexto das mudanças do clima. Para tal, são
utilizadas informações públicas e disponíveis para a composição de indicadores no
desenvolvimento de índices agregados para estimativas do risco de impacto das mudanças do
clima em diversos setores estratégicos como por exemplo: Água, Energia, Saúde e Alimento.
       O INPE é responsável pela aplicação da metodologia, pelas análises e validação dos
indicadores e índices, mas destaca-se o relevante papel de instituições parceiras, tais como,
Agência Nacional de Águas e Saneamento Básico (ANA), Fundação Osvaldo Cruz (Fiocruz),
Universidade Federal do Rio de Janeiro (UFRJ), Embrapa, Cemaden, Rede Clima, entre outras,
na coprodução dos riscos de impacto. Essas parcerias contribuem não apenas na construção da
plataforma, mas também da validação dos indicadores por técnicos, acadêmicos e cientistas
especializados nas distintas temáticas.
       Esse documento apresenta informações referentes aos principais marcos teóricos e
conceituais que descrevem e fundamentam o entendimento do risco de impacto de mudanças
climáticas e metodologias empregadas nas diversas etapas de construção de indicadores de
risco de impacto de mudanças climáticas no Setor Estratégico (SE) de Recursos Hídricos para o
AdaptaBrasil, versão Brasil 2.0, construção período 2023-2025. Aborda a estruturação do SE de
Recursos Hídricos 2.0, composto pelos riscos relacionados ao estresse hídrico e risco de escassez
hídrica. Além disso, detalha as metodologias aplicadas em cada etapa de construção de índices
e indicadores de risco de impacto das mudanças climáticas, assim como os fatores que
influenciam o setor.

## PDF page 5

       1.      Risco de impacto das mudanças climáticas
Segundo o Painel Intergovernamental de Mudanças Climáticas (IPCC, sigla em inglês), o risco é “o
potencial de consequências adversas para os sistemas humanos e/ou ecológicos, onde é considerado
a diversidade de valores e objetivos associados a tais sistemas. Por exemplo, consequências sobre
vidas, meios de subsistência, saúde e bem-estar, ativos e investimentos econômicos, sociais e culturais,
infraestrutura, serviços (incluindo serviços ecossistêmicos), ecossistemas e espécies” (IPCC, 2022).
       No contexto dos impactos das mudanças climáticas, os riscos (climáticos) resultam em
interações dinâmicas entre as ameaças climáticas (ou relacionadas ao clima) com a exposição e a
vulnerabilidade do sistema socioecológico (SSE)1 que é potencialmente afetado (interação essa
denominada, aqui, como flor de risco – Figura 1). Estas dimensões se inserem em um arcabouço
metodológico (framework) que combina conceitos utilizados pelo IPCC (2015; 2022).
       A vulnerabilidade trata da propensão ou predisposição de um sistema socioecológico ser
afetado negativamente, englobando uma variedade de conceitos e elementos, incluindo a
sensibilidade ou suscetibilidade a danos e a falta de capacidade de lidar e adaptar-se a uma situação
de perturbação climática (IPCC, 2021). Em outras palavras, a situação de vulnerabilidade está
relacionada com características intrínsecas de resiliência do SSE em questão, as quais estão
relacionadas direta ou indiretamente com a propensão do SSE ser impactado negativamente por uma
perturbação climática. Nesse sentido, a vulnerabilidade está relacionada com aspectos a priori e
qualitativos do SSE que possuem relação com os danos potenciais da(s) perturbação(ões) climática(s)
e, desta forma, o nível de vulnerabilidade pode aumentar ou diminuir o impacto climático. E conforme
apontado acima, pode ser desmembrada na dimensão de sensibilidade e de capacidade adaptativa do
SSE de análise (TURNER et al., 2003; GALLOPÍN, 2006). A sensibilidade diz respeito ao grau em que o
sistema em análise é afetado, adversamente ou beneficamente, por estímulos relacionados ao clima
(IPCC, 2021). A sensibilidade é uma propriedade inerente de um sistema socioecológico, existente antes
da ameaça climática, independente (separado) da exposição (IPCC, 2001; GALLOPÍN, 2003). Já a


       1   Sistema socioecológico diz respeito ao sistema que inclui subsistemas sociais (humanos) e
       ecológicos (biofísicos) em interação mútua (GALLOPÍN, 1991), ou seja, os sistemas humanos e
       naturais são entrelaçados, de forma interconectada e interdependente (BIGGS et al., 2021). Pode
       ser especificado para qualquer escala, desde a comunidade local e seu ambiente circundante até o
       global (GALLOPÍN, 2006).
                                                       5
                                                                  Teórico-metodológico para avaliação do risco de
                                                                     impacto das mudanças climáticas em Setores
                                                                     Estratégico: Segurança Alimentar e Recursos
                                                                                                         Hídricos

## PDF page 6

capacidade adaptativa está relacionada à habilidade do sistema socioecológico (considerando cada um
dos seus elementos) de se ajustar a um distúrbio ou danos potenciais, aproveitando as oportunidades
e lidando com as consequências de uma transformação que ocorra (IPCC, 2021).

Figura 1 – Modelo conceitual para análise do risco de impacto das mudanças climáticas desenvolvido para o
AdaptaBrasil MCTI 2.0.


Fonte: Elaborado por Karine Rocha, adaptado de IPCC (2015).

       A exposição diz respeito à presença dos elementos que compõem o SSE (pessoas; moradias;
espécies; ecossistemas; serviços, recursos e funções ambientais; infraestrutura; bens econômicos,
sociais ou culturais) em locais e contextos que possam ser afetados negativamente por uma
perturbação climática (IPCC, 2021). A exposição a uma ameaça climática particular pode ser
determinada independentemente da vulnerabilidade (GALLOPÍN, 2003; KASPERSON et al., 2005;
ADGER, 2006, IPCC, 2015).
       As ameaças climáticas (ou relacionadas ao clima) são perturbações climáticas que possuem
uma tendência ou iminência a acontecer e que pode afetar negativamente o sistema socioecológico
em questão. As perturbações climáticas estão associadas aos eventos climáticos extremos definidos a
partir de grandes picos de pressão, além do intervalo normal de variabilidade em que o sistema
socioecológico opera e que, geralmente, se originam além do sistema ou local em questão (GALLOPÍN,
2006). Além disso, interagem com o ambiente de análise e possuem capacidade de transformação
significativa nesse sistema, seja ela lenta ou repentina.

                                                    6
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 7

        As ameaças climáticas possuem características exógenas, endógenas ou ambas, dependendo
do fenômeno e do SSE em análise (TURNER et al., 2003; KASPERSON et al., 2005) – Figura 2. Ao
tratarmos de risco climático no AdaptaBrasil, as ameaças do clima são observadas como um agente
externo (exógenas) ao SSE, ou conjugado com este sistema, ainda que as causas que provocaram essas
ameaças sejam de origem antrópica - emissões de gases de efeito estufa. Essa organização se deve ao
fato de que não é possível associar emissões específicas com ameaças climáticas específicas, no tempo
e espaço. As ameaças de ordem endógena são caracterizadas na dimensão de vulnerabilidade,
conforme o arcabouço que é utilizado pelo IPCC.


Figura 2 – Diferentes fatores ou ameaças relacionadas ao clima.


Fonte: Elaborado por Karine Rocha.

        Os riscos de impacto da mudança climática (riscos climáticos) estão sujeitos à incerteza em
termos de magnitude e probabilidade de ocorrência por estarem relacionados às ameaças, exposição
e vulnerabilidade que podem mudar ao longo do tempo e do espaço devido a mudanças
socioeconômicas e à tomada de decisões humanas (IPCC, 2022). Eles estão se tornando cada vez mais
complexos e gerando impactos cada vez mais sistêmicos, multisetoriais e multiescalares. Tal impacto é
produto de um SSE altamente complexo2, o que implica uma profundidade de entendimento de ordem
sistêmica, multisetorial, multinível e multiescalar. Tais características trazem à tona sobre a
necessidade da avaliação precoce dos riscos com o intuito de se antever, precaver ou mesmo adaptar-
se aos possíveis impactos, considerando as interações entre os múltiplos impulsionadores do risco e
incluindo o papel das respostas de adaptação e mitigação para tal.


2 Utilizamos o termo complexo para comunicar a diversidade de interações entre setores e sistemas que podem
ampliar ou reduzir os riscos relacionados ao clima.
                                                       7
                                                           Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                               climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                         Hídricos

## PDF page 8

1.1. Risco de Impacto em Cascata ou Risco Encadeado
                       Impactos em cascata de eventos meteorológicos/climáticos extremos ocorrem quando um
                       perigo extremo gera uma sequência de eventos secundários em sistemas naturais e humanos
                       que resultam em perturbações físicas, naturais, sociais ou econômicas, em que o impacto
                       resultante é significativamente maior do que o impacto inicial. Os impactos em cascata são
                       complexos e multidimensionais e estão mais associados à magnitude da vulnerabilidade do que
                       a do perigo (IPCC, 2022).

       Em se tratando de riscos climáticos (também chamados de falhas climáticas), eles são
considerados sistêmicos quando se iniciam da consequência de impactos diretos – materializando-se
como uma cadeia ou cascata de impactos – e se agravam produzindo impactos ainda mais severos para
as pessoas e sociedades (GILL; MALAMUD, 2016; TURRENTINE, 2022). Segundo Lawrence; Blackett;
Gradock-Henry (2020), eles representam desafios de gestão significativos devido às suas capacidades
de cascata e recombinação, que exigem coordenação de respostas e tomada de decisão por atores em
vários níveis – ver representação da Figura 3.
       Nessa perspectiva, nem todos os impactos das mudanças climáticas surgirão da mesma forma
ou ao mesmo tempo: alguns surgem abruptamente, outros lentamente e são contínuos, podendo
haver múltiplos impactos ocorrendo simultaneamente e em diferentes combinações (PESCAROLI;
ALEXANDER, 2016; LAWRENCE et al., 2018; LAWRENCE; BLACKETT; CRADOCK-HENRY, 2020). Isso faz
com que seja absolutamente necessária a identificação de quando e onde ocorrem (ou ocorrerão) esses
impactos, pois há exemplos empíricos que indicam uma propagação dos impactos e suas implicações
como cascatas nos sistemas físicos e humanos (LAWRENCE et al., 2016; ROCHA et al., 2018; WILLNER;
OTTO; LEVERMANN, 2018; KOKS, 2018; LAWRENCE; BLACKETT; CRADOCK-HENRY, 2020; MIZRAHI,
2020). Por exemplo, o estudo dos efeitos em cascata de inundações na Tailândia (HILLY et al., 2018)
podem incluir desde perda de serviços críticos, ativos e bens, até congestionamento de tráfego e
atrasos no transporte, perda de negócios e renda, distúrbios e desconforto para os residentes.
       A abordagem do risco em cascata, além de tornar explícita a complexidade das interações entre
os múltiplos riscos, permite uma visão mais compartimentada e com enfoque nas interações dentro e
entre as dimensões de cada risco permitindo, portanto, ajudar a orientar uma avaliação mais detalhada
e precisa (GALAZ et al., 2011; LAWRENCE et al., 2018; SIMPSON et al., 2021). Pois os efeitos combinados
de estressores interativos podem afetar a capacidade de indivíduos, governos e setor privado de se
adaptar a tempo, ou seja, antes que ocorram danos generalizados (LAWRENCE; BLACKETT; CRADOCK-

                                                      8
                                                          Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                              climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                        Hídricos

## PDF page 9

HENRY, 2020; MIZRAHI, 2020).

Figura 1 – Falhas climáticas globais em cascata. Este é um diagrama de loop causal, no qual uma linha completa
representa uma polaridade positiva (por exemplo, feedback amplificador; não necessariamente positivo no
sentido normativo) e uma linha pontilhada denota uma polaridade negativa (significando um feedback
atenuante).


Fonte: Adaptado de Kemp et al. (2022).

                                                      9
                                                          Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                              climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                        Hídricos

## PDF page 10

          Uma estratégia para lhe dar com essa grande complexidade na análise e no entendimento do
risco de impacto associado às mudanças climáticas, é analisar as dimensões da flor de risco
(vulnerabilidade, exposição e ameaça climática) sob um determinado contexto, denominado aqui como
Setor Estratégico (SE). Cada SE possui elementos de impacto potencial específicos, portanto, a
delimitação conceitual de cada SE é fundamental para a construção dos indicadores e análise de risco
de impacto. O AdaptaBrasil MCTI disponibiliza informações para os SE segurança alimentar, segurança
energética, portos, saúde, recursos hídricos, dentre outros.
          Assim sendo, a versão 2.0 do AdaptaBrasil implementou a nova abordagem de avaliação dos
riscos de impacto das mudanças climáticas no estudo do SE Recursos Hídricos, a qual será detalhada a
seguir.


                                                  10
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 11

2.     DELIMITANDO O SETOR ESTRATEGICO RECURSOS HÍDRICOS
       O Setor Estratégico de Recursos Hídricos refere-se à avaliação de risco de impacto das mudanças
do clima nas águas superficiais e subterrâneas disponíveis para o uso humano. O setor avalia os
recursos hídricos do ponto de vista da disponibilidade e acesso aos recursos hídricos na perspectiva da
garantia da segurança hídrica para os diversos usos da água, incluindo o abastecimento humano,
manutenção da saúde e bem-estar, manutenção dos serviços ecossistêmicos de regulação hídrica, e
desenvolvimento de atividades socioeconômicas.
       No Brasil, os recursos hídricos estão fortemente conectados com o desenvolvimento
econômico, social e ambiental do país e são de fundamental importância para a segurança hídrica
nacional (ANA, 2019; ANA, 2024). A segurança hídrica se conforma quando há disponibilidade de água
em quantidade e qualidade suficientes para o atendimento às necessidades humanas, à prática das
atividades produtivas econômicas e à conservação dos ecossistemas aquáticos (ANA, 2019).
       Estimativas apontam que o Brasil detém cerca de 12% a 15% dos recursos hídricos renováveis
do mundo (MARENGO et al., 2016; GETIRANA et al., 2021; ANA, 2024). Dadas suas dimensões
continentais e condições hidroclimáticas, as reservas de água doce do Brasil não são distribuídas de
forma homogênea pelo país, sendo altamente heterogêneas no território e dependentes do clima e da
variabilidade climática no tempo, com áreas que lidam com o desafio da escassez de água devido à
distribuição extremamente desigual dos recursos hídricos e à intensificação do uso da água (MARENGO,
2008; MARENGO et al., 2016; GESUALDO et al., 2021; BALLARÍN et al., 2023). Além disso, o Brasil é
fortemente dependente da hidroeletricidade: aproximadamente 60% da geração de energia vem desse
setor (HUNT et al., 2018). No entanto, espera-se que o país expanda suas áreas irrigadas, o que pode
agravar o estresse hídrico (MULTSCH et al., 2020). Essa situação preocupante não afetará apenas o
Brasil, mas poderá ter proporções globais. O país desempenha um papel fundamental na segurança
alimentar mundial, sendo um dos maiores produtores agrícolas (PEREIRA et al., 2012) e possuindo áreas
classificadas como hotspots globais de biodiversidade (MYERS et al., 2000).
       Das reservas de água doce do Brasil, 80% delas estão localizadas na região amazônica. Por outro
lado, a região semiárida do Nordeste, mesmo incluindo parte da bacia do rio São Francisco, possui
apenas 4% dos recursos hídricos do país, mas abriga 35% da população brasileira, composta
principalmente por famílias de baixa renda e onde grande parte das cidades com mais de cinco mil

                                                  11
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 12

habitantes enfrentarão crise de abastecimento de água para o consumo humano (MARENGO, 2008;
MARENGO et al., 2016). O episódio de crise hídrica na Região Metropolitana de São Paulo (RMSP), uma
das maiores secas da sua história, entre 2014-2015, resultante da combinação de baixos índices
pluviométricos durante o verão 2014 e 2015 e um grande crescimento da demanda de água, que afetou
drasticamente a disponibilidade hídrica dos reservatórios do Sistema Cantareira, o principal sistema de
abastecimento de São Paulo, responsável pelo abastecimento de 6 milhões de habitantes na região
metropolitana, ilustra bem os impactos relacionados ao estresse hídrico (MARENGO; ALVES; 2015).
       Nesse sentido, para obtenção de uma avaliação mais completa dos riscos futuros que impactam
a disponibilidade e acesso aos recursos hídricos é preciso que sejam contemplados certos preceitos da
segurança hídrica, tais como, acesso aos recursos hídricos a um custo acessível e em quantidade e
qualidade aceitáveis para atender necessidades básicas, incluindo condições sanitárias e de higiene, e
a manutenção da saúde e bem-estar; manutenção dos serviços ecossistêmicos de regulação hídrica;
manutenção do desenvolvimento de atividades socioeconômicas relacionadas, governança adequada
para lidar com múltiplos usos, atores e interesses (ANA, 2019; ONU, 2013).
       Os princípios deste SE seguem os fundamentos da Política Nacional de Recursos Hídricos (Lei nº
9.433/1997), que considera: (i) a água é um bem de domínio público; (ii) a água é um recurso natural
limitado, dotado de valor humano e a dessedentação de animais; (iv) a gestão dos recursos hídricos
deve sempre proporcionar o uso múltiplo das águas; (v) a bacia hidrográfica é a unidade territorial para
implementação da Política Nacional de Recursos Hídricos e atuação do Sistema Nacional de
Gerenciamento de Recursos Hídricos; (vi) a gestão dos recursos hídricos deve ser descentralizada e
contar com a participação do Poder Público, dos usuários e das comunidades. Considerando tais
fundamentos, o acesso à água pela população deve ser a um custo acessível e em quantidade e
qualidade aceitáveis para a manutenção da sua subsistência, bem-estar e desenvolvimento
socioeconômico, devendo considerar o planejamento da oferta e do uso da água em um país (ONU,
2013; ANA, 2019).
       Além disso, a incorporação das vulnerabilidades e exposição dos sistemas socioecológicos na
análise do risco climático futuro, amplia maneiras de estar mais bem preparado para os impactos
causados pelo clima considerando as incertezas inerentes ao risco futuro, podendo melhorar a
capacidade adaptativa do sistema para impactos não causados pelo clima (OLSEN et al., 2015) e motivar
melhorias na gestão contínua, incluindo monitoramento de secas e cheias, previsão
                                                  12
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 13

hidrometeorológica, maior conservação da água etc. (SALAS et al., 2012).
       Para lidar com essas complexidades, os procedimentos técnicos, analíticos e de governança
para a gestão hídrica devem acompanhar as crescentes demandas da sociedade e a análise de risco
climático associadas à mudança climática é uma ferramenta imprescindível para o futuro dos recursos
hídricos no Brasil (ANA, 2024). Portanto, o objetivo desta avaliação foi verificar o risco de impacto na
disponibilidade e acesso aos recursos hídricos para diversas finalidades no Brasil devido aos efeitos
adversos do clima que provocam estresse hídrico no sistema socioecológico.
       Para construir esta avaliação, partiu-se de uma avaliação teórica de cadeia de impactos para os
recursos hídricos relacionados à escassez de água. Em discussão com atores da ANA e INPE, construiu-
se uma hierarquia de impactos nos recursos hídricos no tempo (Figura 4). Assim, considerando a
ameaça de escassez hídrica, os impactos de primeira ordem provocam alterações mais diretas no ciclo
hidrológico. Em seguida, numa segunda ordem de impactos, as mudanças no sistema hidrológico
provocado pela escassez de água interferem diretamente na disponibilidade hídrica, principalmente na
capacidade de armazenamento de água e se persistir também na qualidade da água. Nade terceira
ordem, os impactos afetam mais diretamente o sistema humano e seus usos, uma vez que, a
indisponibilidade hídrica e falta de reservação, modificam o acesso aos recursos hídricos e as atividades
dependentes, desde o abastecimento humano, atividades econômicas e até a produção energética.
Desta estruturação teórica, moldou-se a construção dos riscos de estresse hídrico em função do risco
de escassez hídrica, detalhados nas próximas seções.


                                                   13
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 14

Figura 4 - Hierárquica teórica de impactos sobre os recursos hídricos em situações de escassez hídrica.


Fonte: Elaborado por Thales Penha.


2.1. Caracterização do risco de escassez hídrica
        A escassez de água (water scarcity) é um conceito que pode ser entendido amplamente como
a quantidade de água que pode ser acessada fisicamente e que varia conforme a oferta e a demanda
mudam. A escassez de água intensifica-se à medida que a procura aumenta e/ou à medida que o
abastecimento de água é afetado pela diminuição da quantidade ou qualidade da água disponível (UN
WATER, 2023). Portanto, a escassez de água pode ser descrita como uma condição de falta de água
para atender a demanda básica (water demand), excedendo assim o abastecimento de água disponível
(water supply).
        A escassez hídrica emerge de situações em que não há água suficiente para garantir
simultaneamente as necessidades humanas e dos ecossistemas. Pode ser resultante tanto de uma falta
básica de água, ou seja, escassez física de água (water scarcity), mas também pode resultar da falta de
infraestruturas adequadas, tecnologia ou fraca capacidade humana para fornecer acesso aos recursos
hídricos disponíveis (water availability), a qual pode ser referido como escassez económica de água
(economic water scarcity) (PEREIRA et al., 2009; WHITE, 2014; BOND et al., 2019; IPCC, 2022). A

                                                      14
                                                           Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                               climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                         Hídricos

## PDF page 15

escassez física de água pode ocorrer tanto como resultado de fenómenos naturais (por exemplo, aridez,
seca) como de influências humanas (por exemplo, desertificação, armazenamento de água), embora
estas influências sejam frequentemente acopladas e os impactos de maiores proporções ocorrem
sobre o sistema ecológico (PEREIRA et al., 2009; WHITE, 2014; BOND et al., 2019).
       A escassez hídrica pode resultar em perdas econômicas e sociais significativas, impactando
vários setores, da agricultura ao turismo, com efeitos profundos nas comunidades locais. Acarretam
também em problemas que não devem ser avaliados apenas sobre a perspectiva climática ou
ambiental, haja vista que são decorrentes de um conjunto de outros problemas de ordem econômica
e desenvolvimento social (GLEICK, 2000), tais como fatores de disponibilidade e aumento da demanda,
processos de gestão ainda setorial e de resposta a crises e problemas sem atitude preditiva e
abordagem sistêmica (TUNDISI, 2008). Assim, déficits hídricos mais frequentes, podem implicar em
aumento de custos para a sociedade, necessitando de estratégias de adaptação por parte dos usuários
de água para mitigar parte desses custos (ANA, 2024). Tundisi et al. (2008) apontam os principais
problemas e processos que têm prejudicado a oferta de água, observada como um recurso finito: (a)
intensa urbanização, aumentando a demanda e a contaminação da água; (b) estresse e escassez
decorrentes de alterações na disponibilidade e aumento da demanda; (c) fraca infraestrutura na rede
de distribuição de água potável, com muitas perdas; (d) problemas de estresse e escassez em razão de
mudanças ambientais e climáticas.
       Embora sujeitas a incertezas, as projeções de mudança climática indicam possíveis impactos e
desafios futuros sobre os recursos hídricos no Brasil. Os impactos projetados variam de acordo com a
região do Brasil, no entanto, os estudos convergem e indicam que praticamente em todas as bacias
hidrográficas do Brasil existem tendências de diminuição das vazões dos rios no período 2011-2040 e
de forma mais geral os modelos concordam com aumentos na temperatura e evapotranspiração (SÃO
PAULO, 2011; ANA, 2024). As áreas mais ameaçadas pelo aumento na frequência e intensidade de dias
secos consecutivos, por exemplo, compreendem o leste da Amazônia e o Nordeste do Brasil
(MARENGO, 2014). Desta forma, a elevação da temperatura e da evapotranspiração poderá acarretar
principalmente na mudança da disponibilidade de água para diversos usos e, entre outros efeitos,
aumentar a necessidade de irrigação, refrigeração, consumo humano e dessedentação de animais em
determinados períodos e regiões do país, afetando a capacidade de reservação e o balanço hídrico
(ANA, 2019). Ainda de acordo com estudos científicos, eventos hidrológicos extremos, como as secas e
                                                 15
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 16

enchentes, poderão tornar-se mais frequentes e mais intensos a cada grau de aquecimento global
(MARENGO et al., 2014; CARETTA, 2022). Somadas aos impactos esperados no regime hidrológico nos
cenários de mudanças do clima, estão as prováveis mudanças na demanda de diversos setores e
usuários sobre os recursos hídricos, que afetará o balanço hídrico de oferta e demanda, à medida que
as previsões realizadas a partir da expectativa de crescimento populacional e desenvolvimento dos
países possam se concretizar, o que intensificará a escassez hídrica (LIU et al., 2017; HE et al., 2021;
AGHAKOUCHAK et al., 2020; BALLARIN et al., 2023; ANA, 2024).
       Nesta avaliação, o risco de escassez hídrica é compreendido como saldo do meio físico de
disponibilidade de água em função das variações nas vazões em bacias hidrográficas, resultante das
interações dinâmicas entre o sistema hidrológico e a variabilidade climática presente e projetada no
futuro (ex: aumentos de temperatura, eventos de menor precipitação, alterações no escoamento
superficial e na evapotranspiração), que expressa a escassez física da água no sistema natural.


2.2 Caracterização do risco de estresse hídrico

Estresse hídrico como conceito pode ser entendido de forma mais genérica como a capacidade
deficitária das infraestruturas de suprimento de água de atender às necessidades humanas e ecológicas
da água. Quando a demanda por água excede a quantidade disponível durante um determinado
período ou quando a qualidade da água limita seu uso, caracteriza-se o estresse hídrico (UN WATER,
2023). O estresse hídrico emerge de cenários e situações em que o balanço hídrico dos recursos hídricos
é deficitário, isto significa que o saldo de oferta e demanda da água em uma determinada localidade e
negativo (o uso humano da água excede o volume de água disponível), sendo incapaz de oferecer uma
segurança hídrica para os diversos usos da água, inclusive, o abastecimento humano.
       Ao longo do último século, o crescimento substancial da população, das atividades industriais e
agrícolas e dos padrões de vida (ou seja, o uso per capita de água) intensificaram o estresse hídrico em
muitas partes do mundo (AGHAKOUCHAK et al., 2015; MEHRAN et al., 2017), com diferentes graus de
estresse hídrico sendo vivenciados nas condições atuais e em projeções de novas mudanças na
disponibilidade regional de água, fortemente impactada pela contínua redução dos aquíferos devido à
extração excessiva para fins de irrigação (IPCC, 2022). Com um aumento global da temperatura em
aproximadamente 2°C, estima-se que entre 0,9 e 3,9 bilhões de pessoas enfrentarão maior exposição
                                                  16
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 17

ao estresse hídrico, dependendo dos padrões regionais de mudanças climáticas e dos cenários
socioeconômicos considerados (KOUTROULIS et al., 2019).
        Como a disponibilidade de água também está intimamente associada às operações da
infraestrutura de abastecimento hídrico (como reservatórios de água superficial e usinas de
dessalinização) e ao comportamento humano no uso da água (por exemplo, crescimento e ciclos
sazonais na demanda por água), o estresse hídrico advém de fatores socioeconômicos e da pressão da
demanda pelo uso dos recursos hídricos (MEHRAN et al., 2017; MUNIA et al., 2020). Incorporar a
avaliação dessas pressões socioeconômicas é, portanto, muito importante ao analisar o impacto das
mudanças climáticas nos recursos hídricos futuros, especialmente ao discutir planos de adaptação para
a gestão da água (KIGUCHI et al., 2015). Assim, para o setor de recursos hídricos, as incertezas oriundas
da mudança climática incidirão tanto do lado da oferta como também do lado da demanda hídrica
(ANA, 2024).
        Na cadeia de risco de impacto para recursos hídricos (Figura 5), a avaliação do risco de estresse
hídrico é desencadeada pela combinação do risco de escassez hídrica (indisponibilidade hídrica),
enquanto ameaça, com as características de vulnerabilidade e exposição do sistema socioecológico,
que impactam o acesso aos recursos hídricos hídrico para os diversos usuários dos recursos hídricos,
como os setores produtivos (ex: agropecuária, indústria de transformação, mineração e termoenergia)
e o abastecimento humano.


Figura 5 – Desenho teórico da avaliação dos riscos em cascata de escassez hídrica e do risco de estresse hídrico.


Fonte: Elaborado por Thales Penha.
                                                      17
                                                           Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                               climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                         Hídricos

## PDF page 18

3.     Índices e indicadores: perspectivas teóricas
A análise de risco na edição do AdaptaBrasil MCTI 2.0 considerou a construção de uma composição de
indicadores e índices para informar e medir o comportamento ou estado de um sistema ou fenômeno
em termos de atributos expressivos e perceptíveis (OECD, 1993). Os indicadores também podem ser
considerados como variáveis indiretas, do ponto de vista de que uma variável ou fenômeno não pode
ser medido diretamente (GALLOPÍN, 1996).
       Devido a essas características, os indicadores têm sido utilizados para traduzir e comunicar
fenômenos socioambientais complexos para público amplo (MAGGINO, 2017), mas principalmente aos
tomadores de decisão e gestores ambientais, visando monitorar as metas de desenvolvimento
sustentável (JANNUZZI, 2005; VAN BELLEN, 2006; MIOLLA; SCHILTZ, 2019). Considerando que sistemas
complexos, como o sistema socioecológico, exige um entendimento interdisciplinar, ou mesmo
transdisciplinar (OSTROM, 1990), o diálogo e a comunicação entre pesquisadores e setores da
sociedade de diferentes áreas do conhecimento permite o aprofundamento do diagnóstico dos
elementos de risco climático e por conseguinte a construção de indicadores deste risco.
       Toda construção de indicadores é baseada em um referencial conceitual-metodológico. A
publicação elaborada pela Organização para a Cooperação e Desenvolvimento Econômico ou
Económico (OCDE) e a Joint Research Centre (JRC) (OCDE, 2008; BECKER et al., 2019), propõem um
marco metodológico de composição hierárquica de indicadores e índices, que dialoga com a estrutura
clássica da pirâmide da informação, conforme Hammond et al. (1995). Nesta estrutura, parte-se do
princípio de que dados observados de forma isolada não retratam um fenômeno multidimensional ou
complexo e, sendo assim, a informação sintética comunica de forma mais objetiva padrões do
fenômeno, principalmente para o público amplo, mas também permite direcionar melhor recursos e
ações de tomadores de decisão (JANNUZZI, 2006).


                                                 18
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 19

                                 Figura 6 - Pirâmide da informação.


                             Fonte: Adaptado de Hammond et al. (1995).


     Todavia, a ideia não se trata apenas de comunicar a informação sintética em forma de índices –
o topo da pirâmide – mas sim de apresentar a composição hierárquica da informação, de forma que se
possa ter uma leitura analítica da composição da pirâmide. Este tipo de leitura pode alinhar
informações sintéticas, que apontam um estado mais grave do fenômeno, com elementos de forças e
pressões tangíveis que promovem tal estado. Este tipo de tratamento da informação é útil para
tomadores de decisão, pois precisam de informações sinóticas de forma preliminar para agilizar
análises focais e poder responder ou se adaptar às ameaças, neste caso, de mudanças climáticas
(MEADOWS, 1998; JACOB; BLAKE, 2010).


                                                19
                                                     Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                   Hídricos

## PDF page 20

4. Índice de Risco de Impacto às Mudanças Climáticas para
Recursos Hídricos
O risco de impacto das mudanças climáticas é o resultado emergente da interação entre três dimen-
sões, a saber, Vulnerabilidade, Exposição e Ameaça, que, por sua vez, estão associadas intrinseca-
mente às mudanças nos fatores de pressão a que são submetidas. Neste sentido, optou-se por ela-
borar um sistema de índices e indicadores que fosse capaz de captar as relações de casualidade e
influência desses fatores do risco. Essa metodologia incluiu diferentes etapas metodológicas para
obtenção do índice de risco de impacto, incluindo a coleta de dados, tratamentos estatísticos, agre-
gações e métodos de análises (pesquisa bibliográfica, aplicações com sistema de informações geo-
gráficas, análise estatística etc.), além de contemplar múltiplas escalas espaciais (nacional, regional,
estadual e municipal) e temporais (intervalo de análise decadal).
     A estrutura de construção da informação foi baseada na pirâmide da informação - abordada no
capítulo anterior - dentro do escopo das dimensões de risco, conforme IPCC (2015). Para tanto, foram
consideradas informações desde dados brutos, indicadores, indicadores temáticos, índices das di-
mensões do risco de impacto climático e o índice de risco de impacto climático. Estas informações
estão situadas em níveis da composição da informação hierárquica, conforme ilustra a Figura 7 a qual
representa a hierarquia dos indicadores para a avaliação de risco de estresse hídrico.
     O nível 6 representa a composição de cálculo finalizada para integrar a composição de indica-
dores, cujos dados são extraídos a partir de fontes primárias e/ou secundárias. Esta camada de infor-
mação é denominada como dado bruto e não é apresentada na plataforma AdaptaBrasil MCTI. O
dado bruto passar por tratamentos numéricos, tais como, tratamento de outliers, normalizações,
possível inversão de valores e ponderações. O propósito é que se tenha uma unidade numérica única
entre todos os indicadores e que o significado do indicador possa ser representado na sua respectiva
dimensão de risco climático. Ao passar por essas transformações numéricas, o dado bruto, passa a
ser denominado como indicador simples (ou indicador) e integra a informação mais elementar da
Plataforma, de nível 6.


                                                  20
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 21

Figura 7 – Estrutura hierárquica entre as composições de indicadores e índices de risco de impacto das mu-
danças climáticas no SE de recursos hídricos.


Fonte: Elaborado por Thales Penha e Karine Rocha.

      A construção de indicadores e índices de risco climático na plataforma segue três esferas de
entendimento: (i) sistema socioecológico; (ii) Setor Estratégico, e (iii) tipos de perturbação climática
a que o sistema socioecológico e setor estratégico são passíveis de serem submetidos – ameaça cli-
mática.

      Os sistemas socioecológicos (SSE) foram conceituados no primeiro capítulo. Os estudos em SSE
têm canalizado três tipos de visões: (i) como os subsistemas ecológicos podem suprir serviços ecos-
sistêmicos para as necessidades e bem-estar humano; (ii) como as demandas humanas e a obtenção
de recursos ecossistêmicos podem determinar a integridade do subsistema ecológico, e (iii) como os
dois subsistemas podem responder de forma integrada às forças endógenas e exógenas de mudanças
do sistema socioecológico (BERRÖUET; MACHADO; VILLEGAS-PALACIO, 2018). Nesta última aborda-
gem houve avanços sobre a vulnerabilidade e respostas dos SSE em relação às mudanças climáticas
e fenômenos naturais. Na plataforma AdaptaBrasil, os SSE têm sido o grande palco de entendimento


                                                    21
                                                         Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                             climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                       Hídricos

## PDF page 22

sistêmico de vulnerabilidades e riscos associados às possíveis ameaças climáticas, mas considerando
um determinado setor estratégico objeto de impacto potencial.
     Apesar dos SSE ser um arcabouço sistêmico a ser perseguido, a avaliação de riscos climáticos
deve ter um direcionamento para políticas públicas e setores de decisão da sociedade, que, na sua
grande maioria, se apresentam de forma setorizada. Além disso, a construção de uma estrutura hie-
rárquica de composição de indicadores e índices é por si um esforço de síntese de um sistema que é
complexo. Nesse sentido, a avaliação de riscos climáticos por setores estratégicos é providencial para
que a informação possa alcançar os diferentes atores desses setores. Conforme Jones e Boes (2004),
a avaliação dos riscos climáticos pode ser calcada na vulnerabilidade do sistema e partir daí, identifi-
car as ameaças envolvidas. Nesse caso, a vulnerabilidade do sistema é direcionada por Setores Estra-
tégicos no AdaptaBrasil.
     Os objetos concretos de risco de impacto climático que são de interesse do Estado, são, por
exemplo, sociedade, recursos naturais, infraestruturas, seguranças, ativos, acessos e economia. Tais
objetos são passíveis de sofrer impactos negativos relevantes provocados por perturbações climáti-
cas – fator exógeno – e pelas características intrínsecas do objeto de impacto, vulnerabilidade e ex-
posição – fatores endógenos. Cada setor estratégico (SE) do AdaptaBrasil MCTI possui seus objetos
de análise de risco climático. Os primeiros SE a serem considerados na plataforma AdaptaBrasil, no
ano de 2018, foram Água, Alimentos e Energia, na perspectiva da segurança. Desde então a Plata-
forma tem buscado priorizar os setores contemplados na Política Nacional de Adaptação do ano de
2016 e, mais recentemente, no Plano Clima – Adaptação (2024/205), tais como: Agricultura, Recursos
Hídricos, Segurança Alimentar e Nutricional, Biodiversidade, Cidades, Gestão de Riscos e Desastre
Geo-hidrológicos, Indústria e Mineração, Infraestrutura (portuária, rodoviária e ferroviária), Povos e
Populações Vulneráveis, Saúde e Zonas Costeiras.
       Este documento se refere ao SE de Recursos Hídricos que foi desenvolvido pelo INPE em par-
ceria com a ANA para a versão AdaptaBrasil 2.0. O terceiro elemento fundamental para a delimitação
do risco climático é o tipo de perturbação ou ameaça climática que está sendo considerada que afeta
ou possa afetar o SSE em um dado setor estratégico. A Plataforma apresenta o risco de impacto cli-
mático, e sua construção hierárquica de indicadores, para uma ameaça climática específica de forma
separada direta, por exemplo, seca, chuvas intensas, ondas de calor, ventos, dentre outros; ou de


                                                  22
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 23

forma separada indireta, como os eventos hidrológicos. A ameaça climática é codificada na plata-
forma por um índice final climático, resultante de uma composição de indicadores climáticos, não
havendo indicadores temáticos intermediários, conforme ilustração da Figura 7. Na versão Adapta-
Brasil 2.0, conforme já explicado anteriormente, a ameaça construída que afeta o Risco de Estresse
Hídrico é um produto oriundo de modelagem hidrológica que expressa o Risco de Escassez Hídrica,
ao avaliar a disponibilidade hídrica nas vazões de rios devido a interação do sistema hidrológico com
a variabilidade climática presente e futura. Este desenvolvimento será tratado em detalhe na próxima
seção.
         Por fim, cada índice de risco climático na plataforma – nível 1 – deve ser entendido como uma
magnitude potencial de impacto climático ao se concretizar o contato do SSE – com sua vulnerabili-
dade intrínseca - com a perturbação climática – com a sua tendência implícita. Não se deve compre-
ender esse índice como a probabilidade de ocorrência de impacto climático. A construção dos valores
de indicadores e índices de risco climático, que culmina no índice de risco climático, está diretamente
associada a um Setor Estratégico e a uma determinada ameaça climática.


         4.1 Ameaça de escassez hídrica

         No momento, a Plataforma possui um conjunto de indicadores e índices de vulnerabilidade e
exposição (indicadores socioecológicos) situados no presente e de ameaças climáticas situados no
presente e projetados para o futuro, que se conectam/associam conforme representado no esquema
da Figura 8.


                                                  23
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 24

        Figura 8 – Integração das dimensões de ameaça climática com vulnerabilidade e exposição na
avaliação do risco climático: presente e cenários futuros.


       Fonte: Elaborado por Karine Rocha e Gustavo Arcoverde.

       No contexto dos indicadores socioecológicos, o termo "presente" denota dados oriundos da
década de 2010 e 2020, levando em consideração a versão mais recente dos dados oficiais
disponíveis. Em relação aos dados climáticos, o termo "presente" está vinculado à média do período
histórico (baseline) dos modelos climáticos selecionados para o setor (1986-2014), enquanto as
projeções abrangem os períodos 2030 (2015-2040) e 2050 (2041-2070).
       Para a determinação dos cenários climáticos adotados na Plataforma, foram considerados os
cenários de emissões do Sexto Relatório de Avaliação do Painel Intergovernamental sobre Mudanças
Climáticas (AR6/IPCC), utilizando o conjunto de modelos do NASA Earth Exchange Global Daily
Downscaled Projections (NEX-GDDP-CMIP6), derivado de modelos gerais de circulação - General
Circulation Model (GCM) - Coupled Model Intercomparison Project Phase 6 (CMIP6). Esses cenários

                                                 24
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 25

incorporam trajetórias plausíveis de concentração de gases, conhecidas como Shared Socioeconomic
Pathways (SSPs), abrangendo emissões de gases de efeito estufa, emissões de poluentes
atmosféricos e mudanças no uso da terra. Os esforços de mitigação são representados pelos cenários
SSPP2-4.5, caracterizado como intermediário (considerado como Cenário Otimista), e SSP5-8.5,
identificado como um cenário de alta emissão de gases de efeito estufa (denominado Cenário
Pessimista).


               4.1.1. Construção da ameaça de risco de escassez hídrica

A escassez hídrica pode ser entendida no contexto do AdaptaBrasil como uma ameaça relacionada
ao clima que afetaria o sistema socioecológico, devido a interação das alterações e variações
climáticas com o sistema hidrológico. Desta forma, caracteriza-se a escassez hídrica quando há a
diminuição prolongada do volume de água disponível que impacta a disponibilidade hídrica para
diferentes usos.
     O risco de escassez hídrica ou da indisponibilidade hídrica, entendido no contexto dos impactos
das mudanças climáticas, seria resultante de interações dinâmicas entre as ameaças relacionadas ao
clima (por exemplo, aumentos de temperatura, eventos de menor precipitação, alterações no
escoamento superficial e na evapotranspiração), com a exposição do sistema hidrológico (ex: bacias
hidrográficas, rios, aquíferos etc.). A representação deste fenômeno é complexo e impõe desafios
nas escolhas metodológicas, assumindo certos graus de incertezas e limitações para que possam ser
trabalhadas (ANA, 2024).
     Para estimar os impactos da mudança climática na disponibilidade futura de água, os modelos
climáticos globais (MCGs) foram utilizados, porém, por natureza, existe uma simplificação de
processos altamente não-lineares (dinâmicos), e há limitações na modelagem principalmente quanto
as teleconexões de larga escala que afetam significativamente os extremos hidrológicos
(AGHAKOUCHAK et al., 2013; ASCE, 2018). Devido a estes motivos, a seleção dos MCGs mais
adequado é uma fonte também de incerteza, e geralmente é avaliado com base no quão bem eles
são capazes de replicar as condições climáticas atuais (ANA, 2024).
     Nesse sentido, o trabalho denominado Mudanças Climáticas nos Recursos Hídricos do Brasil
desenvolvido pela Agência Nacional de Águas e Saneamento (ANA, 2024) foi utilizado como base para

                                                25
                                                     Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                   Hídricos

## PDF page 26

a construção do índice de risco de escassez hídrica. Conforme descrito nesse documento, em escala
nacional, a abordagem “top--down” é mais adequada para avaliação de disponibilidade hídrica. Essa
abordagem, utilizada nesse estudo, envolveu uma melhoria na resolução espacial (“downscaling”)
das projeções climáticas dos MCGs sob um conjunto de cenários de emissão para fornecer insumos
para modelos hidrológicos e de gestão de recursos hídricos estimando impactos potenciais,
fornecendo subsídios para definição de estratégias de adaptação.
     O estudo da ANA, definiu como estratégia metodológica a escolha do tipo de modelagem
hidrológica que seria mais adequado a transformação dos dados de clima em vazão para avaliação
da disponibilidade hídrica. Nesse processo, foram considerados diferentes aspectos como: escala do
problema, disponibilidade de dados, tempo de execução do estudo, conhecimento da modelagem
hidrológica pela equipe da ANA e exigências computacionais. Nesse sentido, optou-se pela
modelagem hidrológica menos complexa baseada na hipótese de Budyko (ANA, 2024).


               4.1.2. Modelagem hidrológica

A base para geração do índice de ameaça climática de escassez hídrica foi a modelagem hidrológica
realizada pela ANA (2024), adaptada para ser incorporada na estrutura metodológica da
AdaptaBrasil. Assim, uma das primeiras etapas foi a aproximação entre as metodologias.
     A modelagem hidrológica realizada pela ANA é baseada nos métodos de estimativas de
elasticidade climática e na hipótese de Budyko (1974) e posteriormente derivado pela equação de Fu
(2007). Para alimentar o modelo, dados hidroclimáticos observados (passado e presentes) e futuros
foram coletados. Os dados observados de referência são oriundos da base de dados da ANA
denominada HIDRO e XAVIER. A base HIDRO¹ 3contém todas as informações coletadas pela Rede
Hidrometeorológica Nacional (RHN), reunindo dados de níveis fluviais, vazões, chuvas, climatologia,
qualidade da água e sedimentos (ANA, 2024). A base XAVIER4, corresponde a uma grade regular de
0,25 ° × 0,25 ° de resolução espacial construída a partir de dados interpolados de 9259 estação
pluviométricas e 735 estações meteorológicas cobrindo todo o território brasileiro durante o período
de 1980-2015 (XAVIER et al., 2015, 2016). Os dados climáticos projetados de precipitação e


3 https://www.snirh.gov.br/hidroweb/
4 https://utexas.app.box.com/v/Xavier-etal-IJOC-DATA
                                                       26
                                                            Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                                climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                          Hídricos

## PDF page 27

evapotranspiração potencial necessários à modelagem hidrológica foram coletados do conjunto de
dados NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6)5.
     Em seguida. de posse desses dados, foram obtidas estatísticas de interesse da modelagem
hidrológica. Essas estatísticas foram transferidas para a base hidrográfica ottocodificada (BHO) de
referência da ANA. Com base nas estatísticas observadas e a base de disponibilidade hídrica atual
disponível na BHO, foi estimado o parâmetro do modelo hidrológico baseada na hipótese de Budyko,
conforme descrito de forma simplificada nas Equação 1 e Equação 2. Por fim, esse modelo ajustado
foi aplicado na variação relativa do clima futuro em relação ao presente para obtenção das vazões e
disponibilidade hídrica futura (ANA, 2024). A Figura 9 mostra o fluxograma de procedimentos
metodológicos e são minuciosamente detalhados em ANA (2024).


                                                          1
                               𝑄 = [𝑃𝜔 + 𝐸0 𝜔 ] − 𝐸0                                                                    Eq.1
                                                          𝜔

                               𝑑𝑄          𝑑𝑃             𝑑𝐸0
                                    = 𝜀1         − 𝜀2                                                                   Eq.2
                                𝑄           𝑃               𝐸0

Onde: 𝑄 = balanço hídrico expresso em valores de vazão média de longo termo (Qmlt); P =
Precipitação; 𝐸0 = Evapotranspiração potencial; 𝜔 = parâmetro que representa o conjunto de
características da bacia; 𝜀1 e 𝜀2 = coeficientes de elasticidade-precipitação e elasticidade-
evapotranspiração potencial da vazão.
     As saídas do modelo hidrológico correspondem aos valores de vazão média de longo tempo
(Qmlt) em cada ottobacia para os tempos presentes e futuros. Por meio deste método estima-se às
mudanças percentuais da vazão (Qmlt) de uma bacia hidrográfica devido às mudanças na
precipitação (P) e evapotranspiração potencial (P), correspondendo a oferta hídrica de uma bacia
baseado no balanço hídrico. A disponibilidade hídrica futura (vazões) foi gerada para todos os 34
modelos disponíveis do NEX-GDDP-CMIP6 (Disponível em: <https://nex-gddp-cmip6.s3.us-west-
2.amazonaws.com/index.html#NEX-GDDP-CMIP6/>), no entanto, para adequar a metodologia de


5 https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp


                                                   27
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 28

índices do AdaptaBrasil foi selecionado um sub-conjunto para representação dessas projeções no
Brasil.

Figura 9 – Esquema metodológico utilizado na avaliação do impacto da mudança climática nos recursos
hídricos do Brasil.


Fonte: Adaptado de ANA (2024).


      A seleção dos modelos mais adequados para representação climática do Brasil, foi realizada
com base em uma análise interna de sensibilidade dos MCGs, avaliados por meio de testes
estatísticos, que subsidiaram a seleção do subconjunto de 5 modelos climáticos (descritos na Tabela
1). Esta avaliação foi incorporada na metodologia de modelagem da ANA (2024), selecionando um
subconjunto de modelos climáticos para a representação da vazão futura. Sendo geralmente este

                                                28
                                                     Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                   Hídricos

## PDF page 29

tipo de abordagem por conjunto uma estratégia de maior preferência nos estudos de mudanças
climáticas (STEINSCHNEIDER et al., 2015).
     Importante salientar que mesmo abordagem seja considerada uma condição necessária, não
implica em confiabilidade absoluta das projeções climáticas realizada por estes modelos (ANA, 2024).
Há pouco consenso na comunidade científica sobre como se deve escolher modelos adequados
(KUNDZEWICZ et al., 2010; BORGOMEO et al., 2018). Desta forma, todo resultado advindo de
projeções climáticas deve ser observado com parcimônia, considerando as incertezas inerentes dos
modelos e outros possíveis vieses das escolhas metodológicas, o que não inviabiliza qualquer análise,
mas requer ressalvas na interpretação dos resultados.

Tabela 1 – Modelos selecionados do conjunto NEX-GDDP-CMIP6 para representação da disponibilidade hídrica
futura.
       Modelo                 Origem
       GFDL-ESM4              Geophysical Fluid Dynamics Laboratory
       INM-CM5                Marchuk Institute of Numerical Mathematics of the Russian
       MPI-ESM1-2-HR          Max Planck Institute for Meteorology
       MRI-ESM2-0             Meteorological Research Institute Japan Meteorolgical Agency
       NorESM2-MM             Norwegian Earth System Model
Fonte: Elaborado por Thales Penha e George Pedra.


     Outra seleção importante oriunda da modelagem foram os recortes temporais e as trajetórias
socioeconômicas e climáticas. Assim, os períodos temporais considerados nesta avaliação foram o
histórico ou baseline (1980-2014), período centrado no horizonte 2030 (intervalo médio de 2015 a
2040) e período centrado no horizonte 2050 (intervalo médio de 2041 a 2070). As trajetórias
socioeconômicas selecionadas, combinadas aos níveis de forçantes radiativas, foram o SSP2-4.5 para
representar um cenário mais otimista (trajetória de mitigação moderada) e o SSP5-8.5 para
representar um cenário mais pessimista (trajetória de altas emissões e aquecimento acentuado).
Definidos estes recortes, o passo seguinte foi reinterpretar as saídas do modelo hidrológico e
representar ao nível municipal (recorte de análise da AdaptaBrasil) para gerar, por fim, o índice de
ameaça de escassez hídrica, detalhado na seção a seguir.


               4.1.3. Representação municipal da escassez hídrica

                                                    29
                                                         Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                             climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                       Hídricos

## PDF page 30

A representação dos resultados da modelagem hidrológico foi realizado em três etapas principais:
(1) representação da vazão no presente; (2) representação da indisponibilidade hídrica (vazão) no
futuro; e (3) transformação dos resultados da modelagem de ottobacias para representação
municipal. Para cada uma das representações, escolhas metodológicas foram adotadas e são
detalhadas a seguir.
       A representação espacial da vazão (disponibilidade hídrica) no presente foi definida com base
no valor médio dos 5 modelos selecionados no ensemble para representar resposta de valor médio
de Qmlt (m³/s) em cada ottobacias e posteriormente calculada a mediana da proporção de cada
ottobacias pertencente a um município (Figura 10). Primeiro este cálculo foi realizado em nível de
ottobacias e posteriormente transformado para municípios, seguindo a metodologia desenvolvida
pela ANA de ponderação pela demanda e proporção de ottobacias no município.


Figura 10 - Padrão espacial da vazão Qmlt (baseline) transformado para município conforme metodologia da
ANA.


Fonte: Elaborado por Thales Penha e George Pedra.

       A representação municipal da indisponibilidade hídrica (vazão) no futuro se deu através de uma
sequência de etapas, uma vez que a saída do modelo de vazão futura corresponde a um valor
percentual (%) de mudança da disponibilidade no presente em relação ao futuro. Assim, posto o
desafio, propôs-se aplicar uma matriz de correspondência entre as classes do presente de vazão e as
classes de vazão no futuro. O método de matriz de correspondência advém da expertise da ANA em
estudos pretéritos, como por exemplo, o Índice de Segurança Hídrica, que utiliza desta abordagem
porque permite adotar notas (avaliação quali-quanti) para reclassificar o dado de vazão (Qmlt) tanto
no presente quanto no futuro. O exemplo a seguir mostra como funciona a matriz de
correspondência (Figura 11), e foi aplicada para cada ottobacias.

                                                    30
                                                         Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                             climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                       Hídricos

## PDF page 31

     Desta forma, a matriz de correspondência demanda que sejam classificados em intervalos tanto
os valores de vazão no presente quanto no futuro. Para classificar o período presente (baseline) foi
utilizada unicamente a primeira coluna visto que não há comparativos, já para os recortes referente
as trajetórias foram utilizadas todas as colunas. Propôs-se aplicar o conhecimento específico da ANA
e estatístico na definição destas classes, fazendo uso da matriz para cada bioma brasileiro (com o
intuito de conservar a representação relativa das vazões em cada região brasileira).


Figura 11 - Valores numéricos de classes de correspondência da vazão Qmlt futura transformado para
município.


Fonte: Elaborado por Thales Penha e George Pedra.


     A definição de limiares críticos para a representação da mudança na vazão no futuro foi
realizada com base no fatiamento em classes com valores fixos de redução de vazão no futuro até
atingir o limiar crítico de 20% para ambas as trajetórias (SSP2 4.5 e SSP5 8.5), uma vez que o intuito
foi identificar situações de escassez hídrica (Tabela 2).


Tabela 2 - Intervalos de classes de mudança de alteração na vazão do futuro.
                                                                         Alteração percentual da vazão no
      Classe                   Nome da classe
                                                                                           futuro
                                 Normalidade
        S0                                                                     valores positivos até 0%
                            (Sem escassez hídrica)
                         Redução Muito Leve da vazão
        S1                                                                                0% - 5%
                                 (Muito leve)


                                                     31
                                                          Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                              climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                        Hídricos

## PDF page 32

                           Redução Leve da vazão
        S2                                                                               5%- 10%
                                   (Leve)
                        Redução Moderada da vazão
        S3                                                                             10% - 15%
                                (Moderada)
                         Redução Intensa da vazão
        S4                                                                               15 - 20%
                                   (Alta)
                         Redução Extrema da vazão
        S5                                                                           acima de 20%
                                (Muito alta)

Fonte: Elaborado por Thales Penha e George Pedra.

     Uma vez aplicada a matriz de correspondência para cada ottobacias em um bioma, extraiu-se
as informações relativas à disponibilidade hídrica no presente e futuro para cada município. Para
cada município, aplicou-se um método de conversão dos valores calculados de disponibilidade
hídrica nas ottobacias para município, detalhado a seguir.
     O método de transformação de valores calculados em ottobacias para municípios é composto
por duas etapas principais: (1) associação de cada ottobacias com o município correspondente,
respeitando a proporção de área de cada ottobacia inserido no município; (2) ponderação do valor
proporcional da ottobacia no município pela demanda hídrica existente na ottobacia.


               4.1.4. Associação da ottobacia com os municípios


A estimativa de áreas dos municípios inseridas em cada ottobacia foi realizada a partir do cruzamento
dos arquivos vetoriais das ottobacias com os limites municipais da Base Cartográfica do IBGE. A
interseção espacial entre as duas camadas, isto é, entre o polígono de ottobacia e o polígono do
município, foi o critério utilizado de pertencimento da proporção de área de uma ottobacia dentro
dos limites municipais (Figura 12). O percentual da ottobacia dentro de cada município foi sempre
considerado nas ponderações e agregações dos indicadores. Assim, para cada ottobacia foram
associados os municípios os quais está contido ou de outra forma, para cada município todas as
ottobacias que cobriam a porção territorial do município.


                                                    32
                                                         Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                             climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                       Hídricos

## PDF page 33

Figura 12 - Ilustração da intersecção das ottobacias inseridas e associadas em um município: Campo Bonito-
PR.


Fonte: Elaborado por Thales Penha.


               4.1.5. Agregação dos valores brutos da ottobacia nos municípios


A partir dos valores associados de cada município com a ottobacia que continha os resultados da
vazão, efetuou-se a agregação município-ottobacia, ponderando cada trecho de ottobacia pela
estimativa proporcional da demanda hídrica em cada ottobacia, fornecido pela ANA. Baseado no
valor de demanda em cada ottobacia associado a uma fração do município, agrega-se os valores
brutos calculados em cada ottobacia associados a proporção de área de cada município, por mediana
ou moda a fim de representar um valor único municipal. Desta forma, respeitando os cálculos
efetuados com maior granulosidade espacial (escala de maior detalhe) nas ottobacias, porém
representando municipalmente as dinâmicas hidrológicas em todo o território.


                                                   33
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 34

       4.2. Risco de estresse hídrico

O Risco de impacto das mudanças climáticas no balanço hídrico dos sistemas socioecológicos em
função do estresse hídrico, ou simplesmente risco de estresse hídrico, se caracteriza quando o
balanço hídrico dos recursos hídricos é deficitário, isto significa que o saldo de oferta e demanda da
água em uma determinada localidade é negativo, ou seja, o uso humano da água excede o volume
de água disponível, sendo incapaz de oferecer uma segurança hídrica para os diversos usos da água,
inclusive, o abastecimento humano. O Risco de estresse hídrico é resultante da interação entre as
três dimensões (Ameaça, Vulnerabilidade e Exposição), considerando a Ameaça como o saldo
negativo de vazão (indisponibilidade hídrica) nas bacias hidrográficas, oriundo da modelagem
hidrológica com cenários climáticos projetados relacionados ao déficit hídrico (interação das
características biofísicas, precipitação e evapotranspiração potencial), que configura o risco
relacionado à escassez hídrica, conforme detalhado na seção anterior. A componente de
Vulnerabilidade, por sua vez, explicita as características do sistema socioecológico propensas a sofrer
dano; e a Exposição, explicita os elementos em superfície diretamente impactados, como, por
exemplo, os usuários dos recursos hídricos.
     Considera-se, portanto, nesta avaliação o estresse hídrico como situações que o sistema
socioecológico é impactado pelas alterações no regime de vazões em bacias hidrográficas, em função
do déficit hídrico provocado pela diminuição abrupta ou prolongada de precipitação por um período
— uma estação, um ano ou vários anos — em comparação com a média multianual estatística para
uma região que resulta em escassez de água para alguma atividade, grupo ou setor ambiental e que
tornam o saldo de oferta/demanda pelos recursos hídricos no território deficitário. O estresse hídrico
resulta em perdas econômicas e sociais significativas para diversos setores, desde a agricultura,
abastecimento humano, indústrias, energia ao turismo, provocando efeitos profundos nas
comunidades locais. Déficits mais frequentes implicarão em aumento de custos para a sociedade,
necessitando de estratégias de adaptação por parte dos usuários de água (ANA, 2024).
     Nesta seção, para fins didáticos, a metodologia de obtenção dos dados de vulnerabilidade e
exposição e cálculo hierárquico de valores até a obtenção do risco de estresse hídrico foi dividida em
quatro etapas: (4.2.1) Identificação e pré-seleção dos indicadores candidatos; (4.2.2) Construção
numérica e seleção dos indicadores; (4.2.3) Cálculo dos indicadores, índices parciais e final; e (4.2.4)
                                                  34
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 35

Cálculo dos fatores influenciadores. As fases de identificação e construção numérica de indicadores
simples e temáticos e de índices segues vários preceitos metodológicos de composição de
indicadores e índices de Becker et al. (2019) e OCDE (2008).


               4.2.1. Identificação e pré-seleção dos indicadores candidatos


Inicialmente, foi realizado um levantamento de indicadores candidatos a partir de estudos científicos
já realizados para o Brasil, apoiados em artigos e publicações técnicas que contemplasse as exigências
teóricas e operacionais referentes aos aspectos de vulnerabilidade, impacto e adaptação associados
ao tema. Todavia, observou-se alguns requisitos mínimos de ordem técnica: (1) dados disponíveis em
fontes oficiais e públicos; (2) representatividade em escala municipal (preferencialmente) e (3) escala
temporal passível atualização.
     A pré-seleção dos indicadores para o SE Recursos Hídricos foi realizada em oficinas com atores
chave entre setembro e dezembro de 2023, com a participação de representantes do Ministério da
Ciência, Tecnologia e Inovação (MCTI), do Instituto Nacional de Pesquisas Espaciais (INPE) e da
Agência Nacional de Águas e Saneamento Básico (ANA). Nesse período um total de 2 reuniões e 3
workshops foram realizados de modo a selecionar os indicadores mais adequados para compor o
setor de recursos hídricos. Nas referidas ocasiões, os especialistas foram convidados a contribuir com
a seleção e a alocação mais adequada dos indicadores nas respectivas dimensões, levando em
consideração a caracterização do setor estratégico analisado e a relevância nacional e/ou regional
dos mesmos.
     O sistema de índices e indicadores utilizado para a avaliação do risco em recursos hídricos, pela
própria característica multidisciplinar do impacto, não somente equaciona as forçantes relacionadas
ao clima, mas inclui nas análises fatores socioecológicos pertinentes. Desta forma, temáticas
relacionadas ao abastecimento humano, a eficiência de uso da água, o balanço hídrico relacionado a
atividades produtivas dependentes do uso da água, fatores de degradação ambiental, da qualidade
da água, da capacidade de armazenamento de água, bem como, políticas e gestão para recursos
hídricos e perfil de renda da população foram contemplados pelo universo de indicadores elencados.

     O banco de dados construído reuniu informações provenientes de fontes secundárias, extraídas
de bases institucionais consolidadas. Para cada variável considerada, foi realizada uma análise
                                                  35
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 36

rigorosa da qualidade e da consistência dos dados disponíveis, assegurando a confiabilidade das
informações utilizadas. Como resultado, o banco passou a integrar conteúdos quantitativos e
qualitativos robustos, aptos a sustentar uma avaliação técnica precisa e detalhada. Essa base sólida
de dados constitui um pilar essencial para o desenvolvimento das etapas subsequentes do estudo.

Entre as principais instituições consultadas estão:

           •   Agência Nacional de Águas (ANA);

           •   Instituto Brasileiro de Geografia e Estatística (IBGE);

           •   Instituto Nacional de Pesquisas Espaciais (INPE);

           •   Empresa Brasileira de Pesquisa Agropecuária - Solos (Embrapa Solos);

           •   Sistema Nacional de Informações sobre Saneamento (SNIS)/Ministério das Cidades;

           •   Portal de informações sobre Saúde (DATASUS)/Ministério da Saúde

           •   Secretaria Nacional de Proteção e Defesa Civíl (SEDEC)/Ministério da Integração e do
               Desenvolvimento Regional

           •   Laboratório de Processamento de Imagens e Geoprocessamento/Universidade
               Federal de Goiás (Lapig/UFG);

           •   Portal da Transparência da Controladoria-Geral da União (CGU)

           •   Administração Nacional da Aeronáutica e Espaço dos Estados Unidos (NASA).


               4.2.2. Construção numérica e seleção dos indicadores


A construção numérica dos indicadores simples, que compõem as dimensões de vulnerabilidade e
exposição, seguiu os procedimentos metodológicos representados na Figura 13.


                                                   36
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 37

Figura 13 – Fluxograma das etapas de construção numérica e seleção dos indicadores simples do SE Recursos Hídricos.


Fonte: Elaborado por Naurinete Barreto.
                                                                                   37
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                                                                                       Hídricos

## PDF page 38

     A geração dos indicadores simples obedece a um protocolo sistemático de transformações
numéricas aplicadas aos dados brutos de entrada. Esses dados são classificados em duas categorias:
dados discretos (identificados como scores) e dados contínuos (numéricos).
     No caso dos dados discretos, os valores são diretamente atribuídos com base em limites
definidos para cada indicador, geralmente variando entre um mínimo e um máximo — comumente
0 e 1, respectivamente. No entanto, esses limites podem ser ajustados conforme a lógica de
associação entre o desempenho do indicador e o tema ou dimensão a que pertence. Por exemplo,
podem ser utilizados limiares como 0,3 para o valor mínimo e 0,7 para o valor máximo. Nesses casos,
o indicador simples recebe esses valores diretamente, sem a necessidade de outras transformações
numéricas.
     Os dados numéricos passaram por etapas sucessivas de verificação de outliers, aplicação de
winsorização total (quando necessário) e avaliação de curtose e distorção. Quando identificadas
distorções, aplica-se a transformação Box-Cox antes da normalização final. Esse fluxo metodológico
assegura a consistência estatística e a comparabilidade entre os indicadores utilizados na composição
das dimensões de análise. Os critérios individuais de aplicação de cada etapa serão explicados abaixo.


       a) Identificação e tratamento de valores outliers


     O cálculo dos indicadores em cada subsetor passa por um tratamento inicial que verifica a
presença de outliers nos dados, ou seja, valores que se encontram fora do padrão normal de uma
distribuição (SMITI, 2020). A existência de valores extremos em uma variável pode comprometer a
precisão dos procedimentos estatísticos, causar perda de informações relevantes ou até distorcer o
resultado final.
     O método consiste na substituição dos valores extremos pelos valores válidos mais próximos
dentro dos limites definidos pelo intervalo interquartil (IQR). Ele é recomendado principalmente
quando os outliers correspondem a uma pequena proporção do total de observações —
aproximadamente até 5% das unidades.
     A identificação de outliers foi realizada com base no método do intervalo interquartil (IQR), uma
técnica robusta e amplamente utilizada em análises estatísticas. As fórmulas aplicadas foram as
seguintes:
                                                 38
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 39

                                        𝐼𝑄𝑅 = 𝑄3 − 𝑄1
 𝐿𝑖𝑚𝑖𝑛𝑓 = 𝑄1 − 1,5 ∗ 𝐼𝑄𝑅                                 𝑄1 = 𝑃𝐸𝑅𝐶𝐸𝑁𝑇𝐼𝐿(𝑋1 : 𝑋𝑛 ; 0,25)
 𝐿𝑖𝑚𝑠𝑢𝑝 = 𝑄3 + 1,5 ∗ 𝐼𝑄𝑅                                 𝑄3 = 𝑃𝐸𝑅𝐶𝐸𝑁𝑇𝐼𝐿(𝑋1 : 𝑋𝑛 ; 0,75)


Onde: IQR é o valor do intervalo interquartil; 𝐿𝑖𝑚𝑖𝑛𝑓 é o valor do limite inferior para identificação de
outliers; 𝐿𝑖𝑚𝑠𝑢𝑝 é o valor do limite superior para identificação de outliers; Q1 é o valor médio do
primeiro quartil; Q3 é o valor médio do terceiro quartil; 𝑋1 é o valor da variável X no primeiro
município da série; 𝑋𝑛 é o valor da variável X no último município da série.

     Valores que ultrapassam esses limites são classificados como outliers estatísticos e, portanto,
passíveis de tratamento. Neste processo foi utilizada a técnica de Winsorization, onde valores
situados acima do limite superior do intervalo interquartil (IQR) foram ajustados para o próprio valor
deste limite. Da mesma forma, valores que se encontram abaixo do limite inferior do IQR foram
redefinidos para o limite inferior correspondente. Assim:

                            𝐼𝑗𝑝 = 𝐿𝑖𝑚𝑠𝑢𝑝          e        𝐼𝑗𝑚 = 𝐿𝑖𝑚𝑖𝑛𝑓

     Este procedimento garante um tratamento criterioso de valores atípicos, equilibrando a
preservação da informação original com a necessidade de manter a robustez e a confiabilidade dos
indicadores utilizados nas análises.
     A aplicação desse método mostrou-se adequada ao contexto, dado que as séries de dados
associadas a cada subsetor frequentemente apresentam distribuições não normais, refletindo a
variabilidade inerente a fatores climáticos, econômicos e sociais.


       b) Avaliação de curtose e distorção dos dados e aplicação do Box-Cox


A avaliação da distribuição dos dados é uma etapa fundamental para garantir a consistência
estatística dos indicadores utilizados, especialmente em processos que envolvem normalização e
combinação de variáveis. Nesse contexto, foram analisadas duas medidas descritivas essenciais:

                                                  39
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 40

distorção (ou assimetria) e curtose, que permitem avaliar a forma da distribuição dos dados em
relação à distribuição normal.
     A distorção mede o grau de simetria da distribuição de uma variável em torno de sua média.
Uma distribuição perfeitamente simétrica apresenta valor de assimetria igual a zero. Valores
positivos indicam que a cauda da distribuição está deslocada para a direita (assimetria positiva),
enquanto valores negativos indicam deslocamento para a esquerda (assimetria negativa).
Assimetrias acentuadas podem comprometer a interpretação e a robustez de análises estatísticas
baseadas em pressupostos de normalidade, além de indicar concentração de valores em um dos
extremos da série.
     A curtose, por sua vez, está relacionada à altura e à forma da curva da distribuição. Quando
uma distribuição possui uma aparência semelhante à da distribuição normal, diz-se que ela tem uma
curtose padrão (valor igual a 3). Valores superiores a 3,5 indicam distribuições com curvatura muito
alongada e maior concentração de valores extremos nas caudas (leptocúrticas), enquanto valores
inferiores podem indicar distribuições mais achatadas (platicúrticas). Curtoses elevadas sugerem
variabilidade atípica que pode influenciar desproporcionalmente os resultados e obscurecer padrões
relevantes.
     Além dessas medidas, a presença de outliers tem papel importante na decisão de transformar
os dados. A transformação Box-Cox é especialmente indicada quando a distribuição apresenta forte
assimetria, caudas pesadas e elevada proporção de valores extremos. Isso porque os outliers, quando
numerosos, afetam significativamente a média e a variância, prejudicando análises que dependem
desses parâmetros. Nessas situações, técnicas simples como a Winsorization podem não ser
suficientes para corrigir as distorções da distribuição, sendo necessário aplicar uma transformação
mais abrangente, como a Box-Cox, que suaviza o impacto dos valores extremos e melhora a
aproximação da distribuição à normalidade.
     A aplicação da transformação Box-Cox é realizada nos dados brutos (Nível 6), considerando
alguns critérios presentes nos dados que já passaram por winsorization:


     •   A proporção de outliers deve ser superior a 5%, indicando que o simples tratamento por
         Winsorization não seria suficiente para estabilizar a distribuição;


                                                  40
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 41

     •    O valor de distorção deve estar acima de 2 e valor de curtose deve ser superior a 3,5,
          evidenciando uma distribuição inclinada e sinalizando a presença de caudas extremas,
          respectivamente.


     Indicadores que atendem o primeiro ou o segundo critério são submetidos à transformação
Box-Cox, com o objetivo de melhorar a aderência à normalidade e aumentar a comparabilidade entre
variáveis. Esse procedimento contribuiu significativamente para a homogeneização do banco de
dados e para a confiabilidade das análises posteriores.


         c) Normalização dos dados


Para garantir a consistência e a comparabilidade dos dados, aplica-se a normalização, transformando-
as em uma escala que varia entre zero e um. Este procedimento faz parte do processo de composição
de indicadores, pois gera uma unidade comum (adimensional) e uma escala de valores comum. Isso
facilita a comunicação, a comparação e a composição de diferentes indicadores, possibilitando a
construção de uma hierarquia de classes de risco de impacto para os municípios estudados. Assim,
valores mais próximos de zero indicam situações de menor risco, enquanto valores mais próximos de
um representam condições mais críticas, conforme a metodologia adaptada de Lima et al. (2009).
     Nesta perspectiva, para a normalização das variáveis selecionadas utilizou-se a seguinte
expressão matemática, quando o indicador tem relação direta com a dimensão a que pertence:


                                                 𝐼𝑎𝑖 − 𝐼𝑗𝑚
                                         𝐼𝑗𝑖 =
                                                 𝐼𝑗𝑝 − 𝐼𝑗𝑚


Onde: 𝐼𝑗𝑖 é o valor padronizado do indicador j no i-ésimo município; 𝐼𝑎𝑖 é o valor do indicador no i-
ésimo município; 𝐼𝑗𝑝 representa o valor do indicador j no município em pior situação; 𝐼𝑗𝑚 é o valor do
indicador j no município em melhor situação.
     Em algumas situações, o indicador pode apresentar uma relação inversa com a dimensão que
ele representa, ou seja, valores mais elevados podem reduzir o valor final do índice ou indicador

                                                 41
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 42

temático. Nesses casos, é necessário realizar um ajuste nos dados normalizados para garantir que
eles estejam alinhados com a respectiva dimensão de risco climático. Esse ajuste visa facilitar a
interpretação do indicador, de modo que os maiores valores sempre reflitam um aumento no risco
da dimensão à qual o indicador está associado, tornando a leitura mais intuitiva e coerente.


       d) Análise de correlação dos indicadores candidatos


A análise de correlação entre os indicadores candidatos teve como objetivo identificar possíveis
redundâncias e aprimorar a qualidade e parcimônia do conjunto final de variáveis. Após a construção
e normalização do banco de dados preliminar, foi aplicada a correlação de Spearman entre os pares
de indicadores, a fim de detectar sobreposições informacionais. Coeficientes de correlação iguais ou
superiores a 0,6 foram considerados indicativos de alta correlação, sinalizando potenciais
redundâncias e, portanto, a necessidade de análise para possível exclusão (BECKER et al., 2019).
     A seleção dos indicadores a serem excluídos foi orientada por três critérios hierárquicos e
objetivos, com o intuito de preservar tanto a representatividade temática quanto a integridade das
dimensões analíticas?

     • Critério 1: avaliação da correlação entre indicadores entre diferentes dimensões, buscando
     eliminar redundâncias internas sem comprometer a coerência conceitual do grupo;

     • Critério 2: avaliação da correlação entre indicadores pertencentes a um mesmo grupo
     temático, buscando eliminar redundâncias internas sem comprometer a coerência conceitual
     do grupo;

     • Critério 3: avaliação da totalidade da hierarquia de indicadores, permitindo a exclusão de
     variáveis com menor relevância relativa na estrutura geral do modelo.

     Como resultado desse processo de filtragem cuidadoso e técnico, apenas um número restrito
de indicadores foi excluído, garantindo a robustez e a consistência do modelo analítico.
     A lista final dos indicadores selecionados, organizados por subsetor, encontra-se detalhada no
Apêndice A.


                                                 42
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 43

       e)      Elaboração do indicador simples


Os indicadores simples foram calculados diretamente a partir dos dados brutos, utilizando os
procedimentos estabelecidos, ilustrados na Figura 12. A composição hierárquica final pode ser
observada Apêndice A.
     Os indicadores simples, após devidamente ajustados e harmonizados em escala municipal,
tornam-se os insumos fundamentais para a construção dos demais níveis hierárquicos. A próxima
etapa envolve a agregação estruturada desses indicadores simples dentro de seus respectivos grupos
temáticos, respeitando a lógica hierárquica do modelo conceitual adotado, de modo a permitir o
cálculo coerente dos índices parciais, índices de vulnerabilidade e exposição e, por fim, do índice final
de risco de impacto.


               4.2.3. Cálculo dos demais níveis hierárquicos


No SE de Recursos Hídricos no AdaptaBrasil 2.0, adotou-se uma estrutura hierárquica composta por
cinco níveis ou por quatro níveis principais, além dos indicadores simples: a) Indicadores temáticos
(nível 5), que agrupam indicadores simples segundo temas específicos (nível 4); b) Índices parciais de
vulnerabilidade, representados pelos componentes de Sensibilidade e Capacidade Adaptativa, que
refletem dimensões complementares da vulnerabilidade (nível 3); c) Índices das dimensões do risco,
que integram os índices de vulnerabilidade e de exposição (nível 2); d) E, por fim, o Índice de Risco
de Impacto Final, que consolida todas as dimensões anteriores, oferecendo uma visão integrada do
risco climático enfrentado pelos municípios (nível 1)             .

     A principal finalidade dessa estrutura é facilitar a análise e a gestão de fenômenos complexos,
sintetizando grandes volumes de dados em métricas agregadas. Esse processo de simplificação,
realizado por meio de métodos estatísticos e técnicas específicas de agregação, é essencial para
apoiar decisões estratégicas, sobretudo em contextos marcados por vulnerabilidades sociais e riscos
climáticos.

     A construção dos indicadores temáticos e dos índices nos níveis superiores seguiu os
procedimentos metodológicos ilustrados na Figura 14.

                                                   43
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 44

     A seguir, são descritas as etapas e critérios adotados no cálculo de cada nível hierárquico, com
exceção dos indicadores simples, já tratados no item 4.2.2. Cada etapa foi cuidadosamente planejada
para assegurar coerência metodológica, consistência estatística e aderência temática ao contexto do
risco climático analisado.

Figura 14 – Fluxograma das etapas de construção dos indicadores temáticos e índices dos níveis superiores
do SE Recursos Hídricos.


Fonte: Elaborado por Karine Rocha.


                                                  44
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 45

     a) Indicadores temáticos

Os indicadores temáticos foram construídos a partir da mediana dos valores dos indicadores simples
que os compõem. Esse procedimento foi adotado para assegurar que os valores representassem de
forma robusta o comportamento central dos dados, minimizando a influência de valores extremos.
A utilização da mediana, em vez da média, é especialmente útil em contextos em que os dados
podem apresentar distribuições assimétricas ou serem sensíveis a valores extremos.
     O cálculo da mediana foi realizado conforme a expressão abaixo, e cada indicador temático
reflete, assim, uma agregação dos indicadores simples que compõem sua categoria temática,
proporcionando uma visão mais consolidada e representativa das condições de risco climático.


                                      𝐼𝑇𝑗𝑖 = 𝑀𝐸𝐷 (𝐼𝑗𝑖 , … , 𝐼𝑛𝑖 )


Onde: 𝐼𝑇𝑗𝑖 é o indicador temático j do i-ésimo município; 𝐼𝑗𝑖 é o indicador simples j do i-ésimo
município; 𝐼𝑛𝑖 é o indicador simples n do i-ésimo município.


Após o cálculo dos indicadores temáticos, é realizada uma análise dos seus valores máximos e
mínimos. Quando os dados se apresentam concentrados em uma faixa intermediária — isto é,
quando o valor mínimo é superior a 0,1 e/ou o valor máximo inferior a 0,9 —, aplica-se uma
transformação adicional com o objetivo de ajustar o gradiente de variação e garantir maior contraste
e sensibilidade do indicador.
     Essa transformação teve como base a normalização linear, que buscou expandir ou deslocar os
valores para os extremos desejados (≤ 0,1 e ≥ 0,9). Para isso, foram calculados dois coeficientes para
ajuste de cada situação – Tabela 3.


                                                  45
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 46

Tabela 3 – Cálculo dos coeficientes de inclinação (a) e deslocamento (b) para normalização dos valores de
indicadores temáticos.

                                                                                   Ajuste dos valores mínimos
   Ajuste dos valores mínimos        Ajuste dos valores máximos
                                                                                   e máximos
                                             Coeficiente a

               (𝐼𝑇𝑗𝑚 − 0,1)                        (0,9 − 𝐼𝑇𝑗𝑝 )                                  (0,1 − 0,9)
          𝑎=                                 𝑎=                                            𝑎=
               (𝐼𝑇𝑗𝑚 − 𝐼𝑇𝑗𝑝 )                     (𝐼𝑇𝑗𝑚 − 𝐼𝑇𝑗𝑝 )                                 (𝐼𝑇𝑗𝑝 − 𝐼𝑇𝑗𝑚 )

                                             Coeficiente b


       𝑏 = 0,1 − (𝐼𝑇𝑗𝑝 𝑥 𝑎)                𝑏 = 0,9 − (𝐼𝑇𝑗𝑚 𝑥 𝑎)                         𝑏 = 0,9 − (𝐼𝑇𝑗𝑚 𝑥 𝑎)

Onde: a é o coeficiente de inclinação da reta; b é o coeficiente de deslocamento da reta; 𝐼𝑇𝑗𝑖 é o
indicador temático j do i-ésimo município; 𝐼𝑇𝑗𝑚 é o valor máximo do indicador temático j; 𝐼𝑇𝑗𝑝 é o
valor mínimo do indicador temático j.
Fonte: Elaborado por Karine Rocha.


Com esses parâmetros, o valor ajustado do indicador temático foi então obtido pela fórmula:

                                   𝐼𝑇𝑎𝑗𝑢𝑠𝑡 = (𝐼𝑇𝑗𝑖 𝑥 𝑎) + 𝑏
Onde: 𝐼𝑇𝑎𝑗𝑢𝑠𝑡 é o valor ajustado do indicador temático j no i-ésimo município.


     b)         Índices parciais de vulnerabilidade


Os índices parciais da dimensão vulnerabilidade, definidos como sensibilidade (IS) e capacidade
adaptativa (ICA), foram calculados a partir da mediana dos valores dos indicadores temáticos que os
compõem, conforme equação abaixo. A escolha da mediana para a agregação dos indicadores
temáticos foi feita para garantir maior robustez frente à presença de dados extremos e para refletir
de maneira mais fiel o comportamento central das variáveis de interesse.


                                    𝐼𝑃𝑗𝑖 = 𝑀𝐸𝐷 (𝐼𝑇𝑗𝑖 , … , 𝐼𝑇𝑛𝑖 )
                                                   46
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 47

Onde: 𝐼𝑃𝑗𝑖 é o índice parcial j do i-ésimo município, considerando j como índice de sensibilidade (IS)
ou índice de capacidade adaptativa (ICA); 𝐼𝑇𝑗𝑖 é o indicador temático j do i-ésimo município; Ini é o
indicador temático n do i-ésimo município.
     Após a obtenção dos valores de IS e ICA, foi aplicado um procedimento de reescalonamento
por normalização linear simples, ajustando os valores mínimos e máximos para 0 e 1,
respectivamente. Essa etapa visa padronizar os índices parciais em uma mesma escala, facilitando a
comparação entre municípios e garantindo coerência nas etapas subsequentes de integração dos
componentes da vulnerabilidade.
     Esse método de construção assegura que as características específicas de cada subsetor
temático sejam representadas de forma proporcional e consistente. Assim, os índices parciais
sintetizam de maneira clara e objetiva as dimensões fundamentais da vulnerabilidade, fornecendo
subsídios essenciais para a análise da resiliência dos sistemas socioambientais avaliados.


     c) Índices das dimensões do risco


Os índices de dimensão – vulnerabilidade (IV), exposição (IE) e ameaça climática (IAC) - foram
calculados de forma independente e diferenciada entre si. A vulnerabilidade (IV) está em função da
sensibilidade (IS) e capacidade adaptativa (ICA) e foi obtida conforme expressões abaixo:


                                             1 + (𝐼𝑆𝑗𝑖 − 𝐼𝐶𝐴𝑗𝑖 )
                                     𝐼𝑉𝑖 =
                                                     2

Onde: 𝐼𝑉𝑖 é o índice de vulnerabilidade do i-ésimo município; 𝐼𝑆𝑗𝑖 é o índice de sensibilidade do i-ésimo
município; 𝐼𝐶𝐴𝑗𝑖 é o índice de capacidade adaptativa do i-ésimo município.


A exposição (IE) foi obtida pelo cálculo dos valores médios de seus indicadores temáticos
componentes, conforme expressão abaixo:


                                                   47
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 48

                                    𝐼𝐸𝑖 = 𝑀𝐸𝐷 (𝐼𝑇𝑗𝑖 , … , 𝐼𝑇𝑛𝑖 )


Onde: 𝐼𝐸𝑖 é o índice de exposição do i-ésimo município; 𝐼𝑇𝑗𝑖 é o indicador temático j do i-ésimo
município; 𝐼𝑇𝑛𝑖 é o indicador temático n do i-ésimo município.


     d) Índice de risco de impacto final

O Índice de Risco de Impacto (𝐼𝑅𝐼𝑖 ) foi construído com base em uma estrutura dinâmica que integra
as dimensões de exposição (𝐼𝐸), vulnerabilidade (𝐼𝑉) e ameaça climática (𝐼𝐴𝐶). Essa abordagem
permite representar de forma mais realista os possíveis impactos associados a eventos climáticos,
considerando simultaneamente a suscetibilidade dos sistemas analisados, sua capacidade de
resposta e a intensidade das ameaças envolvidas.
     A construção do IRI foi realizada por meio da multiplicação direta dos valores normalizados de
suas três dimensões componentes, conforme expressa a seguinte equação:


                                    𝐼𝑅𝐼𝑖 = (𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 )


Onde: 𝐼𝑅𝐼𝑖 é o índice de risco de impacto do i-ésimo município; 𝐼𝑉𝑖 é o índice de vulnerabilidade do
i-ésimo município; 𝐼𝐸𝑖 é o índice de exposição do i-ésimo município; 𝐼𝐴𝐶𝑗𝑖 é o índice de ameaça
climática j do i-ésimo município.


     Essa formulação multiplicativa foi adotada por refletir, de forma mais fiel, a interdependência
entre as dimensões que compõem o risco. Isso significa que o risco de impacto não é resultado
isolado de uma única dimensão, mas sim da combinação entre vulnerabilidade, exposição e ameaça
climática. Por exemplo, mesmo em contextos de alta exposição, o risco pode ser relativamente baixo
se a vulnerabilidade for reduzida ou se a intensidade da ameaça climática for limitada. Da mesma
forma, uma elevada vulnerabilidade associada a uma ameaça significativa pode gerar alto risco,
mesmo em situações de exposição moderada. Assim, a abordagem multiplicativa permite capturar


                                                48
                                                     Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                   Hídricos

## PDF page 49

essas interações, evitando superestimações ou subestimações que poderiam ocorrer em modelos
aditivos.

     Após o cálculo do 𝐼𝑅𝐼 para cada município, foi aplicada uma normalização linear simples,
realizada separadamente para cada cenário e período de análise. Essa etapa considerou como
referência os valores mínimo e máximo do período presente, reescalonando os resultados para a
faixa compreendida entre 0 e 1. O objetivo desse procedimento foi garantir a comparabilidade dos
valores ao longo do tempo, além de evidenciar de forma proporcional os incrementos ou reduções
projetadas para os cenários futuros.


     4.3.        Cálculo dos fatores influenciadores


Na versão AdaptaBrasil 2.0, o "fator influenciador" foi revisado quanto a sua metodologia, tornando
as análises mais precisas e adaptadas às crescentes demandas por dados complexos e integrados.
Esse fator descreve a contribuição percentual dos indicadores simples na formação de um índice
selecionado.
     O cálculo desse fator é realizado a partir da decomposição logarítmica como fator de
escalonamento de cada componente dentro de um sistema hierárquico, procedimento essencial em
contextos em que indicadores afetam o índice agregado de maneira desigual (WANG; ANG; BIN SU,
2017). O AdaptaBrasil ajustou essa técnica para calcular a contribuição proporcional dos indicadores
simples em diferentes níveis, permitindo uma análise detalhada do impacto de cada fator nos índices
agregados.


            4.3.1. Cálculo da contribuição dos indicadores simples aos Índices de Risco de Impacto
                  (Nível 1 para Nível 5)


Para garantir que os indicadores simples reflitam corretamente suas contribuições para o valor final
do risco normalizado, foram necessárias 5 etapas: 1) Cálculo das contribuições “brutas” das
dimensões para o risco final; 2) Cálculo do fator de escalonamento ou de ajuste da normalização; 3)
Cálculo das contribuições ajustadas das dimensões para o risco final; 4) Cálculo das contribuições

                                                 49
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 50

“brutas” dos indicadores simples para o risco final; e 5) Cálculo das contribuições “ajustadas” dos
indicadores simples para o risco final.


ETAPA 1: Cálculo das contribuições “brutas” das dimensões para o risco final


Considerando que o índice de risco (𝐼𝑅𝐼𝑖 ) é obtido por uma função multiplicativa das suas dimensões
(𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 ) (ver Nível 5 – Índice final), o cálculo das contribuições proporcionais de cada
dimensão para o risco deve utilizar uma transformação logarítmica. Esta tem a propriedade de
converter multiplicações em somas, o que simplifica a análise de como cada variável contribui para
o valor total do risco. Ao aplicar o logaritmo natural (𝑙𝑛) em ambos os lados da equação multiplicativa
do risco, temos:


                                ln (𝐼𝑅𝐼𝑖 ) = 𝑙𝑛(𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 )


Pela propriedade dos logaritmos:


                          ln(𝐼𝑅𝐼𝑖 ) = ln(𝐼𝑉𝑖 ) + ln (𝐼𝐸𝑖 ) + ln (𝐼𝐴𝐶𝑗𝑖 )


Essa fórmula permite que as contribuições relativas de V, E, e A sejam avaliadas separadamente,
facilitando a decomposição logarítmica das dimensões. Em vez de calcular diretamente a
multiplicação dos valores brutos, os valores logarítmicos individuais são somados, fornecendo uma
maneira prática de calcular a elasticidade parcial de cada dimensão em relação ao risco total.


Em seguida, foi possível calcular as contribuições relativas de cada dimensão ao índice bruto,
utilizando as fórmulas:


   ● Contribuição da vulnerabilidade C (𝐼𝑉𝑖 ):
                                                      ln(𝐼𝑉𝑖 )
                                    C (𝐼𝑉𝑖 ) =
                                                 ln (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))

                                                  50
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 51

   ● Contribuição da vulnerabilidade C (𝐼𝐸𝑖 ):
                                                      ln(𝐼𝐸𝑖 )
                                    C (𝐼𝐸𝑖 ) =
                                                 ln (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))


   ● Contribuição da vulnerabilidade C (𝐼𝐴𝐶𝑗𝑖 ):

                                                      ln(𝐼𝐴𝐶𝑗𝑖 )
                                   C (𝐼𝐴𝐶𝑗𝑖 ) =
                                                  ln (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))


É importante destacar que a aplicação do logaritmo natural (𝑙𝑛) às dimensões do risco
(vulnerabilidade, exposição e ameaça climática) deve ser realizada antes da normalização do índice
final de risco, ou seja, no valor do índice de risco bruto (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 ). Isso ocorre porque a transformação
logarítmica é mais eficaz quando aplicada aos valores brutos, permitindo que as contribuições
relativas de cada dimensão sejam calculadas com precisão.
     No entanto, após a normalização do índice, o valor do risco é ajustado para se enquadrar em
uma escala predeterminada utilizada no AdaptaBrasil (valores entre 0 a 1). Esse processo de
normalização altera a magnitude do índice, o que torna necessário o uso de um fator de
escalonamento.


ETAPA 2: Cálculo do fator de escalonamento ou de ajuste da normalização


O fator de escalamento é uma técnica utilizada para ajustar a magnitude das contribuições individuais
das dimensões para garantir que o somatório dessas contribuições esteja alinhado com o valor final
do risco (após a normalização). Seu uso é especialmente importante quando os valores das
contribuições não somam ao valor esperado ou apresentam variações indesejadas.
     O fator de escalamento funciona como uma constante multiplicativa que é aplicada a cada
contribuição individual das dimensões, de modo que o somatório final das contribuições seja
proporcional ao valor do desejado.
     A fórmula básica do fator de escalamento é dada por:


                                                   51
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 52

                                              𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)
                                    F (t) =
                                                 𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡)


Onde: F (t) é o é o fator de escalamento no tempo 𝑡 no i-ésimo município; 𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (t) é o valor
do índice de risco no tempo 𝑡 do i-ésimo município após a normalização; 𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (t) é o valor do
índice de risco no tempo 𝑡 do i-ésimo município antes da normalização.


ETAPA 3: Cálculo das contribuições ajustadas das dimensões para o risco final


Após a normalização, o valor do risco é ajustado para ficar entre 0 e 1, mas a relação entre as
dimensões não se altera de forma direta. Para ajustar as contribuições de forma adequada, levando
em conta o efeito da normalização com limites, você pode usar o seguinte método:


   ● Contribuição da vulnerabilidade C′ (𝐼𝑉𝑖 ):


                                     C ′ (𝐼𝑉𝑖 ) = 𝐹(𝑡) 𝑥 𝐶(𝐼𝑉𝑖 )


   ● Contribuição da vulnerabilidade C′ (𝐼𝐸𝑖 ):


                                     C ′ (𝐼𝐸𝑖 ) = 𝐹(𝑡) 𝑥 𝐶(𝐼𝐸𝑖 )


   ● Contribuição da vulnerabilidade C′ (𝐼𝐴𝐶𝑗𝑖 ):


                                   C ′ (𝐼𝐴𝐶𝑗𝑖 ) = 𝐹 (𝑡) 𝑥 𝐶(𝐼𝐴𝐶𝑗𝑖 )


Onde: C’X(t) é a contribuição ajustada da dimensão X (IV, IE ou IAC) no valor do risco final no tempo
t, ou seja, após a normalização.


ETAPA 4: Cálculo das contribuições “brutas” dos indicadores simples para o risco final

                                                    52
                                                         Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                             climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                       Hídricos

## PDF page 53

Para calcular as contribuições dos indicadores simples ao risco, é essencial considerar toda a cadeia
de agregação, que começa nos indicadores temáticos e culmina no risco total (Ver figuras 7 e 8). O
processo está relacionado à compreensão que cada indicador simples exerce uma influência indireta
sobre o risco e que cadeia de agregação assegura que o impacto de cada indicador simples seja
avaliado não isoladamente, mas dentro do contexto de suas interações e contribuições ao sistema
como um todo.
     Nesse contexto, a contribuição bruta de cada indicador simples no valor final do risco é
condicionada pelas variações nas contribuições de suas respectivas dimensões (vulnerabilidade,
exposição e ameaça). Isso significa que o valor de um indicador simples pode ser amplificado ou
reduzido conforme as características de suas dimensões agregadoras. Assim, o impacto de cada
indicador simples no risco final não é direto, mas moderado pelo comportamento e peso relativo das
subdimensões e dimensões intermediárias dentro do modelo hierárquico.
     A fórmula utilizada para “estimar” esse efeito indireto é dada por:


   ● Contribuição dos indicadores simples relacionados à sensibilidade (𝐶𝐼𝑆𝑠 ) e à capacidade
       adaptativa (𝐶𝐼𝑆𝑐𝑎 ) - dimensão de vulnerabilidade:


                                                𝐼𝑆𝑠
                              𝐶𝐼𝑆𝑠 =                               ∗ C ′ (𝐼𝑉𝑖 )
                                       𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)


                                             1 − 𝐼𝑆𝑐𝑎
                             𝐶𝐼𝑆𝑐𝑎 =                                ∗ C ′ (𝐼𝑉𝑖 )
                                        𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)


   ● Contribuição dos indicadores simples relacionados à dimensão de exposição (𝐶𝐼𝑆𝑒 ):
                                                𝐼𝑆𝑒
                              𝐶𝐼𝑆𝑒 =                               ∗ C ′ (𝐼𝐸𝑖 )
                                       𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)


Onde: 𝐶𝐼𝑆𝑋 é a contribuição bruta do indicador simples x (s ou ca) no valor do risco final no tempo t,
ou seja, após a normalização; ISx é o valor do indicador simples x (s, ca ou e); IRInormalizado (t) é o

                                                  53
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 54

valor do índice de risco no tempo t do i-ésimo município após a normalização; C’X(t) é a contribuição
ajustada da dimensão X (V ou E) no valor do risco final no tempo t, ou seja, após a normalização.


Nota: A versão 2.0 da plataforma AdaptaBrasil ilustra as relações de impactos em cadeia, ou também
chamados, impactos encadeados. Isso significa que os subsetores cujos impactos não são "primários"
possuem hierarquias diferenciadas dentro do modelo de avaliação. Isto ocorre para a ameaça de
escassez hídrica, oriunda de modelagem hidrológica, e, portanto, não possui indicadores simples
diretamente relacionados à ameaça climática (Nível 3), a contribuição da dimensão de ameaça no
cálculo do risco final não pode ser obtida da mesma forma que nas outras dimensões do risco
(vulnerabilidade e exposição) com indicadores simples (nível 5) com relação direta (nível 3).


     Para contornar essa ausência, utilizamos o próprio valor da ameaça no lugar do indicador
simples (Nível 6), condicionado à variação da sua contribuição primária, ou seja, à contribuição de
sua dimensão associada no Nível 3. Esse ajuste permite que a ameaça climática seja adequadamente
representada no cálculo do risco final. Dito isso, foi utilizada a seguinte fórmula:


                                  𝐶𝐴𝐶 (𝑡) = 𝐴𝐶𝑥 (𝑡) ∗ C ′ (𝐼𝐴𝐶𝑗𝑖 )


Onde: 𝐶𝐴𝐶 (𝑡) é a contribuição bruta/redimensionada da ameaça climática no valor do risco final no
tempo t, ou seja, após a normalização; 𝐴𝐶𝑥 (𝑡) é o valor da ameaça climática no município x; C′ (𝐼𝐴𝐶𝑗𝑖 )
é a contribuição ajustada da dimensão de ameaça climática no valor do risco final no tempo t, ou
seja, após a normalização.


ETAPA 5: Cálculo das contribuições “ajustadas” dos indicadores simples para o risco final


Para garantir que a soma das contribuições individuais seja igual a 1 (ou 100%), é necessário ajustar
os valores das contribuições brutas de cada indicador simples. Esse ajuste assegura que cada
contribuição seja proporcional em relação ao valor total do risco ou da métrica que está sendo
calculada. O ajuste é realizado por meio de um processo de normalização, que redistribui as
contribuições relativas, preservando as proporções originais entre elas. Segue a fórmula:
                                                   54
                                                        Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                            climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                      Hídricos

## PDF page 55

                                                             𝐶𝑖 (𝑡)
                                    𝐶𝑖 𝑎𝑗𝑢𝑠𝑡𝑎𝑑𝑜 (𝑡) =
                                                            ∑ 𝐶𝑖 (𝑡)


Onde: 𝐶𝑖 𝑎𝑗𝑢𝑠𝑡𝑎𝑑𝑜 (𝑡) é a contribuição ajustada de cada indicador simples no valor do risco final no

tempo t, ou seja, após a normalização; 𝐶𝑖 (𝑡) é o valor da contribuição “bruta” dos indicadores simples
para o risco final.


          4.3.2. Cálculo da contribuição dos indicadores simples às dimensões associadas (Nível 1
                  para Nível 4)


A metodologia de cálculo desta relação se dá em duas etapas principais: 1- Cálculo das contribuições
“brutas” dos indicadores simples para as dimensões do risco e 2- Cálculo das contribuições
“ajustadas”.


ETAPA 1: Cálculo das contribuições “brutas” dos indicadores simples para as dimensões do risco


A contribuição bruta dos indicadores simples para a dimensão de vulnerabilidade considera o cálculo
diferenciado para os indicadores associados à sensibilidade (s) e à capacidade adaptativa (ca). Assim:


    ● Contribuição dos indicadores simples relacionados à sensibilidade (𝐶𝐼𝑆𝑠 ) e à capacidade
        adaptativa (𝐶𝐼𝑆𝑐𝑎 ) - dimensão de vulnerabilidade:
                                                        𝐼𝑆𝑠
                                            𝐶𝐼𝑆𝑠 =
                                                        𝐼𝑉

                                                   1 − 𝐼𝑆𝑐𝑎
                                        𝐶𝐼𝑆𝑐𝑎 =
                                                      𝐼𝑉

    ● Contribuição dos indicadores simples à dimensão de exposição:


                                                  55
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 56

                                                      𝐼𝑆𝑒
                                           𝐶𝐼𝑆𝑒 =
                                                      𝐼𝐸

   ● Co Contribuição dos indicadores simples à dimensão de ameaça climática:


                                                     𝐼𝑆𝑎𝑐 (𝑡)
                                      𝐶𝐼𝑆𝑎𝑐 (𝑡) =
                                                     𝐼𝐴𝐶 (𝑡)


Onde: 𝐶𝐼𝑆𝑥 é a contribuição bruta do indicador simples x no valor da dimensão a que ele está
associado; 𝐼𝑆𝑥 é o valor do indicador simples x; IV, IE ou IAC é o valor da dimensão do risco após a
normalização.


Nota: Por ser uma dimensão dinâmica, para o cálculo da contribuição dos indicadores simples para a
ameaça climática em um momento específico (tempo t1), todas as variáveis que compõem esse
cálculo devem estar relacionadas e refletir as condições desse mesmo período temporal.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para as dimensões a que se
relacionam


O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma metodologia
descrita anteriormente (tópico 4.3.1, etapa 5). Foram aplicados os mesmos princípios e fórmulas para
determinar as proporções relativas de cada indicador dentro do sistema.


         4.3.3. Cálculo da contribuição dos indicadores simples às subdimensões da
                vulnerabilidade a que estão associadas (Nível 1 para Nível 3)


A metodologia de cálculo desta relação se dá em duas etapas principais, detalhadas abaixo.


ETAPA 1: Cálculo das contribuições “brutas” dos indicadores simples para cada subdimensão
pertencente
                                                56
                                                     Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                   Hídricos

## PDF page 57

Para o cálculo contribuição bruta dos indicadores simples à subdimensão de sensibilidade (S) ou
capacidade adaptativa (CA) foi utilizada a seguinte metodologia:


                                                       𝐼𝑆𝑥
                                           𝐶𝐼𝑆𝑥 =
                                                        𝑋

Onde: 𝐶𝐼𝑆𝑥 é a contribuição bruta do indicador simples x no valor da subdimensão a que ele está
associado; 𝐼𝑆𝑥 é o valor do indicador simples x; X é o valor da subdimensão do risco.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para as subdimensões a que
se relacionam


O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma metodologia
descrita anteriormente (tópico 4.3.1, etapa 5). Foram aplicados os mesmos princípios e fórmulas para
determinar as proporções relativas de cada indicador dentro do sistema.


         4.3.4. Cálculo da contribuição dos indicadores simples aos indicadores temáticos a que
                estão associadas (Categoria 1 para categoria 2)


A metodologia de cálculo destas relações se dá em duas etapas: 1) Cálculo das contribuições “brutas”
dos indicadores simples para cada indicador temático pertencente; 2) Cálculo das contribuições
“ajustadas”.
Para estimar a contribuição “bruta” de cada indicador simples utilizou-se a seguinte equação:


                                                       𝐼𝑆𝑥
                                           𝐶𝐼𝑆𝑥 =
                                                       𝑇𝑦


                                                 57
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 58

Onde: CISx é a contribuição bruta do indicador simples x no valor do indicador temático no i-ésimo
município a que ele está associado; ISx é o valor do indicador simples x no i-ésimo município; Ty é o
valor do indicador temático do i-ésimo município.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para os indicadores
temáticos a que se relacionam


O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma metodologia
descrita anteriormente (tópico 5.3.1, etapa 5). Foram aplicados os mesmos princípios e fórmulas para
determinar as proporções relativas de cada indicador dentro do sistema.


                                                 58
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 59

REFERÊNCIAS BIBLIOGRÁFICAS


ADGER, W. N.. Vulnerability. Global Environmental Change, v. 16, n. 3, p. 268–281, ago. 2006.

AGHAKOUCHAK, A., CHIANG, F., HUNING, L. S., LOVE, C. A., MALLAKPOUR, I., MAZDIYASNI, O., et al.
(2020). Climate extremes and compound hazards in a warming world. Annual Review of Earth and
Planetary Sciences, 48(1), 519–548. https://doi.org/10.1146/annurev-earth-071719-055228

ANA - Agência Nacional de Águas. Impacto da Mudança Climática nos Recursos Hídricos no Brasil /
Agência Nacional de Águas e Saneamento Básico. -- Brasília : ANA, 2024.

ANA - Agência Nacional de Águas. Manual de Usos Consuntivos da Água no Brasil / Agência Nacional
de Águas. - Brasília: ANA, 75 p.: il. ISBN: 978-85-8210-057-8. 2019.

ASCE - American Society of Civil Engineers. Climate-resilient infrastructure: Adaptive design and risk
management (B. M.Ayyub, Ed.). Committee on Adaptation to a Changing Climate. 2018.

BALLARIN, A. S., SOUSA MOTA UCHÔA, J. G., DOS SANTOS, M. S., ALMAGRO, A., MIRANDA, I. P., DA
SILVA, P. G. C., ... & OLIVEIRA, P. T. S. (2023). Brazilian water security threatened by climate change
and human behavior. Water Resources Research, 59(7), e2023WR034914.

BECKER, W. et al. COIN Tool User Guide, EUR 29899 EN, Publications Office of the European Union.
2019.          Disponível           em:          https://ec.europa.eu/jrc/en/coinhttps://composite-
indicators.jrc.ec.europa.eu/EUScienceHubhttps://ec.europa.eu/jrc. Acessado em: 15 set. 2024.

BERROUET, Lina María; MACHADO, Jenny; VILLEGAS-PALACIO, Clara. Vulnerability of socio—
ecological systems: A conceptual Framework. Ecological indicators, 2018, 84: 632-647.

BIGGS, R; VOS, A; PREISER, R; CLEMENTS, H; MACIEJEWSKI, K; SCHLÜTER, M. The Routledge
Handbook of Research Methods for Socioecological Systems. Nova York: Routledge, 2021.

BOND, N. R., BURROWS, R. M., KENNARD, M. J., & BUNN, S. E. (2019). Water scarcity as a driver of
multiple stressor effects. In Multiple stressors in river ecosystems (pp. 111-129). Elsevier.

BORGOMEO, E., MORTAZAVI-NAEINI, M., HALL, J. W., e GUILLOD, B. P. Risk, robustness and water
resources planning under uncertainty. Earths Future, 6(3), 468–487. 2018.


                                                  59
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 60

BUDYKO, M. I. “Climate and life”. Academic Press, Nova Iorque. 1974.

CARETTA, M.A., A. MUKHERJI, M. ARFANUZZAMAN, R.A. BETTS, A. GELFAN, Y. HIRABAYASHI, T.K.
LISSNER, J. LIU, E. LOPEZ GUNN, R. MORGAN, S. MWANGA, AND S. SUPRATID, 2022: Water. In:
Climate Change 2022: Impacts, Adaptation and Vulnerability. Contribution of Working Group II to the
Sixth Assessment Report of the Intergovernmental Panel on Climate Change [H.-O. Pörtner, D.C.
Roberts, M. Tignor, E.S. Poloczanska, K. Mintenbeck, A. Alegría, M. Craig, S. Langsdorf, S. Löschke, V.
Möller, A. Okem, B. Rama (eds.)]. Cambridge University Press, Cambridge, UK and New York, NY, USA,
pp. 551–712, doi:10.1017/9781009325844.006.

FU; GUOBIN; CHARLES, S. P.; CHIEW, F. H. S. “A two-parameter climate elasticity of streamflow index
to assess climate change effects on annual streamflow.” In: Water Resources Research, 43 (11)
(November 24): 1–12. 2007.

GALAZ, V.; MOBERG, F.; OLSSON, E.-K.; PAGLIA, E.; PARKER, C.. Institutional and political leadership
dimensions of cascading ecological crises. Public Administration, 89, p. 361-380. 2011.

GALLOPÍN, G. C. Environmental and sustainability indicators and the concept of situational indicators.
A system approach. Environmental Modelling & Assessment, v.1, p.101-117, 1996.

GALLOPÍN, G. C. Linkages between vulnerability, resilience, and adaptive capacity. Global
Environmental Change, v. 16, p. 293-303, 2006.

GALLOPÍN, G. C.. Box 1: A systemic synthesis of the relations between vulnerability, hazard, exposure
and impact, aimed at policy identification. In: Economic Commission for Latin American and the
Caribbean (ECLAC). Handbook for Estimating the Socio-Economic and Environmental Effects of
Disasters. Mexico, D.F.: ECLAC, LC/MEX/G.S., p. 2–5, 2003.

GALLOPÍN, G. C.. Human dimensions of global change: linking the global and the local processes.
International Social Science Journal, v. 130, p. 707–718, 1991.

GESUALDO, G. C., SONE, J. S., GALVÃO, C. D. O., MARTINS, E. S., MONTENEGRO, S. M. G. L.,
TOMASELLA, J., & MENDIONDO, E. M. (2021). Unveiling water security in Brazil: Current challenges
and     future     perspectives.      Hydrological         Sciences           Journal,          66(5),          759–768.
https://doi.org/10.1080/02626667.2021.1899182


                                                  60
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 61

GETIRANA A, LIBONATI R, CATALDI M. Brazil is in water crisis - it needs a drought plan. Nature. 2021
Dec;600(7888):218-220. doi: 10.1038/d41586-021-03625-w. PMID: 34880440.

GILL, J. C.; MALAMUD, B. D.. Hazard interactions and interaction networks (cascades) within multi-
hazard methodologies. Earth System Dynamics, 7, p. 659-679. 2016.

GLEICK, P. H. The world’s water. 2000-2001. Report on Freshwater Resources. Island Press, 2000.
315p.

HAMMOND, A.; ADRIAANSE, A.; RODENBURG, E.; BRYANT, D.; WOODWARD, R. Environmental
indicators: a systematic approach to measuring and reporting on environmental policy
performance in the context of sustainable development. Washington DC: World Resources Institute,
1995, 43p.

HE, C., LIU, Z., WU, J., PAN, X., FANG, Z., LI, J., & BRYAN, B. A. (2021). Future global urban water
scarcity     and     potential     solutions.     Nature           Communications,                  12(1),          1–11.
https://doi.org/10.1038/s41467-021-25026-3

HILLY, G.; VOJINOVIC, Z.; WEESAKUL, S.; SANCHEZ, A.; HOANG, D. N.; DJORDJEVIC, S.; CHEN, A.S.;
EVANS, B. Methodological framework for analysing cascading effects from flood events: the case of
Sukhumvit Area, Bangkok, Thailand. Water, v. 10, n. 81, 2018.

HUNT, J. D., STILPEN, D., & DE FREITAS, M. A. V. (2018). A review of the causes, impacts and solutions
for electricity supply crises in Brazil. Renewable and Sustainable Energy Reviews, 88(October 2017),
208–222. https://doi.org/10.1016/j.rser.2018.02.030

INTERGOVERNMENTAL PANEL ON CLIMATE CHANGE – IPCC. Climate Change 2014: Synthesis Report.
Working Groups I, II and III to the Fifth Assessment Report of the Intergovernmental Panel on Climate
Change [Core Writing Team, R.K. Pachauri and L.A. Meyer (eds.)]. IPCC, Geneva, Switzerland, 151 pp.
2015.

INTERGOVERNMENTAL PANEL ON CLIMATE CHANGE – IPCC. Climate Change 2022: Impacts,
Adaptation and Vulnerability. Contribution of Working Group II to the Sixth Assessment Report of
the Intergovernmental Panel on Climate Change [H.-O. Pörtner, D.C. Roberts, M. Tignor, E.S.
Poloczanska, K. Mintenbeck, A. Alegría, M. Craig, S. Langsdorf, S. Löschke, V. Möller, A. Okem, B.


                                                 61
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 62

Rama (eds.)]. Cambridge University Press. Cambridge University Press, Cambridge, UK and New York,
NY, USA, 3056 pp., 2022.

JACOB, K.; BLAKE, R.. Chapter 7: Indicators and monitoring. Ann. N.Y. Acad. Sci. v.1196, p. 127–141,
2010.

JANNUZZI, P. D. M.. Indicadores para Diagnóstico, Monitoramento e Avaliação de Programas Sociais
no Brasil. Revista do Serviço Público, v. 56, n. 2, p. 137–160, 2005.

JANNUZZI, P. M. Indicadores Sociais no Brasil: conceitos, fontes de dados e aplicações. Campinas:
Editora Alínea/PUC-Campinas, 141 p. 2006.

KASPERSON, J. X.; KASPERSON, R. E.; TURNER II., B. L., SCHILLER, A., HSIEL, W. H.. Vulnerability to
global environmental change. In: KASPERSON, J. X.; KASPERSON, R. E. (Eds.), Social Contours of Risk,
vol. II. Earthscan, London, 2005. p. 245–285.

KEMP L., XU C., DEPLEDGE J., EBI K.L., GIBBINS G., KOHLER T.A., ROCKSTRÖM J., SCHEFFER M.,
SCHELLNHUBER H.J., STEFFEN W., LENTON T.M. 2022. Climate endgame: Exploring catastrophic
climate change scenarios. Proceedings of the National Academy of Sciences 119: e2108146119.

KIGUCHI, M., SHEN, Y. KANAE, S & OKI, T. (2015) Reevaluation of future water stress due to socio-
economic and climate factors under a warming climate, Hydrological Sciences Journal, 60:1, 14-29,
DOI: 10.1080/02626667.2014.888067

KOKS, E.. Moving flood risk modelling forwards. Nature Climate Change, 8, p. 561-562. 2018.

KOUTROULIS, A. G., PAPADIMITRIOU, L. V., GRILLAKIS, M. G., TSANIS, I. K., WARREN, R., & BETTS, R.
A. (2019). Global water availability under high-end climate change: A vulnerability based
assessment. Global               and              Planetary                        Change, 175,                         52-
63. https://doi.org/10.1016/j.gloplacha.2019.01.013

KUNDZEWICZ, Z. W.; e STAKHIV, E. Z. Are Climate Models ‘ready for Prime Time’ in Water Resources
Management Applications, or Is More Research Needed? Hydrological Sciences Journal 55 (7): 1085–
89. 2010.


                                                  62
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 63

LAWRENCE, J., BLACKETT, P., CRADOCK-HENRY, N.; NISTOR, B.J. Climate Change: The Cascade Effect.
Cascading impacts and implications for Aotearoa New Zealand, 2018. Wellington: Deep South
Challenge.

LAWRENCE, J.; BLACKETT, P.; CRADOCK-HENRY, N. A. Cascading climate change impacts and
implications. Climate Risk Management, v. 29, 2020.

LAWRENCE, J.; BLACKETT, P.; CRADOCK-HENRY, N.; FLOOD, S.; GREENAWAY, A.; DUNNINGHAM, A..
Synthesis Report RA4: Enhancing capacity and increasing coordination to support decision making.
Climate Change Impacts and Implications (CCII) for New Zealand to 2100. Wellington: NZCCRI,
Victoria University of Wellington; NIWA; Landcare Research, 2016.

LIMA, P. V. P. S.; QUEIROZ, F. D. DE S.; MAYORGA, M. I. DE O.; CABRAL, N. R. A. J. A propensão à
degradação ambiental na mesorregião de Jaguaribe no Estado do Ceará. Economia do Ceará em
Debate 2008, p. 27–43, 2009.

LIU, J., YANG, H., GOSLING, S. N., KUMMU, M., FLÖRKE, M., PFISTER, S., ET AL. (2017). Water scarcity
assessments     in    the   past,   present,   and     future.        Earth's       Future,        5(5),       549–559.
https://doi.org/10.1002/2016EF000518

MAGGINO, F.. Complexity in society: from indicators construction to their Synthesis. 1º ed. Roma,
Itália: Springer, 2017.

MARENGO, J. A. Água e mudanças climáticas. Estudos Avançados, v.22, n. 63, p. 83-96, 2008.

MARENGO, J. A. O futuro clima do Brasil. Revista USP, n. 103, p. 25, 2014.

MARENGO, J. A.; ALVES, L. M. Crise Hídrica em São Paulo em 2014: Seca e Desmatamento. GEOUSP
Espaço e Tempo (Online), São Paulo, Brasil, v. 19, n. 3, p. 485–494, 2015. DOI: 10.11606/issn.2179-
0892.geousp.2015.100879. Disponível em: https://revistas.usp.br/geousp/article/view/100879..
Acesso em: 18 ago. 2025.

MARENGO, J.A., TOMASELLA, J., NOBRE, C.A. (2017). Climate Change and Water Resources. In: de
Mattos Bicudo, C., Galizia Tundisi, J., Cortesão Barnsley Scheuenstuhl, M. (eds) Waters of Brazil.
Springer, Cham. https://doi.org/10.1007/978-3-319-41372-3_12


                                                 63
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 64

MEADOWS, D. Indicators and Information Systems for Sustainable Development. Hartland/VT:
Sustainability Institute (1998).

MEHRAN, A., AGHAKOUCHAK, A., NAKHJIRI, N. et al. Compounding Impacts of Human-Induced Water
Stress        and    Climate   Change         on    Water         Availability. Sci          Rep 7,        6282         (2017).
https://doi.org/10.1038/s41598-017-06765-0

MIOLA,        A.;   SCHILTZ,   F.     Measuring      sustainable          development             goals       performance:
How      to     monitor   policy     action    in   the     2030       Agenda         implementation?              Ecological
Economics, v. 164, p. 1–10, 2019.

MIZRAHI, S.. Cascading disasters, information cascades and continuous time models of domino
effects. International Journal of Disaster Risk Reduction, v.49, 2020.

MULTSCH, S., KROL, M. S., PAHLOW, M., ASSUNÇÃO, A. L. C., BARRETTO, A. G. O. P., DE JONG VAN
LIER, Q., & BREUER, L. (2020). Assessment of potential implications of agricultural irrigation policy on
surface water scarcity in Brazil. Hydrology and Earth System Sciences, 24(1), 307–324.
https://doi.org/10.5194/hess-24-307-2020

MUNIA, H. A., GUILLAUME, J. H. A., WADA, Y., VELDKAMP, T., VIRKKI, V., & KUMMU, M. (2020). Future
transboundary water stress and its drivers under climate change: A global study. Earth's Future, 8,
e2019EF001321. https://doi.org/10.1029/2019EF001321

MYERS, N., MITTERMEIER, R. A., MITTERMEIER, C. G., FONSECA, G. A. B., & KENT, J. (2000).
Biodiversity        hotspots   for      conservation        priorities.         Nature,          403(403),           853–858.
https://doi.org/10.1038/35002501

OCDE, Organisation for Economic Co-operation and Development. NARDO, M.; SAISANA, M.;
SALTELLI, A.; TARANTOLA, S.; HOFFMAN, A.; GIOVANNINI, E. Handbook on constructing composite
indicators: methodology and user guide. Paris: Organisation for Economic Co-operation and
Development (OECD), 2008. Disponível em: <https://www.oecd.org/sdd/42495745.pdf>.

OECD. Organization for Economic Cooperation and Development: core set of indicators for
environmental performance reviews; a synthesis report by the group on the State of the
environment. Paris, 1993.


                                                       64
                                                            Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                                climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                          Hídricos

## PDF page 65

OLSEN, J.R. Adapting Infrastructure and Civil Engineering Practice to a Changing Climate. American
Society of Civil Engineers. 2015.

OSTROM, E. Governing the commons: the evolution of institutions for collective
action. Cambridge, New York, Melbourne, Madrid, Cape Town: Cambridge University
Press, 1990.

PEREIRA, L.S., CORDERY, I., IACOVIDES, I., 2009. Coping with Water Scarcity: Addressing the
Challenges. Springer Science & Business Media.

PEREIRA, P. A. A., MARTHA, G. B., SANTANA, C. A., & ALVES, E. (2012). The development of Brazilian
agriculture and future challenges. Agriculture and Food Security, 1(April), 1–12. Retrieved from
http://www.agricultureandfoodsecurity.com/content/1/1/4

PESCAROLI, G.; ALEXANDER, D. Critical infrastructure, panarchies and the vulnerability paths of
cascading disasters. Nat Hazards, 82, p. 175-192. 2016.

ROCHA, J. C.; PETERSON, G. D.; BODIN, O.; LEVIN, S. A. Cascading regime shifts within and across
scales. bioRxiv, 364620. Preprint. 2018.

SALAS, J., B.; RAJAGOPALAN, L.; SAITO, e BROWN, C. Special Section on Climate Change and Water
Resources: Climate Non-Stationarity and Water Resources Management. Journal of Water Resources
Planning and Management 138 (5): 385–88. 2012.

SÃO PAULO. Mudanças climáticas e água no Brasil: iniciativas de adaptação. São Paulo, 2011.

SIMPSON, N. P. et al. A framework for complex climate change risk assessment. One Earth, v. 4, P.
489–501. 2021.

SMITI, A.. A critical overview of outlier detection methods. Computer Science Review, v. 38. 2020.

STEINSCHNEIDER, S.; WI, S.; e BROWN, C. The integrated effects of climate and hydrologic uncertainty
on future flood risk assessments: flood risk under hydrologic and climate uncertainty. Hydrol.
Process., 29(12), 2823–2839. 2015.

TUNDISI, J. G. Recursos hídricos no futuro: problemas e soluções. Estudos Avançados, v. 22, n. 63,
p.7–16, 2008.


                                                 65
                                                      Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                          climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                    Hídricos

## PDF page 66

TURNER, B. L.; KASPERSON, R. E.; MATSON, P. A.; MCCARTHY, J. J.; CORELL, R. W.; CHRISTENSEN, L.;
ECKLEY, N.; KASPERSON, J. X.; LUERS, A.; MARTELLO, M. L.; POLSKY, C.; PULSIPHER, A.; SCHILLER, A..
A framework for vulnerability analysis in sustainability science. Proceedings of the National
Academy of Sciences of the United States of America, v. 100, n. 14, p. 8074–9, 2003.

TURRENTINE, J.. IPCC: We Cannot Look Away—Climate Risks Are Cascading. Natural Resources
Defense Council (NRDC). 2022. Disponível em: < https://www.nrdc.org/stories/ipcc-we-cannot-look-
away-climate-risks-are-cascading>.

UN WATER. Water Scarcity. Available at: https://www.unwater.org/water-facts/water-scarcity.

UNITED     NATIONS     UNIVERSITY/    INSTITUTE        FOR      WATER,          ENVIRONMENT                &      HEALTH
(UNU/INWEH).Water security & the global water agenda: A UN-water analytical brief. Hamilton:
ONU, 2013. 45p

VAN    BELLEN,    H.    M.   Indicadores   de     Sustentabilidade:             uma        análise       comparativa.
2º ed. Rio de Janeiro, RJ, 2006.

WANG, H.; ANG, B. W.; BIN SU. Multiplicative structural decomposition analysis of energy and
emission intensities: Some methodological issues. Energy, v. 123, p. 47-63, 2017.

WHITE, C., 2014. 28. Understanding water scarcity: Definitions and measurements. In: Global Water:
Issues and Insights. 161.

WILLNER, S.; OTTO, C.; LEVERMANN, A.. Global economic response to river floods. Nat. Clim. Change,
8, p. 594-598. 2018.

XAVIER, A.; KING W.; SCANLON, B. Daily gridded meteorological variables in Brazil (1980–2013). Int J
Climatol. 36:2644– 2659. 2015.

XAVIER, A.; KING, C.; SCANLON, B. An update of Xavier, King and Scanlon. Daily precipitation gridded
data set for the Brazil. In: Conference proceedings, pp 562–569. 2016.


                                                  66
                                                       Teórico-metodológico para avaliação do risco de impacto das mudanças
                                                           climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                                                                     Hídricos

## PDF page 67

67
     Teórico-metodológico para avaliação do risco de impacto das mudanças
         climáticas em Setores Estratégico: Segurança Alimentar e Recursos
                                                                   Hídricos

## PDF page 68

    APÊNDICES

        APÊNDICE A           Composição hierárquica do SE Recursos Hídricos.


    Tabela Erro! Use a guia Página Inicial para aplicar APÊNDICE ao texto que deverá aparecer aqui..1 – Indicadores selecionados para a compor a hierarquia do
    Setor Estratégico de Recursos Hídricos.
Setor Estraté-     Índice de
                                     Dimensão            Categoria               Indicadores Temáticos                               Indicadores Simples
    gico             Risco

                                                                           Insegurança do abastecimento hu-      Ineficiência na produção da água
                                                                                        mano                     Ineficiência na distribuição da água

                                                                                                                 Consumo médio per capita de água

                                                                           Balanço hídrico das atividades pro-   Balanço hídrico para agropecuária
                                                                                         dutivas                 Balanço hídrico para indústria
                                                      Índice de Sensibi-
                                                                              Efeitos sobre a saúde humana       Doenças devido ao saneamento inadequado
                                                            lidade
                                                                                                                 Qualidade da água
Impactos para    Índice de Risco
                                   Índice de Vulne-
 Recursos Hí-    de Estresse Hí-                                                                                 Áreas degradadas e/ou desmatadas
                                      rabilidade
    dricos            drico                                                Pressão antrópica e qualidade ambi-
                                                                                                                 Áreas com solos susceptíveis à erosão
                                                                                          ental
                                                                                                                 Vazão ecológica para usos ecossistêmicos

                                                                                                                 Segurança das barragens e rejeitos da mineração

                                                                                                                 Plano municipal de saneamento básico

                                                      Índice de Capaci-       Gestão dos recursos hídricos       Nível de atuação em comitês de bacia
                                                       dade Adaptativa                                           Ações de prevenção relacionadas à seca

                                                                                                                 Alternativas ao abastecimento de água

## PDF page 69

                                                          Investimentos em recursos hídricos

                    Planejamento para recursos hídricos   Investimentos em políticas de adaptação

                                                          Programa cidades resilientes

                                                          Programa cisternas: água para consumo

                                                          Reservação natural
                            Resiliência hídrica
                                                          Reservação artificial

                                                          Potencial de armazenamento subterrâneo

                    Capacidade dos setores produtivos     Participação agropecuária no PIB

                                                          Participação industrial no PIB

                    Capacidade socioeconômica fami-       Renda não afetada pelo preço da água
                                  liar                    Renda superior a dois salários-mínimos

                            População exposta             Densidade populacional

                                                          Usuários urbanos expostos

                                                          Usuários rurais expostos

Índice de Exposi-                                         Usuários industriais expostos
       ção           Usuários dos recursos hídricos ex-
                                                          Usuários da mineração expostos
                                  postos
                                                          Usuários da termoeletricidade expostos

                                                          Usuários da criação animal expostos

                                                          Usuários da irrigação expostos

## PDF page 70

Índice de Ame-
                 Risco de escassez hídrica
      aça
