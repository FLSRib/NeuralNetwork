# 📊 Métricas SNA — Projeto FGV MBA

## 1. Rede One-Mode — Comparativo Baseline vs. Cenário de Estresse

| Métrica | Baseline (39 portos) | Estresse (30 portos) | Variação |
|---------|---------------------|---------------------|----------|
| **Nós** | 39 | 30 | −23,1% |
| **Arestas** | 332 | 213 | −35,8% |
| **Densidade** | 0,4480 | 0,4897 | ▲ +9,3% |
| **Componentes** | 1 | 1 | = |
| **Diâmetro** | 3 | 2 | ▼ −1 |
| **Caminho médio** | 1,556 | 1,510 | ▼ −3,0% |
| **Clustering médio** | 0,5314 | 0,5390 | ▲ +1,4% |

> [!NOTE]
> Paradoxo aparente: remover 9 nós **aumentou** densidade e clustering. Isso ocorre porque os nós removidos (portos ucranianos) possuíam muitas conexões internas entre si — ao retirá-los, a rede remanescente fica mais coesa proporcionalmente. O diâmetro reduzido de 3 → 2 indica que **qualquer par de portos remanescentes está a no máximo 2 passos de distância**.

---

## 2. Centralidades — Rede One-Mode Baseline (39 portos)

### 2.1 Degree (Grau) — Quantidade de conexões diretas

| # | Porto | Grau |
|---|-------|------|
| 1 | **Pivdennyi** | 31 |
| 2 | **Bilhorod-Dnistrovskyi** | 29 |
| 3 | Mesaieed | 25 |
| 4 | Antuérpia | 24 |
| 5 | Antofagasta | 24 |
| 6 | **Mariupol** | 24 |
| 7 | Qingdao | 23 |
| 8 | Tianjin | 23 |
| 9 | Jorf Lasfar | 23 |
| 10 | **Berdyansk** | 23 |

> [!IMPORTANT]
> 4 dos 10 nós mais conectados do baseline são portos ucranianos (em **negrito**) — reforçando o impacto estrutural de sua remoção.

### 2.2 Betweenness Centrality — Intermediação (controle de fluxo)

| # | Porto | Betweenness |
|---|-------|------------|
| 1 | **Pivdennyi** | 0,0971 |
| 2 | **Bilhorod-Dnistrovskyi** | 0,0593 |
| 3 | **Berdyansk** | 0,0517 |
| 4 | **Mariupol** | 0,0396 |
| 5 | Jorf Lasfar | 0,0314 |
| 6 | Antofagasta | 0,0302 |
| 7 | Qingdao | 0,0278 |
| 8 | Mesaieed | 0,0261 |
| 9 | Antuérpia | 0,0248 |
| 10 | Callao | 0,0176 |

> 4 dos 5 maiores intermediadores eram portos ucranianos — a rede perdia mais de **50% do poder de intermediação** dos seus hubs com a remoção.

### 2.3 Closeness Centrality — Proximidade à rede toda

| # | Porto | Closeness |
|---|-------|----------|
| 1 | **Pivdennyi** | 0,8444 |
| 2 | **Bilhorod-Dnistrovskyi** | 0,8085 |
| 3 | Mesaieed | 0,7451 |
| 4 | Antuérpia | 0,7308 |
| 5 | Antofagasta | 0,7308 |
| 6 | Qingdao | 0,7170 |
| 7 | Tianjin | 0,7170 |
| 8 | **Mariupol** | 0,7170 |
| 9 | **Berdyansk** | 0,7170 |
| 10 | Houston | 0,7037 |

### 2.4 Eigenvector Centrality — Prestígio (conectado a nós importantes)

| # | Porto | Eigenvector |
|---|-------|------------|
| 1 | **Pivdennyi** | 0,2343 |
| 2 | **Bilhorod-Dnistrovskyi** | 0,2291 |
| 3 | Mesaieed | 0,2155 |
| 4 | Tianjin | 0,2102 |
| 5 | Antuérpia | 0,2055 |
| 6 | Ras Al-Khair | 0,2029 |
| 7 | Xangai | 0,1994 |
| 8 | Antofagasta | 0,1941 |
| 9 | Callao | 0,1923 |
| 10 | Houston | 0,1922 |

---

## 3. Cenário de Estresse — Novos Hubs (30 portos)

Com a remoção dos 9 portos ucranianos, os **novos líderes** de centralidade são:

| # | Porto (Degree) | Grau | Porto (Betweenness) | B.C. |
|---|----------------|------|---------------------|------|
| 1 | Callao | 20 | Jorf Lasfar | 0,0508 |
| 2 | Antuérpia | 20 | Callao | 0,0431 |
| 3 | Mesaieed | 20 | Antuérpia | 0,0418 |
| 4 | Antofagasta | 20 | Mesaieed | 0,0418 |
| 5 | Jorf Lasfar | 20 | Antofagasta | 0,0392 |

> [!TIP]
> **Jorf Lasfar** (Marrocos) emerge como o principal intermediador no cenário de estresse — porto especializado em fertilizantes fosfatados. Isso é especialmente relevante dado o perfil de insumos críticos do agro brasileiro.

---

## 4. Rede Two-Mode — Portos e Insumos

### 4.1 Portos com maior conectividade a insumos

| # | Porto | Insumos conectados |
|---|-------|--------------------|
| 1 | Qingdao | 17 |
| 2 | Houston | 15 |
| 3 | Xangai | 15 |
| 4 | Roterdã | 15 |
| 5 | Jubail | 14 |
| 6 | Novorossiysk | 13 |
| 7 | Ningbo | 12 |
| 8 | Antuérpia | 12 |
| 9 | Jorf Lasfar | 12 |
| 10 | Vancouver | 11 |

### 4.2 Insumos com maior conectividade a portos

| # | Insumo | Portos associados |
|---|--------|-----------------|
| 1 | Cloreto de potássio (KCl) | 27 |
| 2 | Ureia | 26 |
| 3 | Sulfato de amônio | 20 |
| 4 | MAP (fosfato monoamônico) | 20 |
| 5 | Glifosato | 18 |
| 6 | Enxofre | 17 |
| 7 | Superfosfato triplo (TSP) | 16 |
| 8 | Amônia anidra | 16 |
| 9 | Soda cáustica | 16 |
| 10 | DAP (fosfato diamônico) | 15 |

---

## 5. Exposição por Insumo (Two-Mode) — 11 portos expostos

$$\text{Exposição} = \frac{\text{portos expostos associados}}{\text{total de portos associados ao insumo}}$$

| Insumo | Exposição | Portos expostos | Total portos | Risco |
|--------|-----------|-----------------|--------------|-------|
| **Metanol** | **54,5%** | 6 | 11 | 🔴 Crítico |
| **Etilenoglicol** | **50,0%** | 5 | 10 | 🔴 Crítico |
| **Atrazina** | **50,0%** | 7 | 14 | 🔴 Crítico |
| **Mancozebe** | **50,0%** | 7 | 14 | 🔴 Crítico |
| MAP | 45,0% | 9 | 20 | 🟠 Alto |
| Ureia | 38,5% | 10 | 26 | 🟠 Alto |
| KCl | 37,0% | 10 | 27 | 🟠 Alto |
| Sulfato de amônio | 35,0% | 7 | 20 | 🟠 Alto |
| Ácido fosfórico | 33,3% | 4 | 12 | 🟡 Moderado |
| Amônia anidra | 31,2% | 5 | 16 | 🟡 Moderado |
| Barrilha | 30,8% | 4 | 13 | 🟡 Moderado |
| Enxofre | 29,4% | 5 | 17 | 🟡 Moderado |
| Nitrato de amônio | 28,6% | 2 | 7 | 🟡 Moderado |
| Glifosato | 27,8% | 5 | 18 | 🟡 Moderado |
| DAP | 26,7% | 4 | 15 | 🟡 Moderado |
| Superfosfato triplo (TSP) | 25,0% | 4 | 16 | 🟡 Moderado |
| Ácido sulfúrico | 25,0% | 3 | 12 | 🟡 Moderado |
| Soda cáustica | 18,8% | 3 | 16 | 🟢 Baixo |
| Dióxido de titânio | 15,4% | 2 | 13 | 🟢 Baixo |
| 2,4-D | 14,3% | 1 | 7 | 🟢 Baixo |
| **Sulfato de potássio** | **0,0%** | 0 | 6 | ✅ Sem exposição |

---

## 6. Síntese Analítica para a Apresentação

### Insights principais

1. **Dominância ucraniana no baseline:** Pivdennyi e Bilhorod-Dnistrovskyi lideravam todas as métricas de centralidade — grau, betweenness, closeness e eigenvector simultaneamente.

2. **Resiliência estrutural paradoxal:** Após o estresse, a rede ficou **mais densa** (0,45 → 0,49) e com **menor diâmetro** (3 → 2), mas com **35,8% menos arestas absolutas**. A rede sobrevive, mas com menos alternativas totais.

3. **Risco escondido:** Atrazina e Mancozebe apresentam apenas 14 portos associados cada — grau menor que KCl (27) e Ureia (26) — mas **50% desses portos estão expostos**, superando produtos com grau alto.

4. **Emergência de Jorf Lasfar:** No cenário de estresse, o porto marroquino passa a ser o principal intermediador da rede, evidenciando a dependência crescente dos fertilizantes fosfatados africanos.

5. **Qingdao como hub two-mode:** Com 17 insumos associados, é o porto de maior versatilidade na rede bipartida — ponto único de atenção para diversificação.

---

## 7. Métricas adicionais sugeridas para enriquecer o trabalho

| Métrica | Relevância | Status |
|---------|-----------|--------|
| Degree, Betweenness, Closeness, Eigenvector | Centralidades básicas | ✅ Calculado |
| Clustering coefficient | Coesão local | ✅ Calculado |
| Average path length | Eficiência global | ✅ Calculado |
| Network density | Conectividade geral | ✅ Calculado |
| Índice de resiliência (Δ métricas baseline→estresse) | Impacto do choque | ✅ Calculado |
| Bipartite projection (co-ocorrência entre insumos) | Insumos que compartilham portos | 🔜 Possível |
| Análise de componentes após remoção incremental | Ponto de colapso da rede | 🔜 Possível |
| K-core decomposition | Núcleo mais robusto da rede | 🔜 Possível |
