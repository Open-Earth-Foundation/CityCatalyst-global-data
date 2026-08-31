# Documento teórico-metodológico do Setor Estratégico Segurança Alimentar — AdaptaBrasil MCTI

- Candidate document ID: `doc_dd9ab3b0abf5`
- Workbook source IDs: FS_SRC_001
- Candidate sectors: Food security
- Source PDF: `working/raw/doc_dd9ab3b0abf5.pdf`
- SHA-256: `3dc902cda2cddff66ddc218bbdb782f989dfd59bf5b1476bebe38cb4d05181e1`
- Physical PDF pages: 132
- Extraction: Poppler pdftotext 25.09.1 (-layout)

> Page headings below use the 1-based physical PDF page number. Text order follows Poppler's layout-preserving extraction and has not been substantively edited.

---

## PDF page 1

     Documento teórico-metodológico para avaliação de risco de

    impacto de mudança climática no Setor Estratégico Segurança

         Alimentar da plataforma AdaptaBrasil MCTI - Versão 2.01


1
    Data de revisão do documento: 15 de agosto de 2025.

## PDF page 2

                                                         SUMÁRIO


1        RISCO DE IMPACTO DAS MUDANÇAS CLIMÁTICAS ........................................... 5

1.1      Risco de Impacto em Cascata ou Risco Encadeado .............................................9

2        DELIMITANDO O SETOR ESTRATÉGICO SEGURANÇA ALIMENTAR .............. 12

2.1      Caracterização do Subsetor Disponibilidade de Alimentos ................................15

2.2      Caracterização do subsetor Acesso e Consumo de Alimentos..........................17

3        ÍNDICES E INDICADORES: PERSPECTIVAS TEÓRICAS .................................... 19

4        ÍNDICE DE RISCO DE IMPACTO ÀS MUDANÇAS CLIMÁTICAS PARA
         SEGURANÇA ALIMENTAR .................................................................................... 20

4.1      Ameaças climáticas (ou relacionadas ao clima) ..................................................24

4.1.1 Construção de indicadores e índices de Ameaças Climáticas para o Subsetor de
         Disponibilidade de Alimentos ....................................................................................26

4.2      Vulnerabilidade e Exposição..................................................................................33

4.2.1 Identificação e pré-seleção dos indicadores candidatos ...........................................33

4.2.2 Construção numérica e seleção dos indicadores simples .........................................36

4.2.3 Cálculo dos demais níveis hierárquicos ....................................................................48

4.2.4 Cálculo dos fatores influenciadores ..........................................................................53

REFERÊNCIAS BIBLIOGRÁFICAS .................................................................................. 63

APÊNDICES ....................................................................................................................... 71

## PDF page 3

                                           LISTA DE ILUSTRAÇÕES

Figura 1 – Modelo conceitual para análise do risco de impacto das mudanças climáticas
               desenvolvido para o AdaptaBrasil MCTI 2.0. ......................................................6

Figura 2 – Diferentes fatores ou ameaças relacionadas ao clima. ........................................8

Figura 3 – Riscos climáticos globais em cascata. Este é um diagrama de loop causal, no
               qual uma linha completa representa uma polaridade positiva (por exemplo,
               feedback amplificador; não necessariamente positivo no sentido normativo) e
               uma linha pontilhada denota uma polaridade negativa (significando um
               feedback atenuante). ........................................................................................10

Figura 4 – Dimensões e componentes de segurança alimentar. .........................................13

Figura 5 – Modelo conceitual para análise do risco de impacto das mudanças climáticas no
               Setor Segurança Alimentar desenvolvido para o AdaptaBrasil MCTI 2.0. ........14

Figura 6 – Pirâmide da informação. .....................................................................................20

Figura 7 – Estrutura hierárquica entre as composições de indicadores e índices de risco de
               impacto das mudanças climáticas no subsetor de disponibilidade de alimentos.
                .........................................................................................................................21

Figura 8 – Estrutura hierárquica entre as composições de indicadores e índices de risco de
               impacto das mudanças climáticas no acesso e consumo de alimentos. ..........22

Figura 9 – Integração das dimensões de ameaça climática com vulnerabilidade e
               exposição na avaliação do risco climático: presente e cenários futuros. ..........25

Figura 10 – Identificação e conversão de calendário, de 360 dias para 365. ......................30

Figura 11 – Sistema prático para equiparação de experimentos climáticos e construção de
               Ensemble Mean. ...............................................................................................31

Figura 12 – Preparação e entrega de produtos climáticos solicitados junto a equipe interna
               do AdaptaBrasil MCTI.......................................................................................32

Figura 13 – Organograma das etapas de construção numérica e seleção dos indicadores
               simples do SE Segurança Alimentar. ...............................................................37

Figura 14 – Representação espacial dos municípios que atenderam aos critérios de
               seleção da máscara 1.......................................................................................44

## PDF page 4

Figura 15 – Representação espacial dos pesos que foram atribuídos aos municípios para
            ajuste de indicadores com escala estadual. .....................................................46

Figura 16 – Organograma das etapas de construção dos indicadores temáticos e índices
            dos níveis superiores do SE Segurança Alimentar. ..........................................49


Tabela 1 – Instituições de Pesquisas e Serviços Climáticos integrantes do Projeto
            CORDEX. .........................................................................................................28

Tabela 2 – Modelos Regionais utilizados no Projeto CORDEX com enfoque na América do
            Sul. ...................................................................................................................28

Tabela 3 – Conjunto de Forçantes Atmosféricas utilizadas no Projeto CORDEX. ..............29

Tabela 4 – Cálculo dos coeficientes de inclinação (a) e deslocamento (b) para
            normalização dos valores de indicadores temáticos. .......................................50

Tabela 5 – Indicadores selecionados para a compor a hierarquia do Subsetor
            Disponibilidade de Alimentos para seca. ..........................................................71

Tabela 6 – Indicadores selecionados para a compor a hierarquia do Subsetor Acesso e
            Consumo de Alimentos para seca. ...................................................................73

Tabela 7 – Lista de municípios brasileiros, por estado, que receberam valores NA
            (aplicação da máscara 1) para alguns indicadores do SE Disponibilidade de
            Alimentos para Seca.........................................................................................75

Tabela 8 – Valores dos pesos atribuídos aos municípios brasileiros (aplicação da máscara
            2) para alguns indicadores do SE Disponibilidade de Alimentos para Seca. ....79

Tabela 9 – Tratamentos/procedimentos matemáticos aplicados nos indicadores
            selecionados do Subsetor Disponibilidade de Alimentos para Seca. .............128

Tabela 10 – Tratamentos/procedimentos matemáticos aplicados nos indicadores
            selecionados do Subsetor Acesso e Consumo de Alimentos. ........................131

## PDF page 5

O presente documento teoriza e descreve os principais conceitos que fundamentam o
entendimento sobre o risco de impacto das mudanças climáticas no contexto do
AdaptaBrasil – Versão 2.0. Aborda, também, a estruturação do Setor de Segurança
Alimentar, composta pelos subsetores de Disponibilidade de Alimentos e Acesso e Consumo
de Alimentos. Além disso, detalha as metodologias aplicadas em cada etapa de construção
de índices e indicadores de risco de impacto das mudanças climáticas, assim como os
fatores que influenciam cada subsetor.


1 RISCO DE IMPACTO DAS MUDANÇAS CLIMÁTICAS


Segundo o Painel Intergovernamental de Mudanças Climáticas (IPCC, sigla em inglês), o
risco é “o potencial de consequências adversas para os sistemas humanos e/ou ecológicos,
onde é considerado a diversidade de valores e objetivos associados a tais sistemas. Por
exemplo, consequências sobre vidas, meios de subsistência, saúde e bem-estar, ativos e
investimentos econômicos, sociais e culturais, infraestrutura, serviços (incluindo serviços
ecossistêmicos), ecossistemas e espécies” (IPCC, 2022).

No contexto dos impactos das mudanças climáticas, o risco resulta em interações dinâmicas
entre as ameaças climáticas (ou relacionadas ao clima) com a exposição e vulnerabilidade
do sistema socioecológico (SSE)2 que é potencialmente afetado (interação essa
denominada, aqui, como flor de risco – Figura 1). Estas dimensões se inserem em um
arcabouço metodológico (framework) que combina conceitos utilizados pelo IPCC (2015;
2022).

A vulnerabilidade trata da propensão ou predisposição de um sistema socioecológico ser
afetado negativamente, englobando uma variedade de conceitos e elementos, incluindo a
sensibilidade ou suscetibilidade a danos e a falta de capacidade de lidar e adaptar-se a uma
situação de perturbação climática (IPCC, 2021).


2
  Sistema socioecológico diz respeito ao sistema que inclui subsistemas sociais (humanos) e ecológicos (biofísicos) em
interação mútua (GALLOPÍN, 1991), ou seja, os sistemas humanos e naturais são entrelaçados, de forma interconectada e
interdependente. Pode ser especificado para qualquer escala, desde a comunidade local e seu ambiente circundante até o
global (GALLOPÍN, 2006).

## PDF page 6

Em outras palavras, a situação de vulnerabilidade está relacionada com características
intrínsecas de resiliência do SSE em questão, as quais estão relacionadas direta ou
indiretamente com a propensão do SSE ser impactado negativamente por uma perturbação
climática. Nesse sentido, a vulnerabilidade está associada a aspectos prévios e qualitativos
do SSE, que influenciam os danos potenciais decorrentes das perturbações climáticas.
Assim, o nível de vulnerabilidade pode intensificar ou reduzir o impacto climático. Ela pode
ser desmembrada na dimensão de sensibilidade e de capacidade adaptativa do SSE de
análise (TURNER et al., 2003; GALLOPÍN, 2006). A sensibilidade diz respeito ao grau em
que o sistema em análise é afetado, adversamente ou beneficamente, por estímulos
relacionados ao clima (IPCC, 2021). A sensibilidade é uma propriedade inerente de um
sistema socioecológico, existente antes da ameaça climática, independente (separado) da
exposição (IPCC, 2001; GALLOPÍN, 2003). Já a capacidade adaptativa está relacionada à
habilidade do sistema socioecológico (considerando cada um dos seus elementos) de se
ajustar a um distúrbio ou danos potenciais, aproveitando as oportunidades e lidando com as
consequências de uma transformação que ocorra (IPCC, 2021).


Figura 1 – Modelo conceitual para análise do risco de impacto das mudanças climáticas
            desenvolvido para o AdaptaBrasil MCTI 2.0.

                   Fonte: Elaborado por Karine Rocha, adaptado de IPCC (2015).

## PDF page 7

A exposição diz respeito à presença dos elementos que compõem o SSE (pessoas;
moradias; espécies; ecossistemas; serviços, recursos e funções ambientais; infraestrutura;
bens econômicos, sociais ou culturais) em locais e contextos que possam ser afetados
negativamente por uma perturbação climática (IPCC, 2021). A exposição a uma ameaça
climática particular pode ser determinada independentemente da vulnerabilidade
(GALLOPÍN, 2003; KASPERSON et al., 2005; ADGER, 2006, IPCC, 2015).

As Ameaças climáticas (ou relacionadas ao clima) são perturbações climáticas que
possuem uma tendência ou iminência a acontecer e que pode afetar negativamente o SSE
em questão. As perturbações climáticas estão associadas aos eventos climáticos extremos
definidos a partir de grandes picos de pressão, além do intervalo normal de variabilidade em
que o sistema socioecológico opera e que, geralmente, se originam além do sistema ou local
em questão (GALLOPÍN, 2006). Além disso, interagem com o ambiente de análise e
possuem capacidade de transformação significativa nesse sistema, seja ela lenta ou
repentina.

As ameaças climáticas possuem características exógenas, endógenas ou ambas,
dependendo do fenômeno e do SSE em análise (TURNER et al., 2003; KASPERSON et al.,
2005) – Figura 2. Ao tratarmos de risco climático no AdaptaBrasil, as ameaças do clima são
observadas como um agente externo (exógenas) ao sistema socioecológico, ou conjugado
com este sistema, ainda que as causas que provocaram essas ameaças sejam de origem
antrópica - emissões de gases de efeito estufa. Essa organização se deve ao fato de que
não é possível associar emissões específicas com ameaças climáticas específicas, no
tempo e espaço. As ameaças de ordem endógena são caracterizadas na dimensão de
vulnerabilidade, conforme o arcabouço que é utilizado pelo IPCC.

## PDF page 8

                 Figura 2 – Diferentes fatores ou ameaças relacionadas ao clima.
                                       Fonte: Elaborado por Karine Rocha.


Os riscos de impacto da mudança climática (riscos climáticos) estão sujeitos à incerteza em
termos de magnitude e probabilidade de ocorrência por estarem relacionados à ameaça
climática, exposição e vulnerabilidade; já que tais dimensões podem mudar ao longo do
tempo e do espaço devido às suas características interconectadas físicas e antrópicas
(mudanças socioeconômicas e tomada de decisões humanas) (IPCC, 2022). Tal impacto é
produto de um SSE altamente complexo3, o que implica uma profundidade de entendimento
de ordem sistêmica, multisetorial, multinível e multiescalar. Tais características trazem à tona
sobre a necessidade da avaliação precoce dos riscos com o intuito de se antever, precaver
ou mesmo adaptar-se aos possíveis impactos, considerando as interações entre os múltiplos
impulsionadores do risco e incluindo o papel das respostas de adaptação e mitigação para
tal.


3
  Utilizamos o termo complexo para comunicar a diversidade de interações entre setores e sistemas que podem ampliar ou
reduzir os riscos relacionados ao clima.

## PDF page 9

     1.1 Risco de Impacto em Cascata ou Risco Encadeado


                    Impactos em cascata de eventos meteorológicos/climáticos extremos ocorrem
                    quando um perigo extremo gera uma sequência de eventos secundários em sistemas
                    naturais e humanos que resultam em perturbações físicas, naturais, sociais ou
                    econômicas, em que o impacto resultante é significativamente maior do que o
                    impacto inicial. Os impactos em cascata são complexos e multidimensionais e estão
                    mais associados à magnitude da vulnerabilidade do que a do perigo (IPCC, 2022).


Em se tratando de riscos climáticos, os mesmos são considerados sistêmicos quando se
iniciam da consequência de impactos diretos – materializando-se como uma cadeia ou
cascata de impactos – e se agravam produzindo impactos ainda mais severos para as
pessoas e sociedades (GILL; MALAMUD, 2016; TURRENTINE, 2022). Segundo Lawrence;
Blackett; Gradock-Henry (2020), eles representam desafios de gestão significativos devido
às suas capacidades de cascata e recombinação, que exigem coordenação de respostas e
tomada de decisão por atores em vários níveis – ver representação da Figura 3.

## PDF page 10

Figura 3 – Riscos climáticos globais em cascata. Este é um diagrama de loop causal, no qual
          uma linha completa representa uma polaridade positiva (por exemplo, feedback
          amplificador; não necessariamente positivo no sentido normativo) e uma linha
          pontilhada denota uma polaridade negativa (significando um feedback atenuante).
                             Fonte: Adaptado de Kemp et al., 2022.

## PDF page 11

Nessa perspectiva, nem todos os impactos das mudanças climáticas surgirão da mesma
forma ou ao mesmo tempo: alguns surgem abruptamente, outros lentamente e são
contínuos, podendo haver múltiplos impactos ocorrendo simultaneamente e em diferentes
combinações (PESCAROLI; ALEXANDER, 2016; LAWRENCE et al., 2018; LAWRENCE;
BLACKETT; CRADOCK-HENRY, 2020). Isso faz com que seja absolutamente necessária a
identificação de quando e onde ocorrem (ou ocorrerão) esses impactos, pois há exemplos
empíricos que indicam uma propagação dos impactos e suas implicações como cascatas
nos sistemas físicos e humanos (LAWRENCE et al., 2016; ROCHA et al., 2018; WILLNER;
OTTO; LEVERMANN, 2018; KOKS, 2018; LAWRENCE; BLACKETT; CRADOCK-HENRY,
2020; MIZRAHI, 2020). Por exemplo, o estudo dos efeitos em cascata de inundações na
Tailândia (HILLY et al., 2018) podem incluir desde perda de serviços críticos, ativos e bens,
até congestionamento de tráfego e atrasos no transporte, perda de negócios e renda,
distúrbios e desconforto para os residentes.

A abordagem do risco em cascata ou encadeado, além de tornar explícita a complexidade
das interações entre os múltiplos riscos, permite uma visão mais compartimentada e com
enfoque nas interações dentro e entre as dimensões de cada risco permitindo, portanto,
ajudar a orientar uma avaliação mais detalhada e precisa (GALAZ et al., 2011; LAWRENCE
et al., 2018; SIMPSON et al., 2021). Pois os efeitos combinados de estressores interativos
podem afetar a capacidade de indivíduos, governos e setor privado de se adaptar a tempo,
ou seja, antes que ocorram danos generalizados (LAWRENCE; BLACKETT; CRADOCK-
HENRY, 2020; MIZRAHI, 2020).

Uma estratégia para lidar com essa grande complexidade na análise e no entendimento do
risco de impacto associado às mudanças climáticas, é analisar as dimensões da flor de risco
(vulnerabilidade, exposição e ameaça climática) sob um determinado contexto, denominado
aqui como Setor Estratégico (SE). Cada SE possui elementos de impacto potencial
específicos, portanto, a delimitação conceitual de cada SE é fundamental para a construção
dos indicadores e análise de risco de impacto. O AdaptaBrasil MCTI disponibiliza
informações para os SE segurança alimentar, segurança energética, portos, saúde, recursos
hídricos, dentre outros.

Assim sendo, a versão 2.0 do AdaptaBrasil implementou a nova abordagem de avaliação
dos riscos de impacto das mudanças climáticas no estudo do SE Segurança Alimentar, a
qual será detalhada a seguir.

## PDF page 12

2 DELIMITANDO O SETOR ESTRATÉGICO SEGURANÇA ALIMENTAR


As mudanças climáticas projetadas para as próximas décadas afetarão profundamente
diversos ecossistemas e setores produtivos, entre eles a agricultura. Esse setor enfrenta
uma relação direta e vulnerável com o clima, pois as variações de temperatura e precipitação
impactam diretamente a produção e a qualidade dos alimentos, além de desencadear efeitos
em toda a cadeia pós-produção (ASSAD et al., 2008). O cenário se torna ainda mais
desafiador diante do crescimento populacional, que aumenta a demanda por alimentos, ao
passo que as condições climáticas desfavoráveis ameaçam reduzir sua disponibilidade
(ASSAD et al., 2013). Essa situação ressalta a importância do conceito de Segurança
Alimentar4, particularmente em regiões onde os cultivos são altamente sensíveis ao clima
(MARENGO, 2008).

A segurança alimentar é um conceito amplo que abrange diversos setores inter-
relacionados, com destaque para a agropecuária e os fatores de segurança alimentar
propriamente ditos, que interagem de maneira encadeada. As práticas agrícolas impactam
a qualidade do solo e da água, o que, por sua vez, afeta o equilíbrio das plantas. Essas
plantas, ao serem consumidas, influenciam diretamente a saúde e o bem-estar humano e
animal, mostrando que a segurança alimentar vai além da simples disponibilidade de
alimentos: ela é fundamental para a sustentabilidade ambiental e para a saúde das
populações.

Diante dessa complexidade, surge a necessidade de representar o risco de impacto das
mudanças climáticas na segurança alimentar de forma integrada e encadeada. No
AdaptaBrasil MCTI, essa representação baseia-se nas quatro dimensões de segurança
alimentar definidas pela Organização das Nações Unidas para Agricultura e Alimentação
(FAO, sigla em inglês): Disponibilidade, Acesso, Utilização e Estabilidade – Figura 4.


4
  A Segurança Alimentar e Nutricional (SAN) consiste na realização do direito de todos ao acesso regular e permanente a
alimentos de qualidade, em quantidade suficiente, sem comprometer o acesso a outras necessidades essenciais, tendo como
base práticas alimentares promotoras de saúde, que respeitem a diversidade cultural e que sejam ambiental, cultural,
econômica e socialmente sustentáveis (BRASIL, 2006).

## PDF page 13

                  Fonte: Elaborado por Karine Rocha baseado em Kepple (2014).


                   Fonte: Elaborado por Karine Rocha baseado em FAO (2014).


              Figura 4 – Dimensões e componentes de segurança alimentar.


Cada dimensão é essencial para assegurar que todas as pessoas tenham acesso suficiente
a alimentos seguros e nutritivos, mas cada uma também responde de maneira distinta às
pressões climáticas.

## PDF page 14

Para adaptar a análise do risco climático às dimensões da segurança alimentar, foram
desenvolvidas duas estruturas hierárquicas que representam os principais aspectos em
questão: Disponibilidade de Alimentos e Acesso e Consumo de Alimentos (Figura 5). A
dimensão "estabilidade" foi incorporada como um componente essencial e transversal em
ambas as hierarquias, manifestando-se através de indicadores que refletem a constância e
a resiliência da segurança alimentar ao longo do tempo.


Figura 5 – Modelo conceitual para análise do risco de impacto das mudanças climáticas no
           Setor Segurança Alimentar desenvolvido para o AdaptaBrasil MCTI 2.0.
                              Fonte: Elaborado por Karine Rocha.


Essas hierarquias seguem o conceito de risco de impacto encadeado. No caso da
disponibilidade de alimentos, o impacto das mudanças climáticas é visto como um fenômeno
de primeira ordem, pois a influência da perturbação climática é imediata e direta, afetando
principalmente a produção de alimentos. Esse impacto reflete a vulnerabilidade e a
exposição da produção agropecuária às mudanças climáticas, onde fatores como
temperatura e padrões de precipitação podem alterar o rendimento das culturas e a saúde
do solo.

Por outro lado, o impacto sobre o acesso e consumo de alimentos é considerado secundário
ou indireto, pois depende dos efeitos climáticos sobre a disponibilidade. Aqui, o risco
climático se manifesta como uma ameaça derivada, onde a instabilidade na produção e

## PDF page 15

oferta de alimentos impacta a capacidade de acesso e o consumo, revelando o quanto esses
aspectos estão interligados. Esse entendimento permite desenvolver estratégias mais
eficazes e direcionadas para mitigar os riscos climáticos e fortalecer a resiliência do setor
alimentar, promovendo a segurança alimentar de forma abrangente e sustentável.

Para compreender como cada composição hierárquica foi abordada, apresentamos as
devidas explicações a seguir.


     2.1 Caracterização do Subsetor Disponibilidade de Alimentos


O Subsetor Estratégico de Disponibilidade de Alimentos diz respeito à capacidade de
garantir o fornecimento adequado de alimentos para toda a população, com ênfase na
produção de alimentos in natura para consumo doméstico. Para este setor, priorizou-se os
seguintes produtos agrícolas e de produção animal componentes da cesta básica brasileira
definida pelo Departamento Intersindical de Estatística e Estudos Socioeconômicos
(DIEESE): arroz, batata, feijão, mandioca, milho, trigo, leite, ovos e carnes (bovina, suína e
de aves), da qual são todos altamente dependentes de condições climáticas estáveis para
manter sua oferta.

No Brasil, a agropecuária contribui com cerca de 24,8% do Produto Interno Bruto
(Cepea/USP; CNA, 2023), sendo o mercado interno o principal destino dessa produção. No
entanto, pelo fato de grande parte do plantio agrícola e de pastagens ser de sequeiro
(CITAR), existe uma forte dependência do setor agropecuário aos fatores climáticos,
especialmente em regiões onde há alta variabilidade climática ou de eventos extremos
frequentes. Mudanças na temperatura, alterações no padrão de chuvas e a ocorrência de
eventos climáticos adversos, como secas prolongadas e tempestades intensas, afetam
diretamente a produtividade e a estabilidade do setor.

A produtividade agrícola, por exemplo, é fortemente influenciada pela disponibilidade e pela
distribuição das chuvas. Irregularidades na frequência ou intensidade das precipitações
podem reduzir a capacidade produtiva das culturas, resultando em perdas econômicas
substanciais. Em regiões semiáridas, onde o regime de chuvas é naturalmente restrito, as
secas podem levar, juntamente a outros fatores socioeconômicos e ambientais, à
desertificação e à degradação de áreas cultiváveis, tornando-as inaptas para o cultivo ao
longo do tempo. Além disso, a temperatura e a radiação solar adequadas são fatores críticos

## PDF page 16

para o desenvolvimento das culturas, variando de acordo com as características específicas
de cada espécie e região (BALDISERA; DALLACORT, 2017).

No setor pecuário, as mudanças climáticas afetam tanto a disponibilidade de recursos
naturais, como forragem e água, quanto o bem-estar animal. A redução da forragem e de
outras fontes de alimento devido à escassez hídrica ou às altas temperaturas afeta
diretamente o rendimento da pecuária. O estresse térmico, causado por temperaturas
elevadas, prejudica o metabolismo dos animais, reduzindo sua capacidade produtiva e
aumentando a vulnerabilidade a doenças (PERAZZO et al., 2013). Além disso, fatores
climáticos de excessiva pluviosidade influenciam o desenvolvimento e a proliferação de
pragas e patógenos, que podem se espalhar em novas áreas à medida que as condições se
tornam favoráveis, representando um risco crescente para plantações e rebanhos (GHINI;
HAMADA; BETTIOL, 2011).

Mudanças na distribuição geográfica dessas pragas e doenças aumentam a pressão sobre
os sistemas produtivos e exigem a intensificação das práticas de manejo, incluindo o uso de
pesticidas e medicamentos, o que, por sua vez, eleva os custos de produção e pode ter
efeitos ambientais adversos.

Além dos desafios climáticos, o subsetor de disponibilidade de alimentos enfrenta restrições
associadas a fatores econômicos, sociais e políticos associados à cada atividade em cada
região, que molda e/ou limita as condições ou estratégias de adaptação dos
estabelecimentos agropecuários e dos produtores rurais (EVANGELISTA et al, 2022). As
oscilações nos preços de insumos, como fertilizantes e rações, muitas vezes exacerbadas
por flutuações no mercado internacional, impactam diretamente a produção agrícola e
pecuária no Brasil. Esse contexto torna-se ainda mais delicado quando analisado à luz das
desigualdades regionais, que limitam o acesso a tecnologias modernas e inovações
sustentáveis, essenciais para otimizar o uso de recursos naturais e aumentar a resiliência
dos sistemas produtivos. Em áreas de agricultura familiar, que responde por uma parcela
significativa do abastecimento de alimentos básicos no país, a falta de acesso a crédito e a
assistência técnica adequada agrava a vulnerabilidade do setor a riscos climáticos e
econômicos.

Compreender a disponibilidade de alimentos, portanto, envolve não apenas a produção, mas
também a análise das interações climáticas e socioeconômicas que moldam este subsetor
e, consequentemente, a segurança alimentar no país. A capacidade de a população acessar

## PDF page 17

e consumir esses alimentos está intrinsecamente ligada a uma produção estável e resiliente,
sendo esta uma questão estratégica para assegurar a segurança alimentar no Brasil.


     2.2 Caracterização do subsetor Acesso e Consumo de Alimentos


O Subsetor Estratégico Acesso e Consumo de Alimentos engloba a garantia de que toda a
população tenha acesso econômico e físico a alimentos nutritivos, de forma segura e
socialmente aceitável. Isso inclui não apenas o abastecimento de alimentos, mas também a
redução de barreiras que dificultam seu consumo, especialmente em áreas onde o custo e
a acessibilidade dificultam o acesso a dietas saudáveis e balanceadas.

A fragilidade das estruturas alimentares se tornou evidente com crises globais recentes,
como a pandemia de COVID-19 e o conflito na Ucrânia, que prejudicaram a produção
elevando os custos dos alimentos. O número de pessoas com insegurança alimentar grave
foi cerca de 900 milhões em 2022, o que equivale a 180 milhões a mais de pessoas do que
em 2019. Ainda de acordo com relatório da FAO (2023), a comparação da insegurança
alimentar entre populações rurais, periurbanas e urbanas revela que a insegurança alimentar
global, em ambos os níveis de gravidade, é menor nas áreas urbanas e que as mulheres
são mais afetadas do que os homens em todas as regiões do mundo. Essa situação tende
a agravar-se com o crescimento populacional, as últimas projeções da ONU (2024) sugerem
que a população mundial pode crescer para cerca de 8,5 bilhões em 2030 e 9,7 bilhões em
2050. Estudos já previam que será necessário produzir entre 70% e 100% mais alimentos
até 2050 para atender à demanda global (GODFRAY et al., 2010), o que exige inovações
significativas em todas as etapas da cadeia alimentar.

Não são apenas as mudanças bruscas, como pandemias ou crises políticas, que ameaçam
a estabilidade alimentar. Pressões de longo prazo, como mudanças climáticas, degradação
do solo, crises econômicas e crescimento populacional, também influenciam de forma
crescente e contínua o sistema alimentar global (GODFRAY et al., 2010; PRETTY et al.,
2010; TENDALL et al., 2015). As pressões sociais, ambientais e de saúde sobre o
suprimento de alimentos levam ao aumento dos preços das commodities e à diminuição dos
estoques globais de alimentos (MAXWELL; SLATER, 2003; LANG; HEASMAN, 2004), o que
agrava a insegurança alimentar, especialmente entre as populações mais vulneráveis, onde
as barreiras econômicas restringem o acesso a alimentos básicos e nutritivos, exacerbando
problemas como desnutrição e até mortalidade (TENDALL et al., 2015).

## PDF page 18

Além da questão do acesso, a qualidade das dietas também é uma preocupação crescente.
A Organização Mundial da Saúde (OMS) estima que cerca de 2,7 milhões de mortes anuais
estejam relacionadas ao consumo insuficiente de frutas e hortaliças, destacando a falta de
alimentos saudáveis como um dos maiores fatores de risco para doenças globais (OMS,
2002). Dietas de baixa qualidade, deficientes em micronutrientes essenciais, têm sido
associadas ao aumento da incidência de doenças crônicas como obesidade, diabetes,
doenças cardíacas e AVC, representando uma ameaça significativa à saúde pública
(WILLETT et al., 2019). Os padrões alimentares são influenciados por uma complexa
interação de fatores biológicos, sociais, culturais e econômicos, onde o preço dos alimentos
e a renda familiar exercem grande influência sobre as escolhas alimentares.

No Brasil, a governança em segurança alimentar requer uma análise profunda das
diferenças regionais, particularmente em áreas mais afetadas por mudanças climáticas,
onde os impactos na produção agrícola podem se traduzir em dificuldades de acesso aos
alimentos (BRANDÃO, 2020). O fortalecimento dessa governança envolve considerar uma
abordagem integrada, que inclua não apenas fatores econômicos, mas também aspectos
sociais e ambientais, e que incentive a sustentabilidade das cadeias de abastecimento. Para
enfrentar esses desafios, é essencial que políticas públicas e iniciativas locais promovam a
resiliência dos sistemas alimentares, garantindo que as populações possam não apenas ter
alimentos disponíveis, mas acessá-los de maneira sustentável. Políticas de apoio ao
transporte e à logística de distribuição, programas de subsídios para alimentos básicos e
incentivos para a produção local são algumas das ações que podem reduzir as barreiras de
acesso e aumentar a segurança alimentar (BARLING; LANG, 2012; TENDALL et al., 2015).

A avaliação do risco de impacto da mudança climática na segurança alimentar exige uma
compreensão detalhada das particularidades locais e regionais para promover estratégias
mais eficazes de adaptação. Fortalecer a segurança alimentar é um desafio multifacetado
que demanda cooperação entre setores, inovação tecnológica e políticas inclusivas para
garantir que todos os indivíduos tenham acesso a uma alimentação suficiente e saudável.

Após compreender a importância e as especificidades do setor estratégico de Segurança
Alimentar, com foco nos subsetores de Disponibilidade e Acesso e Consumo de Alimentos,
faz-se necessário aprofundar a análise por meio de métricas que permitam monitorar e
avaliar de forma precisa esses elementos. O uso de índices e indicadores é fundamental
para quantificar a situação da segurança alimentar e identificar fatores de vulnerabilidade,
exposição e potencial de resiliência. No próximo tópico, exploraremos as perspectivas

## PDF page 19

teóricas sobre índices e indicadores, abordando as bases conceituais que sustentam essas
ferramentas e sua aplicação prática no contexto da segurança alimentar.


3 ÍNDICES E INDICADORES: PERSPECTIVAS TEÓRICAS


A análise de risco na edição do AdaptaBrasil MCTI 2.0 considerou a construção de uma
composição de indicadores5 e índices6 para informar e medir o comportamento ou estado de
um sistema ou fenômeno em termos de atributos expressivos e perceptíveis (OECD, 1993).
Os indicadores também podem ser considerados como variáveis indiretas, do ponto de vista
de que uma variável ou fenômeno não pode ser medido diretamente (GALLOPÍN, 1996).

Devido a essas características, os indicadores têm sido utilizados para traduzir e comunicar
fenômenos socioambientais complexos para público amplo (MAGGINO, 2017), mas
principalmente aos tomadores de decisão e gestores ambientais, visando monitorar as
metas de desenvolvimento sustentável (JANNUZZI, 2005; VAN BELLEN, 2006; MIOLLA;
SCHILTZ, 2019). Considerando que sistemas complexos, como o sistema socioecológico,
exige um entendimento interdisciplinar, ou mesmo transdisciplinar (OSTROM, 1990), o
diálogo e a comunicação entre pesquisadores e setores da sociedade de diferentes áreas
do conhecimento permite o aprofundamento do diagnóstico dos elementos de risco climático
e por conseguinte a construção de indicadores deste risco.

Toda construção de indicadores é baseada em um referencial conceitual-metodológico. A
publicação da Organização para a Cooperação e Desenvolvimento Econômico (OCDE)
(2008) e Becker (2019) propõem um marco metodológico de composição hierárquica de
indicadores e índices que dialoga com a estrutura clássica da pirâmide da informação
conforme Hammond et al. (1995). Nesta estrutura, parte-se do princípio de que dados


5
  Trata-se de uma simplificação de informações mais relevantes de um sistema/fenômeno complexo visando facilitar o
processo de comunicação objetiva para um público alvo, que geralmente está associado a alguma tomada de decisão sobre
esse sistema (VAN BELLEN, 2006). De acordo com Tunstall (1992), as principais funções dos indicadores são: avaliação
de condições e tendências; comparação entre lugares e situações; avaliação de condições e tendências em relação às metas
e aos objetivos; prover informações de advertências, e; antecipar futuras condições e tendências.
6
 Valor agregado final de todo um procedimento de cálculo onde se utilizam, inclusive, indicadores como variáveis que o
compõem (SICHE et al., 2007).

## PDF page 20

observados de forma isolada não retratam um fenômeno multidimensional ou complexo e,
sendo assim, a informação sintética comunica de forma mais objetiva padrões do fenômeno,
principalmente para o público amplo, mas também permite direcionar melhor recursos e
ações de tomadores de decisão (JANNUZZI, 2006) – Figura 6.


                            Figura 6 – Pirâmide da informação.
                           Fonte: Adaptado de Hammond et al. (1995).


Todavia, a ideia não se trata apenas de comunicar a informação sintética em forma de
índices – o topo da pirâmide – mas sim de apresentar a composição hierárquica da
informação, de forma que se possa ter uma leitura analítica da composição da pirâmide. Este
tipo de leitura pode alinhar informações sintéticas, que apontam um estado mais grave do
fenômeno, com elementos de forças e pressões tangíveis que promovem tal estado. Este
tipo de tratamento da informação é útil para tomadores de decisão, pois precisam de
informações sinóticas de forma preliminar para agilizar análises focais e poder responder ou
se adaptar às ameaças, neste caso, de mudanças climáticas (MEADOWS, 1998; JACOB;
BLAKE, 2010).


4 ÍNDICE DE RISCO DE IMPACTO ÀS MUDANÇAS CLIMÁTICAS PARA SEGURANÇA
   ALIMENTAR

## PDF page 21

O risco de impacto às mudanças climáticas é o resultado emergente da interação entre suas
dimensões, que, por sua vez, estão associadas intrinsecamente às mudanças nos fatores
de pressão (indicadores) a que são submetidas. Neste sentido, optou-se por elaborar um
sistema de índices e indicadores que fosse capaz de captar as relações de causalidade e
influência desses fatores. Essa metodologia incluiu diferentes métodos de análises
(pesquisa bibliográfica, sistema de informações geográficas, análise estatística, etc.), além
de análises em múltiplas escalas espaciais (nacional, regional, estadual e municipal) e
temporal (intervalo de análise decadal), com múltiplos fatores estressores.

A estrutura de construção da informação foi baseada na pirâmide da informação - abordada
no capítulo anterior - dentro do escopo das dimensões de risco, conforme IPCC (2015). Para
tanto, foram consideradas informações desde dados brutos, indicadores, indicadores
temáticos, índices das dimensões do risco de impacto climático e o índice de risco de
impacto climático. Estas informações estão situadas em níveis da composição da informação
hierárquica, conforme Figuras 7 e 8 das quais representam as hierarquias de disponibilidade
de alimentos e acesso e consumo de alimentos, respectivamente.


Figura 7 – Estrutura hierárquica entre as composições de indicadores e índices de risco de
          impacto das mudanças climáticas no subsetor de disponibilidade de alimentos.
                               Fonte: Elaborado por Karine Rocha.

## PDF page 22

Figura 8 – Estrutura hierárquica entre as composições de indicadores e índices de risco de
          impacto das mudanças climáticas no acesso e consumo de alimentos.
                              Fonte: Elaborado por Karine Rocha.


O nível 6 representa informações (variáveis) utilizadas para a composição de cálculo de
indicadores, cujos dados são extraídos a partir de fontes primárias e/ou secundárias. Esta
camada de informação é denominada como dado bruto e não é apresentada na plataforma
AdaptaBrasil MCTI. O dado bruto passa por tratamentos numéricos, tais como, tratamento
de outliers, normalizações, possível inversão de valores e ponderações. O propósito é que
se tenha uma unidade numérica única entre todos os indicadores e que o significado do
indicador possa ser representado na sua respectiva dimensão de risco climático. Ao passar
por essas transformações numéricas, o dado bruto passa a ser denominado como indicador
simples (ou indicador) e integra a informação mais elementar da Plataforma de nível 5.

A construção de indicadores e índices de risco climático na plataforma segue foram
consideradas três esferas de entendimento: (i) sistema socioecológico; (ii) Setor
Estratégico, e (iii) tipo de perturbação climática a que o sistema socioecológico e setor
estratégico são passíveis de serem submetidos – ameaça climática.

## PDF page 23

Os sistemas socioecológicos (SSE) foram conceituados no primeiro capítulo. Os
estudos em SSE têm canalizado três tipos de visões: (i) como os subsistemas
ecológicos podem suprir serviços ecossistêmicos para as necessidades e bem-estar
humano; (ii) como as demandas humanas e a obtenção de recursos ecossistêmicos
podem determinar a integridade do subsistema ecológico, e (iii) como os dois
subsistemas podem responder de forma integrada às forças endógenas e exógenas de
mudanças do sistema socioecológico (BERRÖUET; MACHADO; VILLEGAS-PALACIO,
2018). Nesta última abordagem houve avanços sobre a vulnerabilidade e respostas
dos SSE em relação às mudanças climáticas e fenômenos naturais. Na plataforma
AdaptaBrasil, os SSE têm sido o grande palco de entendimento sistêmico de
vulnerabilidades    e    riscos   associados     às   possíveis   ameaças     climáticas,   mas
considerando um determinado setor estratégico objeto de impacto potencial.

Apesar dos SSE ser um arcabouço sistêmico a ser perseguido, a avaliação de riscos
climáticos deve ter um direcionamento para políticas públicas e setores de decisão da
sociedade, que, na sua grande maioria, se apresentam de forma setorizada. Além disso, a
construção de uma estrutura hierárquica de composição de indicadores e índices é por si
um esforço de síntese de um sistema que é complexo. Nesse sentido, a avaliação de riscos
climáticos por setores estratégicos é providencial para que a informação possa alcançar os
diferentes atores desses setores. Conforme Jones e Boes (2004), a avaliação dos riscos
climáticos pode ser calcada na vulnerabilidade do sistema e partir daí, identificar as ameaças
envolvidas. Nesse caso, a vulnerabilidade do sistema é direcionada por Setores Estratégicos
no AdaptaBrasil.

Os objetos concretos de risco de impacto climático que são de interesse do
Estado são, por exemplo, sociedade, recursos naturais, infraestruturas, seguranças,
ativos,   acessos    e   economia.   Tais   objetos    são   passíveis   de   sofrer   impactos
negativos relevantes provocados por perturbações climáticas – fator exógeno – e pelas
características intrínsecas do objeto de impacto, vulnerabilidade e exposição - fatores
endógenos. Cada Setor Estratégico no AdaptaBrasil MCTI possui seus objetos de análise
de risco climático. Os primeiros Setores Estratégicos a serem considerados na plataforma
AdaptaBrasil        no      ano      de        2018     foram      Água,       Alimentos      e
Energia, na perspectiva de segurança. Desde então a Plataforma tem buscado priorizar os
setores contemplados na Política Nacional de Adaptação do ano de 2016 e, mais
recentemente, no Plano Clima - Adaptação, tais como: Agricultura, Recursos Hídricos,
Segurança Alimentar e Nutricional, Biodiversidade, Cidades, Gestão de Riscos e Desastres

## PDF page 24

Geo-hidrológicos, Indústria e Mineração, Infraestrutura, Povos e Populações Vulneráveis,
Saúde e Zonas Costeiras. Este documento trata sobre o SE Segurança Alimentar que
foi desenvolvido pelo INPE para a versão AdaptaBrasil 2.0.

O terceiro elemento fundamental para a delimitação do risco climático é o tipo de
perturbação ou ameaça climática que está sendo considerada que afeta ou possa
afetar o SSE em um dado setor estratégico. A Plataforma apresenta o risco de impacto
climático, e sua construção hierárquica de indicadores, para uma ameaça climática
específica de forma separada direta, por exemplo, seca, chuvas intensas, ondas de
calor, ventos, dentre outros; ou de forma separada indireta, como os eventos
hidrológicos. A ameaça climática é codificada na plataforma por um índice final
climático, resultante de uma composição de indicadores climáticos, não havendo
indicadores temáticos intermediários, conforme ilustração da Figura 7. Na versão
AdaptaBrasil 2.0, conforme já explicado anteriormente, apenas no subsetor
Disponibilidade de Alimentos será utilizada a ameaça climática direta (Seca) por se
tratar de o impacto de primeira ordem.


Por fim, cada índice de risco climático na plataforma – nível 1 – deve ser entendido como
uma magnitude potencial de impacto climático ao se concretizar o contato do SSE – com
sua vulnerabilidade intrínseca - com a perturbação climática – com a sua tendência implícita.
Não se deve compreender esse índice como a probabilidade de ocorrência de impacto
climático. A construção dos valores de indicadores e índices de risco climático, que culmina
no índice de risco climático, está diretamente associada a um Setor Estratégico e a uma
determinada ameaça climática.


     4.1 Ameaças climáticas


No momento, a Plataforma possui um conjunto de indicadores e índices de vulnerabilidade
e exposição (indicadores socioecológicos) situados no presente e de ameaças climáticas
situados no presente e projetados para o futuro, que se conectam/associam conforme
representado no esquema da Figura 9.

## PDF page 25

Figura 9 – Integração das dimensões de ameaça climática com vulnerabilidade e exposição
           na avaliação do risco climático: presente e cenários futuros.
                     Fonte: Elaborado por Karine Rocha e Gustavo Arcoverde.


No contexto dos indicadores socioecológicos, o termo "presente" denota dados oriundos das
décadas de 2010 e 2020, conforme seja o Setor Estratégico, levando em consideração a
versão mais recente dos dados oficiais disponíveis. Em relação aos dados climáticos, o
termo "presente" está vinculado à média do período histórico (1986 – 2005), enquanto as
projeções abrangem os períodos 2030 (2021-2040) e 2050 (2041-2060).

Para a determinação dos cenários climáticos adotados na Plataforma, foram considerados
os cenários de emissões do Quinto e Sexto Relatório de Avaliação do Painel
Intergovernamental sobre Mudanças Climáticas (AR5/IPCC). Esses cenários incorporam
trajetórias plausíveis de concentração, conhecidas como Representative Concentration
Pathways (RCPs), abrangendo emissões de gases de efeito estufa, emissões de poluentes

## PDF page 26

atmosféricos e mudanças no uso da terra. Os esforços de mitigação são representados pelos
cenários RCP 4.5, caracterizado como intermediário (considerado como Cenário Otimista),
e RCP 8.5, identificado como um cenário de alta emissão de gases de efeito estufa
(denominado Cenário Pessimista).


              4.1.1    Construção de indicadores e índices de Ameaças Climáticas para o
                       Subsetor de Disponibilidade de Alimentos


A seca meteorológica7 é um evento climático extremo podendo gerar perdas e danos
significativos para a sociedade e para os ecossistemas. Dentre os inúmeros métodos e
índices utilizados na identificação/caracterização de episódios de seca foram selecionados
dois indicadores para compor o índice de seca, sendo estes o número de dias secos
consecutivos (DSC) e o índice padronizado de precipitação-evapotranspiração (SPEI).

O número de dias secos consecutivos consiste em avaliar o número máximo de dias com
precipitação inferior a 1mm ao longo do ano. Já o índice padronizado de precipitação-
evapotranspiração avalia a disponibilidade hídrica, a qual depende tanto do volume
precipitado quanto das condições atmosféricas, tais como radiação solar, temperatura,
magnitude do vento e umidade relativa. O SPEI foi calculado a partir da diferença mensal
entre a precipitação e a evapotranspiração potencial (ETP).

Os valores do SPEI utilizados para o cálculo deste indicador foram aqueles inferiores a -0.5
(valor limite para caracterização de eventos de seca fraca). Valores como -1, -1.5 e inferiores
a -2 caracterizam eventos moderados, severos e extremamente secos, respectivamente.
Desta forma, os valores superiores a -0.5 foram desconsiderados e a eles foi atribuído o
valor NA (Not Available), visto que os mesmos caracterizam normalidade ou excessos de
chuvas quando ponderada a precipitação.

Para o cálculo do índice de seca foi efetuada a média aritmética simples entre os indicadores
normalizados, sendo estes o número de dias secos consecutivos e o índice de precipitação-
evapotranspiração padronizado. Foram utilizados dados climáticos provenientes do Projeto


7
 Considera-se seca meteorológica como um período prolongado — uma estação, um ano ou vários anos — de precipitação
deficiente em comparação com a média multianual estatística para uma região que resulta em escassez de água para alguma
atividade, grupo ou setor ambiental (NDAYIRAGIJE; LI, 2022).

## PDF page 27

CORDEX, o qual consiste em efetuar o processo de downscaling dinâmico de modelos
globais do CMIP5 (Coupled Model Intercomparison Project Phase 5) como condições de
contorno para realizar a regionalização de projeções climáticas, empregando modelos
regionais, com o objetivo de aumentar o nível de detalhamento horizontal e vertical das
forçantes atmosféricas utilizadas. Diversos institutos de pesquisa efetuaram avaliações e
disponibilizaram seus resultados para fins de comparação e melhor entendimento do sistema
climático e as possíveis mudanças a ele associados. Na Tabela 1 são apresentados os
institutos de pesquisa responsáveis pelas avaliações referentes à América do Sul. Outras
informações como a resolução horizontal, o país de origem e a sigla também estão contidas
para o melhor entendimento dos procedimentos adotados na Plataforma AdaptaBrasil MCTI.

A Tabela 2 apresenta o conjunto de modelos regionais que foram utilizados, bem como o
link de acesso para maiores informações e o instituto que o desenvolveu. O uso de diversos
modelos regionais permite avaliar o nível de espalhamento entre as respostas obtidas dos
cenários futuros e assim minimizar as incertezas quanto aos resultados. Já a Tabela 3
apresenta o conjunto de forçantes globais disponibilizadas para a América do Sul, sua
resolução horizontal original, o instituto que a produziu e o modelo regional utilizado.
Baseado nesse conjunto de experimentos foram efetuados os cálculos dos indicadores
climáticos utilizados na plataforma AdaptaBrasil MCTI. A manipulação efetuada nesse
conjunto de informações é melhor detalhada nos esquemas 1, 2 e 3 apresentados abaixo.

## PDF page 28

Tabela 1 – Instituições de Pesquisas e Serviços Climáticos integrantes do Projeto CORDEX.


                             Fonte: Elaborado por George Ulguim.


Tabela 2 – Modelos Regionais utilizados no Projeto CORDEX com enfoque na América do
          Sul.


                             Fonte: Elaborado por George Ulguim.

## PDF page 29

Tabela 3 – Conjunto de Forçantes Atmosféricas utilizadas no Projeto CORDEX.


                             Fonte: Elaborado por George Ulguim.


A primeira atividade destinou-se ao download das variáveis climáticas tanto para o período
histórico como para os RCPs 2.6, 4.5 e 8.5. Pela pouca quantidade de informação disponível

## PDF page 30

no RCP 2.6 o mesmo não foi utilizado. As informações que foram adquiridas são referentes
a seguintes variáveis, as informações entre parênteses são as siglas a estas associadas:
temperatura máxima (tasmax), temperatura mínima (tasmin), temperatura média (tas),
precipitação (pr), evapotranspiração (evspsblpot), runoff (mrro), as componentes zonal e
meridional do vento a 100 metros de altitude (ua100m e va100m), umidade relativa (hurs).

A fim de utilizar dados climáticos na frequência diária no cálculo dos indicadores climáticos
é necessário que o calendário que o rege contemple 365 dias. No caso dos experimentos
utilizados apenas a forçante HadGEM2-ES utiliza o calendário com 360 dias e como
apresentado na Figura 10 foi necessário efetuar a conversão em todos os experimentos e
variáveis que derivam desta forçante, obtendo assim experimentos com calendários
compatíveis.


        Figura 10 – Identificação e conversão de calendário, de 360 dias para 365.
                              Fonte: Elaborado por George Ulguim.

## PDF page 31

Nessa primeira etapa foi identificado que além da divergência entre os calendários, a
diferença de tempos em cada arquivo, a diferença na disposição espacial (tipo de
coordenadas geográficas) e a resolução horizontal, como apresentado na Tabela 3. A
questão temporal e o tipo de sistema de coordenadas são evidenciados quando se manipula
informações de diferentes institutos, isto é, cada instituição utiliza um recorte temporal
variando entre 1 e 5 anos e um sistema de coordenadas distinto. Considerando a
necessidade de os resultados serem comparáveis, a alternativa foi utilizar a conversão para
o sistema de coordenadas retangular (latitude, longitude) em todos os experimentos, bem
como a concatenação dos arquivos tanto para o período histórico quanto para os RCPs 4.5
e 8.5. A partir deste ponto temos à disposição séries temporais longas o suficiente para
serem utilizadas nos cálculos e seus resultados são comparáveis entre si, como apresentado
na Figura 11.


Figura 11 – Sistema prático para equiparação de experimentos climáticos e construção de
           Ensemble Mean.
                             Fonte: Elaborado por George Ulguim.

## PDF page 32

Outra questão bastante pertinente, quando se pretende produzir um experimento sintético
através do método de ensemble, está associado à resolução horizontal dos membros
utilizados, isto é, todos os membros devem ter a mesma configuração.

A Figura 12 retrata os procedimentos necessários para atender às solicitações internas e
instituições parceiras.


Figura 12 – Preparação e entrega de produtos climáticos solicitados junto a equipe interna
             do AdaptaBrasil MCTI.
                             Fonte: Elaborado por George Ulguim

## PDF page 33

Ao falar-se de variáveis secas e úmidas, nesse sentido, estamos falando na verdade de
variáveis com avaliações diferentes como valores médios e acumulados. No nosso caso as
variáveis secas são: tasmax, tasmin, tas, ua100m, va100m e hurs; já as variáveis úmidas
são: pr, evspsblpot e mrro. Após essa divisão foram os indicadores climáticos de
precipitação, temperatura máxima, média e mínima na frequência anual, sendo
aproximadamente 30 indicadores derivados destas quatro variáveis. Outros indicadores
foram calculados, tais como Densidade de Potência (magnitude do vento), Índice
Padronizado de Precipitação-Evapotranspiração (SPEI), Índice Padronizado de Precipitação
(SPI).

Após o preparo das informações deu-se início ao recorte solicitado (município, parques
eólicos, bacias hidrográficas) e nas frequências temporais desejadas (diário, mensal, anual).
Tais informações foram entregues em formato ASCII.


     4.2 Vulnerabilidade e Exposição


Para fins didáticos, a metodologia de obtenção dos dados de vulnerabilidade e exposição e
cálculo hierárquico de valores foi dividida em 4 etapas – Figura 13: (4.2.1) Identificação e
pré-seleção dos indicadores candidatos; (4.2.2) Construção numérica e seleção dos
indicadores simples; (4.2.3) Cálculo dos indicadores temáticos, índices parciais e final; e
(4.2.4) Cálculo dos fatores influenciadores. As fases de identificação e construção numérica
de indicadores simples e temáticos e de índices segues vários preceitos metodológicos de
composição de indicadores e índices de Becker et al. (2019) e OCDE (2008).


          4.2.1   Identificação e pré-seleção dos indicadores candidatos


Inicialmente, o levantamento dos indicadores candidatos teve como base o conjunto final da
versão 1.0. Naquela etapa, os indicadores foram selecionados a partir de estudos científicos
já realizados no Brasil, fundamentados em artigos e publicações técnicas que atendessem
aos requisitos teóricos e operacionais relacionados aos aspectos de vulnerabilidade, impacto
e adaptação. No entanto, também foram considerados alguns critérios técnicos mínimos,
como: disponibilidade de dados em fontes oficiais e de acesso público; representatividade

## PDF page 34

preferencialmente em escala municipal; e possibilidade de atualização em diferentes
recortes temporais.

Para a versão 2.0, foi realizada uma pesquisa bibliográfica complementar com o objetivo de
preencher lacunas identificadas na seleção de indicadores para cada subsetor temático —
Disponibilidade de Alimentos e Acesso e Consumo de Alimentos. Essa etapa visou ampliar
a base conceitual e garantir maior coerência e robustez na representação dos aspectos
específicos de cada dimensão.

A pré-seleção dos indicadores do Subsetor de Disponibilidade de Alimentos foi conduzida
durante uma oficina presencial realizada em Brasília, em maio de 2023, com a participação
de representantes do Ministério da Ciência, Tecnologia e Inovação (MCTI), da Empresa
Brasileira de Pesquisa Agropecuária (Embrapa) e do Instituto Nacional de Pesquisas
Espaciais (INPE). Já para o Subsetor de Acesso e Consumo de Alimentos, o processo
ocorreu em uma reunião remota em outubro de 2023, contando com representantes do
Instituto Nacional do Semiárido (INSA), da Companhia Nacional de Abastecimento (Conab)
e também do INPE. Em ambas as ocasiões, os especialistas convidados colaboraram na
seleção e alocação dos indicadores, buscando assegurar a adequação conceitual e temática
às respectivas dimensões, com base na caracterização do setor estratégico em análise e na
relevância nacional e/ou regional dos indicadores propostos.

O sistema de índices e indicadores adotado para a avaliação de risco em cada subsetor, em
razão da natureza multidimensional dos impactos, não se limita às forçantes climáticas. Ele
também incorpora fatores de vulnerabilidade e exposição específicos de cada contexto
setorial. No caso do Subsetor de Disponibilidade de Alimentos, foram considerados fatores
diretamente relacionados à produção e à produtividade agropecuária, como: aspectos
edáficos, de manejo, instrumentos financeiros e políticas públicas, armazenamento de
alimentos, aspectos econômicos e potencial de intensificação da produção, dependência
econômica local às atividades agropecuárias, exposição de áreas produtivas e distribuição
fundiários.

Para o Subsetor de Acesso e Consumo de Alimentos, os fatores condicionantes analisados
foram predominantemente socioeconômicos, incluindo: perfil da população, infraestrutura
básica, saúde e consumo dos alimentos, instrumentos financeiros e políticas públicas,
capacidade socioeconômica, exposição da população e infraestrutura logística e de acesso
a mercados.

## PDF page 35

O banco de dados construído reuniu informações provenientes de fontes secundárias,
extraídas de bases institucionais consolidadas. Para cada variável considerada, foi realizada
uma análise rigorosa da qualidade e da consistência dos dados disponíveis, assegurando a
confiabilidade das informações utilizadas. Como resultado, o banco passou a integrar
conteúdos quantitativos e qualitativos robustos, aptos a sustentar uma avaliação técnica
precisa e detalhada. Essa base sólida de dados constitui um pilar essencial para o
desenvolvimento das etapas subsequentes do estudo.

Entre as principais instituições consultadas estão:


Subsetor de Disponibilidade de Alimentos


    ● Instituto Brasileiro de Geografia e Estatística (IBGE);
    ● Agência Nacional de Águas (ANA);
    ● 4ª Comunicação Nacional do Brasil/Ministério da Ciência, Tecnologia e Inovação
        (4CN/MCTI);
    ● Instituto Nacional de Pesquisas Espaciais (INPE);
    ● Laboratório de Processamento de Imagens e Geoprocessamento/Universidade
        Federal de Goiás (Lapig/UFG);
    ● Centro de Gestão e Estudos Estratégicos (CGEE);
    ● Comissão Pastoral da Terra (CPT);
    ● Empresa Brasileira de Pesquisa Agropecuária - Solos (Embrapa Solos);
    ● Portal da Transparência da Controladoria-Geral da União (CGU);
    ● Ministério do Desenvolvimento Agrário e Agricultura Familiar (MDA);
    ● Ministério da Agricultura e Pecuária (Mapa);
    ● Empresa Brasileira de Pesquisa Agropecuária (Embrapa);
    ● Companhia Nacional de Abastecimento (Conab);
    ● Ipeadata/ Instituto de Pesquisa Econômica Aplicada (Ipea);
    ● Projeto de Mapeamento Anual da Cobertura e Uso do Solo no Brasil (MapBiomas);
    ● Banco Central do Brasil (BCB);
    ● Secretaria     Especial do     Desenvolvimento    Social/   Ministério   da   Cidadania
        (SEDS/MC);
    ● Trabucco e Zomer (2019);
    ● Bezerra et al. (2020);

## PDF page 36

    ● Coordinated Regional Climate Downscaling Experiment (CORDEX).


Subsetor de Acesso e Consumo de Alimentos


    ● Instituto Brasileiro de Geografia e Estatística (IBGE);
    ● Programa das Nações Unidas para o Desenvolvimento (PNUD);
    ● Agência Nacional de Águas (ANA);
    ● Secretaria de Avaliação e Gestão da Informação Ministério da Cidadania (SAGI/MC);
    ● Secretaria Especial de Agricultura Familiar e do Desenvolvimento Agrário
        (SEAD/DGMA);
    ● Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP);
    ● Informações da Agricultura Familiar da Companhia Nacional de Abastecimento
        (GEIAF/Conab)
    ● Departamento de informática do Sistema Único de Saúde (DATASUS);
    ● Portal da Transparência da Controladoria-Geral da União (CGU);
    ● Secretaria      Especial do    Desenvolvimento     Social/   Ministério   da   Cidadania
        (SEDS/MC).


Após a organização das variáveis candidatas em um banco de dados, foi realizada uma
avaliação inicial das características estatísticas de cada dado com o objetivo de identificar a
distribuição e variações dos dados para cada subsetor, conforme pode-se observar na etapa
a seguir.


             4.2.2   Construção numérica e seleção dos indicadores simples


A construção numérica dos indicadores simples, que compõem as dimensões de
vulnerabilidade e exposição, seguiu os procedimentos metodológicos representados na
Figura 13.

## PDF page 37

Figura 13 – Organograma das etapas de construção numérica e seleção dos indicadores simples do SE Segurança Alimentar.
                                      Fonte: Elaborado por Naurinete Barreto e Gustavo Arcoverde.

## PDF page 38

A geração dos indicadores simples obedece a um protocolo sistemático de transformações
numéricas aplicadas aos dados brutos de entrada. Esses dados são classificados em duas
categorias: dados discretos (identificados como scores) e dados contínuos (numéricos).

No caso dos dados discretos, os valores são diretamente atribuídos com base em limites
definidos para cada indicador, geralmente variando entre um mínimo e um máximo —
comumente 0 e 1, respectivamente. No entanto, esses limites podem ser ajustados conforme
a lógica de associação entre o desempenho do indicador e o tema ou dimensão a que
pertence. Por exemplo, podem ser utilizados limiares como 0,3 para o valor mínimo e 0,7
para o valor máximo. Nesses casos, o indicador simples recebe esses valores diretamente,
sem a necessidade de outras transformações numéricas.

Os dados numéricos passaram por etapas sucessivas de verificação de outliers, aplicação
de winsorização total (quando necessário) e avaliação de curtose e distorção. Quando
identificadas distorções, aplica-se a transformação Box-Cox antes da normalização final.
Esse fluxo metodológico assegura a consistência estatística e a comparabilidade entre os
indicadores utilizados na composição das dimensões de análise. Os critérios individuais de
aplicação de cada etapa serão explicados abaixo.


      a) Identificação e tratamento de valores outliers (winsorization)


O cálculo dos indicadores em cada subsetor passa por um tratamento inicial que verifica a
presença de outliers nos dados, ou seja, valores que se encontram fora do padrão normal
de uma distribuição (TUKEY, 1977; SMITI, 2020). A existência de valores extremos em uma
variável pode comprometer a precisão dos procedimentos estatísticos, causar perda de
informações relevantes ou até distorcer o resultado final.

O método consiste na substituição dos valores extremos pelos valores válidos mais próximos
dentro dos limites definidos pelo intervalo interquartil (IQR). Ele é recomendado
principalmente quando os outliers correspondem a uma pequena proporção do total de
observações — aproximadamente até 5% das unidades.

A identificação de outliers foi realizada com base no método do intervalo interquartil (IQR),
uma técnica robusta e amplamente utilizada em análises estatísticas. As fórmulas aplicadas
foram as seguintes:

## PDF page 39

                                       𝐼𝑄𝑅 = 𝑄3 − 𝑄1
      𝐿𝑖𝑚𝑖𝑛𝑓 = 𝑄1 − 1,5 ∗ 𝐼𝑄𝑅                    𝑄1 = 𝑃𝐸𝑅𝐶𝐸𝑁𝑇𝐼𝐿(𝑋1 : 𝑋𝑛 ; 0,25)

      𝐿𝑖𝑚𝑠𝑢𝑝 = 𝑄3 + 1,5 ∗ 𝐼𝑄𝑅                    𝑄3 = 𝑃𝐸𝑅𝐶𝐸𝑁𝑇𝐼𝐿(𝑋1 : 𝑋𝑛 ; 0,75)

Onde: IQR é o valor do intervalo interquartil; Liminf é o valor do limite inferior para identificação
       de outliers; Limsup é o valor do limite superior para identificação de outliers; Q1 é o
       valor médio do primeiro quartil; Q3 é o valor médio do terceiro quartil; X 1 é o valor da
       variável X no primeiro município da série; Xn é o valor da variável X no último município
       da série.


Valores que ultrapassam esses limites são classificados como outliers estatísticos e,
portanto, passíveis de tratamento. Neste processo foi utilizada a técnica de Winsorization,
onde valores situados acima do limite superior do intervalo interquartil (IQR) foram ajustados
para o próprio valor deste limite. Da mesma forma, valores que se encontram abaixo do limite
inferior do IQR foram redefinidos para o limite inferior correspondente. Assim:


                            𝐼𝑗𝑝 = 𝐿𝑖𝑚𝑠𝑢𝑝         e    𝐼𝑗𝑚 = 𝐿𝑖𝑚𝑖𝑛𝑓

Este procedimento garante um tratamento criterioso de valores atípicos, equilibrando a
preservação da informação original com a necessidade de manter a robustez e a
confiabilidade dos indicadores utilizados nas análises.

A aplicação desse método mostrou-se adequada ao contexto, dado que as séries de dados
associadas a cada subsetor frequentemente apresentam distribuições não normais,
refletindo a variabilidade inerente a fatores climáticos, econômicos e sociais.


       b) Avaliação da curtose e distorção dos dados e aplicação do Box-cox


A avaliação da distribuição dos dados é uma etapa fundamental para garantir a consistência
estatística dos indicadores utilizados, especialmente em processos que envolvem
normalização e combinação de variáveis. Nesse contexto, foram analisadas duas medidas

## PDF page 40

descritivas essenciais: distorção (ou assimetria) e curtose, que permitem avaliar a forma da
distribuição dos dados em relação à distribuição normal.

A distorção mede o grau de simetria da distribuição de uma variável em torno de sua média.
Uma distribuição perfeitamente simétrica apresenta valor de assimetria igual a zero. Valores
positivos indicam que a cauda da distribuição está deslocada para a direita (assimetria
positiva), enquanto valores negativos indicam deslocamento para a esquerda (assimetria
negativa). Assimetrias acentuadas podem comprometer a interpretação e a robustez de
análises estatísticas baseadas em pressupostos de normalidade, além de indicar
concentração de valores em um dos extremos da série.

A curtose, por sua vez, está relacionada à altura e à forma da curva da distribuição. Quando
uma distribuição possui uma aparência semelhante à da distribuição normal, diz-se que ela
tem uma curtose padrão (valor igual a 3). Valores superiores a 3,5 indicam distribuições com
curvatura muito alongada e maior concentração de valores extremos nas caudas
(leptocúrticas), enquanto valores inferiores podem indicar distribuições mais achatadas
(platicúrticas). Curtoses elevadas sugerem variabilidade atípica que pode influenciar
desproporcionalmente os resultados e obscurecer padrões relevantes.

Além dessas medidas, a presença de outliers tem papel importante na decisão de
transformar os dados. A transformação Box-Cox é especialmente indicada quando a
distribuição apresenta forte assimetria, caudas pesadas e elevada proporção de valores
extremos. Isso porque os outliers, quando numerosos, afetam significativamente a média e
a variância, prejudicando análises que dependem desses parâmetros. Nessas situações,
técnicas simples como a Winsorization podem não ser suficientes para corrigir as distorções
da distribuição, sendo necessário aplicar uma transformação mais abrangente, como a Box-
Cox, que suaviza o impacto dos valores extremos e melhora a aproximação da distribuição
à normalidade.

A aplicação da transformação Box-Cox é realizada nos dados brutos (Nível 5), considerando
alguns critérios presentes nos dados que já passaram por winsorization:

   •   A proporção de outliers deve ser superior a 5%, indicando que o simples tratamento
       por Winsorization não seria suficiente para estabilizar a distribuição;
   •   O valor de distorção deve estar acima de 2 e valor de curtose deve ser superior a 3,5,
       evidenciando uma distribuição inclinada e sinalizando a presença de caudas
       extremas, respectivamente.

## PDF page 41

Indicadores que atendem o primeiro ou o segundo critério foram submetidos à transformação
Box-Cox, com o objetivo de melhorar a aderência à normalidade e aumentar a
comparabilidade entre variáveis. Esse procedimento contribui significativamente para a
homogeneização do banco de dados e para a confiabilidade das análises posteriores.


      c) Normalização dos dados


Para garantir a consistência e a comparabilidade dos dados, aplica-se a normalização,
transformando-as em uma escala que varia entre zero e um. Este procedimento faz parte do
processo de composição de indicadores, pois gera uma unidade comum (adimensional) e
uma escala de valores comum. Isso facilita a comunicação, a comparação e a composição
de diferentes indicadores, possibilitando a construção de uma hierarquia de classes de risco
de impacto para os municípios estudados. Assim, valores mais próximos de zero indicam
situações de menor risco, enquanto valores mais próximos de um representam condições
mais críticas, conforme a metodologia adaptada de Lima et al. (2009).

Nesta perspectiva, para a normalização das variáveis selecionadas utilizou-se a seguinte
expressão matemática, quando o indicador tem relação direta com a dimensão a que
pertence:

                                              𝐼𝑎𝑖 − 𝐼𝑗𝑚
                                      𝐼𝑗𝑖 =
                                              𝐼𝑗𝑝 − 𝐼𝑗𝑚

Onde: Iji é o valor normalizado do indicador j no i-ésimo município; Iai é o valor do indicador

      no i-ésimo município; Ijp representa o valor do indicador j no município em pior

      situação; Ijm é o valor do indicador j no município em melhor situação.


Em algumas situações, o indicador pode apresentar uma relação inversa com a dimensão
que ele representa, ou seja, valores mais elevados podem reduzir o valor final do índice ou
indicador temático. Nesses casos, é necessário realizar um ajuste nos dados normalizados
para garantir que eles estejam alinhados com a respectiva dimensão de risco climático. Esse
ajuste visa facilitar a interpretação do indicador, de modo que os maiores valores sempre

## PDF page 42

reflitam um aumento no risco da dimensão à qual o indicador está associado, tornando a
leitura mais intuitiva e coerente.


       d) Análise de correlação dos indicadores candidatos


A análise de correlação entre os indicadores candidatos teve como objetivo identificar
possíveis redundâncias e aprimorar a qualidade e parcimônia do conjunto final de variáveis.
Após a construção e normalização do banco de dados preliminar, foi aplicada a correlação
de Spearman entre os pares de indicadores, a fim de detectar sobreposições informacionais.
Coeficientes de correlação iguais ou superiores a 0,6 foram considerados indicativos de alta
correlação, sinalizando potenciais redundâncias e, portanto, a necessidade de análise para
possível exclusão.

A seleção dos indicadores a serem excluídos foi orientada por três critérios hierárquicos e
objetivos, com o intuito de preservar tanto a representatividade temática quanto a integridade
das dimensões analíticas?

   •   Critério 1: avaliação da correlação entre indicadores entre diferentes dimensões,
       buscando eliminar redundâncias internas sem comprometer a coerência conceitual
       do grupo;
   •   Critério 2: avaliação da correlação entre indicadores pertencentes a um mesmo
       grupo temático, buscando eliminar redundâncias internas sem comprometer a
       coerência conceitual do grupo;
   •   Critério 3: avaliação da totalidade da hierarquia de indicadores, permitindo a
       exclusão de variáveis com menor relevância relativa na estrutura geral do modelo.

Como resultado desse processo de filtragem cuidadoso e técnico, apenas um número restrito
de indicadores foi excluído, garantindo a robustez e a consistência do modelo analítico.

A lista final dos indicadores selecionados, organizados por subsetor, encontra-se detalhada
no Apêndice A.


       e) Elaboração e aplicação de “máscaras”

## PDF page 43

No Subsetor de Disponibilidade de Alimentos, diferentemente de uma composição de
indicadores comum, foi preciso realizar um refinamento dos dados com o objetivo de garantir
que alguns indicadores refletissem com maior precisão a relevância da agropecuária em
cada município, especialmente no que se refere à produção de alimentos. Para isso, foi
analisado cada caso para a elaboração e aplicadas de máscaras para certos indicadores
simples. Foram considerados dois tipos de máscara:

   ● Máscara 1: exclusão (recorte) de municípios com baixa representatividade nos
      aspectos agropecuários de interesse, atribuindo-se a eles valores 'NA' (do inglês Not
      Available, ou Não Disponível);

   ● Máscara 2: ranqueamento dos municípios com base nos valores da produção de
      alimentos. Essa máscara atua como um fator de ponderação, ajustando o peso de
      indicadores originalmente construídos com representação estadual.


As características e critérios para elaboração e aplicação das máscaras são abordadas
abaixo:


MÁSCARA 1 – Exclusão de municípios com potencial agropecuário limitado.

Alguns indicadores são construídos a partir de proporções relacionadas à área ou à
produção agrícola. Nessas situações, municípios com pouca representatividade no setor
agropecuário podem introduzir ruídos nas análises — muitas vezes sem serem identificados
estatisticamente como outliers.

Como estratégia metodológica para reduzir esse viés, foi desenvolvida uma máscara de
exclusão que desconsidera esses municípios na aplicação de determinados indicadores
(Figura 14).

## PDF page 44

Figura 14 – Representação espacial dos municípios que atenderam aos critérios de seleção
             da máscara 1.
                               Fonte: Elaborado por Thales Penha.


A utilização da máscara é condicionada ao atendimento simultâneo de dois critérios:

   •   Critério 1: proporção elevada de áreas protegidas, correspondente a 20% ou mais
       do território municipal, definida pelo somatório, em percentual, das áreas com
       unidades de conservação de proteção integral, terras indígenas e terras quilombolas.
       Dados oriundos do Ministério do Meio Ambiente (MMA).

   •   Critério 2: baixa expressão na produção agropecuária, limitada aos municípios
       situados até o percentil 40 no ranqueamento nacional, desenvolvida a partir da média
       da produção de produtos agrícolas (PPA) e da produção pecuária (PP). Ambos
       obtidos no Instituto Brasileiro de Geografia e Estatística (IBGE).

             - PPA: média do valor normalizado individualmente da produção (em toneladas)
                    dos seguintes produtos agrícolas: Arroz em casca, Batata-inglesa,
                    Feijão preto em grão, Feijão de cor em grão, Feijão fradinho em grão,

## PDF page 45

                        Feijão verde, Mandioca (aipim, macaxeira), Milho em grão, Tomate e
                        Trigo em grão.

             - PP: média do valor normalizado individualmente da produção (em unidade ou
                        cabeça) dos seguintes produtos da pecuária: ovos, leite, carne bovina,
                        frango e carne suína.


Antes do cálculo dos índices, os dados brutos foram submetidos à técnica de winsorização,
com o intuito de mitigar a influência de valores extremos (outliers) que pudessem distorcer
os resultados finais.

A aplicação desta máscara territorial atribui valores "NA" (Not Available / Não Disponível)
aos municípios selecionados conforme os critérios definidos. Esta abordagem garante maior
coerência espacial e temática à análise dos indicadores, especialmente no subsetor de
Disponibilidade de Alimentos.

A lista dos municípios que receberam valores NA pode ser consultada no Apêndice B (Tabela
7).


MÁSCARA 2 – Segmentação produtiva municipal para ajuste de indicadores com
escala estadual.

Esta máscara foi desenvolvida com o objetivo de refinar a representação espacial de
indicadores simples cujos dados brutos estavam disponíveis exclusivamente em nível
estadual. A ausência de desagregação municipal em determinados indicadores limita sua
aplicabilidade em análises locais, especialmente em contextos que exigem sensibilidade
territorial, como a composição de vulnerabilidades socioambientais. Para mitigar esse
problema, optou-se por construir uma máscara de ajuste municipal, com base em proxies
que refletem a relevância produtiva local.

A construção da máscara considerou a produção agrícola acumulada entre os anos de 2010
e 2020, com foco nos cultivos mais representativos para a segurança alimentar e a economia
rural regional: arroz, feijão, mandioca, milho, tomate e trigo. Os dados de produção, obtidos
junto ao Instituto Brasileiro de Geografia e Estatística (IBGE), foram inicialmente
normalizados individualmente para cada cultura, a fim de permitir comparabilidade entre
variáveis com diferentes unidades e magnitudes.

## PDF page 46

Posteriormente, foi aplicada a técnica de winsorização para tratamento de outliers,
substituindo valores extremamente altos por limites pré-definidos (ver o item "a” deste
capítulo). Essa abordagem foi fundamental para suavizar a influência de municípios com
produções atipicamente elevadas, sem eliminar a observação da base de dados.

A produção agrícola total por município, obtida por meio da soma dos valores normalizados,
foi então submetida a uma classificação por quintis, gerando cinco classes de municípios,
do menor ao maior valor de produção. Cada classe recebeu um peso ordinal de 1 a 5, sendo
1 atribuído aos municípios com menor produção agrícola acumulada e 5 àqueles com maior
produção. Assim, cada município passou a contar com um peso proporcional à sua
relevância produtiva, representando de forma mais fiel sua contribuição relativa ao contexto
estadual.

A máscara final (Figura 15) representa um valor (peso) municipal, que foi incorporado como
fator multiplicativo na etapa de construção numérica dos indicadores. Essa aplicação
permitiu redistribuir proporcionalmente os valores estaduais dos indicadores simples,
ajustando-os segundo a importância produtiva de cada município.


Figura 15 – Representação espacial dos pesos que foram atribuídos aos municípios para
            ajuste de indicadores com escala estadual.
                              Fonte: Elaborado por Thales Penha.

## PDF page 47

Essa metodologia garantiu maior coerência territorial e aderência à realidade agrícola local,
especialmente em casos em que a fonte original de dados não oferecia detalhamento
espacial suficiente. Como resultado, os indicadores finais adquiriram maior sensibilidade à
heterogeneidade do espaço rural, fortalecendo a precisão e a utilidade das análises
produzidas.

Os pesos por município podem ser consultados no Apêndice B (Tabela 8).


       f) Elaboração do indicador simples


Os indicadores simples foram calculados levando em consideração a presença ou ausência
de máscaras, conforme explicado no ítem “e” (elaboração e aplicação de “máscaras”).
Quando não houve necessidade de máscaras, os indicadores foram gerados diretamente a
partir dos dados brutos, utilizando os procedimentos estabelecidos, sem a aplicação de
máscaras adicionais. No entanto, nos casos em que as máscaras se mostraram necessárias
para refletir características específicas do contexto, o cálculo dos indicadores simples foi
ajustado a depender do tipo da máscara:

   •   Máscara 1: foi aplicada como última etapa da construção do indicador.

   •   Máscara 2: foi aplicada como fator de ajuste inicial dos valores brutos.


Nesse cenário, cada valor normalizado da variável foi multiplicado pelo valor correspondente
à máscara específica (ver equação abaixo), de acordo com a natureza do indicador em
questão, permitindo uma adaptação mais precisa aos diferentes cenários de risco climático.
O procedimento assegura que os indicadores simples sejam representativos e adequados
às condições específicas de cada variável e dimensão analisada.

                                      𝐼𝑆𝑖 = 𝐼𝑗𝑖 ∗ 𝑉𝑗𝑖
Onde: ISi é o indicador simples do i-ésimo município; Iji é o valor normalizado do indicador j
       no i-ésimo município; V é o valor atribuído à máscara aplicada ao indicador j no i-
       ésimo município.

## PDF page 48

A composição hierárquica final para cada subsetor pode ser observada Apêndice A (Tabelas
5 e 6). Os procedimentos matemáticos aplicados a cada indicador simples podem ser
consultados no Apêndice C (Tabelas 9 e 10).

Os indicadores simples, após devidamente ajustados e harmonizados em escala municipal,
tornam-se os insumos fundamentais para a construção dos demais níveis hierárquicos. A
próxima etapa envolve a agregação estruturada desses indicadores simples dentro de seus
respectivos grupos temáticos, respeitando a lógica hierárquica do modelo conceitual
adotado, de modo a permitir o cálculo coerente dos índices parciais, índices de
vulnerabilidade e exposição e, por fim, do índice final de risco de impacto.


           4.2.3   Cálculo dos demais níveis hierárquicos


Nos subsetores voltados à avaliação do risco de impacto das mudanças climáticas sobre a
segurança alimentar no âmbito do AdaptaBrasil 2.0, foi adotada uma estrutura hierárquica
composta por quatro níveis principais, além dos indicadores simples: a) Indicadores
temáticos (nível 5), que agrupam indicadores simples segundo temas específicos (nível 4);
b) Índices parciais de vulnerabilidade, representados pelos componentes de Sensibilidade e
Capacidade Adaptativa, que refletem dimensões complementares da vulnerabilidade (nível
3); c) Índices das dimensões do risco, que integram os índices de vulnerabilidade e de
exposição (nível 2); d) E, por fim, o Índice de Risco de Impacto Final, que consolida todas as
dimensões anteriores, oferecendo uma visão integrada do risco climático enfrentado pelos
municípios (nível 1).

A principal finalidade dessa estrutura é facilitar a análise e a gestão de fenômenos
complexos, sintetizando grandes volumes de dados em métricas agregadas. Esse processo
de simplificação, realizado por meio de métodos estatísticos e técnicas específicas de
agregação, é essencial para apoiar decisões estratégicas, sobretudo em contextos
marcados por vulnerabilidades sociais e riscos climáticos.

A construção dos indicadores temáticos e dos índices nos níveis superiores seguiu os
procedimentos metodológicos ilustrados na Figura 16.

A seguir, são descritas as etapas e critérios adotados no cálculo de cada nível hierárquico,
com exceção dos indicadores simples, já tratados no item 4.2.2. Cada etapa foi

## PDF page 49

cuidadosamente planejada para assegurar coerência metodológica, consistência estatística
e aderência temática ao contexto do risco climático analisado.


Figura 16 – Organograma das etapas de construção dos indicadores temáticos e índices dos
            níveis superiores do SE Segurança Alimentar.

                              Fonte: Elaborado por Karine Rocha.


      a) Indicadores temáticos


Os indicadores temáticos foram construídos a partir da mediana dos valores dos indicadores
simples que os compõem. Esse procedimento foi adotado para assegurar que os valores
representassem de forma robusta o comportamento central dos dados, minimizando a
influência de valores extremos. A utilização da mediana, em vez da média, é especialmente

## PDF page 50

adequada em contextos em que os dados apresentam assimetrias ou outliers, garantindo
maior estabilidade na representação dos resultados. O cálculo foi realizado por meio da
seguinte expressão:

                                  𝐼𝑇𝑗𝑖 = 𝑀𝐸𝐷 (𝐼𝑗𝑖 , … , 𝐼𝑛𝑖 )

Onde: ITji é o indicador temático j do i-ésimo município; Iji é o indicador simples j do i-ésimo

       município; Ini é o indicador simples n do i-ésimo município.


Após o cálculo dos indicadores temáticos, é realizada uma análise dos seus valores máximos
e mínimos. Quando os dados se apresentam concentrados em uma faixa intermediária —
isto é, quando o valor mínimo é superior a 0,1 e/ou o valor máximo inferior a 0,9 —, aplica-
se uma transformação adicional com o objetivo de ajustar o gradiente de variação e garantir
maior contraste e sensibilidade do indicador.

Essa transformação teve como base a normalização linear, que buscou expandir ou deslocar
os valores para os extremos desejados (≤ 0,1 e ≥ 0,9). Para isso, foram calculados dois
coeficientes para ajuste de cada situação – Tabela 4:


Tabela 4 – Cálculo dos coeficientes de inclinação (a) e deslocamento (b) para normalização
           dos valores de indicadores temáticos.

      Ajuste dos valores                  Ajuste dos valores            Ajuste dos valores
            mínimos                            máximos                 mínimos e máximos

                                           Coeficiente a

            (𝐼𝑇𝑗𝑚 − 0,1)                         (0,9 − 𝐼𝑇𝑗𝑝 )                (0,1 − 0,9)
      𝑎=                                  𝑎=                            𝑎=
            (𝐼𝑇𝑗𝑚 − 𝐼𝑇𝑗𝑝 )                      (𝐼𝑇𝑗𝑚 − 𝐼𝑇𝑗𝑝 )               (𝐼𝑇𝑗𝑝 − 𝐼𝑇𝑗𝑚 )

                                           Coeficiente b


     𝑏 = 0,1 − (𝐼𝑇𝑗𝑝 𝑥 𝑎)               𝑏 = 0,9 − (𝐼𝑇𝑗𝑚 𝑥 𝑎)          𝑏 = 0,9 − (𝐼𝑇𝑗𝑚 𝑥 𝑎)


Onde: a é o coeficiente de inclinação da reta; b é o coeficiente de deslocamento da reta; ITji é o

       indicador temático j do i-ésimo município; ITjm é o valor máximo do indicador temático j;
       ITjp é o valor mínimo do indicador temático j.

## PDF page 51

                               Fonte: Elaborado por Karine Rocha.

Com esses parâmetros, o valor ajustado do indicador temático foi então obtido pela fórmula:

                               𝐼𝑇𝑎𝑗𝑢𝑠𝑡 = (𝐼𝑇𝑗𝑖 𝑥 𝑎) + 𝑏

Onde: ITajust é o valor ajustado do indicador temático j no i-ésimo município.


      b) Índices parciais de vulnerabilidade


Os índices parciais da dimensão vulnerabilidade – definidos como Índice de Sensibilidade
(IS) e Índice de Capacidade Adaptativa (ICA) – foram obtidos a partir da mediana dos valores
dos indicadores temáticos que compõem cada uma dessas categorias. A escolha da
mediana como medida de agregação teve como objetivo garantir maior robustez estatística
frente à presença de valores extremos, assegurando uma representação mais fiel do
comportamento central das variáveis envolvidas.

A fórmula utilizada para o cálculo dos índices parciais é apresentada a seguir:

                              𝐼𝑃𝑗𝑖 = 𝑀𝐸𝐷 (𝐼𝑇𝑗𝑖 , … , 𝐼𝑇𝑛𝑖 )
Onde: IPji é o índice parcial j do i-ésimo município, considerando j como índice de
      sensibilidade (IS) ou índice de capacidade adaptativa (ICA); ITji é o indicador temático
      j do i-ésimo município; Ini é o indicador temático n do i-ésimo município.


Após a obtenção dos valores de IS e ICA, foi aplicado um procedimento de reescalonamento
por normalização linear simples, ajustando os valores mínimos e máximos para 0 e 1,
respectivamente. Essa etapa visa padronizar os índices parciais em uma mesma escala,
facilitando a comparação entre municípios e garantindo coerência nas etapas subsequentes
de integração dos componentes da vulnerabilidade.

Esse método de construção assegura que as características específicas de cada subsetor
temático sejam representadas de forma proporcional e consistente. Assim, os índices
parciais sintetizam de maneira clara e objetiva as dimensões fundamentais da
vulnerabilidade, fornecendo subsídios essenciais para a análise da resiliência dos sistemas
socioambientais avaliados.

## PDF page 52

      c) Índices das dimensões do risco


Os índices de dimensão – vulnerabilidade (IV), exposição (IE) e ameaça climática (IAC) -
foram calculados de forma independente e diferenciada entre si. A vulnerabilidade (IV) está
em função da sensibilidade (IS) e capacidade adaptativa (ICA) e foi obtida conforme
expressões abaixo:

                            𝐼𝑉𝑖 = (1 + (𝐼𝑆𝑗𝑖 − 𝐼𝐶𝐴𝑗𝑖 ))/2

Onde: IVi é o índice de vulnerabilidade do i-ésimo município; ISi é o índice de sensibilidade
      do i-ésimo município; ICAi é o índice de capacidade adaptativa do i-ésimo município.


A exposição (IE) foi obtida pelo cálculo dos valores médios de seus indicadores temáticos
componentes, conforme expressão abaixo:

                              𝐼𝐸𝑖 = 𝑀𝐸𝐷 (𝐼𝑇𝑗𝑖 , … , 𝐼𝑇𝑛𝑖 )

Onde: IEi é o índice de exposição do i-ésimo município; ITji é o indicador temático j do i-
      ésimo município; Ini é o indicador temático n do i-ésimo município.


      d) Índice de risco de impacto final


O Índice de Risco de Impacto (IRI) foi construído com base em uma estrutura dinâmica que
integra as dimensões de exposição (IE), vulnerabilidade (IV) e ameaça climática (IC). Essa
abordagem permite representar de forma mais realista os possíveis impactos associados a
eventos climáticos, considerando simultaneamente a suscetibilidade dos sistemas
analisados, sua capacidade de resposta e a intensidade das ameaças envolvidas.

A construção do IRI foi realizada por meio da multiplicação direta dos valores normalizados
de suas três dimensões componentes, conforme expressa a seguinte equação:

                              𝐼𝑅𝐼𝑖 = (𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 )

## PDF page 53

Onde: IRIi é o índice de risco de impacto do i-ésimo município; IVi é o índice de

      vulnerabilidade do i-ésimo município; IEi é o índice de exposição do i-ésimo município;

      ICji é o índice de ameaça climática j do i-ésimo município.

Essa formulação multiplicativa foi adotada por refletir, de forma mais fiel, a interdependência
entre as dimensões que compõem o risco. Isso significa que o risco de impacto não é
resultado isolado de uma única dimensão, mas sim da combinação entre vulnerabilidade,
exposição e ameaça climática. Por exemplo, mesmo em contextos de alta exposição, o risco
pode ser relativamente baixo se a vulnerabilidade for reduzida ou se a intensidade da
ameaça climática for limitada. Da mesma forma, uma elevada vulnerabilidade associada a
uma ameaça significativa pode gerar alto risco, mesmo em situações de exposição
moderada. Assim, a abordagem multiplicativa permite capturar essas interações, evitando
superestimações ou subestimações que poderiam ocorrer em modelos aditivos.

Após o cálculo do IRI para cada município, foi aplicada uma normalização linear simples,
realizada separadamente para cada cenário e período de análise. Essa etapa considerou
como referência os valores mínimo e máximo do período presente, reescalonando os
resultados para a faixa compreendida entre 0 e 1. O objetivo desse procedimento foi garantir
a comparabilidade dos valores ao longo do tempo, além de evidenciar de forma proporcional
os incrementos ou reduções projetadas para os cenários futuros.


           4.2.4   Cálculo dos fatores influenciadores


Na versão AdaptaBrasil 2.0, o "fator influenciador" foi revisado quanto a sua metodologia,
tornando as análises mais precisas e adaptadas às crescentes demandas por dados
complexos e integrados. Esse fator descreve a contribuição percentual dos indicadores
simples na formação de um índice selecionado.

O cálculo desse fator é realizado a partir da decomposição logarítmica como fator de
escalonamento de cada componente dentro de um sistema hierárquico, procedimento
essencial em contextos onde indicadores afetam o índice agregado de maneira desigual
(WANG; ANG; BIN SU, 2017). O AdaptaBrasil ajustou essa técnica para calcular a
contribuição proporcional dos indicadores simples em diferentes níveis, permitindo uma
análise detalhada do impacto de cada fator nos índices agregados.

## PDF page 54

   a) Cálculo da contribuição dos indicadores simples aos Índices de Risco de

      Impacto (Nível 5 para Nível 1)


Para garantir que os indicadores simples reflitam corretamente suas contribuições para o
valor final do risco normalizado, foram necessárias 5 etapas: 1) Cálculo das contribuições
“brutas” das dimensões para o risco final; 2) Cálculo do fator de escalonamento ou de ajuste
da normalização; 3) Cálculo das contribuições ajustadas das dimensões para o risco final;
4) Cálculo das contribuições “brutas” dos indicadores simples para o risco final; e 5) Cálculo
das contribuições “ajustadas” dos indicadores simples para o risco final.


ETAPA 1: Cálculo das contribuições “brutas” das dimensões para o risco final


Considerando que o índice de risco (IRIi) é obtido por uma função multiplicativa das suas
dimensões (𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 ), o cálculo das contribuições proporcionais de cada dimensão
para o risco deve utilizar uma transformação logarítmica. Esta tem a propriedade de
converter multiplicações em somas, o que simplifica a análise de como cada variável
contribui para o valor total do risco. Ao aplicar o logaritmo natural (ln) em ambos os lados da
equação multiplicativa do risco, temos:

                          𝑙𝑛 (𝐼𝑅𝐼𝑖 ) = 𝑙𝑛(𝐼𝑉𝑖 𝑥 𝐼𝐸𝑖 𝑥 𝐼𝐴𝐶𝑗𝑖 )

Pela propriedade dos logaritmos:

                   𝑙𝑛 (𝐼𝑅𝐼𝑖 ) =𝑙𝑛 (𝐼𝑉𝑖 ) + 𝑙𝑛 (𝐼𝐸𝑖 ) + 𝑙𝑛 (𝐼𝐴𝐶𝑗𝑖 )

Essa fórmula permite que as contribuições relativas de V, E, e A sejam avaliadas
separadamente, facilitando a decomposição logarítmica das dimensões. Em vez de calcular
diretamente a multiplicação dos valores brutos, os valores logarítmicos individuais são
somados, fornecendo uma maneira prática de calcular a elasticidade parcial de cada
dimensão em relação ao risco total.

## PDF page 55

Em seguida é possível calcular as contribuições relativas de cada dimensão ao índice bruto 8,
utilizando as fórmulas:

    ● Contribuição da vulnerabilidade C(IVi):

                                                          𝑙𝑛 (𝐼𝑉𝑖 )
                                      𝐶 (𝐼𝑉𝑖 ) =
                                                      𝑙𝑛 (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))
    ● Contribuição da vulnerabilidade C(IEi):

                                                          𝑙𝑛 (𝐼𝐸𝑖 )
                                      𝐶 (𝐼𝐸𝑖 ) =
                                                      𝑙𝑛 (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))

    ● Contribuição da vulnerabilidade C(IACji):

                                                    𝑙𝑛 (𝐼𝐴𝐶𝑗𝑖 )
                                    𝐶 (𝐼𝐴𝐶𝑗𝑖 ) =
                                                 𝑙𝑛 (𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡))

Importante destacar que a aplicação do logaritmo natural (ln) às dimensões do risco
(vulnerabilidade, exposição e ameaça climática) deve ser realizada antes da normalização
do índice final de risco, ou seja, no valor do índice de risco bruto (IRI bruto). Isso ocorre
porque a transformação logarítmica é mais eficaz quando aplicada aos valores brutos,
permitindo que as contribuições relativas de cada dimensão sejam calculadas com precisão.

No entanto, após a normalização do índice, o valor do risco é ajustado para se enquadrar
em uma escala predeterminada utilizada no AdaptaBrasil (valores entre 0 a 1). Esse
processo de normalização altera a magnitude do índice, o que torna necessário o uso de um
fator de escalonamento.


ETAPA 2: Cálculo do fator de escalonamento ou de ajuste da normalização


O fator de escalamento é uma técnica utilizada para ajustar a magnitude das contribuições
individuais das dimensões para garantir que o somatório dessas contribuições esteja


8
 Entende-se por índice bruto o valor resultante diretamente da aplicação da metodologia de cálculo, ainda não submetido
ao ajuste via fator de escalonamento.

## PDF page 56

alinhado com o valor final do risco (após a normalização). Seu uso é especialmente
importante quando os valores das contribuições não somam ao valor esperado ou
apresentam variações indesejadas.

O fator de escalamento funciona como uma constante multiplicativa que é aplicada a cada
contribuição individual das dimensões, de modo que o somatório final das contribuições seja
proporcional ao valor do desejado.

A fórmula básica do fator de escalamento é dada por:

                                        𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)
                              𝐹 (𝑡) =
                                           𝐼𝑅𝐼𝑏𝑟𝑢𝑡𝑜 (𝑡)
Onde: F(t) é o é o fator de escalamento no tempo t no i-ésimo município; IRInormalizado (t) é

      o valor do índice de risco no tempo t do i-ésimo município após a normalização; IRIbruto

      (t) é o valor do índice de risco no tempo t do i-ésimo município antes da normalização.


ETAPA 3: Cálculo das contribuições ajustadas das dimensões para o risco final


Após a normalização, o valor do risco é ajustado para ficar entre 0 e 1, mas a relação entre
as dimensões não se altera de forma direta. Para ajustar as contribuições de forma
adequada, levando em conta o efeito da normalização com limites, você pode usar o
seguinte método:

   ● Contribuição da vulnerabilidade C’(IVi):

                               𝐶 ′ (𝐼𝑉𝑖 ) = 𝐹 (𝑡) 𝑥 𝐶 (𝐼𝑉𝑖 )

   ● Contribuição da vulnerabilidade C’(IEi):

                               𝐶 ′ (𝐼𝐸𝑖 ) = 𝐹 (𝑡) 𝑥 𝐶 (𝐼𝐸𝑖 )

   ● Contribuição da vulnerabilidade C’(IACji):

                            𝐶 ′ (𝐼𝐴𝐶𝑗𝑖 ) = 𝐹 (𝑡) 𝑥 𝐶(𝐼𝐴𝐶𝑗𝑖 )

## PDF page 57

Onde: C’X(t) é a contribuição ajustada da dimensão X (IV, IE ou IAC) no valor do risco final
      no tempo t, ou seja, após a normalização.


ETAPA 4: Cálculo das contribuições “brutas” dos indicadores simples para o risco final

Para calcular as contribuições dos indicadores simples ao risco, é essencial considerar toda
a cadeia de agregação, que começa nos indicadores temáticos e culmina no risco total (Ver
figuras 7 e 8). O processo está relacionado à compreensão que cada indicador simples
exerce uma influência indireta sobre o risco e que cadeia de agregação assegura que o
impacto de cada indicador simples seja avaliado não isoladamente, mas dentro do contexto
de suas interações e contribuições ao sistema como um todo.

Nesse contexto, a contribuição bruta de cada indicador simples no valor final do risco é
condicionada pelas variações nas contribuições de suas respectivas dimensões
(vulnerabilidade, exposição e ameaça). Isso significa que o valor de um indicador simples
pode ser amplificado ou reduzido conforme as características de suas dimensões
agregadoras. Assim, o impacto de cada indicador simples no risco final não é direto, mas
moderado pelo comportamento e peso relativo das subdimensões e dimensões
intermediárias dentro do modelo hierárquico.

A fórmula utilizada para “estimar” esse efeito indireto é dada por:


   ● Contribuição dos indicadores simples relacionados à sensibilidade (CISs) e à
       capacidade adaptativa (CISca) - dimensão de vulnerabilidade:
                                            𝐼𝑆𝑠
                         𝐶𝐼𝑆𝑠 =                           ∗ 𝐶 ′ (𝐼𝑉𝑖 )
                                  𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)


                                         1 − 𝐼𝑆𝑐𝑎
                        𝐶𝐼𝑆𝑐𝑎 =                           ∗ 𝐶 ′ (𝐼𝑉𝑖 )
                                   𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)

   ● Contribuição dos indicadores simples relacionados à dimensão de exposição (CISe):

                                           𝐼𝑆𝑒
                        𝐶𝐼𝑆𝑒 =                            ∗ 𝐶 ′ (𝐼𝐸𝑖 )
                                  𝐼𝑅𝐼𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑎𝑑𝑜 (𝑡)

## PDF page 58

Onde: CISx é a contribuição bruta do indicador simples x (s ou ca) no valor do risco final no
      tempo t, ou seja, após a normalização; ISx é o valor do indicador simples x (s, ca ou
      e); IRInormalizado (t) é o valor do índice de risco no tempo t do i-ésimo município após
      a normalização; C’X(t) é a contribuição ajustada da dimensão X (V ou E) no valor do
      risco final no tempo t, ou seja, após a normalização.


Nota: A versão 2.0 da plataforma AdaptaBrasil ilustra as relações de impactos em cadeia,
ou também chamados, impactos encadeados. Isso significa que os subsetores cujos
impactos não são "primários" possuem hierarquias diferenciadas dentro do modelo de
avaliação. Um exemplo é o subsetor de Acesso e Consumo de Alimentos (ver figura 8), que
faz parte do setor de Segurança Alimentar. O subsetor não possui indicadores simples
diretamente relacionados à ameaça climática (Nível 3), a contribuição da dimensão de
ameaça no cálculo do risco final não pode ser obtida da mesma forma que nos subsetores
com indicadores climáticos diretos.

Para contornar essa ausência, utilizamos o próprio valor da ameaça no lugar do indicador
simples (Nível 6), condicionado à variação da sua contribuição primária, ou seja, à
contribuição de sua dimensão associada no Nível 3. Esse ajuste permite que a ameaça
climática seja adequadamente representada no cálculo do risco final. Dito isso, foi utilizada
a seguinte fórmula:

                            𝐶𝐴𝐶 (𝑡) = 𝐴𝐶𝑥 (𝑡) ∗ 𝐶 ′ (𝐼𝐴𝐶𝑗𝑖 )
Onde: CAC (t) é a contribuição bruta/redimensionada da ameaça climática no valor do risco
      final no tempo t, ou seja, após a normalização; AC x (t) é o valor da ameaça climática
      no município x; C’(IACji) é a contribuição ajustada da dimensão de ameaça climática
      no valor do risco final no tempo t, ou seja, após a normalização.


ETAPA 5: Cálculo das contribuições “ajustadas” dos indicadores simples para o risco final


Para garantir que a soma das contribuições individuais seja igual a 1 (ou 100%), é necessário
ajustar os valores das contribuições brutas de cada indicador simples. Esse ajuste assegura
que cada contribuição seja proporcional em relação ao valor total do risco ou da métrica que
está sendo calculada. O ajuste é realizado por meio de um processo de normalização, que

## PDF page 59

redistribui as contribuições relativas, preservando as proporções originais entre elas. Segue
a fórmula:

                                                       𝐶𝑖 (𝑡)
                                𝐶𝑖 𝑎𝑗𝑢𝑠𝑡𝑎𝑑𝑜 (𝑡) =
                                                      ∑ 𝐶𝑖 (𝑡)
Onde: Ciajustado (t) é a contribuição ajustada de cada indicador simples no valor do risco final
      no tempo t, ou seja, após a normalização; Ci (t) é o valor da contribuição “bruta” dos
      indicadores simples para o risco final.


   b) Cálculo da contribuição dos indicadores simples às dimensões associadas

       (Categoria 1 para categoria 4)


A metodologia de cálculo desta relação se dá em duas etapas principais: 1- Cálculo das
contribuições “brutas” dos indicadores simples para as dimensões do risco e 2- Cálculo das
contribuições “ajustadas”.


ETAPA 1: Cálculo das contribuições “brutas” dos indicadores simples para as dimensões do
             risco


A contribuição bruta dos indicadores simples para a dimensão de vulnerabilidade considera
o cálculo diferenciado para os indicadores associados à sensibilidade (s) e à capacidade
adaptativa (ca). Assim:

   ● Contribuição dos indicadores simples relacionados à sensibilidade (CISs) e à
       capacidade adaptativa (CISca) - dimensão de vulnerabilidade:

                                                  𝐼𝑆𝑠
                                        𝐶𝐼𝑆𝑠 =
                                                  𝐼𝑉

                                                1 − 𝐼𝑆𝑐𝑎
                                    𝐶𝐼𝑆𝑐𝑎 =
                                                   𝐼𝑉

   ● Contribuição dos indicadores simples à dimensão de exposição:

## PDF page 60

                                                𝐼𝑆𝑒
                                       𝐶𝐼𝑆𝑒 =
                                                𝐼𝐸

   ● Co Contribuição dos indicadores simples à dimensão de ameaça climática:
                                                𝐼𝑆𝑎𝑐 (𝑡)
                                 𝐶𝐼𝑆𝑎𝑐 (𝑡) =
                                                𝐼𝐴𝐶 (𝑡)
Onde: CISx é a contribuição bruta do indicador simples x no valor da dimensão a que ele está
       associado; ISx é o valor do indicador simples x; IV, IE ou IAC é o valor da dimensão
       do risco após a normalização.

Nota: Por ser uma dimensão dinâmica, para o cálculo da contribuição dos indicadores
simples para a ameaça climática em um momento específico (tempo t1), todas as variáveis
que compõem esse cálculo devem estar relacionadas e refletir as condições desse mesmo
período temporal.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para as dimensões
           a que se relacionam


O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma
metodologia descrita anteriormente (tópico 4.3.1, etapa 5). Foram aplicados os mesmos
princípios e fórmulas para determinar as proporções relativas de cada indicador dentro do
sistema.


   c) Cálculo da contribuição dos indicadores simples às subdimensões da

       vulnerabilidade a que estão associadas (Categoria 1 para categoria 3)


A metodologia de cálculo desta relação se dá em duas etapas principais, detalhadas abaixo.


ETAPA 1: Cálculo das contribuições “brutas” dos indicadores simples para cada
           subdimensão pertencente


Para o cálculo contribuição bruta dos indicadores simples à subdimensão de sensibilidade
(S) ou capacidade adaptativa (CA) foi utilizada a seguinte metodologia:

## PDF page 61

                                                  𝐼𝑆𝑥
                                         𝐶𝐼𝑆𝑥 =
                                                   𝑋
Onde: CISx é a contribuição bruta do indicador simples x no valor da subdimensão a que ele
      está associado; ISx é o valor do indicador simples x; X é o valor da subdimensão do
      risco.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para as
           subdimensões a que se relacionam


O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma
metodologia descrita anteriormente (tópico 4.3.1, etapa 5). Foram aplicados os mesmos
princípios e fórmulas para determinar as proporções relativas de cada indicador dentro do
sistema.


   d) Cálculo da contribuição dos indicadores simples aos indicadores temáticos a

      que estão associadas (Categoria 1 para categoria 2)


A metodologia de cálculo destas relações se dá em duas etapas: 1) Cálculo das
contribuições “brutas” dos indicadores simples para cada indicador temático pertencente; 2)
Cálculo das contribuições “ajustadas”.

Para estimar a contribuição “bruta” de cada indicador simples utilizou-se a seguinte equação:

                                                  𝐼𝑆𝑥
                                         𝐶𝐼𝑆𝑥 =
                                                  𝑇𝑦
Onde: CISx é a contribuição bruta do indicador simples x no valor do indicador temático no i-
      ésimo município a que ele está associado; ISx é o valor do indicador simples x no i-
      ésimo município; Ty é o valor do indicador temático do i-ésimo município.


ETAPA 2: Cálculo das contribuições “ajustadas” dos indicadores simples para os indicadores
           temáticos a que se relacionam

## PDF page 62

O cálculo da contribuição dos indicadores simples para as dimensões seguiu a mesma
metodologia descrita anteriormente (tópico 4.3.1, etapa 5). Foram aplicados os mesmos
princípios e fórmulas para determinar as proporções relativas de cada indicador dentro do
sistema.

## PDF page 63

                             REFERÊNCIAS BIBLIOGRÁFICAS


ADGER, W. N.. Vulnerability. Global Environmental Change, v. 16, n. 3, p. 268–281, ago.
2006.


ANG B. W.; LIU, F. L.. A new energy decomposition method: perfect in decomposition and
consistent in aggregation. Energy, v. 26, p. 537-548, 2001.


ANG B. W.. Decomposition analysis for policymaking in energy: which is the preferred
method?. Energy Policy, v. 32, p. 1131-1139, 2004.


ANG B. W.. The LMDI approach to decomposition analysis: a practical guide. Energy Policy,
v. 33, p. 867–871, 2005.


ASSAD, E.; PINTO, H.. Global warming and future scenarios for Brazilian Agriculture.
EMBRAPA e CEPAGRI/UNICAMP, 2008.


ASSAD, E. et al. Impactos das Mudanças Climáticas na Produção Agrícola Brasileira.
Banco Internacional para Reconstrução e Desenvolvimento/Associação Internacional de
Desenvolvimento ou O Banco Mundial, 2013.


BALDISERA, R. S., DALLACORT, R. Influência das variáveis climáticas declinação
solar, fotoperíodo e irradiação no topo da atmosfera em regiões agricultáveis do
Brasil. Revista de Ciências Agroambientais. Recebido: 09/06/2016; Aceito: 01/07/2017.


BECKER, W. et al. COIN Tool User Guide. Publications Office of the European Union:
Luxembourg, 2019.


BIN SU; ANG B. W.. Structural decomposition analysis applied to energy and emissions:
some methodological developments. Energy Econ, v. 34, p. 177-88, 2012.


BIN SU; ANG B. W.. Attribution of changes in the generalized Fisher index with application
to embodied emission studies. Energy, p. 1–9, 2014.

## PDF page 64

BRASIL. LEI Nº 11.346, DE 15 DE SETEMBRO DE 2006. Brasília: 2006. Disponível
em:<http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2006/Lei/L11346.htm>.


CENTRO DE ESTUDOS AVANÇADOS EM ECONOMIA APLICADA - CEPEA Esalq/USP;
CONFEDERAÇÃO DA AGRICULTURA E PECUÁRIA DO BRASIL - CNA. Sustentado por
safra recorde no campo, PIB do agronegócio tem alta modesta no primeiro trimestre.
2023.   Disponível    em:    https://cepea.esalq.usp.br/upload/kceditor/files/PIB-DO-AGRO-
27JUN2023.pdf. Acesso em: 20 de outubro de 2023.


EVANGELISTA, B.A., CAMPOS, L. J. M., SILVA, F.A.M., SIMON, J., RIBEIRO, I. L., VALE,
T. M. Possíveis Impactos das Mudanças Climáticas Sobre o Zoneamento Agrícola de
Risco Climático da Cultura da Soja no Estado do Tocantins. In: COLLICCHIO, E.;
ROCHA, H. R.. Agricultura e mudanças do clima no estado do Tocantins: vulnerabilidades,
projeções e desenvolvimento, p. 167-184.Palmas, TO: EdUFT, 2022.


FOOD AND AGRICULTURE ORGANIZATION OF THE UNITED NATIONS (FAO). The
Water-Energy-Food Nexus: A new approach in support of food security and
sustainable      agriculture.     Rome:       FAO,      2014.      Disponível     em:      <
https://www.fao.org/3/bl496e/bl496e.pdf >


GALAZ, V.; MOBERG, F.; OLSSON, E.-K.; PAGLIA, E.; PARKER, C.. Institutional and
political leadership dimensions of cascading ecological crises. Public Administration, 89, p.
361-380. 2011.


GALLOPÍN, G. C.. Human dimensions of global change: linking the global and the local
processes. International Social Science Journal, v. 130, p. 707–718, 1991.


GALLOPÍN, G. C. Environmental and sustainability indicators and the concept of situational
indicators. A system approach. Environmental Modelling & Assessment, v.1, p.101-117,
1996.


GALLOPÍN, G. C.. Box 1: A systemic synthesis of the relations between vulnerability, hazard,
exposure and impact, aimed at policy identification. In: Economic Commission for Latin
American and the Caribbean (ECLAC). Handbook for Estimating the Socio-Economic and
Environmental Effects of Disasters. Mexico, D.F.: ECLAC, LC/MEX/G.S., p. 2–5, 2003.

## PDF page 65

GALLOPÍN, G. C. Linkages between vulnerability, resilience, and adaptive capacity. Global
Environmental Change, v. 16, p. 293-303, 2006.


GHINI, R., HAMADA, E., BETTIOL, W. Impactos das mudanças climáticas sobre
doenças de importantes culturas no Brasil. Embrapa Meio Ambiente Jaguariúna, SP,
2011.


GILL, J. C.; MALAMUD, B. D.. Hazard interactions and interaction networks (cascades) within
multi-hazard methodologies. Earth System Dynamics, 7, p. 659-679. 2016.


HAMMOND, A.; ADRIAANSE, A.; RODENBURG, E.; BRYANT, D.; WOODWARD, R.
Environmental indicators: a systematic approach to measuring and reporting on
environmental policy performance in the context of sustainable development.
Washington DC: World Resources Institute, 1995, 43p.


HILLY, G.; VOJINOVIC, Z.; WEESAKUL, S.; SANCHEZ, A.; HOANG, D. N.; DJORDJEVIC,
S.; CHEN, A.S.; EVANS, B. Methodological framework for analysing cascading effects from
flood events: the case of Sukhumvit Area, Bangkok, Thailand. Water, v. 10, n. 81, 2018.


HOEKSTRA, R.; JEROEN, J. C. J. M; van der BERGH.. Comparing structural and index
decomposition analysis. Energy Econ, v. 25, p. 39-64, 2003.


INTERGOVERNMENTAL PANEL ON CLIMATE CHANGE – IPCC. Climate Change 2001:
Synthesis Report. A Contribution of Working Groups I, II, and III to the Third Assessment
Report of the Intergovernmental Panel on Climate Change [Watson, R.T. and the Core
Writing Team (eds.)]. Cambridge University Press, Cambridge, United Kingdom, and New
York, NY, USA, 398 pp., 2001.


INTERGOVERNMENTAL PANEL ON CLIMATE CHANGE – IPCC. Climate Change 2014:
Synthesis Report. Working Groups I, II and III to the Fifth Assessment Report of the
Intergovernmental Panel on Climate Change [Core Writing Team, R.K. Pachauri and L.A.
Meyer (eds.)]. IPCC, Geneva, Switzerland, 151 pp. 2015.


INTERGOVERNMENTAL PANEL ON CLIMATE CHANGE – IPCC. Climate Change 2022:
Impacts, Adaptation and Vulnerability. Contribution of Working Group II to the Sixth
Assessment Report of the Intergovernmental Panel on Climate Change [H.-O. Pörtner, D.C.

## PDF page 66

Roberts, M. Tignor, E.S. Poloczanska, K. Mintenbeck, A. Alegría, M. Craig, S. Langsdorf, S.
Löschke, V. Möller, A. Okem, B. Rama (eds.)]. Cambridge University Press. Cambridge
University Press, Cambridge, UK and New York, NY, USA, 3056 pp., 2022.


JACOB, K.; BLAKE, R.. Chapter 7: Indicators and monitoring. Ann. N.Y. Acad. Sci. v.1196,
p. 127–141, 2010.

JANNUZZI, P. D. M.. Indicadores para Diagnóstico, Monitoramento e Avaliação de
Programas Sociais no Brasil. Revista do Serviço Público, v. 56, n. 2, p. 137–160, 2005.


JANNUZZI, P. M. Indicadores Sociais no Brasil: conceitos, fontes de dados e
aplicações. Campinas: Editora Alínea/PUC-Campinas, 141 p. 2006.


KASPERSON, J. X.; KASPERSON, R. E.; TURNER II., B. L., SCHILLER, A., HSIEL, W. H..
Vulnerability to global environmental change. In: KASPERSON, J. X.; KASPERSON, R. E.
(Eds.), Social Contours of Risk, vol. II. Earthscan, London, 2005. p. 245–285.


KEMP L., XU C., DEPLEDGE J., EBI K.L., GIBBINS G., KOHLER T.A., ROCKSTRÖM J.,
SCHEFFER M., SCHELLNHUBER H.J., STEFFEN W., LENTON T.M. 2022. Climate
endgame: Exploring catastrophic climate change scenarios. Proceedings of the National
Academy of Sciences 119: e2108146119.


KEPPLE, A. W.. O estado da segurança alimentar e nutricional no Brasil: Um retrato
multidimensional.      Relatório    2014.     Brasília,    2014.    Disponível    em:     <
https://www.mds.gov.br/webarquivos/publicacao/seguranca_alimentar/SANnoBRasil.pdf>


KOKS, E.. Moving flood risk modelling forwards. Nature Climate Change, 8, p. 561-562.
2018.


LAWRENCE, J.; BLACKETT, P.; CRADOCK-HENRY, N.; FLOOD, S.; GREENAWAY, A.;
DUNNINGHAM, A.. Synthesis Report RA4: Enhancing capacity and increasing
coordination to support decision making. Climate Change Impacts and Implications
(CCII) for New Zealand to 2100. Wellington: NZCCRI, Victoria University of Wellington;
NIWA; Landcare Research, 2016.

## PDF page 67

LAWRENCE, J., BLACKETT, P., CRADOCK-HENRY, N.; NISTOR, B.J. Climate Change:
The Cascade Effect. Cascading impacts and implications for Aotearoa New Zealand, 2018.
Wellington: Deep South Challenge.


LAWRENCE, J.; BLACKETT, P.; CRADOCK-HENRY, N. A. Cascading climate change
impacts and implications. Climate Risk Management, v. 29, 2020.


LIMA, P. V. P. S.; QUEIROZ, F. D. DE S.; MAYORGA, M. I. DE O.; CABRAL, N. R. A. J. A
propensão à degradação ambiental na mesorregião de Jaguaribe no Estado do Ceará.
Economia do Ceará em Debate 2008, p. 27–43, 2009.


MAGGINO, F.. Complexity in society: from indicators construction to their Synthesis.
1º ed. Roma, Itália: Springer, 2017.


MARENGO, J. A. Água e mudanças climáticas. Estudos Avançados, v.22, n. 63, p. 83-96,
2008.


MEADOWS, D. Indicators and Information Systems for Sustainable Development.
Hartland/VT: Sustainability Institute (1998).


MIOLA, A.; SCHILTZ, F. Measuring sustainable development goals performance:
How to monitor policy action in the 2030 Agenda implementation? Ecological
Economics, v. 164, p. 1–10, 2019.


MITCHELL, G. Problems and fundamentals of sustainable development indicators.
Sustainable Development, v. 4, n. 1, p. 1-11, 1996


MIZRAHI, S.. Cascading disasters, information cascades and continuous time models of
domino effects. International Journal of Disaster Risk Reduction, v.49, 2020.


MOTESHARREI, S., RIVAS, J., KALNAY, E. Human and nature dynamics (HANDY):
Modeling inequality and use of resources in the collapse or sustainability of societies.
Ecological     Economics,       v.     101,     p.   90-102,   (2014).   Disponível   em:
<https://www.sciencedirect.com/science/article/pii/S0921800914000615)>

## PDF page 68

MUELLER, C.; TORRES, M.; MORAIS, M. Referencial básico para a construção de um
sistema de indicadores urbanos. Brasília: Instituto de Pesquisa Econômica Aplicada
(IPEA), 1997.


NDAYIRAGIJE, Jean Marie; LI, Fan. Effectiveness of Drought Indices in the Assessment of
Different Types of Droughts, Managing and Mitigating Their Effects. Climate, v. 10, n. 9, p.
125, 2022.


NARDO, M.; SAISANA, M.; SALTELLI, A.; TARANTOLA, S.; HOFFMAN, A.; GIOVANNINI,
E. Handbook on constructing composite indicators: methodology and user guide.
Paris: Organisation for Economic Co-operation and Development (OECD), 2008. Disponível
em: <https://www.oecd.org/sdd/42495745.pdf>.


OECD. Organization for Economic Cooperation and Development: core set of indicators for
environmental performance reviews; a synthesis report by the group on the State of the
environment. Paris, 1993.


OECD. Handbook on Constructing Composite Indicators: Methodology and User Guide.
OECD Publishing: Paris, 2008.


OSTROM, E. Governing the commons: the evolution of institutions for collective
action. Cambridge, New York, Melbourne, Madrid, Cape Town: Cambridge University
Press, 1990.


PERAZZO, A. F., SANTOS, E. M., PINHO, R. M. A., CAMPOS, F. S., RAMOS, J. P. F.,
AQUINO, M. M., SILVA, T.C., BEZERRA, H.F.C. Características agronômicas e eficiência
do uso da chuva em cultivares de sorgo no semiárido Ciência Rural, Santa Maria, v.43,
n.10, p.1771-1776, out, 2013


PESCAROLI, G.; ALEXANDER, D. Critical infrastructure, panarchies and the vulnerability
paths of cascading disasters. Nat Hazards, 82, p. 175-192. 2016.


PRABHU, R., COLFER, C. J. P., DUDLEY, R. G. Guidelines for developing, testing and
selecting criteria and indicators for sustainable forest management. Toolbox Series, n.
1. Indonesia: CIFOR, 1999.

## PDF page 69

ROCHA, J. C.; PETERSON, G. D.; BODIN, O.; LEVIN, S. A. Cascading regime shifts within
and across scales. bioRxiv, 364620. Preprint. 2018.


ROCKSTRÖM, J., STEFFEN, W., NOONE, K. A safe operating space for humanity. Nature,
v. 461, p. 472–475. 2009.


SHIELDS, D.; SOLAR, S.; MARTIN, W. The role of values and objectives in communicating
indicators of sustainability. Ecological Indicator, v. 2, n. 1-2, p. 149-160, nov. 2002.


SICHE, R.; AGOSTINHO, F.; ORTEGA, E.; ROMEIRO, A. Índices versus indicadores:
precisões conceituais na discussão da sustentabilidade de países. Ambiente & Sociedade,
v. X, n. 2, p. 137-148. 2007.


SIMPSON, N. P. et al. A framework for complex climate change risk assessment. One Earth,
v. 4, P. 489–501. 2021.


SMITI, A.. A critical overview of outlier detection methods. Computer Science Review, v.
38. 2020.


TURNER, B. L.; KASPERSON, R. E.; MATSON, P. A.; MCCARTHY, J. J.; CORELL, R. W.;
CHRISTENSEN, L.; ECKLEY, N.; KASPERSON, J. X.; LUERS, A.; MARTELLO, M. L.;
POLSKY, C.; PULSIPHER, A.; SCHILLER, A.. A framework for vulnerability analysis in
sustainability science. Proceedings of the National Academy of Sciences of the United
States of America, v. 100, n. 14, p. 8074–9, 2003.


TURRENTINE, J.. IPCC: We Cannot Look Away—Climate Risks Are Cascading. Natural
Resources       Defense         Council    (NRDC).       2022.       Disponível      em:   <
https://www.nrdc.org/stories/ipcc-we-cannot-look-away-climate-risks-are-cascading>.


VAN BELLEN, H. M. Indicadores de Sustentabilidade: uma análise comparativa.
2º ed. Rio de Janeiro, RJ, 2006.


WANG, H.; ANG, B. W.; BIN SU. Multiplicative structural decomposition analysis of energy
and emission intensities: Some methodological issues. Energy, v. 123, p. 47-63, 2017.

## PDF page 70

WILLNER, S.; OTTO, C.; LEVERMANN, A.. Global economic response to river floods. Nat.
Clim. Change, 8, p. 594-598. 2018.

## PDF page 71

                                                                                                                           APÊNDICES


APÊNDICE A – Composição hierárquica dos Subsetores do SE Segurança Alimentar para ameaça de seca.

Tabela 5 – Indicadores selecionados para a compor a hierarquia do Subsetor Disponibilidade de Alimentos para seca.
 NÍVEL 2                                             NÍVEL 3               NÍVEL 4             NÍVEL 5                                                     NÍVEL 6

                                                                                                               Susceptibilidade climática da produtividade agrícola

                                                                                                               Susceptibilidade climática da produtividade pecuária

                                                                                                               Homogeneidade da produção agrícola local
                                                                                         Práticas Agrícolas
                                                                                                               Agricultura sem práticas agrícolas sustentáveis
   Índice de Risco de Impacto da Mudança Climática


                                                                                                               Susceptibilidade da irrigação em grande escala
                                                                         Sensibilidade                         Incidência de focos de queimada em áreas agropecuárias

                                                                                                               Distância da agropecuária em relação a disponibilidade hídrica
                                                       Vulnerabilidade


                                                                                                               Áreas com atividades agropecuárias de baixo potencial agrícola

                                                                                         Aspectos Biofísicos   Áreas com atividades agropecuárias em solo susceptível a erosão

                                                                                                               Déficit hídrico no solo

                                                                                                               Perdas de cobertura vegetal natural

                                                                                                               Investimento em políticas agrárias e de gestão ambiental

                                                                                                               Cobertura do Programa Garantia Safra

                                                                         Capacidade      Instrumentos          Cobertura do Programa de Fortalecimento da Agricultura Familiar (PRONAF)
                                                                         Adaptativa      financeiros e
                                                                                         políticas públicas    Cobertura do Programa Cisternas

                                                                                                               Cobertura do Proagro Mais

                                                                                                               Cobertura do Programa de Subvenção ao Prêmio do Seguro Rural (PSR)

## PDF page 72

NÍVEL 2   NÍVEL 3        NÍVEL 4         NÍVEL 5                                                   NÍVEL 6

                                                         Nível de orientação técnica

                                   Rede de segurança     Nível de associativismo
                                   para produção         Propriedade da terra

                                                         Estabilidade dos conflitos agrários

                                   Armazenamento de      Capacidade de armazenamento dos armazéns
                                   alimento              Distância dos armazéns às áreas agropecuárias

                                   Aspectos              Diversidade de receitas da produção agropecuária
                                   econômicos e
                                   potencial de          Tratores em estabelecimentos agropecuários de até 4 módulos fiscais
                                   intensificação da
                                   produção              Potencial de expansão agrícola em áreas de pastagem no município

                                   Dependência
                                                         Participação da agropecuária na economia do município
                                   econômica local
             Exposição


                                   Áreas produtivas      Área plantada com culturas agrícolas alimentares
                                   expostas              Área dos estabelecimentos agropecuários com atividade pecuária

                                   Distribuição da       Estabelecimentos agropecuários com agricultura familiar
                                   estrutura fundiária   Densidade de estabelecimentos agropecuários

          Ameaça                                         Dias consecutivos secos
          Climática                                      Índice de precipitação-evapotranspiração padronizado

## PDF page 73

Tabela 6 – Indicadores selecionados para a compor a hierarquia do Subsetor Acesso e Consumo de Alimentos para seca.
 NÍVEL 2                                            NÍVEL 3              NÍVEL 4             NÍVEL 5                                                        NÍVEL 6

                                                                                                             Densidade média de moradores por domicílio

                                                                                       Perfil da População   Mães chefes de família, sem fundamental completo e de baixa renda

                                                                                                             População economicamente dependente

                                                                                                             População com risco de desabastecimento de água por fonte direta

                                                                                                             Água com qualidade comprometida
                                                                                       Infraestrutura
  Índice de Risco de Impacto da Mudança Climática


                                                                                       Básica                Densidade de estabelecimentos comerciais de alimentos ultraprocessados por 10.000
                                                                       Sensibilidade
                                                                                                             habitantes

                                                                                                             Municípios sem rede de abastecimento de alimentos que compõem a cesta básica

                                                                                                             Nível de insegurança alimentar e nutricional
                                                     Vulnerabilidade


                                                                                       Saúde e Consumo       Proporção de crianças menores de 2 anos desnutridas
                                                                                       dos Alimentos         Ocorrência de doenças relacionadas ao saneamento ambiental inadequado

                                                                                                             Nível de sobrepeso e obesidade da população
                                                                                                             Investimento federal per capita em políticas de educação, saúde e infraestrutura para
                                                                                                             adaptação

                                                                                                             Instrumentos de planejamento e gestão da segurança alimentar
                                                                                       Instrumentos
                                                                                       financeiros e         Cobertura do Programa de Abrangência do programa nacional de alimentação escolar (PNAE)
                                                                       Capacidade      políticas públicas    Nível de atendimento das unidades receptoras do PAA em territórios mais susceptíveis
                                                                       Adaptativa
                                                                                                             Fornecedores do PAA classificadas como “Povos e Comunidades Tradicionais”

                                                                                                             Nível de atendimento do Programa Cisternas (P1MC - consumo)

                                                                                       Capacidade            Abrangência do Programa Bolsa Família
                                                                                       Socioeconômica        Igualdade na distribuição de renda intra-domiciliar

## PDF page 74

NÍVEL 2   NÍVEL 3       NÍVEL 4        NÍVEL 5                                                   NÍVEL 6

                                                      Domicílios com renda per capita superior a cinco salários mínimos


            Exposição
                                                      Densidade populacional por município
                                  População Exposta
                                                      População total por munícipio

          Ameaça
                                                      Índice de Risco de Impacto da Seca na Disponibilidade de Alimentos
          Climática

## PDF page 75

APÊNDICE B – Aplicação de máscaras - SE Disponibilidade de Alimentos para Seca.

Tabela 7 – Lista de municípios brasileiros, por estado, que receberam valores NA (aplicação da
             máscara 1) para alguns indicadores do SE Disponibilidade de Alimentos para Seca.

 Cód. IBGE                   Município           Cód. IBGE                 Município

                                             ACRE
 1200054      Assis Brasil                       1200435     Santa Rosa do Purus
 1200328      Jordão
                                           ALAGOAS
 2708204      São Brás
                                           AMAZONAS
 1300060      Amaturá                            1303809     São Gabriel da Cachoeira
 1300144      Apuí                               1304062     Tabatinga
 1300607      Benjamin Constant                  1304237     Tonantins
 1300904      Canutama                           1304302     Urucará
 1301001      Carauari                           1300201     Atalaia do Norte
 1301407      Eirunepé                           1300409     Barcelos
 1301951      Itamarati                          1300508     Barreirinha
 1302306      Jutaí                              1300805     Borba
 1302603      Manaus                             1302108     Japurá
 1303205      Novo Airão                         1303007     Nhamundá
 1303502      Pauini                             1303601     Santa Isabel do Rio Negro
 1303700      Santo Antônio do Içá               1303908     São Paulo de Olivença
                                            AMAPÁ
 1600055      Serra do Navio                     1600204     Calçoene
 1600105      Amapá                              1600279     Laranjal do Jari
 1600154      Pedra Branca do Amapari
                                             BAHIA
 2915403      Itaju do Colônia                   2927101     Rodelas
 2919306      Lençóis                            2932507     Una
 2923506      Palmeiras                          2902658     Banzaê
 2923902      Pau Brasil                         2903706     Boa Nova
 2925303      Porto Seguro                       2920205     Malhada
                                             CEARÁ
 2307254      Jijoca de Jericoacoara
                                         ESPÍRITO SANTO
 3205010      Sooretama                          3202553     Ibitirama
 3201803      Divino de São Lourenço

## PDF page 76

Cód. IBGE                  Município             Cód. IBGE                 Município

                                             GOIÁS
5205307     Cavalcante                           5221080     Teresina de Goiás
                                           MARANHÃO
2102804     Carolina                             2103174     Centro Novo do Maranhão
2103158     Centro do Guilherme                  2104081     Fernando Falcão
2107001     Montes Altos                         2105476     Jenipapo dos Vieiras
2107357     Nova Olinda do Maranhão              2105989     Lajeado Novo
2100204     Alcântara                            2110278     Santo Amaro do Maranhão

2100600     Amarante do Maranhão

                                          MINAS GERAIS
3102050     Alto Caparaó                         3157336     Santa Cruz de Minas

3109204     Buenópolis                           3168705     Timóteo

3121209     Delfinópolis                         3170602     Vargem Bonita

3125507     São Gonçalo do Rio Preto             3139250     Mamonas

3132107     Itacarambi                           3146552     Pai Pedro

3133006     Itamonte                             3162450     São João das Missões

3140308     Marliéria                            3166956     Serranópolis de Minas

3140852     Matias Cardoso

                                       MATO GROSSO DO SUL
5006903     Porto Murtinho

                                          MATO GROSSO
5100359     Alto Boa Vista                       5107743     Santa Cruz do Xingu

5100805     Apiacás                              5106174     Nova Nazaré

5103361     Conquista D'Oeste                    5107578     Rondolândia

5106315     Novo Santo Antônio

                                             PARÁ
1500503     Almeirim                             1507805     Senador José Porfírio

1500859     Anapu                                1501006     Aveiro

1503002     Faro                                 1501725     Brasil Novo

1505437     Ourilândia do Norte                  1506559     Santa Luzia do Pará

                                            PARAÍBA
2501401     Baía da Traição                      2509057     Marcação

                                          PERNAMBUCO
2605459     Fernando de Noronha                  2615805     Tupanatinga

## PDF page 77

Cód. IBGE                  Município             Cód. IBGE                  Município

2608057     Jatobá

                                             PIAUÍ
2201309     Barreiras do Piauí                  2205359      João Costa

2202307     Canto do Buriti                     2205532      Jurema

2210953     Tamboril do Piauí                   2207934      Pedro Laurentino

2202505     Caracol                             2209757      São Gonçalo do Gurguéia

2203750     Fartura do Piauí                    2211357      Várzea Branca

2204550     Guaribas

                                            PARANÁ
4115705     Matinhos

                                        RIO DE JANEIRO
3300100     Angra dos Reis                      3303500      Nova Iguaçu

3302254     Itatiaia                            3303807      Paraty

3302601     Mangaratiba

                                           RONDÔNIA
1100106     Guajará-Mirim

                                           RORAIMA
1400100     Boa Vista                           1400027      Amajari

1400209     Caracaraí                           1400282      Iracema

1400308     Mucajaí                             1400407      Normandia

1400506     São João da Baliza                  1400456      Pacaraima

                                       RIO GRANDE DO SUL
4321352     Tavares                             4303202      Cacique Doble

4302055     Benjamin Constant do Sul            4305371      Charrua

                                        SANTA CATARINA
4206306     Guabiruba                           4202701      Botuverá

4207502     Indaial                             4205175      Entre Rios

4211702     Orleans                             4209151      José Boiteux

4213807     Praia Grande                        4214102      Presidente Nereu

4201257     Apiúna

                                           SERGIPE
2800100     Amparo de São Francisco             2805307      Pirambu

2800506     Areia Branca                        2806305      Santa Luzia do Itanhy

2800704     Brejo Grande

## PDF page 78

Cód. IBGE                  Município         Cód. IBGE                 Município

                                       SÃO PAULO
3506359     Bertioga                        3537602      Peruíbe

3509700     Campos do Jordão                3541000      Praia Grande

3510500     Caraguatatuba                   3548500      Santos

3513504     Cubatão                         3548708      São Bernardo do Campo

3520301     Iguape                          3549607      São José do Barreiro

3520400     Ilhabela                        3550704      São Sebastião

3521200     Iporanga                        3551009      São Vicente

3522109     Itanhaém                        3551801      Sete Barras

3531100     Mongaguá                        3555406      Ubatuba

3537206     Pedro de Toledo

                                       TOCANTINS
1703826     Cachoeirinha                    1718659      Rio da Conceição

1710508     Itacajá                         1719004      Santa Tereza do Tocantins

1712702     Mateiros                        1721208      Tocantinópolis

1712801     Maurilândia do Tocantins        1721109      Tocantínia

1717909     Ponte Alta do Tocantins

## PDF page 79

Tabela 8 – Valores dos pesos atribuídos aos municípios brasileiros (aplicação da máscara 2) para
             alguns indicadores do SE Disponibilidade de Alimentos para Seca.
                                                      Cód.
 Cód. IBGE            Município           Pesos                       Município         Pesos
                                                      IBGE
                                              ACRE
 1200054      Assis Brasil                4          1200609   Tarauacá                 5
 1200104      Brasiléia                   5          1200708   Xapuri                   5
 1200203      Cruzeiro do Sul             5          1200013   Acrelândia               5
 1200252      Epitaciolândia              5          1200138   Bujari                   5
 1200302      Feijó                       5          1200179   Capixaba                 5
 1200336      Mâncio Lima                 5          1200328   Jordão                   4
 1200344      Manoel Urbano               4          1200351   Marechal Thaumaturgo     5
 1200385      Plácido de Castro           5          1200393   Porto Walter             5
 1200401      Rio Branco                  5          1200427   Rodrigues Alves          5
 1200450      Senador Guiomard            5          1200435   Santa Rosa do Purus      4
 1200500      Sena Madureira              5          1200807   Porto Acre               5
                                           ALAGOAS
 2700201      Anadia                      3          2707404   Porto de Pedras          2
 2700300      Arapiraca                   5          2707602   Quebrangulo              2
 2700409      Atalaia                     1          2707701   Rio Largo                1
 2700508      Barra de Santo Antônio      1          2707800   Roteiro                  1
 2700607      Barra de São Miguel         2          2707909   Santa Luzia do Norte     1
 2700706      Batalha                     2          2708006   Santana do Ipanema       2
 2701001      Boca da Mata                2          2708105   Santana do Mundaú        2
 2701100      Branquinha                  3          2708204   São Brás                 3
 2701209      Cacimbinhas                 1          2708303   São José da Laje         2
 2701308      Cajueiro                    1          2708501   São Luís do Quitunde     4
 2701357      Campestre                   1          2708600   São Miguel dos Campos    2
 2701704      Capela                      2          2708907   Satuba                   1
 2701803      Carneiros                   1          2709152   Teotônio Vilela          5
 2701902      Chã Preta                   2          2709301   União dos Palmares       3
 2702108      Colônia Leopoldina          1          2709400   Viçosa                   2
 2702207      Coqueiro Seco               1          2700102   Água Branca              3
 2702306      Coruripe                    4          2700805   Belém                    2
 2702405      Delmiro Gouveia             2          2700904   Belo Monte               3
 2702702      Feliz Deserto               1          2701407   Campo Alegre             3
 2702801      Flexeiras                   2          2701506   Campo Grande             1
 2703007      Ibateguara                  2          2701605   Canapi                   2
 2703403      Jacaré dos Homens           1          2702009   Coité do Nóia            3
 2703502      Jacuípe                     1          2702355   Craíbas                  3
 2703700      Jaramataia                  1          2702504   Dois Riachos             2
 2703809      Joaquim Gomes               3          2702553   Estrela de Alagoas       2
 2703908      Jundiá                      1          2702603   Feira Grande             4
 2704104      Lagoa da Canoa              4          2702900   Girau do Ponciano        5
 2704302      Maceió                      1          2703106   Igaci                    4
 2704401      Major Isidoro               1          2703205   Igreja Nova              4
 2704500      Maragogi                    4          2703304   Inhapi                   2
 2704609      Maravilha                   1          2703601   Japaratinga              2
 2704708      Marechal Deodoro            1          2703759   Jequiá da Praia          1
 2704807      Maribondo                   1          2704005   Junqueiro                4
 2705101      Matriz de Camaragibe        2          2704203   Limoeiro de Anadia       5
 2705200      Messias                     2          2704906   Mar Vermelho             1
 2705507      Murici                      3          2705002   Mata Grande              4
 2705606      Novo Lino                   2          2705309   Minador do Negrão        1
 2705705      Olho d'Água das Flores      1          2705408   Monteirópolis            1
 2705804      Olho d'Água do Casado       2          2705903   Olho d'Água Grande       2
 2706109      Ouro Branco                 1          2706000   Olivença                 1

## PDF page 80

2706208   Palestina                 1       2706406   Pão de Açúcar               2
2706307   Palmeira dos Índios       4       2706422   Pariconha                   2
2706448   Paripueira                1       2707206   Poço das Trincheiras        2
2706505   Passo de Camaragibe       2       2707503   Porto Real do Colégio       4
2706604   Paulo Jacinto             1       2708402   São José da Tapera          2
2706703   Penedo                    4       2708709   São Miguel dos Milagres     1
2706802   Piaçabuçu                 1       2708808   São Sebastião               5
2706901   Pilar                     1       2708956   Senador Rui Palmeira        1
2707008   Pindoba                   1       2709004   Tanque d'Arca               1
2707107   Piranhas                  2       2709103   Taquarana                   5
2707305   Porto Calvo               1       2709202   Traipu                      4
                                    AMAZONAS
1300029   Alvarães                  5       1303502   Pauini                      4
1300060   Amaturá                   2       1303536   Presidente Figueiredo       5
1300102   Anori                     2       1303569   Rio Preto da Eva            4
1300144   Apuí                      4       1303700   Santo Antônio do Içá        3
1300607   Benjamin Constant         3       1303809   São Gabriel da Cachoeira    2
1300631   Beruri                    3       1303957   São Sebastião do Uatumã     4
1300680   Boa Vista do Ramos        3       1304005   Silves                      4
1300706   Boca do Acre              3       1304062   Tabatinga                   2
1300904   Canutama                  2       1304104   Tapauá                      5
1301001   Carauari                  4       1304203   Tefé                        5
1301209   Coari                     4       1304237   Tonantins                   3
1301308   Codajás                   4       1304260   Uarini                      5
1301407   Eirunepé                  4       1304302   Urucará                     4
1301506   Envira                    5       1304401   Urucurituba                 2
1301605   Fonte Boa                 2       1300086   Anamã                       2
1301654   Guajará                   4       1300201   Atalaia do Norte            3
1301704   Humaitá                   5       1300300   Autazes                     5
1301852   Iranduba                  3       1300409   Barcelos                    2
1301902   Itacoatiara               5       1300508   Barreirinha                 3
1301951   Itamarati                 3       1300805   Borba                       4
1302009   Itapiranga                3       1300839   Caapiranga                  2
1302207   Juruá                     2       1301100   Careiro                     4
1302306   Jutaí                     4       1301159   Careiro da Várzea           2
1302405   Lábrea                    5       1301803   Ipixuna                     2
1302504   Manacapuru                5       1302108   Japurá                      3
1302603   Manaus                    3       1302553   Manaquiri                   4
1302801   Maraã                     4       1302702   Manicoré                    5
1302900   Maués                     5       1303007   Nhamundá                    4
1303205   Novo Airão                3       1303106   Nova Olinda do Norte        4
1303304   Novo Aripuanã             4       1303601   Santa Isabel do Rio Negro   3
1303403   Parintins                 5       1303908   São Paulo de Olivença       3
                                        AMAPÁ
1600055   Serra do Navio            4       1600402   Mazagão                     4
1600105   Amapá                     3       1600501   Oiapoque                    5
1600154   Pedra Branca do Amapari   4       1600535   Porto Grande                4
1600204   Calçoene                  4       1600550   Pracuúba                    3
1600212   Cutias                    3       1600600   Santana                     4
1600238   Ferreira Gomes            3       1600709   Tartarugalzinho             4
1600279   Laranjal do Jari          4       1600808   Vitória do Jari             4
1600303   Macapá                    4       1600253   Itaubal                     3
                                        BAHIA
2900207   Abaré                     2       2929750   Saubara                     1
2900306   Acajutiba                 3       2929800   Saúde                       3
2900603   Aiquara                   3       2929909   Seabra                      4
2900702   Alagoinhas                4       2930105   Senhor do Bonfim            3

## PDF page 81

2900801   Alcobaça                4   2930204   Sento Sé                 4
2900900   Almadina                2   2930501   Serrinha                 4
2901007   Amargosa                4   2930600   Serrolândia              3
2901106   Amélia Rodrigues        1   2930709   Simões Filho             2
2901155   América Dourada         4   2930758   Sítio do Mato            4
2901304   Andaraí                 2   2930774   Sobradinho               2
2901809   Antônio Gonçalves       3   2931103   Tanquinho                1
2901908   Aporá                   4   2931301   Tapiramutá               4
2901957   Apuarema                3   2931350   Teixeira de Freitas      4
2902054   Araçás                  3   2931400   Teodoro Sampaio          3
2902203   Aramari                 3   2931707   Terra Nova               2
2902252   Arataca                 1   2932200   Ubaitaba                 3
2902302   Aratuípe                4   2932309   Ubatã                    2
2902401   Aurelino Leal           3   2932408   Uibaí                    3
2902807   Barra da Estiva         4   2932507   Una                      4
2902906   Barra do Choça          5   2929255   São Gabriel              3
2903102   Barra do Rocha          3   2929305   São Gonçalo dos Campos   5
2903201   Barreiras               5   2929354   São José da Vitória      1
2903235   Barro Alto              3   2929370   São José do Jacuípe      2
2903300   Barro Preto             1   2929503   São Sebastião do Passé   3
2903409   Belmonte                3   2929602   Sapeaçu                  4
2903508   Belo Campo              4   2932705   Uruçuca                  3
2903904   Bom Jesus da Lapa       4   2932804   Utinga                   3
2904605   Brumado                 2   2932903   Valença                  5
2904704   Buerarema               1   2933000   Valente                  1
2904902   Cachoeira               4   2933109   Várzea do Poço           4
2905008   Caculé                  4   2933158   Várzea Nova              3
2905206   Caetité                 4   2933208   Vera Cruz                1
2905305   Cafarnaum               5   2933307   Vitória da Conquista     4
2905404   Cairu                   1   2933406   Wagner                   3
2905602   Camacan                 1   2933604   Xique-Xique              3
2905701   Camaçari                3   2900108   Abaíra                   2
2906204   Canarana                4   2900355   Adustina                 5
2906303   Canavieiras             4   2900405   Água Fria                5
2906501   Candeias                1   2900504   Érico Cardoso            2
2906600   Candiba                 3   2901205   Anagé                    2
2906709   Cândido Sales           5   2901353   Andorinha                2
2906824   Canudos                 3   2901403   Angical                  4
2906857   Capela do Alto Alegre   1   2901502   Anguera                  2
2906873   Capim Grosso            2   2901601   Antas                    3
2906907   Caravelas               4   2901700   Antônio Cardoso          3
2907202   Casa Nova               3   2902005   Aracatu                  4
2907301   Castro Alves            4   2902104   Araci                    4
2907509   Catu                    4   2902500   Baianópolis              4
2907608   Central                 3   2902609   Baixa Grande             3
2907806   Cícero Dantas           4   2902658   Banzaê                   3
2907905   Cipó                    2   2902708   Barra                    3
2908002   Coaraci                 2   2903003   Barra do Mendes          3
2908200   Conceição da Feira      4   2903276   Barrocas                 2
2908408   Conceição do Coité      3   2903607   Biritinga                4
2908507   Conceição do Jacuípe    4   2903706   Boa Nova                 3
2908606   Conde                   3   2903805   Boa Vista do Tupim       3
2908804   Contendas do Sincorá    2   2903953   Bom Jesus da Serra       2
2909406   Cotegipe                4   2904001   Boninal                  3
2909505   Cravolândia             3   2904050   Bonito                   3
2909802   Cruz das Almas          5   2904100   Boquira                  2
2910057   Dias d'Ávila            1   2904209   Botuporã                 2
2910503   Entre Rios              4   2904308   Brejões                  3
2910602   Esplanada               4   2904407   Brejolândia              3

## PDF page 82

2910701   Euclides da Cunha      5   2904506   Brotas de Macaúbas        3
2910727   Eunápolis              5   2904753   Buritirama                3
2910776   Feira da Mata          4   2904803   Caatiba                   2
2910800   Feira de Santana       5   2904852   Cabaceiras do Paraguaçu   4
2910859   Filadélfia             3   2905107   Caém                      3
2910909   Firmino Alves          1   2905156   Caetanos                  1
2911006   Floresta Azul          1   2905503   Caldeirão Grande          4
2911105   Formosa do Rio Preto   5   2905800   Camamu                    4
2911204   Gandu                  4   2905909   Campo Alegre de Lourdes   4
2911253   Gavião                 1   2906006   Campo Formoso             5
2911303   Gentio do Ouro         3   2906105   Canápolis                 3
2911501   Gongogi                2   2906402   Candeal                   2
2911709   Guanambi               4   2906808   Cansanção                 4
2911907   Iaçu                   2   2906899   Caraíbas                  2
2912103   Ibicaraí               1   2907004   Cardeal da Silva          2
2912202   Ibicoara               5   2907103   Carinhanha                2
2912301   Ibicuí                 2   2907400   Catolândia                2
2912400   Ibipeba                3   2907558   Caturama                  2
2912608   Ibiquera               2   2907707   Chorrochó                 1
2912806   Ibirapuã               2   2908101   Cocos                     5
2912905   Ibirataia              3   2908309   Conceição do Almeida      4
2913200   Ibotirama              2   2908705   Condeúba                  3
2913309   Ichu                   1   2908903   Coração de Maria          4
2913408   Igaporã                3   2909000   Cordeiros                 2
2913507   Iguaí                  3   2909109   Coribe                    3
2913606   Ilhéus                 4   2909208   Coronel João Sá           3
2913903   Ipiaú                  2   2909307   Correntina                5
2914000   Ipirá                  2   2909604   Crisópolis                5
2914109   Ipupiara               2   2909703   Cristópolis               4
2914604   Irecê                  3   2909901   Curaçá                    3
2914653   Itabela                3   2910008   Dário Meira               3
2914703   Itaberaba              3   2910107   Dom Basílio               2
2914802   Itabuna                1   2910206   Dom Macedo Costa          4
2914901   Itacaré                3   2910305   Elísio Medrado            3
2915106   Itagi                  3   2910404   Encruzilhada              5
2915205   Itagibá                4   2910750   Fátima                    5
2915304   Itagimirim             3   2911402   Glória                    2
2915403   Itaju do Colônia       1   2911600   Governador Mangabeira     4
2915502   Itajuípe               3   2911659   Guajeru                   2
2915601   Itamaraju              4   2911808   Guaratinga                4
2915700   Itamari                3   2911857   Heliópolis                4
2915809   Itambé                 2   2912004   Ibiassucê                 4
2916005   Itanhém                3   2912509   Ibipitanga                1
2916104   Itaparica              1   2912707   Ibirapitanga              4
2916203   Itapé                  1   2913002   Ibitiara                  3
2916302   Itapebi                1   2913101   Ibititá                   4
2916401   Itapetinga             1   2913457   Igrapiúna                 3
2916609   Itapitanga             1   2913705   Inhambupe                 5
2916708   Itaquara               3   2913804   Ipecaetá                  3
2916807   Itarantim              1   2914208   Irajuba                   4
2916856   Itatim                 1   2914307   Iramaia                   2
2916906   Itiruçu                3   2914406   Iraquara                  4
2917102   Itororó                1   2914505   Irará                     5
2917300   Ituberá                3   2915007   Itaeté                    3
2917334   Iuiu                   2   2915353   Itaguaçu da Bahia         3
2917508   Jacobina               4   2915908   Itanagra                  3
2917607   Jaguaquara             4   2916500   Itapicuru                 5
2917706   Jaguarari              4   2917003   Itiúba                    4
2917904   Jandaíra               4   2917201   Ituaçu                    4

## PDF page 83

2918001   Jequié                   3   2917359   Jaborandi                   5
2918308   Jitaúna                  3   2917409   Jacaraci                    3
2918357   João Dourado             4   2917805   Jaguaripe                   4
2918407   Juazeiro                 4   2918100   Jeremoabo                   4
2918506   Jussara                  3   2918209   Jiquiriçá                   3
2918555   Jussari                  1   2918456   Jucuruçu                    4
2918704   Lafaiete Coutinho        2   2918605   Jussiape                    2
2918902   Lajedão                  2   2918753   Lagoa Real                  3
2919058   Lajedo do Tabocal        4   2918803   Laje                        5
2919207   Lauro de Freitas         1   2919009   Lajedinho                   1
2919306   Lençóis                  3   2919108   Lamarão                     2
2919405   Licínio de Almeida       3   2919157   Lapão                       4
2919504   Livramento de Nossa      4   2919801   Macaúbas                    4
          Senhora
2919553   Luís Eduardo Magalhães   5   2919900   Macururé                    1
2919603   Macajuba                 2   2919959   Maetinga                    2
2919702   Macarani                 2   2920205   Malhada                     3
2919926   Madre de Deus            1   2920304   Malhada de Pedras           2
2920007   Maiquinique              1   2920452   Mansidão                    3
2920106   Mairi                    2   2920700   Maraú                       3
2920403   Manoel Vitorino          3   2921054   Matina                      3
2920502   Maracás                  4   2921450   Mirante                     2
2920601   Maragogipe               5   2921500   Monte Santo                 5
2920809   Marcionílio Souza        2   2921807   Mortugaba                   3
2920908   Mascote                  1   2921906   Mucugê                      5
2921005   Mata de São João         3   2922201   Muniz Ferreira              3
2921104   Medeiros Neto            3   2922250   Muquém do São Francisco     2
2921203   Miguel Calmon            4   2922409   Mutuípe                     3
2921302   Milagres                 2   2922607   Nilo Peçanha                2
2921401   Mirangaba                4   2922656   Nordestina                  1
2921609   Morpará                  2   2922706   Nova Canaã                  3
2921708   Morro do Chapéu          4   2922755   Nova Ibiá                   3
2922003   Mucuri                   3   2922805   Nova Itarana                3
2922052   Mulungu do Morro         3   2923035   Novo Horizonte              3
2922102   Mundo Novo               4   2923209   Oliveira dos Brejinhos      2
2922300   Muritiba                 4   2923308   Ouriçangas                  2
2922508   Nazaré                   3   2923357   Ourolândia                  4
2922730   Nova Fátima              1   2923704   Paratinga                   4
2922854   Nova Redenção            3   2923803   Paripiranga                 5
2922904   Nova Soure               3   2924058   Pé de Serra                 1
2923001   Nova Viçosa              3   2924108   Pedrão                      3
2923050   Novo Triunfo             2   2924207   Pedro Alexandre             4
2923100   Olindina                 4   2924306   Piatã                       3
2923407   Palmas de Monte Alto     3   2924405   Pilão Arcado                4
2923506   Palmeiras                3   2924504   Pindaí                      3
2923605   Paramirim                3   2924678   Piraí do Norte              2
2923902   Pau Brasil               1   2924900   Planaltino                  4
2924009   Paulo Afonso             3   2925709   Presidente Jânio Quadros    2
2924603   Pindobaçu                3   2925758   Presidente Tancredo Neves   5
2924652   Pintadas                 1   2925907   Quijingue                   5
2924702   Piripá                   2   2925931   Quixabeira                  2
2924801   Piritiba                 4   2925956   Rafael Jambeiro             2
2925006   Planalto                 3   2926400   Riacho de Santana           4
2925105   Poções                   3   2926509   Ribeira do Amparo           3
2925204   Pojuca                   2   2926806   Rio do Antônio              3
2925253   Ponto Novo               3   2926905   Rio do Pires                2
2925303   Porto Seguro             4   2927309   Salinas da Margarida        1
2925402   Potiraguá                1   2927507   Santa Bárbara               3
2925501   Prado                    4   2927606   Santa Brígida               3

## PDF page 84

2925600   Presidente Dutra         3       2928307   Santanópolis              3
2925808   Queimadas                2       2928505   Santa Terezinha           2
2926004   Remanso                  4       2928901   São Desidério             5
2926103   Retirolândia             1       2929404   São Miguel das Matas      5
2926202   Riachão das Neves        5       2929701   Sátiro Dias               5
2926301   Riachão do Jacuípe       1       2930006   Sebastião Laranjeiras     2
2926608   Ribeira do Pombal        4       2930154   Serra do Ramalho          3
2926657   Ribeirão do Largo        3       2930303   Serra Dourada             4
2926707   Rio de Contas            2       2930402   Serra Preta               1
2927002   Rio Real                 4       2930766   Sítio do Quinto           4
2927101   Rodelas                  1       2930808   Souto Soares              4
2927200   Ruy Barbosa              3       2930907   Tabocas do Brejo Velho    4
2927408   Salvador                 1       2931004   Tanhaçu                   2
2927705   Santa Cruz Cabrália      4       2931053   Tanque Novo               4
2927804   Santa Cruz da Vitória    1       2931202   Taperoá                   4
2927903   Santa Inês               3       2931509   Teofilândia               3
2928000   Santaluz                 2       2931608   Teolândia                 3
2928059   Santa Luzia              1       2931806   Tremedal                  4
2928109   Santa Maria da Vitória   4       2931905   Tucano                    4
2928208   Santana                  4       2932002   Uauá                      3
2928406   Santa Rita de Cássia     4       2932101   Ubaíra                    4
2928604   Santo Amaro              3       2932457   Umburanas                 4
2928703   Santo Antônio de Jesus   5       2932606   Urandi                    2
2928802   Santo Estêvão            4       2933059   Várzea da Roça            3
2928950   São Domingos             1       2933174   Varzedo                   5
2929008   São Félix                4       2933257   Vereda                    2
2929057   São Félix do Coribe      3       2933455   Wanderley                 4
2929107   São Felipe               4       2933505   Wenceslau Guimarães       5
2929206   São Francisco do Conde   2
                                       CEARÁ
2300150   Acarape                  2       2310001   Palhano                   5
2300200   Acaraú                   5       2310209   Paracuru                  4
2300309   Acopiara                 4       2310407   Paramoti                  4
2300606   Altaneira                1       2310506   Pedra Branca              4
2300705   Alto Santo               2       2310605   Penaforte                 3
2300804   Antonina do Norte        1       2310704   Pentecoste                3
2301000   Aquiraz                  2       2310852   Pindoretama               3
2301109   Aracati                  3       2310902   Piquet Carneiro           2
2301208   Aracoiaba                3       2311009   Poranga                   2
2301307   Araripe                  5       2311207   Potengi                   2
2301505   Arneiroz                 2       2311306   Quixadá                   4
2301604   Assaré                   3       2311405   Quixeramobim              4
2301703   Aurora                   3       2311504   Quixeré                   2
2301802   Baixio                   1       2311603   Redenção                  3
2301851   Banabuiú                 2       2311702   Reriutaba                 3
2301901   Barbalha                 3       2311801   Russas                    4
2302008   Barro                    3       2311900   Saboeiro                  2
2302057   Barroquinha              4       2312007   Santana do Acaraú         4
2302107   Baturité                 3       2312106   Santana do Cariri         4
2302404   Boa Viagem               4       2312205   Santa Quitéria            4
2302503   Brejo Santo              4       2312304   São Benedito              5
2302602   Camocim                  5       2312403   São Gonçalo do Amarante   4
2302701   Campos Sales             3       2312601   São Luís do Curu          2
2302800   Canindé                  4       2312700   Senador Pompeu            4
2303006   Caridade                 4       2312809   Senador Sá                3
2303204   Caririaçu                3       2312908   Sobral                    4
2303402   Carnaubal                4       2313005   Solonópole                3
2303501   Cascavel                 3       2313104   Tabuleiro do Norte        2
2303659   Catunda                  3       2313203   Tamboril                  4

## PDF page 85

2303709   Caucaia                4   2313302   Tauá                        4
2303808   Cedro                  2   2313401   Tianguá                     5
2303907   Chaval                 3   2313609   Ubajara                     5
2303956   Chorozinho             3   2313708   Umari                       1
2304004   Coreaú                 2   2313757   Umirim                      3
2304103   Crateús                5   2313807   Uruburetama                 1
2304202   Crato                  4   2313906   Uruoca                      3
2304236   Croatá                 4   2313955   Varjota                     3
2304277   Ererê                  1   2314003   Várzea Alegre               3
2304285   Eusébio                1   2300101   Abaiara                     2
2304350   Forquilha              2   2300408   Aiuaba                      3
2304400   Fortaleza              1   2300507   Alcântaras                  2
2304459   Fortim                 3   2300754   Amontada                    5
2304509   Frecheirinha           3   2300903   Apuiarés                    2
2304608   General Sampaio        2   2301257   Ararendá                    2
2304707   Granja                 5   2301406   Aratuba                     4
2304905   Groaíras               2   2301950   Barreira                    3
2304954   Guaiúba                2   2302206   Beberibe                    4
2305100   Guaramiranga           1   2302305   Bela Cruz                   5
2305209   Hidrolândia            4   2302909   Capistrano                  3
2305233   Horizonte              4   2303105   Cariré                      3
2305332   Ibicuitinga            3   2303303   Cariús                      3
2305506   Iguatu                 4   2303600   Catarina                    2
2305704   Ipaumirim              2   2303931   Choró                       2
2305803   Ipu                    4   2304251   Cruz                        5
2305902   Ipueiras               4   2304269   Deputado Irapuan Pinheiro   2
2306009   Iracema                1   2304301   Farias Brito                3
2306108   Irauçuba               3   2304657   Graça                       3
2306207   Itaiçaba               2   2304806   Granjeiro                   2
2306256   Itaitinga              2   2305001   Guaraciaba do Norte         5
2306306   Itapajé                3   2305266   Ibaretama                   3
2306405   Itapipoca              5   2305308   Ibiapina                    4
2306504   Itapiúna               3   2305357   Icapuí                      2
2306603   Itatira                3   2305407   Icó                         4
2306702   Jaguaretama            3   2305605   Independência               3
2306801   Jaguaribara            2   2305654   Ipaporanga                  3
2306900   Jaguaribe              3   2306553   Itarema                     5
2307007   Jaguaruana             3   2307106   Jardim                      3
2307205   Jati                   2   2307254   Jijoca de Jericoacoara      3
2307304   Juazeiro do Norte      2   2308351   Milhã                       3
2307403   Jucás                  3   2308401   Missão Velha                4
2307502   Lavras da Mangabeira   3   2308500   Mombaça                     3
2307601   Limoeiro do Norte      4   2308807   Moraújo                     2
2307635   Madalena               3   2308906   Morrinhos                   4
2307650   Maracanaú              1   2309102   Mulungu                     3
2307700   Maranguape             3   2309458   Ocara                       4
2307809   Marco                  4   2309805   Pacoti                      2
2307908   Martinópole            3   2310100   Palmácia                    1
2308005   Massapê                3   2310258   Paraipaba                   5
2308104   Mauriti                4   2310308   Parambu                     4
2308203   Meruoca                2   2310803   Pereiro                     2
2308302   Milagres               3   2310951   Pires Ferreira              3
2308377   Miraíma                2   2311108   Porteiras                   3
2308609   Monsenhor Tabosa       3   2311231   Potiretama                  3
2308708   Morada Nova            4   2311264   Quiterianópolis             3
2309003   Mucambo                3   2311355   Quixelô                     3
2309201   Nova Olinda            3   2311959   Salitre                     5
2309300   Nova Russas            2   2312502   São João do Jaguaribe       2
2309409   Novo Oriente           4   2313252   Tarrafas                    2

## PDF page 86

2309508   Orós                         2       2313351   Tejuçuoca                 3
2309607   Pacajus                      4       2313500   Trairi                    5
2309706   Pacatuba                     1       2313559   Tururu                    4
2309904   Pacujá                       2       2314102   Viçosa do Ceará           4
                                    DISTRITO FEDERAL
5300108   Brasília                     5
                                     ESPÍRITO SANTO
3200102   Afonso Cláudio               4       3203601   Mucurici                  3
3200169   Água Doce do Norte           2       3203809   Muqui                     1
3200201   Alegre                       2       3203908   Nova Venécia              3
3200359   Alto Rio Novo                1       3204054   Pedro Canário             3
3200409   Anchieta                     3       3204104   Pinheiros                 4
3200508   Apiacá                       1       3204203   Piúma                     1
3200607   Aracruz                      4       3204252   Ponto Belo                3
3200706   Atílio Vivacqua              2       3204401   Rio Novo do Sul           2
3200805   Baixo Guandu                 2       3204609   Santa Teresa              4
3200904   Barra de São Francisco       2       3204708   São Gabriel da Palha      1
3201001   Boa Esperança                2       3204807   São José do Calçado       2
3201100   Bom Jesus do Norte           1       3204906   São Mateus                4
3201209   Cachoeiro de Itapemirim      3       3204955   São Roque do Canaã        3
3201308   Cariacica                    2       3205002   Serra                     1
3201407   Castelo                      4       3205010   Sooretama                 3
3201506   Colatina                     3       3205069   Venda Nova do Imigrante   5
3201605   Conceição da Barra           3       3205101   Viana                     2
3201704   Conceição do Castelo         3       3205200   Vila Velha                1
3202009   Dores do Rio Preto           3       3205309   Vitória                   1
3202108   Ecoporanga                   2       3200136   Águia Branca              1
3202207   Fundão                       2       3200300   Alfredo Chaves            5
3202306   Guaçuí                       3       3201159   Brejetuba                 3
3202405   Guarapari                    3       3201803   Divino de São Lourenço    1
3202454   Ibatiba                      4       3201902   Domingos Martins          5
3202504   Ibiraçu                      2       3202256   Governador Lindenberg     1
3202603   Iconha                       2       3202553   Ibitirama                 3
3202702   Itaguaçu                     3       3202652   Irupi                     3
3202801   Itapemirim                   4       3202900   Itarana                   4
3203007   Iúna                         3       3203163   Laranja da Terra          4
3203056   Jaguaré                      2       3203700   Muniz Freire              5
3203106   Jerônimo Monteiro            1       3204005   Pancas                    1
3203130   João Neiva                   1       3204302   Presidente Kennedy        5
3203205   Linhares                     4       3204351   Rio Bananal               3
3203304   Mantenópolis                 2       3204500   Santa Leopoldina          4
3203320   Marataízes                   3       3204559   Santa Maria de Jetibá     5
3203346   Marechal Floriano            4       3204658   São Domingos do Norte     1
3203353   Marilândia                   1       3205036   Vargem Alta               3
3203403   Mimoso do Sul                2       3205150   Vila Pavão                1
3203502   Montanha                     4       3205176   Vila Valério              2
                                           GOIÁS
5200050   Abadia de Goiás              4       5212253   Lagoa Santa               1
5200100   Abadiânia                    4       5212303   Leopoldo de Bulhões       4
5200134   Acreúna                      5       5212501   Luziânia                  5
5200159   Adelândia                    2       5212600   Mairipotaba               2
5200209   Água Limpa                   1       5212709   Mambaí                    2
5200258   Águas Lindas de Goiás        2       5212808   Mara Rosa                 2
5200308   Alexânia                     4       5212907   Marzagão                  1
5200506   Aloândia                     1       5212956   Matrinchã                 5
5200555   Alto Horizonte               1       5213004   Maurilândia               2
5200605   Alto Paraíso de Goiás        5       5213087   Minaçu                    3

## PDF page 87

5200803   Alvorada do Norte       3   5213103   Mineiros                   5
5200852   Americano do Brasil     3   5213400   Moiporá                    1
5200902   Amorinópolis            2   5213707   Montes Claros de Goiás     5
5201108   Anápolis                4   5213756   Montividiu                 5
5201207   Anhanguera              1   5213806   Morrinhos                  5
5201306   Anicuns                 3   5213855   Morro Agudo de Goiás       1
5201405   Aparecida de Goiânia    1   5213905   Mossâmedes                 4
5201454   Aparecida do Rio Doce   2   5214002   Mozarlândia                2
5201504   Aporé                   2   5214051   Mundo Novo                 3
5201603   Araçu                   3   5214101   Mutunópolis                2
5201702   Aragarças               1   5214408   Nazário                    4
5201801   Aragoiânia              1   5214507   Nerópolis                  3
5202155   Araguapaz               2   5214606   Niquelândia                5
5202353   Arenópolis              2   5214705   Nova América               1
5202502   Aruanã                  3   5214804   Nova Aurora                2
5202601   Aurilândia              2   5214838   Nova Crixás                3
5202809   Avelinópolis            3   5214861   Nova Glória                4
5203203   Barro Alto              4   5214879   Nova Iguaçu de Goiás       1
5203302   Bela Vista de Goiás     5   5215009   Nova Veneza                4
5203401   Bom Jardim de Goiás     3   5215207   Novo Brasil                2
5203500   Bom Jesus de Goiás      5   5215231   Novo Gama                  3
5203559   Bonfinópolis            3   5215256   Novo Planalto              2
5203609   Brazabrantes            4   5215306   Orizona                    5
5203807   Britânia                4   5215405   Ouro Verde de Goiás        3
5203906   Buriti Alegre           3   5215504   Ouvidor                    2
5203939   Buriti de Goiás         1   5215652   Palestina de Goiás         4
5203962   Buritinópolis           1   5215702   Palmeiras de Goiás         5
5204003   Cabeceiras              5   5215801   Palmelo                    1
5204102   Cachoeira Alta          1   5215900   Palminópolis               5
5204201   Cachoeira de Goiás      1   5216007   Panamá                     3
5204250   Cachoeira Dourada       3   5216304   Paranaiguara               3
5204300   Caçu                    2   5216403   Paraúna                    5
5204409   Caiapônia               5   5216452   Perolândia                 5
5204508   Caldas Novas            5   5216809   Petrolina de Goiás         4
5204557   Caldazinha              2   5217104   Piracanjuba                5
5204607   Campestre de Goiás      4   5217203   Piranhas                   2
5204656   Campinaçu               3   5217302   Pirenópolis                4
5204706   Campinorte              2   5217401   Pires do Rio               3
5204805   Campo Alegre de Goiás   5   5217609   Planaltina                 5
5204854   Campo Limpo de Goiás    4   5217708   Pontalina                  5
5204904   Campos Belos            2   5218003   Porangatu                  3
5204953   Campos Verdes           1   5218052   Porteirão                  3
5205000   Carmo do Rio Verde      3   5218102   Portelândia                4
5205059   Castelândia             2   5218300   Posse                      2
5205109   Catalão                 5   5218391   Professor Jamil            1
5205208   Caturaí                 3   5218508   Quirinópolis               4
5205307   Cavalcante              3   5218607   Rialma                     2
5205406   Ceres                   2   5218706   Rianápolis                 3
5205455   Cezarina                4   5218789   Rio Quente                 1
5205471   Chapadão do Céu         5   5218805   Rio Verde                  5
5205497   Cidade Ocidental        4   5218904   Rubiataba                  1
5205521   Colinas do Sul          1   5219001   Sanclerlândia              2
5205703   Córrego do Ouro         2   5219100   Santa Bárbara de Goiás     2
5205802   Corumbá de Goiás        5   5219258   Santa Fé de Goiás          4
5205901   Corumbaíba              3   5219308   Santa Helena de Goiás      5
5206206   Cristalina              5   5219407   Santa Rita do Araguaia     3
5206305   Cristianópolis          4   5219506   Santa Rosa de Goiás        4
5206404   Crixás                  2   5219605   Santa Tereza de Goiás      2
5206503   Cromínia                4   5219704   Santa Terezinha de Goiás   1

## PDF page 88

5206602   Cumari                 2     5219712   Santo Antônio da Barra       3
5206701   Damianópolis           2     5219738   Santo Antônio de Goiás       3
5206800   Damolândia             3     5219753   Santo Antônio do             3
                                                 Descoberto
5206909   Davinópolis            2     5219803   São Domingos                 2
5207105   Diorama                2     5219902   São Francisco de Goiás       3
5207253   Doverlândia            4     5220009   São João d'Aliança           5
5207352   Edealina               5     5220058   São João da Paraúna          3
5207402   Edéia                  5     5220108   São Luís de Montes Belos     2
5207501   Estrela do Norte       2     5220157   São Luiz do Norte            4
5207535   Faina                  2     5220207   São Miguel do Araguaia       4
5207600   Fazenda Nova           2     5220264   São Miguel do Passa Quatro   5
5207808   Firminópolis           4     5220280   São Patrício                 2
5208004   Formosa                5     5220405   São Simão                    1
5208103   Formoso                2     5220454   Senador Canedo               2
5208301   Divinópolis de Goiás   2     5220504   Serranópolis                 5
5208400   Goianápolis            4     5220603   Silvânia                     5
5208509   Goiandira              2     5220686   Simolândia                   1
5208608   Goianésia              5     5221007   Taquaral de Goiás            3
5208707   Goiânia                2     5221080   Teresina de Goiás            1
5208806   Goianira               3     5221197   Terezópolis de Goiás         3
5208905   Goiás                  5     5221304   Três Ranchos                 2
5209101   Goiatuba               5     5221403   Trindade                     5
5209150   Gouvelândia            2     5221452   Trombas                      3
5209200   Guapó                  4     5221502   Turvânia                     5
5209291   Guaraíta               2     5221551   Turvelândia                  4
5209457   Guarinos               2     5221577   Uirapuru                     1
5209606   Heitoraí               2     5221601   Uruaçu                       4
5209705   Hidrolândia            5     5221700   Uruana                       5
5209804   Hidrolina              2     5221809   Urutaí                       3
5209903   Iaciara                3     5221858   Valparaíso de Goiás          1
5209937   Inaciolândia           3     5221908   Varjão                       2
5209952   Indiara                5     5222005   Vianópolis                   5
5210000   Inhumas                5     5222054   Vicentinópolis               5
5210109   Ipameri                5     5222203   Vila Boa                     3
5210208   Iporá                  3     5200175   Água Fria de Goiás           5
5210307   Israelândia            1     5200829   Amaralina                    1
5210406   Itaberaí               5     5203104   Baliza                       2
5210562   Itaguari               4     5203575   Bonópolis                    3
5210604   Itaguaru               4     5205513   Cocalzinho de Goiás          4
5210802   Itajá                  1     5207907   Flores de Goiás              5
5210901   Itapaci                4     5208152   Gameleira de Goiás           5
5211008   Itapirapuã             3     5209408   Guarani de Goiás             2
5211206   Itapuranga             2     5210158   Ipiranga de Goiás            2
5211305   Itarumã                2     5213053   Mimoso de Goiás              4
5211404   Itauçu                 4     5213509   Monte Alegre de Goiás        2
5211503   Itumbiara              4     5213772   Montividiu do Norte          3
5211602   Ivolândia              2     5214903   Nova Roma                    2
5211701   Jandaia                4     5215603   Padre Bernardo               5
5211800   Jaraguá                4     5216908   Pilar de Goiás               2
5211909   Jataí                  5     5219209   Santa Cruz de Goiás          5
5212006   Jaupaci                2     5219357   Santa Isabel                 4
5212055   Jesúpolis              2     5219456   Santa Rita do Novo Destino   4
5212105   Joviânia               5     5220702   Sítio d'Abadia               4
5212204   Jussara                5     5222302   Vila Propício                4
                                 MARANHÃO
2100055   Açailândia             3     2111763   Senador La Rocque            1
2100105   Afonso Cunha           2     2111904   Sucupira do Norte            3
2100303   Aldeias Altas          3     2111953   Sucupira do Riachão          2

## PDF page 89

2100436   Alto Alegre do Maranhão    3   2112001   Tasso Fragoso               5
2100501   Alto Parnaíba              4   2112100   Timbiras                    3
2100550   Amapá do Maranhão          3   2112209   Timon                       4
2100808   Anapurus                   4   2112233   Trizidela do Vale           2
2100832   Apicum-Açu                 3   2112274   Tufilândia                  2
2101004   Arari                      4   2112605   Urbano Santos               5
2101202   Bacabal                    5   2112704   Vargem Grande               5
2101301   Bacuri                     3   2112803   Viana                       4
2101400   Balsas                     5   2112852   Vila Nova dos Martírios     1
2101509   Barão de Grajaú            2   2112902   Vitória do Mearim           4
2101608   Barra do Corda             5   2113009   Vitorino Freire             4
2101731   Belágua                    4   2114007   Zé Doca                     5
2101806   Benedito Leite             2   2100154   Água Doce do Maranhão       4
2101970   Boa Vista do Gurupi        3   2100204   Alcântara                   4
2102150   Brejo de Areia             4   2100402   Altamira do Maranhão        3
2102309   Buriti Bravo               3   2100477   Alto Alegre do Pindaré      5
2102325   Buriticupu                 5   2100600   Amarante do Maranhão        3
2102556   Campestre do Maranhão      2   2100709   Anajatuba                   4
2102606   Cândido Mendes             4   2100873   Araguanã                    4
2102705   Cantanhede                 4   2100907   Araioses                    5
2102754   Capinzal do Norte          3   2100956   Arame                       5
2102804   Carolina                   4   2101103   Axixá                       3
2102903   Carutapera                 4   2101251   Bacabeira                   3
2103000   Caxias                     4   2101350   Bacurituba                  3
2103125   Central do Maranhão        3   2101707   Barreirinhas                5
2103158   Centro do Guilherme        4   2101772   Bela Vista do Maranhão      2
2103208   Chapadinha                 4   2101905   Bequimão                    4
2103307   Codó                       5   2101939   Bernardo do Mearim          3
2103406   Coelho Neto                2   2102002   Bom Jardim                  5
2103505   Colinas                    4   2102036   Bom Jesus das Selvas        4
2103554   Conceição do Lago-Açu      3   2102077   Bom Lugar                   3
2103604   Coroatá                    3   2102101   Brejo                       4
2103703   Cururupu                   3   2102200   Buriti                      4
2103752   Davinópolis                1   2102358   Buritirana                  2
2103802   Dom Pedro                  2   2102374   Cachoeira Grande            4
2103901   Duque Bacelar              2   2102408   Cajapió                     3
2104008   Esperantinópolis           3   2102507   Cajari                      3
2104057   Estreito                   2   2103109   Cedral                      3
2104107   Fortaleza dos Nogueiras    4   2103174   Centro Novo do Maranhão     4
2104206   Fortuna                    4   2103257   Cidelândia                  1
2104305   Godofredo Viana            4   2104073   Feira Nova do Maranhão      3
2104503   Governador Archer          2   2104081   Fernando Falcão             4
2104628   Governador Luiz Rocha      3   2104099   Formosa da Serra Negra      3
2104677   Governador Nunes Freire    4   2104404   Gonçalves Dias              3
2104701   Graça Aranha               3   2104552   Governador Edison Lobão     1
2104800   Grajaú                     5   2104602   Governador Eugênio Barros   3
2104909   Guimarães                  3   2104651   Governador Newton Bello     4
2105153   Igarapé do Meio            3   2105005   Humberto de Campos          4
2105203   Igarapé Grande             2   2105104   Icatu                       4
2105302   Imperatriz                 1   2105351   Itaipava do Grajaú          3
2105401   Itapecuru Mirim            5   2105450   Jatobá                      3
2105427   Itinga do Maranhão         3   2105476   Jenipapo dos Vieiras        3
2105500   João Lisboa                1   2105609   Joselândia                  2
2105658   Junco do Maranhão          3   2105807   Lago do Junco               3
2105708   Lago da Pedra              4   2105906   Lago Verde                  3
2105948   Lago dos Rodrigues         3   2105922   Lagoa do Mato               3
2105963   Lagoa Grande do Maranhão   3   2105989   Lajeado Novo                2
2106003   Lima Campos                2   2106359   Marajá do Sena              3
2106102   Loreto                     4   2106409   Mata Roma                   4

## PDF page 90

2106201   Luís Domingues                3      2106508   Matinha                     4
2106300   Magalhães de Almeida          4      2106607   Matões                      4
2106326   Maracaçumé                    4      2106631   Matões do Norte             4
2106375   Maranhãozinho                 5      2106672   Milagres do Maranhão        4
2106755   Miranda do Norte              3      2106706   Mirador                     4
2106805   Mirinzal                      3      2106904   Monção                      4
2107001   Montes Altos                  1      2107100   Morros                      4
2107308   Nova Iorque                   2      2107209   Nina Rodrigues              4
2107357   Nova Olinda do Maranhão       4      2107258   Nova Colinas                3
2107407   Olho d'Água das Cunhãs        3      2107456   Olinda Nova do Maranhão     4
2107506   Paço do Lumiar                1      2107605   Palmeirândia                4
2107704   Paraibano                     3      2107803   Parnarama                   4
2107902   Passagem Franca               3      2108058   Paulino Neves               4
2108009   Pastos Bons                   3      2108256   Pedro do Rosário            4
2108108   Paulo Ramos                   4      2108405   Peri Mirim                  4
2108207   Pedreiras                     2      2108454   Peritoró                    2
2108306   Penalva                       4      2108900   Poção de Pedras             3
2108504   Pindaré-Mirim                 2      2109056   Porto Rico do Maranhão      3
2108603   Pinheiro                      5      2109205   Presidente Juscelino        4
2108702   Pio XII                       3      2109270   Presidente Sarney           4
2108801   Pirapemas                     4      2109304   Presidente Vargas           4
2109007   Porto Franco                  2      2109403   Primeira Cruz               3
2109106   Presidente Dutra              3      2109759   Santa Filomena do           3
                                                         Maranhão
2109239   Presidente Médici             3      2110005   Santa Luzia                 5
2109452   Raposa                        1      2110203   Santa Rita                  4
2109502   Riachão                       5      2110237   Santana do Maranhão         4
2109551   Ribamar Fiquene               2      2110278   Santo Amaro do Maranhão     4
2109601   Rosário                       4      2110302   Santo Antônio dos Lopes     2
2109700   Sambaíba                      4      2110609   São Bernardo                4
2109809   Santa Helena                  3      2110807   São Félix de Balsas         2
2109908   Santa Inês                    4      2110856   São Francisco do Brejão     1
2110039   Santa Luzia do Paruá          4      2110906   São Francisco do Maranhão   3
2110104   Santa Quitéria do Maranhão    4      2111003   São João Batista            4
2110401   São Benedito do Rio Preto     4      2111078   São João do Soter           3
2110500   São Bento                     3      2111201   São José de Ribamar         1
2110658   São Domingos do Azeitão       4      2111250   São José dos Basílios       2
2110708   São Domingos do Maranhão      5      2111409   São Luís Gonzaga do         4
                                                         Maranhão
2111029   São João do Carú              4      2111631   São Raimundo do Doca        2
                                                         Bezerra
2111052   São João do Paraíso           2      2111706   São Vicente Ferrer          4
2111102   São João dos Patos            3      2111722   Satubinha                   3
2111300   São Luís                      1      2111789   Serrano do Maranhão         4
2111508   São Mateus do Maranhão        4      2111805   Sítio Novo                  3
2111532   São Pedro da Água Branca      1      2112308   Tuntum                      4
2111573   São Pedro dos Crentes         3      2112407   Turiaçu                     5
2111607   São Raimundo das              4      2112456   Turilândia                  4
          Mangabeiras
2111672   São Roberto                   2      2112506   Tutóia                      5
2111748   Senador Alexandre Costa       3
                                       MINAS GERAIS
3100104   Abadia dos Dourados           2      3144201   Nacip Raydan                1
3100203   Abaeté                        3      3144300   Nanuque                     2
3100302   Abre Campo                    3      3144359   Naque                       1
3100401   Acaiaca                       1      3144375   Natalândia                  3
3100708   Água Comprida                 3      3144409   Natércia                    2
3100807   Aguanil                       3      3144508   Nazareno                    4
3100906   Águas Formosas                3      3144607   Nepomuceno                  4

## PDF page 91

3101003   Águas Vermelhas          3   3144706   Nova Era                  1
3101102   Aimorés                  4   3144805   Nova Lima                 1
3101201   Aiuruoca                 3   3144904   Nova Módica               1
3101409   Albertina                1   3145000   Nova Ponte                5
3101508   Além Paraíba             1   3145059   Nova Porteirinha          2
3101607   Alfenas                  5   3145109   Nova Resende              4
3101631   Alfredo Vasconcelos      4   3145208   Nova Serrana              1
3101706   Almenara                 4   3145455   Olhos-d'Água              2
3101805   Alpercata                1   3145505   Olímpio Noronha           1
3101904   Alpinópolis              4   3145604   Oliveira                  4
3102001   Alterosa                 4   3145703   Oliveira Fortes           1
3102050   Alto Caparaó             1   3145802   Onça de Pitangui          4
3102209   Alvarenga                1   3145851   Oratórios                 1
3102308   Alvinópolis              2   3145901   Ouro Branco               3
3102506   Amparo do Serra          2   3146008   Ouro Fino                 3
3102605   Andradas                 5   3146107   Ouro Preto                3
3102704   Cachoeira de Pajeú       3   3146206   Ouro Verde de Minas       2
3102803   Andrelândia              4   3146255   Padre Carvalho            2
3102852   Angelândia               2   3146305   Padre Paraíso             3
3102902   Antônio Carlos           3   3146404   Paineiras                 1
3103009   Antônio Dias             1   3146503   Pains                     3
3103108   Antônio Prado de Minas   1   3146602   Paiva                     1
3103207   Araçaí                   1   3146701   Palma                     1
3103306   Aracitaba                1   3146750   Palmópolis                2
3103405   Araçuaí                  3   3146909   Papagaios                 3
3103504   Araguari                 5   3147006   Paracatu                  5
3103603   Arantina                 1   3147105   Pará de Minas             3
3103751   Araporã                  3   3147204   Paraguaçu                 5
3103801   Arapuá                   2   3147303   Paraisópolis              4
3103900   Araújos                  3   3147402   Paraopeba                 2
3104007   Araxá                    5   3147501   Passabém                  1
3104106   Arceburgo                2   3147600   Passa Quatro              3
3104205   Arcos                    4   3147709   Passa Tempo               4
3104304   Areado                   3   3147808   Passa Vinte               2
3104403   Argirita                 1   3147907   Passos                    5
3104502   Arinos                   5   3148004   Patos de Minas            5
3104601   Astolfo Dutra            1   3148103   Patrocínio                5
3104700   Ataléia                  3   3148202   Patrocínio do Muriaé      1
3104809   Augusto de Lima          2   3148301   Paula Cândido             3
3104908   Baependi                 3   3148509   Pavão                     2
3105004   Baldim                   3   3148608   Peçanha                   3
3105103   Bambuí                   5   3148707   Pedra Azul                3
3105202   Bandeira                 2   3148806   Pedra do Anta             2
3105301   Bandeira do Sul          2   3148905   Pedra do Indaiá           1
3105400   Barão de Cocais          1   3149002   Pedra Dourada             1
3105509   Barão de Monte Alto      1   3149101   Pedralva                  3
3105608   Barbacena                5   3149150   Pedras de Maria da Cruz   1
3105905   Barroso                  1   3149200   Pedrinópolis              5
3106002   Bela Vista de Minas      1   3149309   Pedro Leopoldo            1
3106200   Belo Horizonte           1   3149408   Pedro Teixeira            1
3106309   Belo Oriente             1   3149507   Pequeri                   1
3106606   Bertópolis               2   3149606   Pequi                     4
3106655   Berizal                  2   3149705   Perdigão                  3
3106705   Betim                    1   3149804   Perdizes                  5
3106903   Bicas                    1   3149903   Perdões                   3
3107000   Biquinhas                2   3149952   Periquito                 2
3107109   Boa Esperança            5   3150000   Pescador                  1
3107208   Bocaina de Minas         1   3150109   Piau                      2
3107307   Bocaiúva                 4   3150158   Piedade de Caratinga      3

## PDF page 92

3107406   Bom Despacho            4   3150208   Piedade de Ponte Nova   1
3107505   Bom Jardim de Minas     2   3150307   Piedade do Rio Grande   4
3107604   Bom Jesus da Penha      4   3150505   Pimenta                 5
3107802   Bom Jesus do Galho      3   3150539   Pingo d'Água            1
3107901   Bom Repouso             5   3150604   Piracema                4
3108008   Bom Sucesso             3   3150703   Pirajuba                3
3108107   Bonfim                  4   3151008   Piranguinho             1
3108206   Bonfinópolis de Minas   5   3151107   Pirapetinga             1
3108305   Borda da Mata           4   3151206   Pirapora                2
3108404   Botelhos                3   3151305   Piraúba                 3
3108503   Botumirim               2   3151404   Pitangui                3
3108552   Brasilândia de Minas    5   3151503   Piumhi                  5
3108602   Brasília de Minas       3   3151602   Planura                 4
3108701   Brás Pires              2   3151701   Poço Fundo              3
3108909   Brazópolis              3   3151800   Poços de Caldas         5
3109006   Brumadinho              3   3151909   Pocrane                 2
3109105   Bueno Brandão           5   3152006   Pompéu                  4
3109204   Buenópolis              3   3152105   Ponte Nova              2
3109303   Buritis                 5   3152131   Ponto Chique            3
3109402   Buritizeiro             5   3152204   Porteirinha             2
3109451   Cabeceira Grande        5   3152402   Poté                    3
3109501   Cabo Verde              3   3152501   Pouso Alegre            5
3109600   Cachoeira da Prata      1   3152600   Pouso Alto              2
3109709   Cachoeira de Minas      5   3152709   Prados                  4
3109808   Cachoeira Dourada       3   3152808   Prata                   4
3109907   Caetanópolis            1   3152907   Pratápolis              4
3110004   Caeté                   1   3153004   Pratinha                5
3110103   Caiana                  1   3153301   Presidente Kubitschek   1
3110202   Cajuri                  3   3153400   Presidente Olegário     5
3110301   Caldas                  5   3153509   Alto Jequitibá          2
3110509   Camanducaia             5   3153608   Prudente de Morais      1
3110608   Cambuí                  3   3153707   Quartel Geral           1
3110707   Cambuquira              4   3153905   Raposos                 1
3110806   Campanário              1   3154002   Raul Soares             3
3110905   Campanha                4   3154101   Recreio                 1
3111002   Campestre               5   3154150   Reduto                  1
3111101   Campina Verde           2   3154200   Resende Costa           4
3111200   Campo Belo              3   3154309   Resplendor              2
3111309   Campo do Meio           4   3154408   Ressaquinha             4
3111408   Campo Florido           4   3154457   Riachinho               4
3111507   Campos Altos            5   3154507   Riacho dos Machados     1
3111606   Campos Gerais           4   3154606   Ribeirão das Neves      1
3111804   Canápolis               4   3154705   Ribeirão Vermelho       1
3111903   Cana Verde              2   3154804   Rio Acima               1
3112000   Candeias                4   3154903   Rio Casca               3
3112059   Cantagalo               2   3155009   Rio Doce                1
3112307   Capelinha               3   3155108   Rio do Prado            2
3112406   Capetinga               3   3155306   Rio Manso               2
3112505   Capim Branco            1   3155405   Rio Novo                1
3112604   Capinópolis             4   3155504   Rio Paranaíba           5
3112653   Capitão Andrade         1   3155702   Rio Piracicaba          1
3112703   Capitão Enéas           3   3155801   Rio Pomba               2
3112802   Capitólio               3   3155900   Rio Preto               1
3113206   Carandaí                5   3156106   Ritápolis               2
3113305   Carangola               2   3156205   Rochedo de Minas        1
3113404   Caratinga               4   3156304   Rodeiro                 1
3113503   Carbonita               2   3156403   Romaria                 5
3113602   Careaçu                 4   3156452   Rosário da Limeira      1
3113701   Carlos Chagas           3   3156601   Rubim                   2

## PDF page 93

3113800   Carmésia                   1   3156700   Sabará                        1
3113909   Carmo da Cachoeira         4   3156809   Sabinópolis                   2
3114006   Carmo da Mata              2   3156908   Sacramento                    5
3114105   Carmo de Minas             3   3157005   Salinas                       3
3114204   Carmo do Cajuru            3   3157104   Salto da Divisa               1
3114303   Carmo do Paranaíba         4   3157203   Santa Bárbara                 1
3114402   Carmo do Rio Claro         5   3157252   Santa Bárbara do Leste        3
3114501   Carmópolis de Minas        5   3157278   Santa Bárbara do Monte        1
                                                   Verde
3114550   Carneirinho                2   3157302   Santa Bárbara do Tugúrio      2
3114600   Carrancas                  5   3157336   Santa Cruz de Minas           1
3114709   Carvalhópolis              2   3157500   Santa Efigênia de Minas       1
3114808   Carvalhos                  1   3157609   Santa Fé de Minas             2
3114907   Casa Grande                4   3157658   Santa Helena de Minas         2
3115003   Cascalho Rico              3   3157708   Santa Juliana                 5
3115102   Cássia                     4   3157807   Santa Luzia                   1
3115201   Conceição da Barra de      3   3157906   Santa Margarida               3
          Minas
3115300   Cataguases                 1   3158003   Santa Maria de Itabira        1
3115359   Catas Altas                1   3158102   Santa Maria do Salto          2
3115474   Catuti                     1   3158201   Santa Maria do Suaçuí         2
3115508   Caxambu                    1   3158300   Santana da Vargem             3
3115607   Cedro do Abaeté            1   3158409   Santana de Cataguases         1
3115706   Central de Minas           1   3158706   Santana do Garambéu           1
3115805   Centralina                 4   3158805   Santana do Jacaré             1
3115904   Chácara                    1   3158904   Santana do Manhuaçu           2
3116001   Chalé                      1   3158953   Santana do Paraíso            2
3116159   Chapada Gaúcha             4   3159001   Santana do Riacho             1
3116209   Chiador                    1   3159100   Santana dos Montes            1
3116407   Claraval                   2   3159209   Santa Rita de Caldas          5
3116506   Claro dos Poções           2   3159308   Santa Rita de Jacutinga       1
3116605   Cláudio                    3   3159357   Santa Rita de Minas           2
3116704   Coimbra                    4   3159407   Santa Rita de Ibitipoca       2
3116902   Comendador Gomes           3   3159605   Santa Rita do Sapucaí         4
3117108   Conceição da Aparecida     4   3159704   Santa Rosa da Serra           2
3117207   Conceição das Pedras       3   3159803   Santa Vitória                 2
3117306   Conceição das Alagoas      5   3159902   Santo Antônio do Amparo       2
3117504   Conceição do Mato Dentro   2   3160009   Santo Antônio do              2
                                                   Aventureiro
3117702   Conceição do Rio Verde     5   3160108   Santo Antônio do Grama        1
3117801   Conceição dos Ouros        4   3160306   Santo Antônio do Jacinto      4
3117876   Confins                    1   3160405   Santo Antônio do Monte        3
3117900   Congonhal                  4   3160504   Santo Antônio do Rio Abaixo   1
3118007   Congonhas                  1   3160603   Santo Hipólito                1
3118106   Congonhas do Norte         2   3160702   Santos Dumont                 1
3118205   Conquista                  3   3160801   São Bento Abade               4
3118304   Conselheiro Lafaiete       3   3160900   São Brás do Suaçuí            2
3118403   Conselheiro Pena           2   3160959   São Domingos das Dores        2
3118502   Consolação                 1   3161007   São Domingos do Prata         2
3118601   Contagem                   1   3161056   São Félix de Minas            2
3118700   Coqueiral                  4   3161106   São Francisco                 2
3118809   Coração de Jesus           5   3161205   São Francisco de Paula        3
3118908   Cordisburgo                2   3161304   São Francisco de Sales        2
3119005   Cordislândia               4   3161403   São Francisco do Glória       1
3119104   Corinto                    2   3161502   São Geraldo                   2
3119203   Coroaci                    2   3161650   São Geraldo do Baixio         1
3119302   Coromandel                 5   3161700   São Gonçalo do Abaeté         5
3119401   Coronel Fabriciano         1   3161809   São Gonçalo do Pará           1
3119500   Coronel Murta              1   3161908   São Gonçalo do Rio Abaixo     1

## PDF page 94

3119609   Coronel Pacheco          1   3162005   São Gonçalo do Sapucaí        5
3119708   Coronel Xavier Chaves    3   3162104   São Gotardo                   5
3119807   Córrego Danta            2   3162203   São João Batista do Glória    5
3119906   Córrego do Bom Jesus     3   3162252   São João da Lagoa             3
3119955   Córrego Fundo            2   3162302   São João da Mata              4
3120003   Córrego Novo             1   3162500   São João del Rei              5
3120102   Couto de Magalhães de    1   3162575   São João do Manteninha        1
          Minas
3120151   Crisólita                2   3162609   São João do Oriente           1
3120201   Cristais                 4   3162807   São João Evangelista          3
3120300   Cristália                2   3162906   São João Nepomuceno           1
3120409   Cristiano Otoni          3   3162922   São Joaquim de Bicas          2
3120508   Cristina                 4   3162948   São José da Barra             4
3120607   Crucilândia              3   3162955   São José da Lapa              1
3120706   Cruzeiro da Fortaleza    4   3163003   São José da Safira            1
3120805   Cruzília                 4   3163102   São José da Varginha          4
3120839   Cuparaque                1   3163201   São José do Alegre            2
3120870   Curral de Dentro         2   3163300   São José do Divino            1
3120904   Curvelo                  4   3163409   São José do Goiabal           1
3121001   Datas                    4   3163607   São José do Mantimento        2
3121209   Delfinópolis             4   3163706   São Lourenço                  1
3121258   Delta                    1   3163805   São Miguel do Anta            3
3121308   Descoberto               1   3163904   São Pedro da União            4
3121407   Desterro de Entre Rios   3   3164001   São Pedro dos Ferros          2
3121605   Diamantina               2   3164209   São Romão                     5
3121803   Dionísio                 1   3164308   São Roque de Minas            5
3121902   Divinésia                1   3164407   São Sebastião da Bela Vista   3
3122009   Divino                   3   3164431   São Sebastião da Vargem       2
                                                 Alegre
3122108   Divino das Laranjeiras   1   3164472   São Sebastião do Anta         2
3122207   Divinolândia de Minas    1   3164605   São Sebastião do Oeste        2
3122306   Divinópolis              3   3164704   São Sebastião do Paraíso      5
3122355   Divisa Alegre            2   3164803   São Sebastião do Rio Preto    1
3122405   Divisa Nova              4   3164902   São Sebastião do Rio Verde    1
3122454   Divisópolis              2   3165008   São Tiago                     2
3122470   Dom Bosco                3   3165107   São Tomás de Aquino           2
3122504   Dom Cavati               2   3165206   São Thomé das Letras          3
3122603   Dom Joaquim              1   3165305   São Vicente de Minas          4
3122702   Dom Silvério             1   3165404   Sapucaí-Mirim                 3
3122900   Dona Eusébia             1   3165537   Sarzedo                       1
3123007   Dores de Campos          2   3165560   Sem-Peixe                     1
3123205   Dores do Indaiá          2   3165578   Senador Amaral                5
3123403   Doresópolis              2   3165602   Senador Cortes                1
3123502   Douradoquara             1   3165701   Senador Firmino               2
3123528   Durandé                  1   3166006   Senhora de Oliveira           1
3123601   Elói Mendes              3   3166303   Sericita                      2
3123700   Engenheiro Caldas        1   3166402   Seritinga                     1
3123809   Engenheiro Navarro       2   3166600   Serra da Saudade              1
3123858   Entre Folhas             2   3166709   Serra dos Aimorés             1
3123908   Entre Rios de Minas      4   3166808   Serra do Salitre              5
3124005   Ervália                  4   3166907   Serrania                      3
3124104   Esmeraldas               2   3167004   Serranos                      1
3124203   Espera Feliz             3   3167103   Serro                         2
3124302   Espinosa                 3   3167202   Sete Lagoas                   2
3124609   Estrela Dalva            1   3167301   Silveirânia                   1
3124708   Estrela do Indaiá        4   3167400   Silvianópolis                 4
3124807   Estrela do Sul           5   3167509   Simão Pereira                 1
3124906   Eugenópolis              1   3167707   Sobrália                      1
3125002   Ewbank da Câmara         1   3167806   Soledade de Minas             2

## PDF page 95

3125101   Extrema                    3   3167905   Tabuleiro                1
3125200   Fama                       2   3168002   Taiobeiras               4
3125309   Faria Lemos                1   3168101   Tapira                   5
3125507   São Gonçalo do Rio Preto   1   3168200   Tapiraí                  3
3125606   Felisburgo                 2   3168408   Tarumirim                2
3125705   Felixlândia                3   3168507   Teixeiras                2
3125804   Fernandes Tourinho         1   3168606   Teófilo Otoni            4
3126000   Florestal                  3   3168705   Timóteo                  1
3126109   Formiga                    5   3168804   Tiradentes               2
3126208   Formoso                    5   3168903   Tiros                    4
3126307   Fortaleza de Minas         3   3169000   Tocantins                3
3126406   Fortuna de Minas           1   3169208   Tombos                   2
3126604   Francisco Dumont           1   3169307   Três Corações            5
3126703   Francisco Sá               2   3169356   Três Marias              3
3126901   Frei Inocêncio             1   3169406   Três Pontas              4
3127008   Fronteira                  1   3169505   Tumiritinga              1
3127057   Fronteira dos Vales        2   3169604   Tupaciguara              5
3127107   Frutal                     4   3169703   Turmalina                2
3127206   Funilândia                 1   3169802   Turvolândia              5
3127305   Galiléia                   1   3169901   Ubá                      3
3127370   Goiabeira                  1   3170008   Ubaí                     3
3127388   Goianá                     1   3170057   Ubaporanga               3
3127503   Gonzaga                    1   3170107   Uberaba                  5
3127602   Gouveia                    3   3170206   Uberlândia               5
3127701   Governador Valadares       3   3170305   Umburatiba               1
3127909   Grupiara                   1   3170404   Unaí                     5
3128006   Guanhães                   2   3170438   União de Minas           1
3128105   Guapé                      4   3170479   Uruana de Minas          4
3128253   Guaraciama                 2   3170503   Urucânia                 1
3128303   Guaranésia                 3   3170578   Vargem Alegre            4
3128402   Guarani                    1   3170602   Vargem Bonita            3
3128501   Guarará                    1   3170651   Vargem Grande do Rio     2
                                                   Pardo
3128600   Guarda-Mor                 5   3170701   Varginha                 3
3128709   Guaxupé                    2   3170750   Varjão de Minas          5
3128808   Guidoval                   2   3170800   Várzea da Palma          3
3128907   Guimarânia                 4   3171006   Vazante                  4
3129004   Guiricema                  3   3171030   Verdelândia              2
3129202   Heliodora                  4   3171071   Veredinha                1
3129301   Iapu                       3   3171105   Veríssimo                2
3129400   Ibertioga                  4   3171204   Vespasiano               1
3129509   Ibiá                       5   3171303   Viçosa                   3
3129608   Ibiaí                      2   3171402   Vieiras                  1
3129657   Ibiracatu                  2   3171501   Mathias Lobato           1
3129707   Ibiraci                    3   3171600   Virgem da Lapa           3
3129806   Ibirité                    1   3171808   Virginópolis             3
3129905   Ibitiúra de Minas          1   3171907   Virgolândia              1
3130002   Ibituruna                  1   3172004   Visconde do Rio Branco   2
3130101   Igarapé                    2   3172103   Volta Grande             1
3130200   Igaratinga                 1   3172202   Wenceslau Braz           2
3130309   Iguatama                   5   3100500   Açucena                  2
3130408   Ijaci                      2   3100609   Água Boa                 3
3130507   Ilicínea                   3   3101300   Alagoa                   1
3130606   Inconfidentes              3   3102100   Alto Rio Doce            3
3130705   Indianópolis               5   3102407   Alvorada de Minas        1
3130804   Ingaí                      4   3103702   Araponga                 2
3130903   Inhapim                    4   3104452   Aricanduva               2
3131000   Inhaúma                    1   3105707   Barra Longa              2
3131109   Inimutaba                  1   3106101   Belmiro Braga            1

## PDF page 96

3131158   Ipaba                2   3106408   Belo Vale                   3
3131208   Ipanema              2   3106507   Berilo                      2
3131307   Ipatinga             1   3106804   Bias Fortes                 1
3131406   Ipiaçu               3   3107703   Bom Jesus do Amparo         1
3131505   Ipuiúna              5   3108255   Bonito de Minas             3
3131604   Iraí de Minas        5   3108800   Braúnas                     1
3131703   Itabira              1   3109253   Bugre                       2
3131802   Itabirinha           1   3110400   Camacho                     2
3131901   Itabirito            2   3111150   Campo Azul                  2
3132107   Itacarambi           4   3111705   Canaã                       3
3132206   Itaguara             3   3112109   Caparaó                     1
3132404   Itajubá              3   3112208   Capela Nova                 3
3132503   Itamarandiba         3   3112901   Caputira                    2
3132602   Itamarati de Minas   1   3113008   Caraí                       4
3132701   Itambacuri           2   3113107   Caranaíba                   2
3132909   Itamogi              3   3115409   Catas Altas da Noruega      1
3133006   Itamonte             3   3115458   Catuji                      3
3133105   Itanhandu            1   3116100   Chapada do Norte            2
3133204   Itanhomi             1   3116308   Cipotânea                   3
3133303   Itaobim              2   3116803   Coluna                      2
3133402   Itapagipe            2   3117009   Comercinho                  3
3133501   Itapecerica          2   3117405   Conceição de Ipanema        1
3133600   Itapeva              3   3117603   Conceição do Pará           3
3133709   Itatiaiuçu           2   3117836   Cônego Marinho              3
3133758   Itaú de Minas        2   3121100   Delfim Moreira              4
3133808   Itaúna               2   3121506   Desterro do Melo            2
3134103   Itueta               2   3121704   Diogo de Vasconcelos        2
3134202   Ituiutaba            3   3122801   Dom Viçoso                  2
3134301   Itumirim             2   3123106   Dores de Guanhães           1
3134400   Iturama              2   3123304   Dores do Turvo              2
3134509   Itutinga             5   3124401   Espírito Santo do Dourado   5
3134608   Jaboticatubas        2   3124500   Estiva                      5
3134707   Jacinto              4   3125408   Felício dos Santos          2
3134806   Jacuí                3   3125903   Ferros                      2
3134905   Jacutinga            2   3125952   Fervedouro                  2
3135001   Jaguaraçu            1   3126505   Francisco Badaró            1
3135050   Jaíba                5   3126752   Franciscópolis              2
3135076   Jampruca             1   3126802   Frei Gaspar                 2
3135100   Janaúba              4   3126950   Frei Lagonegro              1
3135209   Januária             5   3127073   Fruta de Leite              2
3135308   Japaraíba            2   3127339   Gameleiras                  3
3135407   Jeceaba              2   3127354   Glaucilândia                1
3135506   Jequeri              2   3127404   Gonçalves                   2
3135605   Jequitaí             3   3127800   Grão Mogol                  3
3135803   Jequitinhonha        3   3128204   Guaraciaba                  3
3135902   Jesuânia             1   3129103   Gurinhatã                   2
3136009   Joaíma               2   3130051   Icaraí de Minas             3
3136207   João Monlevade       1   3130556   Imbé de Minas               3
3136306   João Pinheiro        5   3130655   Indaiabira                  3
3136405   Joaquim Felício      2   3132008   Itacambira                  2
3136504   Jordânia             2   3132305   Itaipé                      3
3136579   Josenópolis          2   3132800   Itambé do Mato Dentro       1
3136603   Nova União           1   3133907   Itaverava                   4
3136652   Juatuba              1   3134004   Itinga                      3
3136702   Juiz de Fora         1   3135357   Japonvar                    2
3136801   Juramento            2   3135456   Jenipapo de Minas           1
3136900   Juruaia              2   3135704   Jequitibá                   3
3136959   Juvenília            4   3136108   Joanésia                    1
3137106   Lagamar              4   3136520   José Gonçalves de Minas     1

## PDF page 97

3137205   Lagoa da Prata           1   3136553   José Raydan                 2
3137304   Lagoa dos Patos          1   3137007   Ladainha                    3
3137403   Lagoa Dourada            5   3137908   Lamim                       1
3137502   Lagoa Formosa            5   3138351   Leme do Prado               1
3137536   Lagoa Grande             5   3138674   Luisburgo                   2
3137601   Lagoa Santa              1   3138682   Luislândia                  2
3137700   Lajinha                  2   3139250   Mamonas                     1
3137809   Lambari                  2   3140530   Martins Soares              2
3138005   Laranjal                 1   3140605   Materlândia                 1
3138104   Lassance                 2   3141801   Minas Novas                 3
3138203   Lavras                   4   3142254   Miravânia                   2
3138302   Leandro Ferreira         1   3142304   Moeda                       1
3138401   Leopoldina               1   3143153   Monte Formoso               1
3138500   Liberdade                1   3143450   Montezuma                   2
3138609   Lima Duarte              2   3144656   Ninheira                    3
3138625   Limeira do Oeste         2   3144672   Nova Belém                  1
3138658   Lontra                   1   3145307   Novo Cruzeiro               4
3138708   Luminárias               5   3145356   Novo Oriente de Minas       2
3138807   Luz                      3   3145372   Novorizonte                 1
3138906   Machacalis               1   3145406   Olaria                      1
3139003   Machado                  5   3145877   Orizânia                    2
3139102   Madre de Deus de Minas   5   3146552   Pai Pedro                   1
3139201   Malacacheta              4   3147956   Patis                       2
3139300   Manga                    5   3148400   Paulistas                   2
3139409   Manhuaçu                 3   3148756   Pedra Bonita                2
3139508   Manhumirim               1   3150406   Piedade dos Gerais          4
3139607   Mantena                  2   3150570   Pintópolis                  3
3139706   Maravilhas               4   3150802   Piranga                     4
3139805   Mar de Espanha           1   3150901   Piranguçu                   1
3139904   Maria da Fé              5   3152170   Ponto dos Volantes          3
3140001   Mariana                  2   3152303   Porto Firme                 3
3140100   Marilac                  3   3153103   Presidente Bernardes        3
3140159   Mário Campos             1   3153202   Presidente Juscelino        1
3140209   Maripá de Minas          1   3153806   Queluzito                   3
3140308   Marliéria                1   3155207   Rio Espera                  2
3140407   Marmelópolis             2   3155603   Rio Pardo de Minas          5
3140506   Martinho Campos          3   3156007   Rio Vermelho                3
3140555   Mata Verde               2   3156502   Rubelita                    2
3140704   Mateus Leme              2   3157377   Santa Cruz de Salinas       2
3140803   Matias Barbosa           1   3157401   Santa Cruz do Escalvado     1
3140852   Matias Cardoso           3   3158508   Santana de Pirapama         3
3140902   Matipó                   3   3158607   Santana do Deserto          1
3141009   Mato Verde               2   3159506   Santa Rita do Itueto        2
3141108   Matozinhos               2   3160207   Santo Antônio do Itambé     1
3141207   Matutina                 2   3160454   Santo Antônio do Retiro     2
3141306   Medeiros                 5   3161601   São Geraldo da Piedade      1
3141405   Medina                   3   3162401   São João da Ponte           3
3141504   Mendes Pimentel          1   3162450   São João das Missões        3
3141603   Mercês                   2   3162559   São João do Manhuaçu        2
3141702   Mesquita                 1   3162658   São João do Pacuí           2
3141900   Minduri                  5   3162708   São João do Paraíso         3
3142007   Mirabela                 2   3163508   São José do Jacuri          2
3142106   Miradouro                1   3164100   São Pedro do Suaçuí         2
3142205   Miraí                    1   3164506   São Sebastião do Maranhão   3
3142403   Moema                    1   3165503   Sardoá                      2
3142502   Monjolos                 1   3165552   Setubinha                   2
3142601   Monsenhor Paulo          3   3165800   Senador José Bento          4
3142700   Montalvânia              4   3165909   Senador Modestino           3
                                                 Gonçalves

## PDF page 98

3142809   Monte Alegre de Minas       5      3166105   Senhora do Porto           1
3142908   Monte Azul                  2      3166204   Senhora dos Remédios       3
3143005   Monte Belo                  3      3166501   Serra Azul de Minas        1
3143104   Monte Carmelo               5      3166956   Serranópolis de Minas      1
3143203   Monte Santo de Minas        4      3167608   Simonésia                  2
3143302   Montes Claros               4      3168051   Taparuba                   1
3143401   Monte Sião                  3      3168309   Taquaraçu de Minas         1
3143500   Morada Nova de Minas        5      3169059   Tocos do Moji              3
3143609   Morro da Garça              1      3169109   Toledo                     4
3143708   Morro do Pilar              1      3170529   Urucuia                    4
3143807   Munhoz                      5      3170909   Varzelândia                3
3143906   Muriaé                      3      3171154   Vermelho Novo              2
3144003   Mutum                       3      3171709   Virgínia                   5
3144102   Muzambinho                  4
                                  MATO GROSSO DO SUL
5000203   Água Clara                  3      5005152   Juti                       5
5000252   Alcinópolis                 3      5005202   Ladário                    1
5000609   Amambai                     5      5005400   Maracaju                   5
5000708   Anastácio                   4      5005608   Miranda                    5
5000807   Anaurilândia                5      5005681   Mundo Novo                 5
5000856   Angélica                    5      5005707   Naviraí                    5
5000906   Antônio João                5      5005806   Nioaque                    4
5001003   Aparecida do Taboado        2      5006002   Nova Alvorada do Sul       5
5001102   Aquidauana                  3      5006200   Nova Andradina             5
5001243   Aral Moreira                5      5006259   Novo Horizonte do Sul      5
5001508   Bandeirantes                4      5006309   Paranaíba                  4
5001904   Bataguassu                  3      5006358   Paranhos                   4
5002001   Batayporã                   5      5006408   Pedro Gomes                3
5002100   Bela Vista                  5      5006606   Ponta Porã                 5
5002159   Bodoquena                   3      5006903   Porto Murtinho             3
5002209   Bonito                      5      5007109   Ribas do Rio Pardo         3
5002308   Brasilândia                 2      5007208   Rio Brilhante              5
5002407   Caarapó                     5      5007307   Rio Negro                  3
5002605   Camapuã                     3      5007406   Rio Verde de Mato Grosso   3
5002704   Campo Grande                5      5007505   Rochedo                    3
5002803   Caracol                     3      5007554   Santa Rita do Pardo        2
5002902   Cassilândia                 4      5007695   São Gabriel do Oeste       5
5002951   Chapadão do Sul             5      5007703   Sete Quedas                5
5003157   Coronel Sapucaia            4      5007802   Selvíria                   2
5003207   Corumbá                     3      5007901   Sidrolândia                5
5003256   Costa Rica                  5      5007935   Sonora                     5
5003306   Coxim                       4      5007976   Taquarussu                 5
5003454   Deodápolis                  5      5008305   Três Lagoas                1
5003504   Douradina                   4      5008404   Vicentina                  4
5003702   Dourados                    5      5003108   Corguinho                  2
5003751   Eldorado                    5      5003488   Dois Irmãos do Buriti      3
5003801   Fátima do Sul               4      5004601   Itaquiraí                  5
5003900   Figueirão                   1      5004809   Japorã                     5
5004007   Glória de Dourados          4      5004908   Jaraguari                  4
5004106   Guia Lopes da Laguna        4      5005103   Jateí                      5
5004304   Iguatemi                    5      5005251   Laguna Carapã              5
5004403   Inocência                   2      5006275   Paraíso das Águas          3
5004502   Itaporã                     5      5007950   Tacuru                     5
5004700   Ivinhema                    5      5008008   Terenos                    4
5005004   Jardim                      4
                                     MATO GROSSO
5100102   Acorizal                    2      5106299   Paranaíta                  4
5100201   Água Boa                    5      5106307   Paranatinga                5

## PDF page 99

5100250   Alta Floresta           4   5106315   Novo Santo Antônio        2
5100300   Alto Araguaia           4   5106372   Pedra Preta               5
5100359   Alto Boa Vista          4   5106422   Peixoto de Azevedo        5
5100409   Alto Garças             5   5106455   Planalto da Serra         4
5100508   Alto Paraguai           3   5106505   Poconé                    3
5100607   Alto Taquari            5   5106653   Pontal do Araguaia        2
5100805   Apiacás                 2   5106703   Ponte Branca              1
5101001   Araguaiana              2   5106752   Pontes e Lacerda          4
5101209   Araguainha              1   5106778   Porto Alegre do Norte     4
5101258   Araputanga              3   5106802   Porto dos Gaúchos         5
5101308   Arenápolis              2   5107008   Poxoréu                   5
5101407   Aripuanã                4   5107040   Primavera do Leste        5
5101704   Barra do Bugres         4   5107107   São José dos Quatro       2
                                                Marcos
5101803   Barra do Garças         3   5107156   Reserva do Cabaçal        2
5101852   Bom Jesus do Araguaia   5   5107180   Ribeirão Cascalheira      5
5101902   Brasnorte               5   5107198   Ribeirãozinho             4
5102504   Cáceres                 4   5107206   Rio Branco                2
5102637   Campo Novo do Parecis   5   5107248   Santa Carmem              5
5102678   Campo Verde             5   5107263   Santo Afonso              4
5102686   Campos de Júlio         5   5107297   São José do Povo          1
5102694   Canabrava do Norte      4   5107305   São José do Rio Claro     5
5102702   Canarana                5   5107354   São José do Xingu         5
5102850   Castanheira             3   5107404   São Pedro da Cipa         1
5103007   Chapada dos Guimarães   5   5107602   Rondonópolis              5
5103056   Cláudia                 5   5107701   Rosário Oeste             4
5103106   Cocalinho               2   5107743   Santa Cruz do Xingu       4
5103205   Colíder                 4   5107750   Salto do Céu              2
5103254   Colniza                 5   5107768   Santa Rita do Trivelato   5
5103304   Comodoro                5   5107792   Santo Antônio do Leste    5
5103353   Confresa                5   5107859   São Félix do Araguaia     5
5103361   Conquista D'Oeste       2   5107875   Sapezal                   5
5103403   Cuiabá                  3   5107883   Serra Nova Dourada        2
5103437   Curvelândia             2   5107909   Sinop                     5
5103452   Denise                  2   5107925   Sorriso                   5
5103502   Diamantino              5   5107941   Tabaporã                  5
5103601   Dom Aquino              5   5107958   Tangará da Serra          5
5103700   Feliz Natal             5   5108006   Tapurah                   5
5103809   Figueirópolis D'Oeste   1   5108105   Tesouro                   4
5103957   Glória D'Oeste          1   5108204   Torixoréu                 3
5104104   Guarantã do Norte       4   5108303   União do Sul              5
5104203   Guiratinga              5   5108402   Várzea Grande             2
5104500   Indiavaí                1   5108501   Vera                      5
5104526   Ipiranga do Norte       5   5108600   Vila Rica                 4
5104542   Itanhangá               5   5108857   Nova Marilândia           4
5104559   Itaúba                  5   5108907   Nova Maringá              5
5104807   Jaciara                 4   5108956   Nova Monte Verde          3
5105002   Jauru                   2   5101605   Barão de Melgaço          1
5105101   Juara                   5   5102603   Campinápolis              5
5105150   Juína                   4   5102793   Carlinda                  3
5105176   Juruena                 3   5103379   Cotriguaçu                4
5105200   Juscimeira              4   5103858   Gaúcha do Norte           5
5105234   Lambari D'Oeste         2   5103908   General Carneiro          5
5105259   Lucas do Rio Verde      5   5104609   Itiquira                  5
5105309   Luciara                 2   5104906   Jangada                   2
5105580   Marcelândia             5   5105507   Vila Bela da Santíssima   4
                                                Trindade
5105606   Matupá                  5   5106109   Nossa Senhora do          3
                                                Livramento

## PDF page 100

5105622   Mirassol d'Oeste           3          5106158   Nova Bandeirantes           3
5105903   Nobres                     5          5106174   Nova Nazaré                 3
5106000   Nortelândia                4          5106265   Novo Mundo                  5
5106182   Nova Lacerda               3          5106828   Porto Esperidião            2
5106190   Nova Santa Helena          4          5106851   Porto Estrela               3
5106208   Nova Brasilândia           3          5107065   Querência                   5
5106216   Nova Canaã do Norte        5          5107578   Rondolândia                 1
5106224   Nova Mutum                 5          5107776   Santa Terezinha             5
5106232   Nova Olímpia               3          5107800   Santo Antônio do Leverger   4
5106240   Nova Ubiratã               5          5108055   Terra Nova do Norte         4
5106257   Nova Xavantina             5          5108352   Vale de São Domingos        2
5106273   Novo Horizonte do Norte    3          5108808   Nova Guarita                4
5106281   Novo São Joaquim           5
                                         PARÁ
1500107   Abaetetuba                 5          1508159   Uruará                      5
1500131   Abel Figueiredo            4          1508209   Vigia                       4
1500404   Alenquer                   5          1508407   Xinguara                    4
1500503   Almeirim                   3          1500206   Acará                       5
1500602   Altamira                   5          1500305   Afuá                        2
1500800   Ananindeua                 2          1500347   Água Azul do Norte          4
1500859   Anapu                      4          1500701   Anajás                      2
1501204   Baião                      5          1500909   Augusto Corrêa              5
1501402   Belém                      2          1500958   Aurora do Pará              5
1501501   Benevides                  1          1501006   Aveiro                      4
1501576   Bom Jesus do Tocantins     4          1501105   Bagre                       3
1501709   Bragança                   5          1501253   Bannach                     1
1501758   Brejo Grande do Araguaia   2          1501303   Barcarena                   5
1501782   Breu Branco                5          1501451   Belterra                    5
1501808   Breves                     3          1501600   Bonito                      4
1502152   Canaã dos Carajás          3          1501725   Brasil Novo                 3
1502202   Capanema                   5          1501907   Bujaru                      4
1502400   Castanhal                  5          1501956   Cachoeira do Piriá          5
1502707   Conceição do Araguaia      3          1502004   Cachoeira do Arari          4
1502756   Concórdia do Pará          5          1502103   Cametá                      5
1502772   Curionópolis               4          1502301   Capitão Poço                5
1502939   Dom Eliseu                 5          1502509   Chaves                      1
1502954   Eldorado do Carajás        4          1502608   Colares                     3
1503002   Faro                       4          1502764   Cumaru do Norte             4
1503044   Floresta do Araguaia       5          1502806   Curralinho                  3
1503093   Goianésia do Pará          4          1502855   Curuá                       3
1503200   Igarapé-Açu                5          1502905   Curuçá                      4
1503606   Itaituba                   5          1503077   Garrafão do Norte           5
1503804   Jacundá                    4          1503101   Gurupá                      3
1504059   Mãe do Rio                 5          1503309   Igarapé-Miri                5
1504208   Marabá                     5          1503408   Inhangapi                   5
1504422   Marituba                   1          1503457   Ipixuna do Pará             5
1504604   Mocajuba                   5          1503507   Irituia                     4
1504752   Mojuí dos Campos           5          1503705   Itupiranga                  5
1504976   Nova Ipixuna               3          1503754   Jacareacanga                5
1505031   Novo Progresso             5          1503903   Juruti                      5
1505106   Óbidos                     5          1504000   Limoeiro do Ajuru           2
1505304   Oriximiná                  5          1504109   Magalhães Barata            4
1505437   Ourilândia do Norte        3          1504307   Maracanã                    4
1505494   Palestina do Pará          2          1504406   Marapanim                   5
1505502   Paragominas                5          1504455   Medicilândia                4
1505536   Parauapebas                5          1504505   Melgaço                     3
1505551   Pau D'Arco                 3          1504703   Moju                        5
1505601   Peixe-Boi                  4          1504802   Monte Alegre                5
1505700   Ponta de Pedras            1          1504901   Muaná                       2

## PDF page 101

1505809   Portel                     5    1504950   Nova Esperança do Piriá      5
1506104   Primavera                  4    1505007   Nova Timboteua               5
1506138   Redenção                   5    1505064   Novo Repartimento            5
1506161   Rio Maria                  3    1505205   Oeiras do Pará               5
1506187   Rondon do Pará             5    1505403   Ourém                        4
1506203   Salinópolis                3    1505486   Pacajá                       5
1506302   Salvaterra                 2    1505635   Piçarra                      5
1506401   Santa Cruz do Arari        5    1505650   Placas                       4
1506500   Santa Izabel do Pará       3    1505908   Porto de Moz                 4
1506609   Santa Maria do Pará        5    1506005   Prainha                      5
1506708   Santana do Araguaia        5    1506112   Quatipuru                    3
1506807   Santarém                   5    1506195   Rurópolis                    4
1507003   Santo Antônio do Tauá      4    1506351   Santa Bárbara do Pará        2
1507151   São Domingos do Araguaia   5    1506559   Santa Luzia do Pará          4
1507300   São Félix do Xingu         5    1506583   Santa Maria das Barreiras    5
1507458   São Geraldo do Araguaia    4    1506906   Santarém Novo                4
1507474   São João de Pirabas        3    1507102   São Caetano de Odivelas      4
1507607   São Miguel do Guamá        5    1507201   São Domingos do Capim        5
1507755   Sapucaia                   2    1507409   São Francisco do Pará        5
1507805   Senador José Porfírio      4    1507466   São João da Ponta            3
1507904   Soure                      1    1507508   São João do Araguaia         4
1507953   Tailândia                  5    1507706   São Sebastião da Boa Vista   3
1507979   Terra Santa                2    1507961   Terra Alta                   4
1508001   Tomé-Açu                   5    1508035   Tracuateua                   5
1508084   Tucumã                     3    1508050   Trairão                      5
1508100   Tucuruí                    5    1508308   Viseu                        5
1508126   Ulianópolis                5    1508357   Vitória do Xingu             5
                                     PARAÍBA
2500205   Aguiar                     1    2512747   Riachão                      1
2500304   Alagoa Grande              3    2512754   Riachão do Bacamarte         1
2500403   Alagoa Nova                3    2512788   Riacho de Santo Antônio      1
2500502   Alagoinha                  2    2512804   Riacho dos Cavalos           1
2500577   Algodão de Jandaíra        1    2512903   Rio Tinto                    2
2500601   Alhandra                   4    2513307   Santa Helena                 1
2500734   Amparo                     1    2513406   Santa Luzia                  1
2500775   Aparecida                  1    2513604   Santana dos Garrotes         1
2500908   Arara                      2    2513703   Santa Rita                   2
2501005   Araruna                    3    2513802   Santa Teresinha              1
2501104   Areia                      3    2513901   São Bento                    1
2501153   Areia de Baraúnas          1    2513927   São Bentinho                 1
2501203   Areial                     2    2514008   São João do Cariri           1
2501302   Aroeiras                   2    2514503   São José de Piranhas         1
2501351   Assunção                   2    2514651   São José do Brejo do Cruz    1
2501534   Baraúna                    1    2514701   São José do Sabugi           1
2501609   Barra de Santa Rosa        2    2514909   São Mamede                   1
2501807   Bayeux                     1    2515203   São Sebastião do             1
                                                    Umbuzeiro
2501906   Belém                      3    2515302   Sapé                         3
2502003   Belém do Brejo do Cruz     1    2515500   Serra Branca                 1
2502102   Boa Ventura                1    2515609   Serra da Raiz                2
2502151   Boa Vista                  1    2515708   Serra Grande                 1
2502409   Bonito de Santa Fé         1    2515807   Serra Redonda                2
2502508   Boqueirão                  3    2515906   Serraria                     3
2502607   Igaracy                    1    2515930   Sertãozinho                  2
2502706   Borborema                  3    2516003   Solânea                      3
2502805   Brejo do Cruz              1    2516102   Soledade                     2
2502904   Brejo dos Santos           1    2516151   Sossêgo                      1
2503001   Caaporã                    2    2516201   Sousa                        2
2503209   Cabedelo                   1    2516300   Sumé                         2

## PDF page 102

2503506   Cacimba de Dentro   3   2516508   Taperoá                    2
2503605   Caiçara             2   2516706   Teixeira                   2
2503704   Cajazeiras          1   2516755   Tenório                    2
2503803   Caldas Brandão      2   2516904   Uiraúna                    1
2503902   Camalaú             2   2517100   Várzea                     1
2504009   Campina Grande      3   2517407   Zabelê                     1
2504033   Capim               1   2500106   Água Branca                2
2504108   Carrapateira        1   2500536   Alcantil                   1
2504157   Casserengue         3   2500700   São João do Rio do Peixe   1
2504207   Catingueira         1   2500809   Araçagi                    4
2504306   Catolé do Rocha     1   2501401   Baía da Traição            2
2504405   Conceição           2   2501500   Bananeiras                 4
2504504   Condado             1   2501575   Barra de Santana           1
2504603   Conde               3   2501708   Barra de São Miguel        2
2504702   Congo               2   2502052   Bernardino Batista         1
2504801   Coremas             1   2502201   Bom Jesus                  1
2505006   Cubati              2   2502300   Bom Sucesso                1
2505105   Cuité               2   2503100   Cabaceiras                 2
2505204   Cuitegi             2   2503308   Cachoeira dos Índios       1
2505303   Curral Velho        1   2503407   Cacimba de Areia           2
2505402   Desterro            2   2503555   Cacimbas                   1
2505600   Diamante            1   2503753   Cajazeirinhas              1
2505808   Duas Estradas       2   2504074   Caraúbas                   1
2505907   Emas                1   2504355   Caturité                   1
2506004   Esperança           3   2504850   Coxixola                   1
2506103   Fagundes            2   2504900   Cruz do Espírito Santo     3
2506202   Frei Martinho       1   2505238   Cuité de Mamanguape        3
2506301   Guarabira           2   2505279   Curral de Cima             2
2506509   Gurjão              1   2505352   Damião                     1
2506608   Ibiara              1   2505501   Vista Serrana              1
2506806   Ingá                1   2505709   Dona Inês                  3
2506905   Itabaiana           2   2506251   Gado Bravo                 1
2507002   Itaporanga          2   2506400   Gurinhém                   2
2507101   Itapororoca         3   2506707   Imaculada                  2
2507200   Itatuba             2   2508000   Juru                       2
2507309   Jacaraú             2   2508307   Lagoa Seca                 4
2507408   Jericó              1   2508406   Lastro                     1
2507507   João Pessoa         1   2508554   Logradouro                 1
2507606   Juarez Távora       1   2508703   Mãe d'Água                 1
2507705   Juazeirinho         2   2509057   Marcação                   2
2507804   Junco do Seridó     1   2509206   Massaranduba               2
2507903   Juripiranga         1   2509339   Matinhas                   2
2508109   Lagoa               1   2509370   Mato Grosso                1
2508208   Lagoa de Dentro     2   2509404   Mogeiro                    3
2508505   Livramento          2   2509909   Natuba                     1
2508604   Lucena              1   2510006   Nazarezinho                1
2508802   Malta               1   2511103   Pedra Lavrada              2
2508901   Mamanguape          2   2512036   Poço Dantas                1
2509008   Manaíra             2   2512077   Poço de José de Moura      1
2509107   Mari                4   2512408   Puxinanã                   4
2509156   Marizópolis         1   2512606   Quixaba                    1
2509305   Mataraca            1   2512721   Pedro Régis                1
2509396   Maturéia            2   2512762   Riachão do Poço            2
2509503   Montadas            2   2513000   Salgadinho                 1
2509602   Monte Horebe        1   2513109   Salgado de São Félix       2
2509701   Monteiro            2   2513158   Santa Cecília              1
2509800   Mulungu             2   2513208   Santa Cruz                 1
2510105   Nova Floresta       1   2513356   Santa Inês                 1
2510204   Nova Olinda         1   2513505   Santana de Mangueira       1

## PDF page 103

2510303   Nova Palmeira              1     2513653   Joca Claudino               1
2510402   Olho d'Água                1     2513851   Santo André                 1
2510501   Olivedos                   1     2513943   São Domingos do Cariri      1
2510600   Ouro Velho                 1     2513968   São Domingos                1
2510659   Parari                     1     2513984   São Francisco               1
2510709   Passagem                   1     2514107   São João do Tigre           1
2510808   Patos                      1     2514206   São José da Lagoa Tapada    1
2510907   Paulista                   1     2514305   São José de Caiana          1
2511004   Pedra Branca               1     2514404   São José de Espinharas      1
2511202   Pedras de Fogo             4     2514453   São José dos Ramos          2
2511301   Piancó                     1     2514552   São José de Princesa        2
2511400   Picuí                      2     2514602   São José do Bonfim          1
2511509   Pilar                      2     2514800   São José dos Cordeiros      2
2511608   Pilões                     2     2515005   São Miguel de Taipu         2
2511707   Pilõezinhos                2     2515104   São Sebastião de Lagoa de   2
                                                     Roça
2511806   Pirpirituba                2     2515401   São Vicente do Seridó       1
2511905   Pitimbu                    3     2515971   Sobrado                     3
2512002   Pocinhos                   2     2516409   Tacima                      1
2512101   Pombal                     1     2516607   Tavares                     3
2512200   Prata                      2     2516805   Triunfo                     1
2512309   Princesa Isabel            3     2517001   Umbuzeiro                   1
2512507   Queimadas                  2     2517209   Vieirópolis                 1
2512705   Remígio                    2
                                    PERNAMBUCO
2600054   Abreu e Lima               3     2611002   Petrolândia                 3
2600104   Afogados da Ingazeira      2     2611101   Petrolina                   4
2600302   Agrestina                  2     2611200   Poção                       2
2600401   Água Preta                 1     2611309   Pombos                      3
2600500   Águas Belas                4     2611408   Primavera                   1
2600609   Alagoinha                  2     2611507   Quipapá                     3
2600708   Aliança                    1     2611606   Recife                      1
2600807   Altinho                    1     2611804   Ribeirão                    2
2600906   Amaraji                    3     2611903   Rio Formoso                 1
2601003   Angelim                    2     2612000   Sairé                       3
2601052   Araçoiaba                  1     2612208   Salgueiro                   2
2601102   Araripina                  5     2612307   Saloá                       4
2601201   Arcoverde                  2     2612406   Sanharó                     3
2601300   Barra de Guabiraba         2     2612505   Santa Cruz do Capibaribe    2
2601409   Barreiros                  1     2612802   Santa Terezinha             2
2601508   Belém de Maria             2     2612901   São Benedito do Sul         1
2601607   Belém do São Francisco     2     2613008   São Bento do Una            5
2601706   Belo Jardim                3     2613107   São Caitano                 2
2601904   Bezerros                   4     2613305   São Joaquim do Monte        3
2602100   Bom Conselho               4     2613404   São José da Coroa Grande    1
2602308   Bonito                     3     2613503   São José do Belmonte        4
2602605   Brejo da Madre de Deus     2     2613602   São José do Egito           3
2602704   Buenos Aires               1     2613701   São Lourenço da Mata        1
2602902   Cabo de Santo Agostinho    3     2613800   São Vicente Férrer          1
2603009   Cabrobó                    4     2613909   Serra Talhada               3
2603108   Cachoeirinha               3     2614105   Sertânia                    3
2603454   Camaragibe                 1     2614204   Sirinhaém                   1
2603504   Camocim de São Félix       4     2614303   Moreilândia                 2
2603603   Camutanga                  1     2614501   Surubim                     2
2603702   Canhotinho                 4     2614600   Tabira                      3
2604007   Carpina                    1     2614709   Tacaimbó                    3
2604106   Caruaru                    2     2614857   Tamandaré                   1
2604205   Catende                    1     2615003   Taquaritinga do Norte       1
2604304   Cedro                      3     2615201   Terra Nova                  1

## PDF page 104

2604403   Chã de Alegria            1   2615300   Timbaúba                    2
2604502   Chã Grande                2   2615409   Toritama                    1
2604601   Condado                   1   2615508   Tracunhaém                  1
2604700   Correntes                 3   2615607   Trindade                    2
2604809   Cortês                    1   2615706   Triunfo                     2
2605004   Cupira                    2   2615904   Tuparetama                  1
2605103   Custódia                  4   2616001   Venturosa                   3
2605202   Escada                    2   2616209   Vertentes                   1
2605301   Exu                       5   2616407   Vitória de Santo Antão      3
2605400   Feira Nova                3   2616506   Xexéu                       1
2605459   Fernando de Noronha       1   2600203   Afrânio                     2
2605509   Ferreiros                 1   2601805   Betânia                     2
2605707   Floresta                  3   2602001   Bodocó                      4
2605905   Gameleira                 2   2602209   Bom Jardim                  2
2606002   Garanhuns                 4   2602407   Brejão                      2
2606101   Glória do Goitá           3   2602506   Brejinho                    2
2606200   Goiana                    2   2602803   Buíque                      5
2606408   Gravatá                   3   2603207   Caetés                      5
2606606   Ibimirim                  4   2603306   Calçado                     5
2606804   Igarassu                  2   2603405   Calumbi                     1
2606903   Iguaracy                  2   2603801   Capoeiras                   4
2607109   Ingazeira                 1   2603900   Carnaíba                    3
2607208   Ipojuca                   3   2603926   Carnaubeira da Penha        3
2607307   Ipubi                     5   2604155   Casinhas                    1
2607406   Itacuruba                 1   2604908   Cumaru                      2
2607604   Ilha de Itamaracá         1   2605152   Dormentes                   2
2607653   Itambé                    1   2605608   Flores                      3
2607703   Itapetim                  2   2605806   Frei Miguelinho             1
2607752   Itapissuma                1   2606309   Granito                     3
2607802   Itaquitinga               1   2606507   Iati                        4
2607901   Jaboatão dos Guararapes   2   2606705   Ibirajuba                   2
2607950   Jaqueira                  1   2607000   Inajá                       4
2608008   Jataúba                   1   2607505   Itaíba                      3
2608107   João Alfredo              3   2608057   Jatobá                      1
2608206   Joaquim Nabuco            1   2608255   Jucati                      5
2608305   Jupi                      5   2608750   Lagoa Grande                4
2608404   Jurema                    4   2609154   Manari                      4
2608453   Lagoa do Carro            1   2609709   Orobó                       2
2608503   Lagoa de Itaenga          1   2609808   Orocó                       3
2608602   Lagoa do Ouro             2   2610301   Paranatama                  4
2608701   Lagoa dos Gatos           2   2610400   Parnamirim                  3
2608800   Lajedo                    4   2611533   Quixaba                     2
2608909   Limoeiro                  2   2611705   Riacho das Almas            2
2609006   Macaparana                1   2612109   Salgadinho                  1
2609105   Machados                  1   2612455   Santa Cruz                  3
2609204   Maraial                   1   2612471   Santa Cruz da Baixa Verde   2
2609303   Mirandiba                 3   2612554   Santa Filomena              4
2609402   Moreno                    2   2612604   Santa Maria da Boa Vista    4
2609501   Nazaré da Mata            1   2612703   Santa Maria do Cambucá      2
2609600   Olinda                    1   2613206   São João                    5
2609907   Ouricuri                  4   2614006   Serrita                     2
2610004   Palmares                  2   2614402   Solidão                     1
2610103   Palmeirina                1   2614808   Tacaratu                    2
2610202   Panelas                   3   2615102   Terezinha                   2
2610509   Passira                   3   2615805   Tupanatinga                 3
2610608   Paudalho                  1   2616100   Verdejante                  2
2610707   Paulista                  1   2616183   Vertente do Lério           1
2610806   Pedra                     3   2616308   Vicência                    1
2610905   Pesqueira                 4

## PDF page 105

                                        PIAUÍ
2200103   Agricolândia              2           2201804   Bocaina                     2
2200202   Água Branca               2           2201919   Bom Princípio do Piauí      5
2200277   Alegrete do Piauí         3           2201929   Bonfim do Piauí             2
2200301   Alto Longá                2           2201945   Boqueirão do Piauí          1
2200400   Altos                     3           2201960   Brasileira                  2
2200509   Amarante                  4           2201988   Brejo do Piauí              1
2200608   Angical do Piauí          2           2202026   Buriti dos Montes           2
2200707   Anísio de Abreu           2           2202059   Cabeceiras do Piauí         2
2200806   Antônio Almeida           2           2202075   Cajazeiras do Piauí         1
2200905   Aroazes                   1           2202083   Cajueiro da Praia           4
2201002   Arraial                   1           2202091   Caldeirão Grande do Piauí   5
2201101   Avelino Lopes             2           2202109   Campinas do Piauí           2
2201150   Baixa Grande do Ribeiro   5           2202117   Campo Alegre do Fidalgo     1
2201176   Barra D'Alcântara         1           2202133   Campo Grande do Piauí       3
2201200   Barras                    3           2202174   Campo Largo do Piauí        2
2201309   Barreiras do Piauí        2           2202251   Canavieira                  2
2201408   Barro Duro                2           2202455   Capitão Gervásio Oliveira   1
2201572   Belém do Piauí            2           2202505   Caracol                     2
2201606   Beneditinos               2           2202539   Caraúbas do Piauí           3
2201705   Bertolínia                2           2202554   Caridade do Piauí           2
2201903   Bom Jesus                 5           2202653   Caxingó                     3
2202000   Buriti dos Lopes          4           2202703   Cocal                       5
2202208   Campo Maior               2           2202729   Cocal dos Alves             4
2202307   Canto do Buriti           4           2202737   Coivaras                    1
2202406   Capitão de Campos         2           2202778   Colônia do Piauí            2
2202604   Castelo do Piauí          2           2202851   Coronel José Dias           1
2202711   Cocal de Telha            1           2203008   Cristalândia do Piauí       2
2202752   Colônia do Gurguéia       1           2203230   Currais                     5
2202802   Conceição do Canindé      3           2203255   Curralinhos                 1
2202901   Corrente                  4           2203271   Curral Novo do Piauí        3
2203107   Cristino Castro           2           2203354   Dirceu Arcoverde            1
2203206   Curimatá                  2           2203420   Domingos Mourão             1
2203305   Demerval Lobão            1           2203453   Dom Inocêncio               2
2203404   Dom Expedito Lopes        3           2203750   Fartura do Piauí            1
2203503   Elesbão Veloso            3           2203800   Flores do Piauí             2
2203602   Eliseu Martins            1           2203859   Floresta do Piauí           1
2203701   Esperantina               3           2204154   Francisco Macedo            1
2203909   Floriano                  3           2204204   Francisco Santos            3
2204006   Francinópolis             1           2204352   Geminiano                   3
2204105   Francisco Ayres           2           2204550   Guaribas                    2
2204303   Fronteiras                4           2204907   Isaías Coelho               2
2204402   Gilbués                   4           2205003   Itainópolis                 3
2204501   Guadalupe                 2           2205151   Jacobina do Piauí           2
2204600   Hugo Napoleão             3           2205201   Jaicós                      4
2204659   Ilha Grande               2           2205250   Jardim do Mulato            2
2204709   Inhuma                    4           2205276   Jatobá do Piauí             1
2204808   Ipiranga do Piauí         3           2205359   João Costa                  1
2205102   Itaueira                  3           2205409   Joaquim Pires               2
2205300   Jerumenha                 1           2205458   Joca Marques                2
2205508   José de Freitas           3           2205516   Juazeiro do Piauí           1
2205540   Lagoinha do Piauí         2           2205524   Júlio Borges                2
2205607   Landri Sales              3           2205532   Jurema                      2
2205805   Luzilândia                3           2205557   Lagoa Alegre                2
2205904   Manoel Emídio             2           2205565   Lagoa do Barro do Piauí     2
2205953   Marcolândia               4           2205573   Lagoa de São Francisco      1
2206001   Marcos Parente            1           2205581   Lagoa do Piauí              1
2206308   Miguel Leão               2           2205599   Lagoa do Sítio              3
2206407   Monsenhor Gil             3           2205706   Luís Correia                5

## PDF page 106

2206704   Nazaré do Piauí              1        2205854   Madeiro                      2
2206902   Novo Oriente do Piauí        1        2206050   Massapê do Piauí             2
2207009   Oeiras                       3        2206100   Matias Olímpio               1
2207306   Paes Landim                  1        2206209   Miguel Alves                 4
2207603   Parnaguá                     2        2206357   Milton Brandão               2
2207702   Parnaíba                     2        2206506   Monsenhor Hipólito           3
2207751   Passagem Franca do Piauí     2        2206605   Monte Alegre do Piauí        4
2207801   Paulistana                   2        2206654   Morro Cabeça no Tempo        2
2207850   Pavussu                      2        2206670   Morro do Chapéu do Piauí     2
2207900   Pedro II                     2        2206696   Murici dos Portelas          4
2208007   Picos                        3        2206720   Nazária                      2
2208304   Piracuruca                   2        2206753   Nossa Senhora de Nazaré      1
2208403   Piripiri                     3        2206803   Nossa Senhora dos            2
                                                          Remédios
2208502   Porto                        1        2206951   Novo Santo Antônio           1
2208551   Porto Alegre do Piauí        1        2207108   Olho D'Água do Piauí         1
2208601   Prata do Piauí               1        2207207   Padre Marcos                 2
2208700   Redenção do Gurguéia         2        2207355   Pajeú do Piauí               2
2208809   Regeneração                  3        2207405   Palmeira do Piauí            4
2208858   Riacho Frio                  1        2207504   Palmeirais                   3
2208908   Ribeiro Gonçalves            5        2207553   Paquetá                      3
2209005   Rio Grande do Piauí          2        2207777   Patos do Piauí               2
2209104   Santa Cruz do Piauí          2        2207793   Pau D'Arco do Piauí          1
2209153   Santa Cruz dos Milagres      1        2207934   Pedro Laurentino             1
2209203   Santa Filomena               4        2207959   Nova Santa Rita              1
2209302   Santa Luz                    2        2208106   Pimenteiras                  3
2209377   Santa Rosa do Piauí          1        2208205   Pio IX                       4
2209401   Santo Antônio de Lisboa      3        2208650   Queimada Nova                2
2209500   Santo Inácio do Piauí        1        2208874   Ribeira do Piauí             1
2209609   São Félix do Piauí           1        2209351   Santana do Piauí             4
2209807   São Gonçalo do Piauí         2        2209450   Santo Antônio dos Milagres   1
2209906   São João da Serra            1        2209559   São Braz do Piauí            2
2209971   São João do Arraial          1        2209658   São Francisco de Assis do    2
                                                          Piauí
2210003   São João do Piauí            2        2209708   São Francisco do Piauí       2
2210052   São José do Divino           2        2209757   São Gonçalo do Gurguéia      2
2210102   São José do Peixe            1        2209856   São João da Canabrava        3
2210383   São Miguel da Baixa Grande   1        2209872   São João da Fronteira        1
2210508   São Pedro do Piauí           3        2209955   São João da Varjota          2
2210607   São Raimundo Nonato          3        2210201   São José do Piauí            4
2210805   Simplício Mendes             2        2210300   São Julião                   2
2210953   Tamboril do Piauí            2        2210359   São Lourenço do Piauí        1
2211001   Teresina                     3        2210375   São Luis do Piauí            1
2211100   União                        3        2210391   São Miguel do Fidalgo        1
2211209   Uruçuí                       5        2210409   São Miguel do Tapuio         3
2211308   Valença do Piauí             3        2210623   Sebastião Barros             2
2211407   Várzea Grande                1        2210631   Sebastião Leal               4
2200053   Acauã                        2        2210656   Sigefredo Pacheco            2
2200251   Alagoinha do Piauí           3        2210706   Simões                       5
2200459   Alvorada do Gurguéia         3        2210904   Socorro do Piauí             2
2200954   Aroeiras do Itaim            1        2210938   Sussuapara                   2
2201051   Assunção do Piauí            3        2210979   Tanque do Piauí              1
2201507   Batalha                      3        2211357   Várzea Branca                2
2201556   Bela Vista do Piauí          1        2211506   Vera Mendes                  2
2201739   Betânia do Piauí             2        2211605   Vila Nova do Piauí           3
2201770   Boa Hora                     1        2211704   Wall Ferraz                  2
                                           PARANÁ
4100103   Abatiá                       5        4117222   Nova Santa Rosa              5
4100400   Almirante Tamandaré          4        4117255   Nova Prata do Iguaçu         5

## PDF page 107

4100459   Altamira do Paraná         2   4117297   Novo Itacolomi              4
4100509   Altônia                    5   4117404   Ourizona                    4
4100608   Alto Paraná                5   4117453   Ouro Verde do Oeste         5
4100707   Alto Piquiri               5   4117503   Paiçandu                    4
4100806   Alvorada do Sul            5   4117602   Palmas                      5
4100905   Amaporã                    5   4117701   Palmeira                    5
4101002   Ampére                     5   4117800   Palmital                    4
4101051   Anahy                      5   4117909   Palotina                    5
4101101   Andirá                     5   4118006   Paraíso do Norte            4
4101150   Ângulo                     3   4118105   Paranacity                  4
4101200   Antonina                   3   4118204   Paranaguá                   3
4101408   Apucarana                  5   4118303   Paranapoema                 3
4101507   Arapongas                  5   4118402   Paranavaí                   5
4101606   Arapoti                    5   4118451   Pato Bragado                4
4101705   Araruna                    5   4118501   Pato Branco                 5
4101804   Araucária                  5   4118600   Paula Freitas               5
4101903   Assaí                      5   4118808   Peabiru                     5
4102000   Assis Chateaubriand        5   4118857   Perobal                     5
4102109   Astorga                    5   4118907   Pérola                      5
4102208   Atalaia                    4   4119152   Pinhais                     1
4102307   Balsa Nova                 5   4119202   Pinhalão                    5
4102406   Bandeirantes               5   4119301   Pinhão                      5
4102505   Barbosa Ferraz             5   4119400   Piraí do Sul                5
4102604   Barracão                   4   4119509   Piraquara                   3
4102703   Barra do Jacaré            5   4119608   Pitanga                     5
4102802   Bela Vista do Paraíso      5   4119657   Pitangueiras                4
4102901   Bituruna                   5   4119707   Planaltina do Paraná        5
4103008   Boa Esperança              5   4119905   Ponta Grossa                5
4103057   Boa Vista da Aparecida     5   4119954   Pontal do Paraná            1
4103206   Bom Sucesso                4   4120002   Porecatu                    3
4103222   Bom Sucesso do Sul         5   4120101   Porto Amazonas              5
4103305   Borrazópolis               5   4120200   Porto Rico                  5
4103354   Braganey                   5   4120309   Porto Vitória               4
4103370   Brasilândia do Sul         5   4120333   Prado Ferreira              4
4103404   Cafeara                    3   4120358   Pranchita                   5
4103453   Cafelândia                 5   4120408   Presidente Castelo Branco   4
4103479   Cafezal do Sul             5   4120507   Primeiro de Maio            5
4103503   Califórnia                 5   4120655   Quarto Centenário           5
4103602   Cambará                    5   4120705   Quatiguá                    3
4103701   Cambé                      5   4120804   Quatro Barras               2
4103800   Cambira                    5   4120853   Quatro Pontes               4
4103909   Campina da Lagoa           5   4120903   Quedas do Iguaçu            5
4104006   Campina Grande do Sul      3   4121000   Querência do Norte          5
4104055   Campo Bonito               5   4121109   Quinta do Sol               5
4104105   Campo do Tenente           5   4121257   Ramilândia                  4
4104204   Campo Largo                5   4121307   Rancho Alegre               5
4104253   Campo Magro                5   4121356   Rancho Alegre D'Oeste       5
4104303   Campo Mourão               5   4121406   Realeza                     5
4104451   Cantagalo                  5   4121505   Rebouças                    5
4104501   Capanema                   5   4121604   Renascença                  5
4104600   Capitão Leônidas Marques   5   4121703   Reserva                     5
4104659   Carambeí                   5   4121752   Reserva do Iguaçu           5
4104709   Carlópolis                 5   4121802   Ribeirão Claro              5
4104808   Cascavel                   5   4121901   Ribeirão do Pinhal          5
4104907   Castro                     5   4122107   Rio Bom                     5
4105003   Catanduvas                 5   4122206   Rio Branco do Sul           4
4105102   Centenário do Sul          4   4122305   Rio Negro                   5
4105300   Céu Azul                   5   4122404   Rolândia                    5
4105409   Chopinzinho                5   4122503   Roncador                    5

## PDF page 108

4105508   Cianorte               5   4122602   Rondon                      5
4105607   Cidade Gaúcha          5   4122651   Rosário do Ivaí             4
4105706   Clevelândia            5   4122701   Sabáudia                    5
4105805   Colombo                3   4122800   Salgado Filho               4
4105904   Colorado               4   4122909   Salto do Itararé            5
4106001   Congonhinhas           5   4123006   Salto do Lontra             5
4106100   Conselheiro Mairinck   5   4123105   Santa Amélia                4
4106209   Contenda               5   4123204   Santa Cecília do Pavão      5
4106308   Corbélia               5   4123303   Santa Cruz de Monte         5
                                               Castelo
4106407   Cornélio Procópio      5   4123402   Santa Fé                    4
4106506   Coronel Vivida         5   4123501   Santa Helena                5
4106555   Corumbataí do Sul      4   4123600   Santa Inês                  4
4106571   Cruzeiro do Iguaçu     4   4123709   Santa Isabel do Ivaí        5
4106605   Cruzeiro do Oeste      5   4123808   Santa Izabel do Oeste       5
4106704   Cruzeiro do Sul        5   4123824   Santa Lúcia                 5
4106852   Cruzmaltina            5   4123907   Santa Mariana               5
4106902   Curitiba               1   4124004   Santana do Itararé          5
4107009   Curiúva                5   4124020   Santa Tereza do Oeste       5
4107108   Diamante do Norte      5   4124053   Santa Terezinha de Itaipu   5
4107157   Diamante D'Oeste       5   4124103   Santo Antônio da Platina    5
4107207   Dois Vizinhos          5   4124202   Santo Antônio do Caiuá      5
4107256   Douradina              5   4124301   Santo Antônio do Paraíso    5
4107306   Doutor Camargo         4   4124400   Santo Antônio do Sudoeste   5
4107504   Engenheiro Beltrão     5   4124509   Santo Inácio                4
4107538   Entre Rios do Oeste    4   4124608   São Carlos do Ivaí          4
4107553   Farol                  5   4124707   São Jerônimo da Serra       5
4107603   Faxinal                5   4124806   São João                    5
4107652   Fazenda Rio Grande     4   4124905   São João do Caiuá           5
4107702   Fênix                  4   4125001   São João do Ivaí            5
4107751   Figueira               4   4125209   São Jorge d'Oeste           5
4107801   Floraí                 5   4125308   São Jorge do Ivaí           5
4107900   Floresta               4   4125357   São Jorge do Patrocínio     5
4108007   Florestópolis          4   4125407   São José da Boa Vista       5
4108106   Flórida                4   4125456   São José das Palmeiras      5
4108205   Formosa do Oeste       5   4125506   São José dos Pinhais        4
4108304   Foz do Iguaçu          5   4125555   São Manoel do Paraná        3
4108320   Francisco Alves        5   4125605   São Mateus do Sul           5
4108403   Francisco Beltrão      5   4125704   São Miguel do Iguaçu        5
4108452   Foz do Jordão          5   4125753   São Pedro do Iguaçu         5
4108502   General Carneiro       4   4125803   São Pedro do Ivaí           5
4108601   Goioerê                5   4125902   São Pedro do Paraná         5
4108700   Grandes Rios           5   4126009   São Sebastião da Amoreira   5
4108809   Guaíra                 5   4126108   São Tomé                    4
4108908   Guairaçá               5   4126207   Sapopema                    5
4109005   Guapirama              5   4126256   Sarandi                     5
4109104   Guaporema              4   4126272   Saudade do Iguaçu           3
4109203   Guaraci                3   4126306   Sengés                      5
4109302   Guaraniaçu             5   4126355   Serranópolis do Iguaçu      4
4109401   Guarapuava             5   4126405   Sertaneja                   5
4109609   Guaratuba              3   4126504   Sertanópolis                5
4109708   Ibaiti                 5   4126603   Siqueira Campos             5
4109757   Ibema                  5   4126678   Tamarana                    5
4109807   Ibiporã                5   4126702   Tamboara                    5
4109906   Icaraíma               5   4126801   Tapejara                    5
4110003   Iguaraçu               4   4126900   Tapira                      5
4110052   Iguatu                 5   4127106   Telêmaco Borba              1
4110078   Imbaú                  4   4127205   Terra Boa                   5
4110102   Imbituva               5   4127304   Terra Rica                  5

## PDF page 109

4110201   Inácio Martins            4   4127403   Terra Roxa                 5
4110300   Inajá                     5   4127502   Tibagi                     5
4110409   Indianópolis              4   4127700   Toledo                     5
4110607   Iporã                     5   4127858   Três Barras do Paraná      5
4110656   Iracema do Oeste          4   4127908   Tuneiras do Oeste          5
4110706   Irati                     5   4127957   Tupãssi                    5
4110805   Iretama                   5   4128005   Ubiratã                    5
4110904   Itaguajé                  4   4128104   Umuarama                   5
4110953   Itaipulândia              5   4128203   União da Vitória           4
4111001   Itambaracá                5   4128302   Uniflor                    4
4111100   Itambé                    4   4128401   Uraí                       5
4111209   Itapejara d'Oeste         5   4128500   Wenceslau Braz             5
4111258   Itaperuçu                 4   4128534   Ventania                   5
4111308   Itaúna do Sul             5   4128559   Vera Cruz do Oeste         5
4111506   Ivaiporã                  5   4128625   Alto Paraíso               5
4111555   Ivaté                     5   4128658   Virmond                    4
4111605   Ivatuba                   4   4128708   Vitorino                   5
4111704   Jaboti                    4   4100202   Adrianópolis               5
4111803   Jacarezinho               5   4100301   Agudos do Sul              4
4111902   Jaguapitã                 4   4101309   Antônio Olinto             5
4112009   Jaguariaíva               5   4101655   Arapuã                     5
4112108   Jandaia do Sul            4   4101853   Ariranha do Ivaí           5
4112207   Janiópolis                5   4102752   Bela Vista da Caroba       5
4112306   Japira                    5   4103024   Boa Esperança do Iguaçu    4
4112405   Japurá                    5   4103040   Boa Ventura de São Roque   5
4112504   Jardim Alegre             5   4103107   Bocaiúva do Sul            4
4112603   Jardim Olinda             4   4103156   Bom Jesus do Sul           4
4112702   Jataizinho                5   4103958   Campina do Simão           5
4112751   Jesuítas                  5   4104402   Cândido de Abreu           5
4112801   Joaquim Távora            4   4104428   Candói                     5
4112900   Jundiaí do Sul            5   4105201   Cerro Azul                 5
4112959   Juranda                   5   4106456   Coronel Domingos Soares    4
4113007   Jussara                   5   4106803   Cruz Machado               5
4113106   Kaloré                    5   4107124   Diamante do Sul            4
4113205   Lapa                      5   4107405   Enéas Marques              4
4113304   Laranjeiras do Sul        5   4107520   Esperança Nova             5
4113403   Leópolis                  5   4107546   Espigão Alto do Iguaçu     5
4113429   Lidianópolis              5   4107736   Fernandes Pinheiro         5
4113502   Loanda                    5   4107850   Flor da Serra do Sul       5
4113601   Lobato                    4   4108551   Godoy Moreira              4
4113700   Londrina                  5   4108650   Goioxim                    5
4113734   Luiziana                  5   4108957   Guamiranga                 5
4113759   Lunardelli                5   4109500   Guaraqueçaba               3
4113809   Lupionópolis              4   4109658   Honório Serpa              5
4113908   Mallet                    5   4110508   Ipiranga                   5
4114005   Mamborê                   5   4111407   Ivaí                       5
4114104   Mandaguaçu                4   4113254   Laranjal                   3
4114203   Mandaguari                5   4113452   Lindoeste                  5
4114401   Mangueirinha              5   4114302   Mandirituba                5
4114500   Manoel Ribas              5   4114351   Manfrinópolis              4
4114609   Marechal Cândido Rondon   5   4115457   Marquinho                  4
4114708   Maria Helena              5   4115739   Mato Rico                  5
4114807   Marialva                  5   4116208   Morretes                   3
4114906   Marilândia do Sul         5   4116950   Nova Esperança do          4
                                                  Sudoeste
4115002   Marilena                  5   4117057   Nova Laranjeiras           4
4115101   Mariluz                   5   4117271   Nova Tebas                 5
4115200   Maringá                   5   4117305   Ortigueira                 5
4115309   Mariópolis                5   4118709   Paulo Frontin              5

## PDF page 110

4115358   Maripá                          5      4119004   Pérola d'Oeste           5
4115408   Marmeleiro                      5      4119103   Piên                     5
4115507   Marumbi                         4      4119251   Pinhal de São Bento      3
4115606   Matelândia                      5      4119806   Planalto                 5
4115705   Matinhos                        1      4120150   Porto Barreiro           5
4115754   Mauá da Serra                   5      4120606   Prudentópolis            5
4115804   Medianeira                      4      4121208   Quitandinha              5
4115853   Mercedes                        5      4122008   Rio Azul                 5
4115903   Mirador                         5      4122156   Rio Bonito do Iguaçu     5
4116000   Miraselva                       1      4122172   Rio Branco do Ivaí       5
4116059   Missal                          5      4123857   Santa Maria do Oeste     5
4116109   Moreira Sales                   5      4123956   Santa Mônica             5
4116307   Munhoz de Melo                  3      4125100   São João do Triunfo      5
4116406   Nossa Senhora das Graças        3      4126652   Sulina                   4
4116505   Nova Aliança do Ivaí            5      4127007   Teixeira Soares          5
4116604   Nova América da Colina          5      4127601   Tijucas do Sul           5
4116703   Nova Aurora                     5      4127809   Tomazina                 5
4116802   Nova Cantu                      5      4127882   Tunas do Paraná          3
4116901   Nova Esperança                  5      4127965   Turvo                    5
4117008   Nova Fátima                     5      4128609   Verê                     5
4117107   Nova Londrina                   5      4128633   Doutor Ulysses           5
4117206   Nova Olímpia                    4      4128807   Xambrê                   5
4117214   Nova Santa Bárbara              5
                                        RIO DE JANEIRO
3300100   Angra dos Reis                  1      3303203   Nilópolis                5
3300159   Aperibé                         1      3303302   Niterói                  1
3300209   Araruama                        2      3303401   Nova Friburgo            4
3300225   Areal                           1      3303500   Nova Iguaçu              3
3300233   Armação dos Búzios              1      3303609   Paracambi                1
3300258   Arraial do Cabo                 5      3303708   Paraíba do Sul           4
3300308   Barra do Piraí                  1      3303807   Paraty                   1
3300407   Barra Mansa                     1      3303856   Paty do Alferes          5
3300456   Belford Roxo                    1      3303906   Petrópolis               2
3300506   Bom Jardim                      4      3303955   Pinheiral                1
3300605   Bom Jesus do Itabapoana         3      3304003   Piraí                    1
3300704   Cabo Frio                       2      3304102   Porciúncula              2
3300803   Cachoeiras de Macacu            4      3304110   Porto Real               1
3300902   Cambuci                         5      3304128   Quatis                   1
3300936   Carapebus                       1      3304144   Queimados                2
3300951   Comendador Levy                 1      3304151   Quissamã                 3
          Gasparian
3301009   Campos dos Goytacazes           3      3304201   Resende                  2
3301108   Cantagalo                       1      3304300   Rio Bonito               3
3301157   Cardoso Moreira                 2      3304409   Rio Claro                1
3301207   Carmo                           1      3304508   Rio das Flores           1
3301306   Casimiro de Abreu               3      3304524   Rio das Ostras           1
3301405   Conceição de Macabu             2      3304557   Rio de Janeiro           5
3301504   Cordeiro                        2      3304607   Santa Maria Madalena     2
3301603   Duas Barras                     4      3304706   Santo Antônio de Pádua   4
3301702   Duque de Caxias                 3      3304755   São Francisco de         5
                                                           Itabapoana
3301801   Engenheiro Paulo de Frontin     1      3304805   São Fidélis              3
3301850   Guapimirim                      3      3304904   São Gonçalo              1
3301876   Iguaba Grande                   1      3305000   São João da Barra        1
3301900   Itaboraí                        1      3305109   São João de Meriti       5
3302007   Itaguaí                         2      3305208   São Pedro da Aldeia      2
3302056   Italva                          3      3305307   São Sebastião do Alto    4
3302106   Itaocara                        3      3305406   Sapucaia                 3
3302205   Itaperuna                       4      3305505   Saquarema                2

## PDF page 111

3302254   Itatiaia                      1      3305554    Seropédica                 2
3302270   Japeri                        3      3305604    Silva Jardim               3
3302304   Laje do Muriaé                2      3305752    Tanguá                     3
3302403   Macaé                         3      3305802    Teresópolis                3
3302452   Macuco                        1      3306008    Três Rios                  1
3302502   Magé                          3      3306107    Valença                    1
3302601   Mangaratiba                   1      3306156    Varre-Sai                  2
3302700   Maricá                        1      3306206    Vassouras                  4
3302809   Mendes                        1      3306305    Volta Redonda              1
3302858   Mesquita                      1      3305133    São José de Ubá            5
3302908   Miguel Pereira                2      3305158    São José do Vale do Rio    4
                                                          Preto
3303005   Miracema                      3      3305703    Sumidouro                  4
3303104   Natividade                    2      3305901    Trajano de Moraes          4
                                    RIO GRANDE DO NORTE
2400109   Acari                         1      2409902    Pendências                 1
2400208   Açu                           2      2410009    Pilões                     1
2400307   Afonso Bezerra                2      2410108    Poço Branco                3
2400406   Água Nova                     1      2410207    Portalegre                 1
2400505   Alexandria                    1      2410256    Porto do Mangue            1
2400604   Almino Afonso                 1      2410306    Serra Caiada               4
2400703   Alto do Rodrigues             1      2410504    Rafael Fernandes           1
2400802   Angicos                       1      2410603    Rafael Godeiro             1
2400901   Antônio Martins               1      2410702    Riacho da Cruz             1
2401008   Apodi                         3      2410900    Riachuelo                  1
2401107   Areia Branca                  1      2411007    Rodolfo Fernandes          1
2401206   Arês                          1      2411056    Tibau                      1
2401305   Augusto Severo                1      2411106    Ruy Barbosa                1
2401404   Baía Formosa                  1      2411205    Santa Cruz                 2
2401453   Baraúna                       2      2411403    Santana do Matos           3
2401651   Bodó                          4      2411429    Santana do Seridó          1
2401701   Bom Jesus                     4      2411502    Santo Antônio              4
2401800   Brejinho                      2      2411700    São Bento do Trairí        1
2401859   Caiçara do Norte              1      2411809    São Fernando               1
2401909   Caiçara do Rio do Vento       1      2411908    São Francisco do Oeste     1
2402006   Caicó                         1      2412005    São Gonçalo do Amarante    4
2402105   Campo Redondo                 1      2412104    São João do Sabugi         1
2402204   Canguaretama                  2      2412302    São José do Campestre      1
2402303   Caraúbas                      2      2412401    São José do Seridó         1
2402402   Carnaúba dos Dantas           1      2412500    São Miguel                 2
2402501   Carnaubais                    2      2412559    São Miguel do Gostoso      4
2402600   Ceará-Mirim                   3      2412609    São Paulo do Potengi       2
2403004   Cruzeta                       1      2412708    São Pedro                  2
2403103   Currais Novos                 1      2412807    São Rafael                 1
2403251   Parnamirim                    2      2412906    São Tomé                   1
2403400   Equador                       1      2413003    São Vicente                2
2403509   Espírito Santo                1      2413201    Senador Georgino Avelino   1
2403608   Extremoz                      2      2413300    Serra de São Bento         1
2403707   Felipe Guerra                 1      2413409    Serra Negra do Norte       1
2403756   Fernando Pedroza              1      2413557    Serrinha dos Pintos        1
2403806   Florânia                      2      2413706    Sítio Novo                 1
2403905   Francisco Dantas              1      2413805    Taboleiro Grande           1
2404002   Frutuoso Gomes                1      2414001    Tangará                    1
2404101   Galinhos                      1      2414100    Tenente Ananias            1
2404200   Goianinha                     2      2414209    Tibau do Sul               1
2404309   Governador Dix-Sept           2      2414308    Timbaúba dos Batistas      1
          Rosado
2404408   Grossos                       1      2414456    Triunfo Potiguar           1
2404804   Ipueira                       1      2414506    Umarizal                   1

## PDF page 112

2404853   Itajá                   1     2414605   Upanema                     1
2404903   Itaú                    2     2414704   Várzea                      1
2405009   Jaçanã                  1     2414902   Viçosa                      1
2405108   Jandaíra                1     2415008   Vila Flor                   1
2405207   Janduís                 1     2401503   Barcelona                   1
2405405   Japi                    1     2401602   Bento Fernandes             2
2405603   Jardim de Piranhas      1     2402709   Cerro Corá                  4
2405702   Jardim do Seridó        1     2402808   Coronel Ezequiel            1
2405801   João Câmara             2     2402907   Coronel João Pessoa         1
2406007   José da Penha           1     2403202   Doutor Severiano            1
2406106   Jucurutu                1     2403301   Encanto                     1
2406205   Lagoa d'Anta            4     2404507   Guamaré                     2
2406403   Lagoa de Velhos         1     2404606   Ielmo Marinho               3
2406502   Lagoa Nova              3     2404705   Ipanguaçu                   1
2406601   Lagoa Salgada           3     2405306   Januário Cicco              5
2406700   Lajes                   1     2405504   Jardim de Angicos           1
2406809   Lajes Pintadas          1     2405900   João Dias                   1
2406908   Lucrécia                1     2406155   Jundiá                      1
2407005   Luís Gomes              1     2406304   Lagoa de Pedras             2
2407104   Macaíba                 3     2407500   Maxaranguape                2
2407203   Macau                   1     2407807   Monte Alegre                2
2407252   Major Sales             1     2408201   Nísia Floresta              3
2407302   Marcelino Vieira        1     2408607   Paraná                      1
2407401   Martins                 1     2408953   Rio do Fogo                 2
2407609   Messias Targino         1     2409209   Passagem                    2
2407708   Montanhas               2     2409506   Pedra Grande                2
2407906   Monte das Gameleiras    1     2409605   Pedra Preta                 2
2408003   Mossoró                 3     2410405   Pureza                      4
2408102   Natal                   1     2410801   Riacho de Santana           1
2408300   Nova Cruz               2     2411601   São Bento do Norte          1
2408409   Olho d'Água do Borges   1     2412203   São José de Mipibu          3
2408508   Ouro Branco             1     2413102   Senador Elói de Souza       3
2408706   Paraú                   1     2413359   Serra do Mel                3
2408805   Parazinho               2     2413508   Serrinha                    1
2408904   Parelhas                1     2413607   Severiano Melo              2
2409100   Passa e Fica            4     2413904   Taipu                       3
2409308   Patu                    1     2414159   Tenente Laurentino Cruz     3
2409332   Santa Maria             1     2414407   Touros                      5
2409407   Pau dos Ferros          1     2414753   Venha-Ver                   1
2409704   Pedro Avelino           1     2414803   Vera Cruz                   4
2409803   Pedro Velho             2
                                  RONDÔNIA
1100015   Alta Floresta D'Oeste   5     1101401   Monte Negro                 5
1100023   Ariquemes               4     1101468   Pimenteiras do Oeste        4
1100049   Cacoal                  5     1101492   São Francisco do Guaporé    4
1100056   Cerejeiras              5     1100031   Cabixi                      4
1100064   Colorado do Oeste       4     1100072   Corumbiara                  5
1100080   Costa Marques           3     1100148   Nova Brasilândia D'Oeste    4
1100098   Espigão D'Oeste         4     1100262   Rio Crespo                  4
1100106   Guajará-Mirim           4     1100320   São Miguel do Guaporé       4
1100114   Jaru                    5     1100379   Alto Alegre dos Parecis     5
1100122   Ji-Paraná               4     1100502   Novo Horizonte do Oeste     3
1100130   Machadinho D'Oeste      5     1100601   Cacaulândia                 4
1100155   Ouro Preto do Oeste     3     1100700   Campo Novo de Rondônia      4
1100189   Pimenta Bueno           4     1100908   Castanheiras                4
1100205   Porto Velho             5     1100924   Chupinguaia                 5
1100254   Presidente Médici       4     1101005   Governador Jorge Teixeira   4
1100288   Rolim de Moura          4     1101203   Ministro Andreazza          3
1100296   Santa Luzia D'Oeste     3     1101435   Nova União                  3

## PDF page 113

1100304   Vilhena                    5       1101450   Parecis                     3
1100338   Nova Mamoré                5       1101476   Primavera de Rondônia       2
1100346   Alvorada D'Oeste           4       1101484   São Felipe D'Oeste          3
1100403   Alto Paraíso               4       1101500   Seringueiras                4
1100452   Buritis                    5       1101559   Teixeirópolis               3
1100809   Candeias do Jamari         5       1101609   Theobroma                   4
1100940   Cujubim                    4       1101708   Urupá                       4
1101104   Itapuã do Oeste            3       1101757   Vale do Anari               4
1101302   Mirante da Serra           4       1101807   Vale do Paraíso             3
1100015   Alta Floresta D'Oeste      5       1101401   Monte Negro                 5
1100023   Ariquemes                  4       1101468   Pimenteiras do Oeste        4
1100049   Cacoal                     5       1101492   São Francisco do Guaporé    4
1100056   Cerejeiras                 5       1100031   Cabixi                      4
1100064   Colorado do Oeste          4       1100072   Corumbiara                  5
1100080   Costa Marques              3       1100148   Nova Brasilândia D'Oeste    4
1100098   Espigão D'Oeste            4       1100262   Rio Crespo                  4
1100106   Guajará-Mirim              4       1100320   São Miguel do Guaporé       4
1100114   Jaru                       5       1100379   Alto Alegre dos Parecis     5
1100122   Ji-Paraná                  4       1100502   Novo Horizonte do Oeste     3
1100130   Machadinho D'Oeste         5       1100601   Cacaulândia                 4
1100155   Ouro Preto do Oeste        3       1100700   Campo Novo de Rondônia      4
1100189   Pimenta Bueno              4       1100908   Castanheiras                4
1100205   Porto Velho                5       1100924   Chupinguaia                 5
1100254   Presidente Médici          4       1101005   Governador Jorge Teixeira   4
1100288   Rolim de Moura             4       1101203   Ministro Andreazza          3
1100296   Santa Luzia D'Oeste        3       1101435   Nova União                  3
1100304   Vilhena                    5       1101450   Parecis                     3
1100338   Nova Mamoré                5       1101476   Primavera de Rondônia       2
1100346   Alvorada D'Oeste           4       1101484   São Felipe D'Oeste          3
1100403   Alto Paraíso               4       1101500   Seringueiras                4
1100452   Buritis                    5       1101559   Teixeirópolis               3
1100809   Candeias do Jamari         5       1101609   Theobroma                   4
1100940   Cujubim                    4       1101708   Urupá                       4
1101104   Itapuã do Oeste            3       1101757   Vale do Anari               4
1101302   Mirante da Serra           4       1101807   Vale do Paraíso             3
                                      RORAIMA
1400100   Boa Vista                  4       1400175   Cantá                       5
1400209   Caracaraí                  3       1400233   Caroebe                     4
1400308   Mucajaí                    4       1400282   Iracema                     3
1400506   São João da Baliza         3       1400407   Normandia                   4
1400605   São Luiz                   3       1400456   Pacaraima                   4
1400027   Amajari                    4       1400472   Rorainópolis                4
1400050   Alto Alegre                4       1400704   Uiramutã                    5
1400159   Bonfim                     5
                                  RIO GRANDE DO SUL
4300208   Ajuricaba                  5       4319901   Sapiranga                   3
4300406   Alegrete                   5       4320008   Sapucaia do Sul             1
4300604   Alvorada                   1       4320107   Sarandi                     5
4300646   Ametista do Sul            3       4320206   Seberi                      5
4300802   Antônio Prado              3       4320230   Sede Nova                   5
4300851   Arambaré                   5       4320305   Selbach                     5
4300877   Araricá                    1       4320404   Serafina Corrêa             3
4300901   Aratiba                    4       4320503   Sertão                      5
4301008   Arroio do Meio             3       4320701   Sobradinho                  3
4301057   Arroio do Sal              1       4320800   Soledade                    5
4301107   Arroio dos Ratos           4       4320909   Tapejara                    4
4301305   Arroio Grande              5       4321006   Tapera                      5
4301404   Arvorezinha                3       4321105   Tapes                       5

## PDF page 114

4301503   Augusto Pestana       5   4321204   Taquara                      4
4301602   Bagé                  5   4321303   Taquari                      4
4301636   Balneário Pinhal      2   4321352   Tavares                      4
4301651   Barão                 3   4321402   Tenente Portela              5
4301701   Barão de Cotegipe     4   4321436   Terra de Areia               2
4301800   Barracão              5   4321451   Teutônia                     3
4301875   Barra do Quaraí       5   4321501   Torres                       4
4301909   Barra do Ribeiro      5   4321600   Tramandaí                    2
4301958   Barra Funda           4   4321667   Três Cachoeiras              4
4302105   Bento Gonçalves       3   4321709   Três Coroas                  3
4302204   Boa Vista do Buricá   4   4321808   Três de Maio                 5
4302303   Bom Jesus             5   4321857   Três Palmeiras               5
4302352   Bom Princípio         4   4321907   Três Passos                  5
4302378   Bom Progresso         4   4321956   Trindade do Sul              5
4302402   Bom Retiro do Sul     2   4322004   Triunfo                      5
4302501   Bossoroca             5   4322103   Tucunduva                    5
4302600   Braga                 5   4322202   Tupanciretã                  5
4302659   Brochier              3   4322251   Tupandi                      2
4302709   Butiá                 4   4322301   Tuparendi                    5
4302808   Caçapava do Sul       5   4322400   Uruguaiana                   5
4302907   Cacequi               5   4322509   Vacaria                      5
4303004   Cachoeira do Sul      5   4322541   Vale Real                    2
4303103   Cachoeirinha          1   4322558   Vanini                       2
4303301   Caibaté               5   4322608   Venâncio Aires               5
4303509   Camaquã               5   4322707   Vera Cruz                    5
4303806   Campinas do Sul       5   4322806   Veranópolis                  2
4303905   Campo Bom             2   4322905   Viadutos                     4
4304002   Campo Novo            5   4323002   Viamão                       5
4304101   Campos Borges         4   4323408   Vila Maria                   5
4304200   Candelária            5   4323457   Vila Nova do Sul             4
4304408   Canela                2   4323804   Xangri-lá                    1
4304606   Canoas                2   4300034   Aceguá                       5
4304630   Capão da Canoa        1   4300059   Água Santa                   5
4304663   Capão do Leão         5   4300109   Agudo                        5
4304671   Capivari do Sul       5   4300307   Alecrim                      4
4304689   Capela de Santana     4   4300455   Alegria                      5
4304705   Carazinho             5   4300471   Almirante Tamandaré do Sul   5
4304804   Carlos Barbosa        3   4300505   Alpestre                     4
4304903   Casca                 4   4300554   Alto Alegre                  4
4304952   Caseiros              5   4300570   Alto Feliz                   2
4305009   Catuípe               5   4300638   Amaral Ferrador              3
4305108   Caxias do Sul         5   4300661   André da Rocha               5
4305124   Cerrito               3   4300703   Anta Gorda                   4
4305207   Cerro Largo           5   4301073   Arroio do Padre              1
4305306   Chapada               5   4301206   Arroio do Tigre              5
4305355   Charqueadas           5   4301552   Áurea                        4
4305405   Chiapetta             5   4301750   Barão do Triunfo             3
4305439   Chuí                  4   4301859   Barra do Guarita             3
4305454   Cidreira              3   4301925   Barra do Rio Azul            3
4305504   Ciríaco               5   4302006   Barros Cassal                4
4305603   Colorado              5   4302055   Benjamin Constant do Sul     3
4305702   Condor                5   4302154   Boa Vista das Missões        5
4305801   Constantina           5   4302220   Boa Vista do Cadeado         5
4305900   Coronel Bicaco        5   4302238   Boa Vista do Incra           5
4305959   Cotiporã              2   4302253   Boa Vista do Sul             3
4305975   Coxilha               5   4302451   Boqueirão do Leão            3
4306056   Cristal               5   4302584   Bozano                       5
4306106   Cruz Alta             5   4303202   Cacique Doble                4
4306205   Cruzeiro do Sul       5   4303400   Caiçara                      5

## PDF page 115

4306403   Dois Irmãos               3   4303558   Camargo                  3
4306429   Dois Irmãos das Missões   5   4303608   Cambará do Sul           4
4306452   Dois Lajeados             2   4303673   Campestre da Serra       4
4306601   Dom Pedrito               5   4303707   Campina das Missões      4
4306700   Dona Francisca            4   4304309   Cândido Godói            5
4306734   Doutor Maurício Cardoso   5   4304358   Candiota                 4
4306767   Eldorado do Sul           5   4304507   Canguçu                  5
4306809   Encantado                 3   4304614   Canudos do Vale          2
4306908   Encruzilhada do Sul       5   4304622   Capão Bonito do Sul      5
4306932   Entre-Ijuís               5   4304655   Capão do Cipó            5
4306957   Entre Rios do Sul         4   4304697   Capitão                  2
4306973   Erebango                  4   4304713   Caraá                    4
4307005   Erechim                   5   4304853   Carlos Gomes             4
4307054   Ernestina                 4   4305116   Centenário               4
4307104   Herval                    3   4305132   Cerro Branco             4
4307203   Erval Grande              3   4305157   Cerro Grande             4
4307401   Esmeralda                 5   4305173   Cerro Grande do Sul      4
4307500   Espumoso                  5   4305371   Charrua                  4
4307559   Estação                   4   4305447   Chuvisca                 4
4307609   Estância Velha            2   4305587   Colinas                  1
4307708   Esteio                    2   4305835   Coqueiro Baixo           1
4307807   Estrela                   4   4305850   Coqueiros do Sul         4
4307831   Eugênio de Castro         5   4305871   Coronel Barros           5
4307864   Fagundes Varela           3   4305934   Coronel Pilar            3
4307906   Farroupilha               3   4306007   Crissiumal               5
4308003   Faxinal do Soturno        4   4306072   Cristal do Sul           4
4308052   Faxinalzinho              4   4306130   Cruzaltense              4
4308078   Fazenda Vilanova          2   4306304   David Canabarro          4
4308102   Feliz                     3   4306320   Derrubadas               5
4308201   Flores da Cunha           2   4306353   Dezesseis de Novembro    3
4308458   Fortaleza dos Valos       5   4306379   Dilermando de Aguiar     4
4308508   Frederico Westphalen      5   4306502   Dom Feliciano            4
4308607   Garibaldi                 2   4306551   Dom Pedro de Alcântara   2
4308706   Gaurama                   4   4306759   Doutor Ricardo           2
4308805   General Câmara            5   4306924   Engenho Velho            4
4308904   Getúlio Vargas            5   4307302   Erval Seco               5
4309001   Giruá                     5   4307450   Esperança do Sul         4
4309100   Gramado                   3   4307815   Estrela Velha            5
4309209   Gravataí                  3   4308250   Floriano Peixoto         4
4309308   Guaíba                    5   4308300   Fontoura Xavier          3
4309407   Guaporé                   4   4308409   Formigueiro              5
4309506   Guarani das Missões       5   4308433   Forquetinha              2
4309555   Harmonia                  2   4308656   Garruchos                5
4309605   Horizontina               5   4308854   Gentil                   4
4309654   Hulha Negra               4   4309050   Glorinha                 4
4309704   Humaitá                   5   4309126   Gramado dos Loureiros    4
4309803   Ibiaçá                    5   4309159   Gramado Xavier           3
4309902   Ibiraiaras                5   4309258   Guabiju                  3
4309951   Ibirapuitã                4   4309571   Herveiras                2
4310009   Ibirubá                   5   4309753   Ibarama                  4
4310108   Igrejinha                 2   4310462   Ipiranga do Sul          5
4310207   Ijuí                      5   4310553   Itacurubi                5
4310306   Ilópolis                  2   4310579   Itapuca                  2
4310330   Imbé                      1   4310652   Itati                    3
4310363   Imigrante                 2   4310702   Itatiba do Sul           3
4310405   Independência             5   4310751   Ivorá                    4
4310413   Inhacorá                  5   4310850   Jaboticaba               4
4310439   Ipê                       4   4310876   Jacuizinho               5
4310504   Iraí                      5   4311130   Jari                     5

## PDF page 116

4310538   Itaara                   4   4311155   Jóia                      5
4310603   Itaqui                   5   4311239   Lagoa Bonita do Sul       3
4310801   Ivoti                    2   4311254   Lagoão                    4
4310900   Jacutinga                5   4311429   Lajeado do Bugre          4
4311007   Jaguarão                 5   4311601   Liberato Salzano          4
4311106   Jaguari                  4   4311643   Linha Nova                2
4311122   Jaquirana                2   4311718   Maçambará                 5
4311205   Júlio de Castilhos       5   4311734   Mampituba                 4
4311270   Lagoa dos Três Cantos    4   4311775   Maquiné                   4
4311304   Lagoa Vermelha           5   4311791   Maratá                    3
4311403   Lajeado                  3   4311981   Mariana Pimentel          4
4311502   Lavras do Sul            5   4312054   Marques de Souza          3
4311627   Lindolfo Collor          2   4312138   Mato Castelhano           4
4311700   Machadinho               4   4312153   Mato Leitão               4
4311759   Manoel Viana             5   4312179   Mato Queimado             5
4311809   Marau                    5   4312302   Miraguaí                  4
4311908   Marcelino Ramos          4   4312351   Montauri                  3
4312005   Mariano Moro             3   4312377   Monte Alegre dos Campos   4
4312104   Mata                     4   4312385   Monte Belo do Sul         2
4312203   Maximiliano de Almeida   5   4312427   Mormaço                   5
4312252   Minas do Leão            4   4312443   Morrinhos do Sul          4
4312401   Montenegro               4   4312450   Morro Redondo             2
4312476   Morro Reuter             3   4312617   Muitos Capões             5
4312500   Mostardas                5   4312625   Muliterno                 4
4312609   Muçum                    2   4312674   Nicolau Vergueiro         4
4312658   Não-Me-Toque             5   4312757   Nova Alvorada             3
4312708   Nonoai                   5   4312955   Nova Boa Vista            4
4312807   Nova Araçá               3   4313011   Nova Candelária           4
4312906   Nova Bassano             5   4313086   Nova Pádua                2
4313003   Nova Bréscia             1   4313334   Nova Ramada               5
4313037   Nova Esperança do Sul    3   4313391   Novo Cabrais              4
4313060   Nova Hartz               3   4313425   Novo Machado              5
4313102   Nova Palma               4   4313441   Novo Tiradentes           4
4313201   Nova Petrópolis          3   4313466   Novo Xingu                4
4313300   Nova Prata               3   4313490   Novo Barreiro             5
4313359   Nova Roma do Sul         3   4314027   Paraíso do Sul            5
4313375   Nova Santa Rita          4   4314035   Pareci Novo               2
4313409   Novo Hamburgo            4   4314068   Passa Sete                3
4313508   Osório                   4   4314076   Passo do Sobrado          4
4313607   Paim Filho               4   4314134   Paulo Bento               4
4313656   Palmares do Sul          5   4314175   Pedras Altas              4
4313706   Palmeira das Missões     5   4314464   Pinhal da Serra           4
4313805   Palmitinho               4   4314472   Pinhal Grande             4
4313904   Panambi                  5   4314498   Pinheirinho do Vale       4
4313953   Pantano Grande           5   4314548   Pinto Bandeira            2
4314001   Paraí                    3   4314555   Pirapó                    4
4314050   Parobé                   3   4314753   Poço das Antas            1
4314100   Passo Fundo              5   4314779   Pontão                    5
4314159   Paverama                 3   4314787   Ponte Preta               4
4314209   Pedro Osório             4   4315008   Porto Lucena              4
4314308   Pejuçara                 5   4315057   Porto Mauá                4
4314407   Pelotas                  5   4315073   Porto Vera Cruz           4
4314423   Picada Café              2   4315131   Pouso Novo                3
4314456   Pinhal                   4   4315156   Progresso                 3
4314506   Pinheiro Machado         3   4315172   Protásio Alves            2
4314605   Piratini                 4   4315206   Putinga                   3
4314704   Planalto                 4   4315321   Quevedos                  4
4314803   Portão                   3   4315404   Redentora                 5
4314902   Porto Alegre             3   4315453   Relvado                   2

## PDF page 117

4315107   Porto Xavier                4   4315552   Rio dos Índios           5
4315149   Presidente Lucena           3   4315958   Rolador                  5
4315305   Quaraí                      5   4316204   Rondinha                 4
4315313   Quatro Irmãos               5   4316303   Roque Gonzales           5
4315354   Quinze de Novembro          5   4316428   Sagrada Família          4
4315503   Restinga Sêca               5   4316477   Salvador das Missões     4
4315602   Rio Grande                  5   4316733   Santa Cecília do Sul     4
4315701   Rio Pardo                   5   4316972   Santa Margarida do Sul   5
4315750   Riozinho                    2   4317004   Santana da Boa Vista     4
4315800   Roca Sales                  3   4317251   Santa Tereza             2
4315909   Rodeio Bonito               4   4317558   Santo Antônio do Palma   3
4316006   Rolante                     4   4317954   Santo Expedito do Sul    3
4316105   Ronda Alta                  5   4318457   São José das Missões     4
4316402   Rosário do Sul              5   4318465   São José do Herval       2
4316436   Saldanha Marinho            5   4318499   São José do Inhacorá     4
4316451   Salto do Jacuí              5   4318614   São José do Sul          3
4316501   Salvador do Sul             2   4319125   São Martinho da Serra    5
4316600   Sananduva                   5   4319307   São Paulo das Missões    5
4316709   Santa Bárbara do Sul        5   4319356   São Pedro da Serra       1
4316758   Santa Clara do Sul          3   4319364   São Pedro das Missões    4
4316808   Santa Cruz do Sul           5   4319372   São Pedro do Butiá       4
4316907   Santa Maria                 5   4319711   São Valentim do Sul      2
4316956   Santa Maria do Herval       4   4319737   São Valério do Sul       5
4317103   Sant'Ana do Livramento      5   4320263   Segredo                  4
4317202   Santa Rosa                  5   4320321   Senador Salgado Filho    5
4317301   Santa Vitória do Palmar     5   4320354   Sentinela do Sul         5
4317400   Santiago                    5   4320453   Sério                    2
4317509   Santo Ângelo                5   4320552   Sertão Santana           4
4317608   Santo Antônio da Patrulha   5   4320578   Sete de Setembro         4
4317707   Santo Antônio das Missões   5   4320602   Severiano de Almeida     4
4317756   Santo Antônio do Planalto   5   4320651   Silveira Martins         4
4317806   Santo Augusto               5   4320677   Sinimbu                  4
4317905   Santo Cristo                5   4320859   Tabaí                    1
4318002   São Borja                   5   4321329   Taquaruçu do Sul         4
4318051   São Domingos do Sul         3   4321469   Tio Hugo                 4
4318101   São Francisco de Assis      5   4321477   Tiradentes do Sul        5
4318200   São Francisco de Paula      5   4321493   Toropi                   4
4318309   São Gabriel                 5   4321626   Travesseiro              2
4318408   São Jerônimo                4   4321634   Três Arroios             4
4318424   São João da Urtiga          4   4321832   Três Forquilhas          3
4318432   São João do Polêsine        4   4322152   Tunas                    3
4318440   São Jorge                   3   4322186   Tupanci do Sul           4
4318481   São José do Hortêncio       4   4322327   Turuçu                   4
4318507   São José do Norte           4   4322343   Ubiretama                4
4318606   São José do Ouro            5   4322350   União da Serra           3
4318622   São José dos Ausentes       5   4322376   Unistalda                4
4318705   São Leopoldo                1   4322525   Vale Verde               4
4318804   São Lourenço do Sul         5   4322533   Vale do Sol              4
4318903   São Luiz Gonzaga            5   4322855   Vespasiano Corrêa        2
4319000   São Marcos                  3   4323101   Vicente Dutra            5
4319109   São Martinho                5   4323200   Victor Graeff            5
4319158   São Miguel das Missões      5   4323309   Vila Flores              2
4319208   São Nicolau                 5   4323358   Vila Lângaro             4
4319406   São Pedro do Sul            5   4323507   Vista Alegre             3
4319505   São Sebastião do Caí        4   4323606   Vista Alegre do Prata    3
4319604   São Sepé                    5   4323705   Vista Gaúcha             4
4319703   São Valentim                4   4323754   Vitória das Missões      5
4319752   São Vendelino               1   4323770   Westfália                1
4319802   São Vicente do Sul          5

## PDF page 118

                                      SANTA CATARINA
4200101   Abelardo Luz                  5      4216008   São Carlos               4
4200200   Agrolândia                    4      4216057   São Cristóvão do Sul     2
4200408   Água Doce                     5      4216107   São Domingos             5
4200507   Águas de Chapecó              3      4216206   São Francisco do Sul     1
4201000   Anita Garibaldi               4      4216305   São João Batista         4
4201307   Araquari                      4      4216354   São João do Itaperiú     4
4201406   Araranguá                     5      4216503   São Joaquim              4
4201505   Armazém                       3      4216602   São José                 2
4201604   Arroio Trinta                 3      4216701   São José do Cedro        4
4201703   Ascurra                       3      4216909   São Lourenço do Oeste    4
4201950   Balneário Arroio do Silva     1      4217006   São Ludgero              2
4202008   Balneário Camboriú            1      4217204   São Miguel do Oeste      4
4202057   Balneário Barra do Sul        1      4217253   São Pedro de Alcântara   3
4202073   Balneário Gaivota             2      4217303   Saudades                 4
4202107   Barra Velha                   2      4217402   Schroeder                2
4202156   Belmonte                      3      4217501   Seara                    4
4202206   Benedito Novo                 3      4217550   Serra Alta               4
4202305   Biguaçu                       4      4217600   Siderópolis              2
4202404   Blumenau                      3      4217709   Sombrio                  5
4202453   Bombinhas                     1      4217808   Taió                     4
4202503   Bom Jardim da Serra           4      4217907   Tangará                  4
4202537   Bom Jesus                     4      4218004   Tijucas                  4
4202602   Bom Retiro                    5      4218202   Timbó                    3
4202800   Braço do Norte                3      4218251   Timbó Grande             3
4202859   Braço do Trombudo             3      4218301   Três Barras              5
4202909   Brusque                       2      4218350   Treviso                  1
4203006   Caçador                       5      4218400   Treze de Maio            4
4203105   Caibi                         3      4218509   Treze Tílias             3
4203154   Calmon                        4      4218608   Trombudo Central         4
4203204   Camboriú                      3      4218707   Tubarão                  5
4203303   Campo Alegre                  4      4218806   Turvo                    5
4203402   Campo Belo do Sul             5      4218905   Urubici                  4
4203501   Campo Erê                     5      4218954   Urupema                  3
4203600   Campos Novos                  5      4219002   Urussanga                2
4203709   Canelinha                     3      4219101   Vargeão                  3
4203808   Canoinhas                     5      4219176   Vargem Bonita            2
4203907   Capinzal                      4      4219309   Videira                  4
4203956   Capivari de Baixo             4      4219507   Xanxerê                  5
4204004   Catanduvas                    2      4219705   Xaxim                    4
4204103   Caxambu do Sul                4      4219853   Zortéa                   4
4204202   Chapecó                       5      4200051   Abdon Batista            3
4204251   Cocal do Sul                  2      4200309   Agronômica               4
4204301   Concórdia                     4      4200556   Águas Frias              3
4204400   Coronel Freitas               3      4200606   Águas Mornas             4
4204509   Corupá                        2      4200705   Alfredo Wagner           4
4204558   Correia Pinto                 4      4200754   Alto Bela Vista          2
4204608   Criciúma                      4      4200804   Anchieta                 3
4204707   Cunha Porã                    5      4200903   Angelina                 4
4204806   Curitibanos                   5      4201109   Anitápolis               4
4204905   Descanso                      4      4201208   Antônio Carlos           3
4205001   Dionísio Cerqueira            4      4201257   Apiúna                   3
4205100   Dona Emma                     2      4201273   Arabutã                  2
4205159   Doutor Pedrinho               3      4201653   Arvoredo                 2
4205209   Erval Velho                   4      4201802   Atalanta                 3
4205308   Faxinal dos Guedes            5      4201901   Aurora                   3
4205407   Florianópolis                 1      4202081   Bandeirante              3
4205456   Forquilhinha                  5      4202099   Barra Bonita             3
4205506   Fraiburgo                     5      4202131   Bela Vista do Toldo      4

## PDF page 119

4205605   Galvão                   4   4202438   Bocaina do Sul               3
4205704   Garopaba                 3   4202578   Bom Jesus do Oeste           4
4205803   Garuva                   3   4202701   Botuverá                     2
4205902   Gaspar                   5   4202875   Brunópolis                   4
4206009   Governador Celso Ramos   1   4203253   Capão Alto                   4
4206108   Grão Pará                2   4204152   Celso Ramos                  3
4206306   Guabiruba                2   4204178   Cerro Negro                  4
4206504   Guaramirim               5   4204194   Chapadão do Lageado          3
4206603   Guarujá do Sul           3   4204350   Cordilheira Alta             2
4206702   Herval d'Oeste           3   4204459   Coronel Martins              3
4206900   Ibirama                  2   4204756   Cunhataí                     3
4207007   Içara                    5   4205175   Entre Rios                   3
4207106   Ilhota                   4   4205191   Ermo                         4
4207304   Imbituba                 5   4205357   Flor do Sertão               2
4207502   Indaial                  3   4205431   Formosa do Sul               2
4207601   Ipira                    3   4205555   Frei Rogério                 4
4207650   Iporã do Oeste           4   4206207   Gravatal                     2
4207809   Irani                    3   4206405   Guaraciaba                   4
4208005   Itá                      2   4206652   Guatambú                     4
4208104   Itaiópolis               5   4206751   Ibiam                        2
4208203   Itajaí                   4   4206801   Ibicaré                      3
4208302   Itapema                  3   4207205   Imaruí                       5
4208401   Itapiranga               4   4207403   Imbuia                       3
4208450   Itapoá                   1   4207577   Iomerê                       3
4208500   Ituporanga               5   4207684   Ipuaçu                       5
4208708   Jacinto Machado          5   4207700   Ipumirim                     3
4208807   Jaguaruna                5   4207759   Iraceminha                   4
4208906   Jaraguá do Sul           4   4207858   Irati                        2
4209003   Joaçaba                  3   4207908   Irineópolis                  5
4209102   Joinville                5   4208609   Jaborá                       3
4209177   Jupiá                    3   4208955   Jardinópolis                 3
4209201   Lacerdópolis             3   4209151   José Boiteux                 2
4209300   Lages                    5   4209458   Lajeado Grande               4
4209409   Laguna                   4   4209805   Leoberto Leal                3
4209508   Laurentino               2   4209854   Lindóia do Sul               2
4209607   Lauro Müller             1   4210001   Luiz Alves                   2
4209706   Lebon Régis              5   4210050   Macieira                     4
4209904   Lontras                  4   4210209   Major Gercino                2
4210035   Luzerna                  3   4210308   Major Vieira                 5
4210100   Mafra                    5   4210555   Marema                       3
4210407   Maracajá                 4   4211256   Morro Grande                 4
4210506   Maravilha                4   4211454   Nova Itaberaba               3
4210605   Massaranduba             5   4211652   Novo Horizonte               3
4210704   Matos Costa              4   4211850   Ouro Verde                   5
4210803   Meleiro                  5   4211876   Paial                        2
4210852   Mirim Doce               4   4211892   Painel                       2
4210902   Modelo                   4   4212056   Palmeira                     2
4211009   Mondaí                   3   4212239   Paraíso                      3
4211058   Monte Carlo              4   4212270   Passos Maia                  4
4211108   Monte Castelo            4   4212403   Pedras Grandes               5
4211207   Morro da Fumaça          3   4212650   Pescaria Brava               3
4211306   Navegantes               4   4212700   Petrolândia                  3
4211405   Nova Erechim             3   4213153   Planalto Alegre              3
4211504   Nova Trento              4   4213906   Presidente Castello Branco   1
4211603   Nova Veneza              5   4214102   Presidente Nereu             2
4211702   Orleans                  3   4214151   Princesa                     3
4211751   Otacílio Costa           4   4214300   Rancho Queimado              4
4211801   Ouro                     4   4214409   Rio das Antas                4
4211900   Palhoça                  3   4214508   Rio do Campo                 4

## PDF page 120

4212007   Palma Sola                  5        4214904   Rio Fortuna                2
4212106   Palmitos                    4        4215059   Rio Rufino                 3
4212205   Papanduva                   5        4215075   Riqueza                    3
4212254   Passo de Torres             2        4215208   Romelândia                 3
4212304   Paulo Lopes                 4        4215356   Saltinho                   3
4212502   Penha                       1        4215455   Sangão                     5
4212601   Peritiba                    3        4215554   Santa Helena               3
4212809   Balneário Piçarras          2        4215604   Santa Rosa de Lima         1
4212908   Pinhalzinho                 4        4215653   Santa Rosa do Sul          4
4213005   Pinheiro Preto              2        4215679   Santa Terezinha            4
4213104   Piratuba                    3        4215687   Santa Terezinha do         2
                                                         Progresso
4213203   Pomerode                    3        4215695   Santiago do Sul            3
4213302   Ponte Alta                  4        4215752   São Bernardino             3
4213351   Ponte Alta do Norte         1        4215901   São Bonifácio              3
4213401   Ponte Serrada               3        4216255   São João do Oeste          3
4213500   Porto Belo                  1        4216404   São João do Sul            5
4213609   Porto União                 4        4216800   São José do Cerrito        5
4213708   Pouso Redondo               4        4217105   São Martinho               4
4213807   Praia Grande                4        4217154   São Miguel da Boa Vista    2
4214003   Presidente Getúlio          3        4217758   Sul Brasil                 3
4214201   Quilombo                    4        4217956   Tigrinhos                  3
4214607   Rio do Oeste                4        4218103   Timbé do Sul               4
4214706   Rio dos Cedros              4        4218756   Tunápolis                  3
4214805   Rio do Sul                  3        4218855   União do Oeste             3
4215000   Rio Negrinho                4        4219150   Vargem                     4
4215109   Rodeio                      3        4219200   Vidal Ramos                4
4215307   Salete                      2        4219358   Vitor Meireles             4
4215406   Salto Veloso                3        4219408   Witmarsum                  3
4215505   Santa Cecília               3        4219606   Xavantina                  3
4215703   Santo Amaro da Imperatriz   4        4220000   Balneário Rincão           1
4215802   São Bento do Sul            3
                                          SERGIPE
2800100   Amparo de São Francisco     1        2805505   Poço Verde                 5
2800209   Aquidabã                    3        2805703   Propriá                    4
2800308   Aracaju                     1        2805901   Riachuelo                  3
2800506   Areia Branca                3        2806008   Ribeirópolis               4
2800605   Barra dos Coqueiros         1        2806107   Rosário do Catete          1
2800670   Boquim                      3        2806404   Santana do São Francisco   2
2800704   Brejo Grande                3        2806503   Santa Rosa de Lima         3
2801009   Campo do Brito              4        2806602   Santo Amaro das Brotas     2
2801207   Canindé de São Francisco    3        2806701   São Cristóvão              2
2801306   Capela                      3        2806800   São Domingos               4
2801405   Carira                      5        2806909   São Francisco              2
2801504   Carmópolis                  2        2807105   Simão Dias                 5
2801603   Cedro de São João           2        2807402   Tobias Barreto             4
2801702   Cristinápolis               3        2807600   Umbaúba                    3
2801900   Cumbe                       3        2800407   Arauá                      3
2802007   Divina Pastora              1        2801108   Canhoba                    3
2802106   Estância                    4        2802403   Gararu                     2
2802205   Feira Nova                  2        2802809   Indiaroba                  3
2802304   Frei Paulo                  4        2803203   Itaporanga d'Ajuda         4
2802502   General Maynard             1        2803302   Japaratuba                 4
2802601   Gracho Cardoso              2        2803401   Japoatã                    4
2802700   Ilha das Flores             3        2803807   Malhada dos Bois           2
2802908   Itabaiana                   5        2803906   Malhador                   3
2803005   Itabaianinha                4        2804102   Moita Bonita               3
2803104   Itabi                       1        2804300   Muribeca                   2
2803500   Lagarto                     5        2804458   Nossa Senhora Aparecida    3

## PDF page 121

2803609   Laranjeiras                2     2804904   Pacatuba                  4
2803708   Macambira                  3     2805000   Pedra Mole                3
2804003   Maruim                     1     2805406   Poço Redondo              4
2804201   Monte Alegre de Sergipe    2     2805604   Porto da Folha            3
2804409   Neópolis                   4     2805802   Riachão do Dantas         4
2804508   Nossa Senhora da Glória    3     2806206   Salgado                   4
2804607   Nossa Senhora das Dores    4     2806305   Santa Luzia do Itanhy     4
2804706   Nossa Senhora de Lourdes   1     2807006   São Miguel do Aleixo      2
2804805   Nossa Senhora do Socorro   1     2807204   Siriri                    1
2805109   Pedrinhas                  2     2807303   Telha                     2
2805208   Pinhão                     3     2807501   Tomar do Geru             3
2805307   Pirambu                    2
                                     SÃO PAULO
3500105   Adamantina                 3     3529500   Mendonça                  3
3500204   Adolfo                     4     3529609   Meridiano                 1
3500303   Aguaí                      5     3529658   Mesópolis                 3
3500402   Águas da Prata             3     3529708   Miguelópolis              5
3500501   Águas de Lindóia           1     3529807   Mineiros do Tietê         2
3500550   Águas de Santa Bárbara     4     3529906   Miracatu                  1
3500600   Águas de São Pedro         1     3530003   Mira Estrela              1
3500709   Agudos                     2     3530102   Mirandópolis              3
3500758   Alambari                   4     3530201   Mirante do Paranapanema   4
3500808   Alfredo Marcondes          2     3530300   Mirassol                  2
3500907   Altair                     1     3530409   Mirassolândia             1
3501004   Altinópolis                4     3530508   Mococa                    5
3501103   Alto Alegre                3     3530607   Mogi das Cruzes           4
3501152   Alumínio                   1     3530706   Mogi Guaçu                5
3501202   Álvares Florence           3     3530805   Mogi Mirim                5
3501301   Álvares Machado            4     3530904   Mombuca                   1
3501400   Álvaro de Carvalho         3     3531001   Monções                   1
3501509   Alvinlândia                3     3531100   Mongaguá                  1
3501608   Americana                  1     3531209   Monte Alegre do Sul       1
3501707   Américo Brasiliense        1     3531308   Monte Alto                4
3501806   Américo de Campos          4     3531407   Monte Aprazível           2
3501905   Amparo                     3     3531506   Monte Azul Paulista       1
3502002   Analândia                  1     3531605   Monte Castelo             1
3502101   Andradina                  4     3531803   Monte Mor                 4
3502200   Angatuba                   5     3531902   Morro Agudo               2
3502309   Anhembi                    5     3532009   Morungaba                 2
3502408   Anhumas                    3     3532058   Motuca                    1
3502507   Aparecida                  2     3532108   Murutinga do Sul          2
3502606   Aparecida d'Oeste          2     3532157   Nantes                    3
3502705   Apiaí                      5     3532207   Narandiba                 3
3502754   Araçariguama               1     3532405   Nazaré Paulista           1
3502804   Araçatuba                  4     3532504   Neves Paulista            1
3502903   Araçoiaba da Serra         4     3532603   Nhandeara                 2
3503000   Aramina                    1     3532702   Nipoã                     1
3503109   Arandu                     4     3532801   Nova Aliança              2
3503158   Arapeí                     1     3532827   Nova Campina              5
3503208   Araraquara                 3     3532868   Nova Castilho             2
3503307   Araras                     4     3532900   Nova Europa               1
3503356   Arco-Íris                  4     3533007   Nova Granada              3
3503406   Arealva                    2     3533106   Nova Guataporanga         1
3503505   Areias                     1     3533205   Nova Independência        1
3503604   Areiópolis                 2     3533254   Novais                    1
3503703   Ariranha                   1     3533304   Nova Luzitânia            2
3503802   Artur Nogueira             4     3533403   Nova Odessa               3
3503901   Arujá                      1     3533502   Novo Horizonte            4
3503950   Aspásia                    1     3533601   Nuporanga                 2

## PDF page 122

3504008   Assis                     4   3533700   Ocauçu                  5
3504107   Atibaia                   4   3533809   Óleo                    4
3504206   Auriflama                 1   3533908   Olímpia                 2
3504305   Avaí                      3   3534005   Onda Verde              1
3504404   Avanhandava               1   3534104   Oriente                 2
3504503   Avaré                     5   3534203   Orindiúva               2
3504602   Bady Bassitt              2   3534302   Orlândia                1
3504800   Bálsamo                   2   3534401   Osasco                  1
3504909   Bananal                   1   3534500   Oscar Bressane          3
3505005   Barão de Antonina         4   3534609   Osvaldo Cruz            1
3505104   Barbosa                   2   3534708   Ourinhos                3
3505203   Bariri                    2   3534757   Ouroeste                1
3505302   Barra Bonita              1   3534807   Ouro Verde              1
3505500   Barretos                  3   3534906   Pacaembu                2
3505609   Barrinha                  1   3535002   Palestina               4
3505708   Barueri                   1   3535101   Palmares Paulista       1
3505807   Bastos                    2   3535200   Palmeira d'Oeste        1
3505906   Batatais                  3   3535309   Palmital                5
3506003   Bauru                     1   3535408   Panorama                3
3506102   Bebedouro                 2   3535507   Paraguaçu Paulista      4
3506201   Bento de Abreu            2   3535705   Paraíso                 2
3506300   Bernardino de Campos      4   3535804   Paranapanema            5
3506359   Bertioga                  1   3535903   Paranapuã               4
3506409   Bilac                     3   3536000   Parapuã                 5
3506508   Birigui                   4   3536109   Pardinho                5
3506607   Biritiba Mirim            3   3536208   Pariquera-Açu           2
3506706   Boa Esperança do Sul      4   3536257   Parisi                  4
3506805   Bocaina                   1   3536307   Patrocínio Paulista     2
3506904   Bofete                    4   3536406   Paulicéia               1
3507001   Boituva                   2   3536505   Paulínia                1
3507100   Bom Jesus dos Perdões     1   3536570   Paulistânia             1
3507159   Bom Sucesso de Itararé    2   3536604   Paulo de Faria          4
3507209   Borá                      3   3536703   Pederneiras             2
3507308   Boracéia                  1   3536901   Pedranópolis            3
3507407   Borborema                 4   3537008   Pedregulho              2
3507456   Borebi                    2   3537107   Pedreira                1
3507506   Botucatu                  5   3537156   Pedrinhas Paulista      4
3507605   Bragança Paulista         4   3537206   Pedro de Toledo         1
3507704   Braúna                    2   3537305   Penápolis               3
3507753   Brejo Alegre              2   3537404   Pereira Barreto         5
3507803   Brodowski                 1   3537503   Pereiras                1
3507902   Brotas                    3   3537602   Peruíbe                 1
3508009   Buri                      5   3537701   Piacatu                 3
3508108   Buritama                  3   3537909   Pilar do Sul            5
3508207   Buritizal                 3   3538006   Pindamonhangaba         3
3508306   Cabrália Paulista         2   3538105   Pindorama               2
3508405   Cabreúva                  1   3538204   Pinhalzinho             4
3508504   Caçapava                  4   3538303   Piquerobi               2
3508603   Cachoeira Paulista        2   3538501   Piquete                 1
3508702   Caconde                   3   3538600   Piracaia                2
3508801   Cafelândia                3   3538709   Piracicaba              4
3508900   Caiabu                    2   3538808   Piraju                  5
3509007   Caieiras                  1   3538907   Pirajuí                 2
3509205   Cajamar                   1   3539004   Pirangi                 1
3509254   Cajati                    1   3539103   Pirapora do Bom Jesus   1
3509304   Cajobi                    1   3539202   Pirapozinho             3
3509403   Cajuru                    2   3539301   Pirassununga            4
3509452   Campina do Monte Alegre   5   3539400   Piratininga             1
3509502   Campinas                  3   3539509   Pitangueiras            1

## PDF page 123

3509601   Campo Limpo Paulista    1   3539608   Planalto               2
3509700   Campos do Jordão        1   3539707   Platina                5
3509809   Campos Novos Paulista   5   3539806   Poá                    1
3509908   Cananéia                2   3539905   Poloni                 1
3509957   Canas                   3   3540002   Pompéia                2
3510005   Cândido Mota            5   3540101   Pongaí                 2
3510104   Cândido Rodrigues       1   3540200   Pontal                 1
3510153   Canitar                 1   3540259   Pontalinda             2
3510203   Capão Bonito            5   3540309   Pontes Gestal          4
3510302   Capela do Alto          4   3540408   Populina               2
3510401   Capivari                1   3540507   Porangaba              2
3510500   Caraguatatuba           1   3540606   Porto Feliz            3
3510609   Carapicuíba             1   3540705   Porto Ferreira         5
3510708   Cardoso                 5   3540754   Potim                  2
3510807   Casa Branca             5   3540804   Potirendaba            3
3510906   Cássia dos Coqueiros    1   3540853   Pracinha               3
3511003   Castilho                3   3540903   Pradópolis             2
3511102   Catanduva               1   3541000   Praia Grande           1
3511201   Catiguá                 1   3541059   Pratânia               1
3511300   Cedral                  2   3541109   Presidente Alves       2
3511409   Cerqueira César         4   3541208   Presidente Bernardes   4
3511508   Cerquilho               4   3541307   Presidente Epitácio    3
3511607   Cesário Lange           5   3541406   Presidente Prudente    2
3511706   Charqueada              1   3541505   Presidente Venceslau   3
3511904   Clementina              2   3541604   Promissão              3
3512001   Colina                  4   3541703   Quatá                  4
3512100   Colômbia                2   3541802   Queiroz                4
3512209   Conchal                 5   3541901   Queluz                 1
3512308   Conchas                 1   3542008   Quintana               4
3512407   Cordeirópolis           2   3542107   Rafard                 1
3512506   Coroados                4   3542206   Rancharia              5
3512605   Coronel Macedo          5   3542305   Redenção da Serra      1
3512704   Corumbataí              2   3542404   Regente Feijó          4
3512803   Cosmópolis              3   3542503   Reginópolis            4
3512902   Cosmorama               3   3542602   Registro               2
3513009   Cotia                   1   3542701   Restinga               1
3513108   Cravinhos               3   3542909   Ribeirão Bonito        3
3513207   Cristais Paulista       3   3543006   Ribeirão Branco        5
3513306   Cruzália                4   3543105   Ribeirão Corrente      1
3513405   Cruzeiro                2   3543204   Ribeirão do Sul        5
3513504   Cubatão                 1   3543238   Ribeirão dos Índios    2
3513603   Cunha                   3   3543303   Ribeirão Pires         1
3513702   Descalvado              5   3543402   Ribeirão Preto         3
3513801   Diadema                 5   3543501   Riversul               4
3513850   Dirce Reis              1   3543600   Rifaina                2
3513900   Divinolândia            5   3543709   Rincão                 1
3514007   Dobrada                 1   3543808   Rinópolis              4
3514106   Dois Córregos           2   3543907   Rio Claro              3
3514205   Dolcinópolis            1   3544004   Rio das Pedras         1
3514304   Dourado                 1   3544103   Rio Grande da Serra    1
3514403   Dracena                 2   3544202   Riolândia              5
3514502   Duartina                3   3544251   Rosana                 5
3514601   Dumont                  1   3544301   Roseira                3
3514700   Echaporã                5   3544400   Rubiácea               4
3514809   Eldorado                1   3544509   Rubinéia               1
3514908   Elias Fausto            4   3544608   Sabino                 4
3514924   Elisiário               1   3544707   Sagres                 1
3514957   Embaúba                 1   3544806   Sales                  4
3515004   Embu das Artes          1   3544905   Sales Oliveira         1

## PDF page 124

3515103   Embu-Guaçu                   1   3545001   Salesópolis                  2
3515129   Emilianópolis                2   3545100   Salmourão                    3
3515152   Engenheiro Coelho            4   3545159   Saltinho                     1
3515186   Espírito Santo do Pinhal     4   3545209   Salto                        2
3515194   Espírito Santo do Turvo      3   3545308   Salto de Pirapora            4
3515202   Estrela d'Oeste              2   3545407   Salto Grande                 5
3515301   Estrela do Norte             3   3545506   Sandovalina                  3
3515350   Euclides da Cunha Paulista   5   3545605   Santa Adélia                 1
3515400   Fartura                      4   3545704   Santa Albertina              1
3515509   Fernandópolis                1   3545803   Santa Bárbara d'Oeste        2
3515608   Fernando Prestes             1   3546009   Santa Branca                 1
3515657   Fernão                       3   3546108   Santa Clara d'Oeste          3
3515707   Ferraz de Vasconcelos        1   3546207   Santa Cruz da Conceição      2
3515806   Flora Rica                   1   3546256   Santa Cruz da Esperança      1
3515905   Floreal                      1   3546306   Santa Cruz das Palmeiras     5
3516002   Flórida Paulista             2   3546405   Santa Cruz do Rio Pardo      5
3516101   Florínea                     4   3546504   Santa Ernestina              1
3516200   Franca                       2   3546603   Santa Fé do Sul              1
3516309   Francisco Morato             1   3546702   Santa Gertrudes              1
3516408   Franco da Rocha              1   3546801   Santa Isabel                 1
3516507   Gabriel Monteiro             2   3546900   Santa Lúcia                  2
3516606   Gália                        4   3547007   Santa Maria da Serra         5
3516705   Garça                        4   3547106   Santa Mercedes               2
3516804   Gastão Vidigal               1   3547205   Santana da Ponte Pensa       2
3516853   Gavião Peixoto               4   3547304   Santana de Parnaíba          1
3516903   General Salgado              2   3547403   Santa Rita d'Oeste           1
3517000   Getulina                     3   3547502   Santa Rita do Passa Quatro   3
3517109   Glicério                     3   3547601   Santa Rosa de Viterbo        1
3517208   Guaiçara                     2   3547650   Santa Salete                 1
3517307   Guaimbê                      3   3547700   Santo Anastácio              4
3517406   Guaíra                       5   3547809   Santo André                  1
3517505   Guapiaçu                     1   3547908   Santo Antônio da Alegria     4
3517703   Guará                        2   3548005   Santo Antônio de Posse       4
3517802   Guaraçaí                     2   3548054   Santo Antônio do Aracanguá   3
3517901   Guaraci                      1   3548104   Santo Antônio do Jardim      1
3518008   Guarani d'Oeste              1   3548203   Santo Antônio do Pinhal      2
3518107   Guarantã                     1   3548302   Santo Expedito               1
3518206   Guararapes                   5   3548401   Santópolis do Aguapeí        1
3518305   Guararema                    3   3548500   Santos                       1
3518404   Guaratinguetá                4   3548609   São Bento do Sapucaí         2
3518503   Guareí                       4   3548708   São Bernardo do Campo        1
3518602   Guariba                      1   3548807   São Caetano do Sul           5
3518701   Guarujá                      1   3548906   São Carlos                   3
3518800   Guarulhos                    1   3549003   São Francisco                1
3518859   Guatapará                    2   3549102   São João da Boa Vista        5
3518909   Guzolândia                   1   3549201   São João das Duas Pontes     1
3519006   Herculândia                  4   3549250   São João de Iracema          1
3519055   Holambra                     3   3549300   São João do Pau d'Alho       1
3519071   Hortolândia                  2   3549409   São Joaquim da Barra         3
3519105   Iacanga                      1   3549508   São José da Bela Vista       2
3519204   Iacri                        4   3549607   São José do Barreiro         1
3519303   Ibaté                        1   3549706   São José do Rio Pardo        4
3519402   Ibirá                        3   3549805   São José do Rio Preto        2
3519501   Ibirarema                    5   3549904   São José dos Campos          4
3519600   Ibitinga                     2   3549953   São Lourenço da Serra        1
3519808   Icém                         2   3550001   São Luiz do Paraitinga       3
3519907   Iepê                         4   3550100   São Manuel                   1
3520004   Igaraçu do Tietê             1   3550209   São Miguel Arcanjo           5
3520103   Igarapava                    2   3550308   São Paulo                    1

## PDF page 125

3520202   Igaratá                1   3550407   São Pedro                1
3520301   Iguape                 4   3550506   São Pedro do Turvo       5
3520400   Ilhabela               1   3550605   São Roque                3
3520426   Ilha Comprida          5   3550704   São Sebastião            1
3520442   Ilha Solteira          3   3550803   São Sebastião da Grama   4
3520509   Indaiatuba             4   3550902   São Simão                2
3520608   Indiana                3   3551009   São Vicente              1
3520707   Indiaporã              1   3551108   Sarapuí                  4
3520806   Inúbia Paulista        1   3551207   Sarutaiá                 4
3520905   Ipaussu                2   3551306   Sebastianópolis do Sul   2
3521002   Iperó                  3   3551405   Serra Azul               2
3521101   Ipeúna                 2   3551504   Serrana                  1
3521150   Ipiguá                 2   3551603   Serra Negra              3
3521200   Iporanga               2   3551702   Sertãozinho              1
3521309   Ipuã                   4   3551801   Sete Barras              2
3521408   Iracemápolis           1   3551900   Severínia                1
3521507   Irapuã                 4   3552007   Silveiras                1
3521606   Irapuru                2   3552106   Socorro                  5
3521705   Itaberá                5   3552205   Sorocaba                 4
3521804   Itaí                   5   3552304   Sud Mennucci             4
3521903   Itajobi                2   3552403   Sumaré                   5
3522000   Itaju                  1   3552502   Suzano                   1
3522109   Itanhaém               1   3552551   Suzanápolis              4
3522158   Itaoca                 2   3552601   Tabapuã                  1
3522208   Itapecerica da Serra   1   3552700   Tabatinga                2
3522307   Itapetininga           5   3552809   Taboão da Serra          1
3522406   Itapeva                5   3552908   Taciba                   3
3522505   Itapevi                1   3553005   Taguaí                   4
3522604   Itapira                4   3553104   Taiaçu                   2
3522653   Itapirapuã Paulista    2   3553203   Taiúva                   3
3522703   Itápolis               4   3553302   Tambaú                   5
3522802   Itaporanga             5   3553401   Tanabi                   2
3522901   Itapuí                 1   3553500   Tapiraí                  1
3523008   Itapura                4   3553609   Tapiratiba               3
3523107   Itaquaquecetuba        1   3553658   Taquaral                 1
3523206   Itararé                5   3553708   Taquaritinga             3
3523305   Itariri                1   3553807   Taquarituba              5
3523404   Itatiba                2   3553856   Taquarivaí               5
3523503   Itatinga               3   3553906   Tarabai                  3
3523602   Itirapina              1   3553955   Tarumã                   3
3523701   Itirapuã               2   3554003   Tatuí                    5
3523800   Itobi                  5   3554102   Taubaté                  4
3523909   Itu                    2   3554201   Tejupá                   4
3524006   Itupeva                2   3554300   Teodoro Sampaio          5
3524105   Ituverava              4   3554409   Terra Roxa               1
3524204   Jaborandi              4   3554508   Tietê                    3
3524303   Jaboticabal            4   3554607   Timburi                  3
3524402   Jacareí                2   3554656   Torre de Pedra           1
3524501   Jaci                   2   3554706   Torrinha                 3
3524600   Jacupiranga            2   3554755   Trabiju                  1
3524709   Jaguariúna             2   3554805   Tremembé                 4
3524808   Jales                  2   3554904   Três Fronteiras          2
3524907   Jambeiro               1   3554953   Tuiuti                   3
3525003   Jandira                1   3555000   Tupã                     5
3525102   Jardinópolis           2   3555109   Tupi Paulista            1
3525201   Jarinu                 3   3555208   Turiúba                  1
3525300   Jaú                    2   3555307   Turmalina                1
3525409   Jeriquara              4   3555356   Ubarana                  3
3525508   Joanópolis             2   3555406   Ubatuba                  1

## PDF page 126

3525607   João Ramalho             3     3555505   Ubirajara                 5
3525706   José Bonifácio           4     3555604   Uchoa                     2
3525805   Júlio Mesquita           3     3555703   União Paulista            1
3525854   Jumirim                  1     3555802   Urânia                    2
3525904   Jundiaí                  2     3555901   Uru                       1
3526001   Junqueirópolis           1     3556008   Urupês                    1
3526100   Juquiá                   1     3556107   Valentim Gentil           2
3526209   Juquitiba                1     3556206   Valinhos                  1
3526308   Lagoinha                 2     3556305   Valparaíso                2
3526407   Laranjal Paulista        3     3556354   Vargem                    3
3526506   Lavínia                  1     3556404   Vargem Grande do Sul      5
3526605   Lavrinhas                1     3556453   Vargem Grande Paulista    1
3526704   Leme                     4     3556503   Várzea Paulista           1
3526803   Lençóis Paulista         1     3556602   Vera Cruz                 1
3526902   Limeira                  3     3556701   Vinhedo                   2
3527009   Lindóia                  1     3556800   Viradouro                 1
3527108   Lins                     2     3556909   Vista Alegre do Alto      1
3527207   Lorena                   3     3556958   Vitória Brasil            1
3527256   Lourdes                  2     3557006   Votorantim                1
3527306   Louveira                 1     3557105   Votuporanga               2
3527405   Lucélia                  1     3557154   Zacarias                  3
3527504   Lucianópolis             4     3557204   Chavantes                 2
3527603   Luís Antônio             1     3557303   Estiva Gerbi              3
3527702   Luiziânia                2     3504701   Balbinos                  1
3527801   Lupércio                 3     3505351   Barra do Chapéu           5
3527900   Lutécia                  5     3505401   Barra do Turvo            1
3528007   Macatuba                 2     3509106   Caiuá                     3
3528106   Macaubal                 1     3517604   Guapiara                  5
3528205   Macedônia                1     3519253   Iaras                     4
3528304   Magda                    1     3519709   Ibiúna                    5
3528403   Mairinque                2     3528700   Marabá Paulista           4
3528502   Mairiporã                1     3531704   Monteiro Lobato           1
3528601   Manduri                  5     3532306   Natividade da Serra       2
3528809   Maracaí                  5     3532843   Nova Canaã Paulista       1
3528858   Marapoama                1     3535606   Paraibuna                 2
3528908   Mariápolis               4     3536802   Pedra Bela                4
3529005   Marília                  5     3537800   Piedade                   4
3529104   Marinópolis              1     3541653   Quadra                    5
3529203   Martinópolis             5     3542800   Ribeira                   2
3529302   Matão                    3     3543253   Ribeirão Grande           4
3529401   Mauá                     1
                                   TOCANTINS
1700251   Abreulândia              2     1714203   Natividade                3
1700301   Aguiarnópolis            1     1714880   Nova Olinda               3
1700350   Aliança do Tocantins     2     1715002   Nova Rosalândia           3
1700400   Almas                    3     1715101   Novo Acordo               2
1700707   Alvorada                 3     1715150   Novo Alegre               2
1701002   Ananás                   2     1715259   Novo Jardim               2
1701051   Angico                   3     1715507   Oliveira de Fátima        2
1701101   Aparecida do Rio Negro   4     1715754   Palmeirópolis             2
1702000   Araguaçu                 3     1716109   Paraíso do Tocantins      3
1702109   Araguaína                4     1716307   Pau D'Arco                2
1702158   Araguanã                 2     1716505   Pedro Afonso              4
1702208   Araguatins               3     1716604   Peixe                     4
1702307   Arapoema                 2     1716703   Colméia                   2
1702406   Arraias                  4     1717008   Pindorama do Tocantins    3
1702554   Augustinópolis           1     1717503   Pium                      5
1702703   Aurora do Tocantins      2     1717800   Ponte Alta do Bom Jesus   3
1702901   Axixá do Tocantins       2     1717909   Ponte Alta do Tocantins   3

## PDF page 127

1703057   Bandeirantes do Tocantins   2   1718006   Porto Alegre do Tocantins    2
1703073   Barra do Ouro               3   1718204   Porto Nacional               4
1703107   Barrolândia                 1   1718303   Praia Norte                  2
1703206   Bernardo Sayão              2   1718402   Presidente Kennedy           2
1703305   Bom Jesus do Tocantins      3   1718451   Pugmil                       2
1703602   Brasilândia do Tocantins    2   1718501   Recursolândia                2
1703701   Brejinho de Nazaré          3   1718659   Rio da Conceição             2
1703800   Buriti do Tocantins         1   1718808   Sampaio                      1
1703826   Cachoeirinha                2   1718840   Sandolândia                  2
1703842   Campos Lindos               5   1718865   Santa Fé do Araguaia         4
1703867   Cariri do Tocantins         3   1718881   Santa Maria do Tocantins     3
1703883   Carmolândia                 2   1718907   Santa Rosa do Tocantins      3
1703891   Carrasco Bonito             1   1719004   Santa Tereza do Tocantins    2
1703909   Caseara                     4   1720002   Santa Terezinha do           1
                                                    Tocantins
1704105   Centenário                  3   1720101   São Bento do Tocantins       3
1704600   Chapada de Areia            1   1720150   São Félix do Tocantins       1
1705102   Chapada da Natividade       3   1720259   São Salvador do Tocantins    2
1705508   Colinas do Tocantins        2   1720309   São Sebastião do Tocantins   1
1705557   Combinado                   3   1720499   São Valério                  3
1705607   Conceição do Tocantins      2   1720655   Silvanópolis                 4
1706100   Cristalândia                4   1720804   Sítio Novo do Tocantins      1
1706258   Crixás do Tocantins         4   1720853   Sucupira                     3
1706506   Darcinópolis                4   1720903   Taguatinga                   4
1707009   Dianópolis                  4   1720937   Taipas do Tocantins          1
1707108   Divinópolis do Tocantins    3   1720978   Talismã                      2
1707306   Dueré                       5   1721000   Palmas                       4
1707405   Esperantina                 2   1721208   Tocantinópolis               2
1707553   Fátima                      3   1721257   Tupirama                     2
1707652   Figueirópolis               3   1721307   Tupiratins                   2
1707702   Filadélfia                  3   1722081   Wanderlândia                 4
1708205   Formoso do Araguaia         5   1722107   Xambioá                      3
1708254   Fortaleza do Tabocão        2   1701309   Aragominas                   3
1708304   Goianorte                   2   1701903   Araguacema                   4
1709302   Guaraí                      3   1703008   Babaçulândia                 3
1709500   Gurupi                      3   1706001   Couto Magalhães              3
1709807   Ipueiras                    2   1707207   Dois Irmãos do Tocantins     3
1710508   Itacajá                     3   1709005   Goiatins                     5
1710706   Itaguatins                  2   1711506   Jaú do Tocantins             3
1710904   Itapiratins                 3   1711803   Juarina                      2
1711100   Itaporã do Tocantins        2   1713601   Monte do Carmo               4
1711902   Lagoa da Confusão           5   1713700   Monte Santo do Tocantins     2
1711951   Lagoa do Tocantins          2   1714302   Nazaré                       2
1712009   Lajeado                     2   1715705   Palmeirante                  3
1712157   Lavandeira                  2   1716208   Paranã                       2
1712405   Lizarda                     3   1716653   Pequizeiro                   2
1712454   Luzinópolis                 2   1717206   Piraquê                      3
1712504   Marianópolis do Tocantins   3   1718550   Riachinho                    2
1712702   Mateiros                    4   1718709   Rio dos Bois                 2
1712801   Maurilândia do Tocantins    2   1718758   Rio Sono                     2
1713205   Miracema do Tocantins       4   1718899   Santa Rita do Tocantins      5
1713304   Miranorte                   3   1720200   São Miguel do Tocantins      1
1713809   Palmeiras do Tocantins      2   1721109   Tocantínia                   2
1713957   Muricilândia                2

## PDF page 128

APÊNDICE C – Tratamentos/procedimentos matemáticos aplicados aos indicadores simples dos Subsetores Disponibilidade
de Alimentos e Acesso e Consumo de Alimentos.

Tabela 9 – Tratamentos/procedimentos matemáticos aplicados nos indicadores selecionados do Subsetor Disponibilidade de Alimentos para Seca.
                                                 Categoria do                   Logaritmo
          INDICADORES SIMPLES                                   Winsorization                  BoxCox       Normalização       Máscara
                                                    dado                        Neperiano
Baixa produtividade agrícola                      Numérico

Baixa produtividade pecuária                      Numérico

Homogeneidade da produção agrícola local          Numérico

Agricultura sem práticas agrícolas                Numérico
sustentáveis

Dependência da irrigação em grande escala         Numérico

Focos de calor em áreas agropecuárias             Numérico

Distância da agropecuária em relação à            Numérico
disponibilidade hídrica

Áreas agropecuárias com baixo potencial           Numérico
agrícola no município

Áreas agropecuarias com solo susceptível a        Numérico
erosão no município

Déficit hídrico no solo em áreas agropecuarias    Numérico

Perdas de cobertura natural e vegetal no          Numérico
município

Investimento em políticas agrárias e de gestão    Numérico
ambiental

Cobertura do Programa Garantia Safra              Numérico

Cobertura do Programa de Fortalecimento da
                                                  Numérico
Agricultura Familiar (PRONAF)

## PDF page 129

                                              Categoria do                   Logaritmo
          INDICADORES SIMPLES                                Winsorization               BoxCox   Normalização   Máscara
                                                 dado                        Neperiano
Cobertura do Programa Cisternas                Numérico

Cobertura do Proagro Mais                      Numérico

Cobertura do PSR                               Numérico

Nível de orientação técnica                    Numérico

Nível de associativismo                        Numérico

Propriedade da terra                           Numérico

Redução de conflitos agrários                  Numérico

Capacidade de armazenamento dos armazéns       Numérico

Proximidade dos armazéns às áreas
                                               Numérico
agropecuárias

Diversidade de receitas da produção
                                               Numérico
agropecuária

Áreas prioritárias para intensificação da
                                               Numérico
pecuária

Potencial de conversão de pastagem
                                               Numérico
degradada

Participação da agropecuária na economia do
                                               Numérico
município

Área plantada com culturas agrícolas
                                               Numérico
alimentares

Área dos estabelecimentos agropecuários com
                                               Numérico
atividade pecuária

Estabelecimentos agropecuários com
                                               Numérico
agricultura familiar

## PDF page 130

                                              Categoria do                   Logaritmo
          INDICADORES SIMPLES                                Winsorization               BoxCox   Normalização   Máscara
                                                 dado                        Neperiano
Densidade de estabelecimentos agropecuários    Numérico

Dias consecutivos secos                        Numérico

Índice de precipitação-evapotranspiração
                                               Numérico
padronizado

## PDF page 131

Tabela 10 – Tratamentos/procedimentos matemáticos aplicados nos indicadores selecionados do Subsetor Acesso e Consumo de Alimentos.
                                                                Categoria do   Conversão de
                   INDICADORES SIMPLES                                                        Winsorization   BoxCox    Normalização
                                                                   dado          escalas
 Densidade média de moradores por domicílio                      Numérico

 Mães chefes de família, sem fundamental completo e de baixa
                                                                 Numérico
 renda

 População economicamente dependente                             Numérico

 População com risco de desabastecimento de água por fonte
                                                                 Numérico
 direta

 Água com qualidade comprometida expressa pela concentração
                                                                 Numérico
 da Demanda Bioquímica de Oxigênio (DBO)

 Densidade de estabelecimentos comerciais de alimentos
                                                                 Numérico
 ultraprocessados por 10.000 habitantes

 Municípios sem rede de abastecimento de alimentos que
                                                                 Numérico
 compõem a cesta básica

 Nível de insegurança alimentar e nutricional                      Score

 Proporção de crianças menores de 2 anos desnutridas             Numérico

 Ocorrência de doenças relacionadas ao saneamento ambiental
                                                                 Numérico
 inadequado

 Nível de sobrepeso e obesidade da população                     Numérico

 Investimento federal per capita em políticas de educação,
                                                                 Numérico
 saúde e infraestrutura para adaptação

 Instrumentos de planejamento e gestão da segurança alimentar      Score

 Cobertura do Programa de Abrangência do programa nacional
                                                                 Numérico
 de alimentação escolar (PNAE)

## PDF page 132

                                                              Categoria do   Conversão de
                   INDICADORES SIMPLES                                                      Winsorization   BoxCox   Normalização
                                                                 dado          escalas
Nível de atendimento à população das unidades receptoras do
PAA nos territórios com maior susceptibilidade ambiental e     Numérico
sanitária às mudanças climáticas

Fornecedores do PAA classificadas como “povos e comunidades
                                                               Numérico
tradicionais”

Nível de atendimento do programa cisternas (P1MC - consumo)    Numérico

Abrangência do programa bolsa família                          Numérico

Igualdade na distribuição de renda intra-domiciliar            Numérico

Domicílios com renda per capita superior a cinco salários
                                                               Numérico
mínimos

Densidade populacional                                         Numérico

População total                                                Numérico
