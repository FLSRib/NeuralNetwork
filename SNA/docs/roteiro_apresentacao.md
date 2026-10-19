# 🎤 Roteiro de Apresentação — Projeto SNA | FGV MBA

---

## ⚠️ Parte 1 — Avaliação de Gaps das Matrizes Fixas

> [!IMPORTANT]
> As matrizes de adjacência foram construídas manualmente (fixas, binárias). Antes de apresentar, é importante saber quais conceitos de SNA ficam **plenamente suportados**, quais requerem **cuidado na fala** e quais são **inaplicáveis**.

### Mapa de Gaps

| # | Conceito SNA | Status | Avaliação |
|---|-------------|--------|-----------|
| 1 | **Grau (Degree)** | ✅ Pleno | Válido. Conta conexões diretas na matriz — exatamente o que foi construído. |
| 2 | **Densidade** | ✅ Pleno | Válido. Razão entre arestas existentes e possíveis — independe de pesos. |
| 3 | **Componentes / Conectividade** | ✅ Pleno | Válido e revelador: a remoção incremental fragmentou a rede em **até 3 componentes**. |
| 4 | **Betweenness Centrality** | ⚠️ Cuidado | Calculável, mas assume que fluxos reais seguem caminhos mínimos na rede. Como a rede é construída e não observada, a betweenness é um **proxy estrutural**, não uma medida de fluxo real. |
| 5 | **Closeness / Eigenvector** | ⚠️ Cuidado | Válidos como indicadores relativos de posição na rede construída. Não representam distâncias geográficas ou logísticas reais. |
| 6 | **Clustering Coefficient** | ⚠️ Cuidado | O alto clustering (0,53) pode ser **artefato da construção**: se o critério de ligação porto-porto foi baseado em rotas similares, grupos coesos surgem naturalmente. Não indica triângulos "orgânicos". |
| 7 | **Exposição por insumo (Two-Mode)** | ✅ Pleno | Conceito central do trabalho. Dado que a binarização é intencional e a classificação de portos expostos é externa ao modelo, o cálculo é válido no cen ário modelado. |
| 8 | **K-core decomposition** | ✅ Bônus | Revelou que Kherson e Skadovsk têm k=3 (periferia extrema), enquanto 28 portos estão no k=13. Isso confirma que os 9 portos removidos **não eram todos igualmente centrais** — apenas Pivdennyi e Bilhorod-Dnistrovskyi eram realmente estruturais. |

---

### Gaps Críticos — Como Tratar na Apresentação

> [!WARNING]
> **GAP 1 — Fragmentação temporária:** A remoção incremental mostrou que, ao retirar Berdyansk (3º porto por betweenness), a rede se fragmenta em **3 componentes** antes de Mariupol e Chornomorsk. No estado final (30 portos), a rede volta a ser conectada porque Kherson e Skadovsk (k=3, periferia) funcionavam como "pontes locais" entre os nós ucranianos. A narrativa "a rede sobrevive como um único componente" é verdadeira no estado final, mas **omite a fragmentação intermediária**.

> [!WARNING]
> **GAP 2 — Betweenness vs. criticidade real:** Afirmar que Pivdennyi "controla fluxos" é impreciso para uma rede construída. O correto é dizer que Pivdennyi ocupa a **posição estrutural** de maior intermediação *no modelo* — o que sugere, mas não confirma, que seria o ponto mais crítico numa rede real.

> [!NOTE]
> **GAP 3 — Clustering:** O coeficiente de clustering elevado (0,53 baseline → 0,54 estresse) é mencionável como sinal de coesão, mas não deve ser central no argumento. Dizer "a rede é coesa" basta; evitar afirmar que isso deriva de comportamento orgânico dos portos.

### Veredicto geral

> ✅ **Os gaps são aceitáveis para um trabalho de MBA.** O documento já tem disclaimer explícito e bem redigido. As limitações mais relevantes (betweenness como proxy, fragmentação intermediária) podem ser incorporadas naturalmente ao roteiro sem enfraquecer a argumentação — pelo contrário, demonstram maturidade analítica.

---

---

## 🎬 Parte 2 — Roteiro de Apresentação

> **Duração sugerida:** 15–20 minutos + perguntas  
> **Estrutura:** 10 slides  
> **Público:** Banca acadêmica de MBA

---

### SLIDE 1 — Abertura (1 min)

**Título:** Vulnerabilidade da Cadeia de Suprimentos de Insumos Químicos

**Fala sugerida:**
> *"As cadeias brasileiras de insumos químicos dependem de uma rede internacional de portos e corredores marítimos sujeitos a choques geopolíticos. Neste estudo, utilizamos Análise de Redes Sociais para avaliar duas dimensões dessa vulnerabilidade: primeiro, a perda de alternativas logísticas; segundo, a concentração de exposição por insumo. O resultado é um mapa estrutural do risco — não uma previsão, mas uma lente para identificar onde o sistema é mais frágil."*

**Elementos visuais:** Mapa-múndi destacando Mar Negro, Estreito de Ormuz e Mar Vermelho.

---

### SLIDE 2 — Pergunta Central e Contexto (1,5 min)

**Título:** Por que isso importa agora?

**Conteúdo:**
- Pergunta central: *"Quão vulnerável é a cadeia de insumos do agro e da indústria química brasileira a interrupções nos três corredores críticos?"*
- Cliente de referência: diretoria de suprimentos de trading ou cooperativa agrícola
- Pergunta prática: *"Quais insumos e portos, se indisponíveis, ampliam o risco de abastecimento?"*

**Fala sugerida:**
> *"Partimos de uma decisão prática, não de um exercício abstrato. O decisor que nos orienta precisa saber onde concentrar esforços de contingência — e uma lista de fornecedores não responde isso. Uma rede, responde."*

---

### SLIDE 3 — Por que SNA? (2 min)

**Título:** A lista não enxerga o que a rede enxerga

**Conteúdo — tabela comparativa:**

| Abordagem tradicional | Abordagem SNA |
|-----------------------|---------------|
| Lista de fornecedores por insumo | Mapa de dependências compartilhadas |
| Risco individual por fornecedor | Vulnerabilidade estrutural sistêmica |
| Não evidencia concentração | Revela hubs e pontes críticas |
| Não simula choques | Permite cenários de remoção de nós |

**Fala sugerida:**
> *"Uma lista diz 'temos 26 portos para ureia'. Uma rede diz '10 desses 26 estão expostos ao mesmo choque geopolítico, e 3 deles são pontes para os demais'. A diferença é o risco estrutural escondido."*

---

### SLIDE 4 — Modelagem e Camadas (2 min)

**Título:** Duas redes, duas perguntas

**Conteúdo:**

| Camada | Nós | Arestas | Pergunta |
|--------|-----|---------|----------|
| **One-Mode — Baseline** | 39 portos | 332 | Como a rede está estruturada antes do choque? |
| **One-Mode — Estresse** | 30 portos (−23,1%) | 213 (−35,8%) | O que muda com a perda dos 9 portos do Mar Negro? |
| **Two-Mode — Atual** | 30 portos × 21 insumos | — | Quais insumos dependem de portos expostos? |

**Fórmula de exposição:**

$$\text{Exposição} = \frac{\text{portos expostos associados ao insumo}}{\text{total de portos associados ao insumo}}$$

**Fala sugerida:**
> *"Construímos matrizes binárias — conexão existe ou não existe. Essa escolha é intencional: o objetivo é mapear dependência estrutural, não volume de carga. As limitações dessa simplificação estão documentadas e serão retomadas ao final."*

---

### SLIDE 5 — One-Mode: Baseline (2 min)

**Título:** Rede baseline — os hubs que dominam a conectividade

**Conteúdo — métricas globais:**
- Densidade: **0,448** | Diâmetro: **3** | Caminho médio: **1,56** | Clustering: **0,53**

**Top 5 por Betweenness (proxy de criticidade estrutural):**

| Porto | Betweenness | Tipo |
|-------|-------------|------|
| Pivdennyi | 0,097 | 🔴 Ucraniano |
| Bilhorod-Dnistrovskyi | 0,059 | 🔴 Ucraniano |
| Berdyansk | 0,052 | 🔴 Ucraniano |
| Mariupol | 0,040 | 🔴 Ucraniano |
| Jorf Lasfar | 0,031 | 🟡 Marrocos |

**Fala sugerida:**
> *"Quatro dos cinco maiores intermediadores estruturais da rede são portos ucranianos. Isso não é coincidência — é o sinal de que o Mar Negro concentrava posições estruturais críticas, não apenas volume de carga."*

---

### SLIDE 6 — One-Mode: Cenário de Estresse + Achado da Fragmentação (2,5 min)

**Título:** O choque revela mais do que a foto final

**Conteúdo:**

**Foto final (30 portos):**
- Rede permanece conexa — 1 componente
- Densidade **sobe**: 0,448 → 0,490
- Diâmetro **cai**: 3 → 2

**Mas o caminho importa:**

| Remoção (ordem por betweenness) | Componentes |
|----------------------------------|-------------|
| Após −Pivdennyi | 1 ✅ |
| Após −Bilhorod-Dnistrovskyi | 1 ✅ |
| Após −Berdyansk | **2 ⚠️** |
| Após −Mariupol | **3 🔴** |
| Após −Chornomorsk, Olvia, Mykolaiv | **3 🔴** |
| Após −Skadovsk | 2 |
| Após −Kherson (final) | 1 ✅ |

**Fala sugerida:**
> *"A foto final mostra uma rede conectada — e isso é verdade. Mas a remoção sequencial revela que a rede chegou a ter 3 componentes isolados durante o processo. A resiliência final existe porque os últimos nós removidos — Kherson e Skadovsk — eram periféricos e funcionavam como pontes internas entre os portos ucranianos, não entre eles e o restante da rede."*

**Novos líderes no cenário de estresse:**
- **Jorf Lasfar** (Marrocos) assume a maior betweenness: 0,051 — porto especializado em fertilizantes fosfatados.

---

### SLIDE 7 — Two-Mode: Exposição por Insumo (2 min)

**Título:** Onde está o risco escondido?

**Conteúdo — ranking de exposição:**

| Insumo | Exposição | Portos | Risco |
|--------|-----------|--------|-------|
| Metanol | 54,5% | 6/11 | 🔴 |
| Etilenoglicol | 50,0% | 5/10 | 🔴 |
| **Atrazina** | **50,0%** | **7/14** | **🔴 Escondido** |
| **Mancozebe** | **50,0%** | **7/14** | **🔴 Escondido** |
| MAP | 45,0% | 9/20 | 🟠 |
| Ureia | 38,5% | 10/26 | 🟠 |
| KCl | 37,0% | 10/27 | 🟠 |
| Sulfato de potássio | 0,0% | 0/6 | ✅ |

**Fala sugerida:**
> *"KCl e Ureia têm grau altíssimo — 27 e 26 portos associados — mas apenas 37–38% estão expostos. São resilientes pela escala. Atrazina e Mancozebe têm apenas 14 portos cada, mas metade está exposta. São o risco estrutural escondido: aparentemente diversificados, mas concentrados nos corredores críticos."*

---

### SLIDE 8 — Two-Mode: Projeção Bipartida — Dependência Compartilhada (1,5 min)

**Título:** Insumos que falham juntos

**Conteúdo — top pares de insumos que compartilham portos:**

| Par de insumos | Portos em comum |
|----------------|-----------------|
| KCl ↔ Ureia | 24 |
| MAP ↔ KCl | 20 |
| Ureia ↔ Sulfato de amônio | 20 |
| KCl ↔ Sulfato de amônio | 18 |
| MAP ↔ Ureia | 17 |

**Fala sugerida:**
> *"A projeção bipartida mostra quais insumos falham juntos quando um porto é removido. KCl e Ureia compartilham 24 dos mesmos portos — um choque único no Mar Negro ou no Estreito de Ormuz impacta os dois simultaneamente. Isso é risco sistêmico de fertilizantes — não risco individual."*

---

### SLIDE 9 — Recomendações (1,5 min)

**Título:** Da estrutura à decisão

**Conteúdo:**

| Ação | Prioridade | Insumos-alvo |
|------|-----------|--------------|
| Validar com MDIC/ComexStat volumes reais | Alta | Todos |
| Diversificar rotas para insumos com exposição >40% | Alta | Metanol, Etilenoglicol, Atrazina, Mancozebe, MAP |
| Monitorar Jorf Lasfar como hub emergente no estresse | Média | Fertilizantes fosfatados |
| Avaliar estoque estratégico por criticidade + substituibilidade | Alta | KCl, Ureia, MAP |
| Ponderar modelo com toneladas/valor (próxima fase) | Futura | Todos |

---

### SLIDE 10 — Limitações, Disclaimer e Encerramento (1 min)

**Título:** O que o modelo diz — e o que não diz

**Conteúdo:**
- Matrizes binárias: sem pesos por volume, valor ou frequência
- "Porto associado" ≠ fornecedor econômico prioritário
- Betweenness e closeness são proxies estruturais, não medidas de fluxo real
- O cenário de 30 portos é modelado, não histórico

**Fala de encerramento:**
> *"Este estudo não prevê crises — ele mapeia onde a estrutura é frágil. A rede de insumos químicos brasileira é resiliente no estado final, mas o caminho até lá passa por fragmentações. E o risco estrutural escondido — como atrazina e mancozebe — só aparece quando você para de olhar para listas e começa a olhar para redes."*

---

## ⏱️ Cronograma de Apresentação

| Slide | Conteúdo | Tempo |
|-------|----------|-------|
| 1 | Abertura | 1 min |
| 2 | Contexto e pergunta | 1,5 min |
| 3 | Por que SNA | 2 min |
| 4 | Modelagem | 2 min |
| 5 | One-Mode baseline | 2 min |
| 6 | Cenário de estresse + fragmentação | 2,5 min |
| 7 | Two-Mode: exposição | 2 min |
| 8 | Projeção bipartida | 1,5 min |
| 9 | Recomendações | 1,5 min |
| 10 | Limitações + encerramento | 1 min |
| **Total** | | **~17 min** |
