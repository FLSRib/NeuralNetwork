# 🔗 Projeto SNA — FGV MBA | Escopo do Trabalho em Grupo

## Pergunta Central

> **Quão vulnerável é a cadeia de suprimento de insumos químicos do agro e da indústria brasileira a interrupções no Mar Negro, no Estreito de Ormuz e no Mar Vermelho — e onde está o risco estrutural escondido?**

---

## Contexto

O Brasil depende de importações para parcela relevante do abastecimento de insumos do agro e da indústria química. Esses fluxos utilizam **redes marítimas** sujeitas a riscos geopolíticos, especialmente em três corredores críticos:

- 🌊 **Mar Negro** — portos ucranianos (Mariupol, Odessa, etc.)
- 🛢️ **Estreito de Ormuz** — passagem do Golfo Pérsico
- 🚢 **Mar Vermelho** — rota entre Ásia/Europa via Canal de Suez

---

## Cliente / Decisor de Referência

Diretoria de suprimentos de uma **trading de insumos** ou de uma **cooperativa agrícola**.

**Pergunta prática:** quais insumos e quais portos, se indisponíveis, ampliam o risco de abastecimento?

---

## Por que Análise de Redes (SNA)?

Uma lista de fornecedores não evidencia concentração estrutural e dependências compartilhadas. As redes permitem:

| Rede | Utilidade |
|------|-----------|
| **One-Mode** | Examinar conectividade, centralidade e perda de alternativas portuárias |
| **Two-Mode** | Relacionar portos × insumos e calcular exposição de cada produto |

> As duas redes são dimensões complementares — suas arestas **não** possuem o mesmo significado.

---

## Modelagem

### Camadas do Modelo

| Camada | Definição | Pergunta respondida |
|--------|-----------|---------------------|
| **One-Mode — baseline** | 39 portos em matriz binária, simétrica e não direcionada | Como a rede está estruturada antes do cenário de estresse? |
| **Cenário de estresse** | 9 nós exclusivos retirados; permanecem 30 portos | O que representa a redução de 39 → 30 alternativas? |
| **Two-Mode — atual** | 30 portos × 21 insumos; aresta = associação porto–insumo | Quais insumos têm maior dependência de portos expostos? |

### Redução Modelada

| Baseline | Cenário atual | Redução |
|----------|--------------|---------|
| 39 portos | 30 portos | **23,1%** dos nós |

### 9 Portos Exclusivos do Baseline (retirados no cenário de estresse)

> Todos são portos ucranianos no Mar Negro

1. Mariupol
2. Berdyansk
3. Kherson
4. Skadovsk
5. Mykolaiv
6. Olvia
7. Chornomorsk
8. Pivdennyi
9. Bilhorod-Dnistrovskyi

### Fórmula de Exposição (Two-Mode)

$$\text{Exposição do insumo} = \frac{\text{portos associados e classificados como expostos}}{\text{total de portos associados ao insumo}}$$

---

## Achados Principais (Two-Mode)

| Insumo | Exposição |
|--------|-----------|
| Metanol | 54,5% |
| Etilenoglicol | 50,0% |
| Atrazina | 50,0% |
| Mancozebe | 50,0% |
| MAP | 45,0% |
| Ureia | 38,5% |
| KCl | 37,0% |

> **KCl** e **Ureia** têm os maiores graus (27 e 26 portos associados, respectivamente).

### Risco Estrutural Escondido

**Atrazina** e **Mancozebe** são exemplos notáveis: apesar de hipóteses iniciais de baixa exposição, a matriz os conecta a **50% de portos expostos**.

---

## Interpretação

O modelo evidencia **duas formas complementares de vulnerabilidade**:

1. **Perda de alternativas logísticas** — passagem de 39 → 30 portos
2. **Concentração da exposição por insumo** — observada na rede bipartida

---

## Recomendações

- ✅ Validar com dados do **MDIC/ComexStat** os volumes, valores e origens reais
- ✅ Ponderar arestas por toneladas, valor importado, frequência, lead time e capacidade portuária
- ✅ Avaliar diversificação de rotas para insumos com grau elevado + exposição relevante
- ✅ Definir **estoque estratégico** por criticidade, substituibilidade e tempo de reposição
- ✅ Monitorar portos de maior centralidade como pontos sensíveis

---

## Limitações e Disclaimer

> [!IMPORTANT]
> Este estudo é **acadêmico e ilustrativo**. As matrizes são binárias e **não incorporam** volume transportado, valor comercial, frequência de embarques, capacidade portuária ou substituibilidade dos insumos.

- "Porto associado" ≠ fornecedor econômico real
- 0% de exposição do sulfato de potássio no modelo ≠ capacidade de substituir outros fertilizantes
- Afirmações sobre itinerários marítimos devem ser validadas com dados observados

---

## Arquivos do Projeto

| Arquivo | Conteúdo |
|---------|----------|
| `business_atualizado_V2.docx` | Roteiro e escopo (este documento) |
| `grafo_one_mode_v2.png` | Visualização da rede One-Mode |
| `grafo_two_mode_v2.png` | Visualização da rede Two-Mode |
| `Projeto_SNA_atributos_produtos_portos_v2.xlsx` | Atributos dos produtos e portos |
| `Rede One Mode_Tarefa em Grupo_Paulista T16_v2.xlsx` | Matriz One-Mode (dados) |
| `Rede Two Mode_Tarefa em Grupo_Paulista T16_v2.xlsx` | Matriz Two-Mode (dados) |
| `Rede_One_Mode_V2.xlsx` | Rede One-Mode alternativa |
| `Rede_Projeto_SNA_v2.xlsx` | Dados principais da rede SNA |
