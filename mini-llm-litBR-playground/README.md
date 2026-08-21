# 🧠 Mini-LLM Playground - Aprendizado Profundo de Linguagem

Um playground web interativo e educacional para desmistificar o funcionamento interno de **Modelos de Linguagem (LLMs)** e **Redes Neurais Recorrentes (LSTMs)** a partir do experimento do notebook `13-mini-llm-poucos-textos.ipynb`.

---

## 🌟 Principais Funcionalidades Didáticas

1. **Diagrama Gráfico Animado da Arquitetura Neural**:
   - Visualização do fluxo de dados: **Tokenização por Caractere $\rightarrow$ Lookup de Embedding ($d=16$) $\rightarrow$ Célula Recorrente LSTM $\rightarrow$ Camada Densa & Softmax com Temperatura ($\tau$)**.
   - Exibição em tempo real do estado das portas da LSTM (**Forget Gate $f_t$**, **Input Gate $i_t$**, **Output Gate $o_t$**, **Cell State $C_t$** e **Hidden State $h_t$**).

2. **Amostragem por Temperatura ($\tau$) Dinâmica**:
   - Slider interativo que recomputa e ajusta o gráfico de barras da distribuição probabilística Softmax em tempo real.
   - Demonstração do efeito da temperatura na amostragem:
     - **$\tau = 0.10$**: Conservador / Determinístico (escolhe sempre o caractere de maior probabilidade).
     - **$\tau = 0.70$**: Equilibrado (padrão didático).
     - **$\tau = 2.00$**: Aleatório / Criativo (achata as probabilidades, gerando maior variabilidade).

3. **Geração de Texto Passo a Passo**:
   - Controle total da geração token por token: botão **+1 Char**, **Gerar Auto** e **Pausar**.
   - Acompanhamento da realimentação do caractere sorteado na entrada para a próxima previsão.

4. **Treinamento Live no Navegador**:
   - Treinamento online via *Backpropagation* e *Gradient Descent* em JavaScript no corpus de texto.
   - Visualização da evolução das métricas de **Perda (Loss)** e **Acurácia** ao longo das épocas.

5. **Tokenizador & Fórmulas Matemáticas**:
   - Tabela interativa com os 36 caracteres únicos do vocabulário e seus respectivos índices numéricos.
   - Equações matemáticas nítidas em **KaTeX**.

---

## 🚀 Como Executar

O projeto é **standalone** em HTML5, JavaScript puro e TailwindCSS CDN:

1. Acesse a pasta `mini-llm-playground`:
   ```
   C:\Users\A57441456\.gemini\antigravity\scratch\mini-llm-playground
   ```
2. Abra o arquivo `index.html` em qualquer navegador web.
3. Ou sirva via servidor local em Python:
   ```bash
   python -m http.server 8080
   ```
   E acesse `http://localhost:8080`.

---

## 📁 Estrutura de Arquivos

```
mini-llm-playground/
├── index.html          # Interface web principal
├── css/
│   └── styles.css      # Estilos e tema dark mode
├── js/
│   ├── lstm_engine.js  # Motor de RNN/LSTM, Embedding, Softmax e Amostragem por Temperatura
│   ├── network_vis.js  # Renderizador em HTML5 Canvas da arquitetura da rede neural
│   ├── charts.js       # Gráficos Chart.js de distribuições e métricas de treino
│   └── app.js          # Controlador principal da aplicação
└── README.md           # Guia didático do projeto
```
