# Análise v5 — Fabio Lima da Silva Ribeiro (`FLSRib`)

**Projeto:** Chatbot de atendimento CRM — classificação de sentimento em tickets
**Repositório:** [FLSRib/NeuralNetwork](https://github.com/FLSRib/NeuralNetwork)
**Pasta analisada:** `chatbot-atendimento-CRM_rev_V5/` (commit `6cdc1c39`, 17/09)
**Nota v1:** 3,0/10 → v2: 7,2/10 → v3: 8,0/10 → v4: 8,3/10 → **Nota v5: 8,7/10**

---

## 1. Abertura

Fabio, os 3 pontos não-bloqueantes que deixei na v4 foram resolvidos integralmente, e o primeiro deles com um rigor que foi além do que eu pedi. Reexecutei o pipeline 4 vezes, em ambientes independentes, para confirmar.

## 2. Os 3 pedidos da v4 — verificação item a item

| # | Pedido da v4 | Situação na v5 |
|---|---|---|
| 1 | Documentar no README a limitação de reprodutibilidade cross-máquina | **Corrigido, além do pedido.** Nova seção 5.1 traz a tabela Windows vs. macOS com fundamentação técnica correta (não-convexidade do Adam, diferenças de acumulação de ponto flutuante entre BLAS/LAPACK, não-associatividade IEEE754), e explica por que os pesos congelados em `model_weights_v5.json`/`playground.html` não sofrem dessa divergência. É tratamento científico completo, não uma frase de aviso. |
| 2 | Guard `if __name__ == "__main__":` em `generate_rev_v5_artifacts.py` | **Corrigido.** Confirmado na linha 486 — toda a lógica de treino está dentro de `main()`; importar o módulo não dispara retreino. |
| 3 | Remover paths absolutos do Windows pessoal | **Corrigido.** Busca por `C:\Users`/`fribeiro` em toda a pasta não retornou ocorrência; agora usa `pathlib.Path(__file__).resolve().parent`. |

## 3. Reexecução independente — 4x, bit-idêntico

Rodei o pipeline completo (script e notebook via `nbconvert --execute`) 4 vezes em ambientes totalmente novos (clone fresco + venv nova a cada vez). As 4 execuções deram resultado **bit-idêntico**: teste MLP 76,08%, LR 74,90%; CV 5-fold GroupKFold MLP 81,95% (σ=0,0556), LR 81,03% (σ=0,0566). Isso reproduz exatamente a faixa que eu já tinha relatado para macOS na v4, e confirma que a reprodutibilidade *intra-máquina* agora é sólida.

## 4. Vazamentos históricos e teste de estresse — sem regressão

Confirmei diretamente no código: split por frase-base com `assert` de zero sobreposição (ativo), `TfidfVectorizer` dentro de `Pipeline`+`GroupKFold` (ativo, idêntico ao padrão aprovado desde a v3). O treino auxiliar novo em `chatbot_tickets.py` (para a demo interativa) usa holdout simples sem CV — não reintroduz o vazamento antigo. O teste de estresse no README continua reportando os 7 casos completos, sem omissão seletiva.

## 5. Achado novo — a divergência cross-máquina também aparece no nível de caso individual

Um ponto que sua nova seção 5.1 não cobre: a divergência entre Windows e macOS que você documentou no nível agregado (acurácia/desvio) também aparece no teste de estresse, caso a caso. Reexecutando os 7 casos no macOS, 2 vereditos se invertem frente à sua tabela (gerada no Windows):

- Caso 2 ("atendimento bom, mas link instável"): seu README acerta (NEGATIVO 80,7%); minha reexecução erra (POSITIVO 95,0%).
- Caso 4 ("checar latência no roteador core"): seu README erra (NEGATIVO 36,5%); minha reexecução acerta (NEUTRO 82,1%).

A contagem agregada ("3 acertos, 4 erros") se mantém nas duas plataformas — mas os casos específicos que sustentam sua narrativa de negócio ("o modelo acerta onde importa: mensagem mista") não são robustos entre máquinas. Não é um problema de honestidade (os 7 casos seguem todos reportados), é uma extensão natural do próprio ponto que você já documentou — vale uma nota de rodapé numa eventual v6.

Também vale registrar, para deixar claro: os números "de auditoria macOS" que sua seção 5.1 cita são os que eu relatei na v4 — você não rodou em macOS, documentou corretamente o que já tinha sido relatado. Isso é o comportamento certo, só quero que fique explícito que não é uma segunda fonte independente.

## 6. Nota final

**8,7 / 10** *(v4: 8,3/10)* — os 3 pedidos foram resolvidos com evidência sólida em código (não só alegação no README), sem nenhuma regressão nos vazamentos históricos ou no teste de estresse, e o tratamento da reprodutibilidade foi exemplar. A alta é modesta porque a v5 é essencialmente consolidação de engenharia (guard, paths, empacotamento) — não há avanço metodológico novo além do que já era pedido, e o achado do item 5 (divergência de caso individual) fica em aberto, ainda que fora do escopo pedido.

Não há pedido obrigatório para uma v6. Se quiser fechar o ciclo, o único ponto que valeria endereçar é reconhecer no README que a robustez do teste de estresse caso-a-caso também varia entre máquinas, não só a métrica agregada.
