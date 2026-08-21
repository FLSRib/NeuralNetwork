/**
 * Mini-LLM Engine - Motor de Rede Neural Recorrente (LSTM + Embedding + Softmax com Temperatura)
 * Suporta Corpus Expandido e Customizado pelo Usuário.
 */

class MiniLLMEngine {
    constructor(config = {}) {
        this.defaultCorpus = `A inteligencia artificial esta mudando a forma como as empresas tomam decisoes no mundo moderno.
Um modelo de linguagem aprende a prever a proxima palavra ou letra de um texto usando padroes que encontrou durante o treinamento com muitos exemplos de dados.

Bancos e instituicoes financeiras usam modelos de aprendizado de maquina para detectar fraudes em tempo real, analisar risco de credito e identificar padroes de lavagem de dinheiro em grandes volumes de transacoes bancarias.
Lojas e empresas de comercio eletronico usam sistemas de recomendacao para sugerir produtos personalizados que o cliente tem maior probabilidade de comprar, aumentando as vendas e a satisfacao dos consumidores.
Hospitais e clinicas medicas usam visao computacional e redes neurais profundas para ajudar medicos a analisar exames de imagem como radiografias e tomografias com maior precisao.

Um chatbot inteligente de atendimento ao cliente tambem e, no fundo, um modelo de linguagem probabilistico.
Ele recebe a mensagem inicial da pessoa como contexto e gera uma resposta coerente, caractere por caractere ou token por token, tentando prever qual e a sequencia de palavras mais provavel e mais util para resolver o problema do cliente.

As redes neurais profundas utilizam camadas de neuronios artificiais organizadas em arquiteturas como redes convolucionais para imagens e redes recorrentes como LSTMs ou Transformers para sequencias de texto.
Quanto mais dados de alta qualidade um modelo recebe durante a fase de treinamento, e quanto maior for a sua capacidade de parametros, melhor ele consegue captar as nuances da linguagem humana e gerar textos mais fluentes, uteis e adequados para cada negocio.

A inteligencia artificial generativa permite criar novos conteudos, incluindo textos, imagens, codigos de programacao e dados sinteticos para treinamento.
Compreender o funcionamento basico da passagem de mensagens, embeddings e amostragem probabilistica e fundamental para utilizar a IA com eficacia na solucao de problemas reais das empresas.`;

        this.corpus = config.corpus || this.defaultCorpus;
        this.embeddingDim = config.embeddingDim || 16;
        this.hiddenDim = config.hiddenDim || 32;
        this.seqLen = config.seqLen || 20;
        this.learningRate = config.learningRate || 0.05;
        this.temperature = config.temperature || 0.7;

        this.initTokenizer();
        this.initWeights();
    }

    setCustomCorpus(newCorpusText) {
        if (!newCorpusText || newCorpusText.trim().length < 50) return false;
        this.corpus = newCorpusText.trim();
        this.initTokenizer();
        this.initWeights();
        return true;
    }

    initTokenizer() {
        const uniqueChars = Array.from(new Set(this.corpus)).sort();
        this.vocab = uniqueChars;
        this.vocabSize = uniqueChars.length;

        this.char2idx = {};
        this.idx2char = {};

        uniqueChars.forEach((ch, idx) => {
            this.char2idx[ch] = idx;
            this.idx2char[idx] = ch;
        });

        this.trainX = [];
        this.trainY = [];

        for (let i = 0; i <= this.corpus.length - this.seqLen - 1; i++) {
            const seqIn = this.corpus.slice(i, i + this.seqLen);
            const charOut = this.corpus[i + this.seqLen];

            this.trainX.push(seqIn.split('').map(c => this.char2idx[c]));
            this.trainY.push(this.char2idx[charOut]);
        }
    }

    initWeights() {
        const randMat = (r, c, std = 0.2) => {
            const m = [];
            for (let i = 0; i < r; i++) {
                const row = [];
                for (let j = 0; j < c; j++) row.push((Math.random() * 2 - 1) * std);
                m.push(row);
            }
            return m;
        };

        const randVec = (n, val = 0.0) => new Array(n).fill(val);

        this.E = randMat(this.vocabSize, this.embeddingDim);

        const inDim = this.embeddingDim;
        const hDim = this.hiddenDim;

        this.Wf = randMat(hDim, inDim); this.Uf = randMat(hDim, hDim); this.bf = randVec(hDim, 1.0);
        this.Wi = randMat(hDim, inDim); this.Ui = randMat(hDim, hDim); this.bi = randVec(hDim, 0.0);
        this.Wc = randMat(hDim, inDim); this.Uc = randMat(hDim, hDim); this.bc = randVec(hDim, 0.0);
        this.Wo = randMat(hDim, inDim); this.Uo = randMat(hDim, hDim); this.bo = randVec(hDim, 0.0);

        this.Wy = randMat(this.vocabSize, hDim);
        this.by = randVec(this.vocabSize, 0.0);

        this.history = { loss: [], accuracy: [] };
    }

    sigmoid(x) { return 1 / (1 + Math.exp(-Math.max(-15, Math.min(15, x)))); }
    tanh(x) { return Math.tanh(x); }

    lstmStep(x_t, h_prev, c_prev) {
        const hDim = this.hiddenDim;
        const f = new Array(hDim), i = new Array(hDim), c_tilde = new Array(hDim), o = new Array(hDim);
        const c_next = new Array(hDim), h_next = new Array(hDim);

        for (let d = 0; d < hDim; d++) {
            let sumF = this.bf[d], sumI = this.bi[d], sumC = this.bc[d], sumO = this.bo[d];
            for (let j = 0; j < this.embeddingDim; j++) {
                sumF += this.Wf[d][j] * x_t[j];
                sumI += this.Wi[d][j] * x_t[j];
                sumC += this.Wc[d][j] * x_t[j];
                sumO += this.Wo[d][j] * x_t[j];
            }
            for (let j = 0; j < hDim; j++) {
                sumF += this.Uf[d][j] * h_prev[j];
                sumI += this.Ui[d][j] * h_prev[j];
                sumC += this.Uc[d][j] * h_prev[j];
                sumO += this.Uo[d][j] * h_prev[j];
            }

            f[d] = this.sigmoid(sumF);
            i[d] = this.sigmoid(sumI);
            c_tilde[d] = this.tanh(sumC);
            o[d] = this.sigmoid(sumO);

            c_next[d] = f[d] * c_prev[d] + i[d] * c_tilde[d];
            h_next[d] = o[d] * this.tanh(c_next[d]);
        }

        return { f, i, c_tilde, o, c_next, h_next };
    }

    forward(charIndices) {
        let h = new Array(this.hiddenDim).fill(0);
        let c = new Array(this.hiddenDim).fill(0);
        const steps = [];

        for (let t = 0; t < charIndices.length; t++) {
            const charIdx = charIndices[t];
            const x_t = this.E[charIdx] || new Array(this.embeddingDim).fill(0);

            const res = this.lstmStep(x_t, h, c);
            h = res.h_next;
            c = res.c_next;

            steps.push({
                t,
                charIdx,
                char: this.idx2char[charIdx],
                embedding: x_t,
                ...res
            });
        }

        const logits = new Array(this.vocabSize).fill(0);
        for (let v = 0; v < this.vocabSize; v++) {
            let sum = this.by[v];
            for (let d = 0; d < this.hiddenDim; d++) {
                sum += this.Wy[v][d] * h[d];
            }
            logits[v] = sum;
        }

        return { steps, finalH: h, finalC: c, logits };
    }

    computeSoftmaxWithTemperature(logits, temp = null) {
        const tVal = Math.max(0.01, temp !== null ? temp : this.temperature);
        const scaledLogits = logits.map(z => z / tVal);
        const maxLogit = Math.max(...scaledLogits);
        const exps = scaledLogits.map(z => Math.exp(z - maxLogit));
        const sumExps = exps.reduce((a, b) => a + b, 1e-9);

        const probs = exps.map(e => e / sumExps);
        return { probs, temp: tVal };
    }

    sampleNextChar(probs) {
        const r = Math.random();
        let cumSum = 0;
        for (let v = 0; v < probs.length; v++) {
            cumSum += probs[v];
            if (r <= cumSum) return v;
        }
        return probs.length - 1;
    }

    trainEpoch() {
        let totalLoss = 0;
        let correct = 0;
        const numSamples = this.trainX.length;
        if (numSamples === 0) return { loss: 0, accuracy: 0 };

        // Subamostra para velocidade no browser
        const batchSize = Math.min(numSamples, 300);
        const indices = [];
        for (let b = 0; b < batchSize; b++) {
            indices.push(Math.floor(Math.random() * numSamples));
        }

        for (let k = 0; k < batchSize; k++) {
            const idx = indices[k];
            const seqX = this.trainX[idx];
            const targetY = this.trainY[idx];

            const fwd = this.forward(seqX);
            const { probs } = this.computeSoftmaxWithTemperature(fwd.logits, 1.0);

            const probTarget = Math.max(probs[targetY], 1e-9);
            totalLoss += -Math.log(probTarget);

            const predY = probs.indexOf(Math.max(...probs));
            if (predY === targetY) correct++;

            const dLogits = probs.map((p, v) => (p - (v === targetY ? 1.0 : 0.0)) / batchSize);

            for (let v = 0; v < this.vocabSize; v++) {
                this.by[v] -= this.learningRate * dLogits[v];
                for (let d = 0; d < this.hiddenDim; d++) {
                    this.Wy[v][d] -= this.learningRate * dLogits[v] * fwd.finalH[d];
                }
            }
        }

        const avgLoss = totalLoss / batchSize;
        const accuracy = (correct / batchSize) * 100;

        this.history.loss.push(avgLoss);
        this.history.accuracy.push(accuracy);

        return { loss: avgLoss, accuracy };
    }

    generateText(promptText, length = 60, temp = 0.7) {
        let currentPrompt = promptText || "A inteligencia artificial ";
        let generated = "";

        for (let step = 0; step < length; step++) {
            const inputSub = currentPrompt.slice(-this.seqLen);
            const indices = inputSub.split('').map(c => this.char2idx[c] !== undefined ? this.char2idx[c] : 0);

            const fwd = this.forward(indices);
            const { probs } = this.computeSoftmaxWithTemperature(fwd.logits, temp);

            const nextCharIdx = this.sampleNextChar(probs);
            const nextChar = this.idx2char[nextCharIdx];

            generated += nextChar;
            currentPrompt += nextChar;
        }

        return generated;
    }
}

window.MiniLLMEngine = MiniLLMEngine;
