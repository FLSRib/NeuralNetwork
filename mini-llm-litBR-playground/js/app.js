/**
 * Mini-LLM App Controller - Controlador Principal com Suporte a Corpus Customizável
 */

document.addEventListener('DOMContentLoaded', () => {
    const engine = new MiniLLMEngine();
    window.miniEngine = engine;

    const canvas = document.getElementById('networkCanvas');
    const netVis = new NetworkVisualizer(canvas);
    const charts = new PlaygroundCharts();

    let isAutoGenerating = false;
    let autoGenInterval = null;

    let isTraining = false;
    let trainInterval = null;
    let currentEpoch = 0;

    let currentGeneratedText = "";

    // Preenche o textarea com o corpus default
    const corpusArea = document.getElementById('corpusTextarea');
    if (corpusArea) {
        corpusArea.value = engine.corpus;
        document.getElementById('corpusSizeLabel').textContent = `${engine.corpus.length} chars`;
    }

    // Inicialização da UI
    initTokenizerTable();
    updateMathFormulas();
    runSingleStep();

    // --- Vinculação de Eventos UI ---

    // Atualização de Corpus Customizado
    document.getElementById('btnUpdateCorpus').addEventListener('click', () => {
        const text = corpusArea.value;
        if (engine.setCustomCorpus(text)) {
            document.getElementById('corpusSizeLabel').textContent = `${engine.corpus.length} chars`;
            reinitWeights();
            initTokenizerTable();
            alert(`Corpus atualizado com sucesso! ${engine.corpus.length} caracteres e ${engine.vocabSize} símbolos únicos.`);
        } else {
            alert("O texto do corpus precisa ter pelo menos 50 caracteres.");
        }
    });

    // Prompt Presets
    document.getElementById('promptPresetSelect').addEventListener('change', (e) => {
        document.getElementById('promptInput').value = e.target.value;
        resetGeneration();
    });

    document.getElementById('promptInput').addEventListener('input', () => {
        resetGeneration();
    });

    // Slider de Temperatura
    const tempSlider = document.getElementById('tempRange');
    tempSlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        document.getElementById('tempVal').textContent = val.toFixed(2);
        engine.temperature = val;

        updateMathFormulas();
        runSingleStep();
    });

    // Botões de Geração
    document.getElementById('btnStepGen').addEventListener('click', generateNextCharStep);
    document.getElementById('btnPlayGen').addEventListener('click', toggleAutoGeneration);
    document.getElementById('btnResetGen').addEventListener('click', resetGeneration);

    // Botão de Treinamento Live
    document.getElementById('btnTrainToggle').addEventListener('click', toggleTraining);
    document.getElementById('btnResetWeights').addEventListener('click', reinitWeights);

    // Speed Slider
    const speedSlider = document.getElementById('speedRange');
    speedSlider.addEventListener('input', (e) => {
        document.getElementById('speedVal').textContent = `${e.target.value}ms`;
        if (isAutoGenerating) {
            stopAutoGeneration();
            startAutoGeneration();
        }
    });

    function resetGeneration() {
        stopAutoGeneration();
        const prompt = document.getElementById('promptInput').value || "A inteligencia artificial ";
        currentGeneratedText = prompt;
        document.getElementById('outputText').textContent = currentGeneratedText;
        runSingleStep();
    }

    function runSingleStep() {
        const prompt = currentGeneratedText || "A inteligencia artificial ";
        const sub = prompt.slice(-engine.seqLen);
        const indices = sub.split('').map(c => engine.char2idx[c] !== undefined ? engine.char2idx[c] : 0);

        const fwd = engine.forward(indices);
        const { probs } = engine.computeSoftmaxWithTemperature(fwd.logits, engine.temperature);

        const lastStep = fwd.steps[fwd.steps.length - 1];
        netVis.setStepData(lastStep, fwd.logits, probs, engine.temperature);

        const sampledIdx = engine.sampleNextChar(probs);
        charts.updateSoftmaxChart(engine.vocab, probs, sampledIdx);

        return { fwd, probs, sampledIdx };
    }

    function generateNextCharStep() {
        const { probs, sampledIdx } = runSingleStep();

        const sampledChar = engine.idx2char[sampledIdx];
        currentGeneratedText += sampledChar;

        const outElem = document.getElementById('outputText');
        outElem.textContent = currentGeneratedText;
        outElem.scrollTop = outElem.scrollHeight;

        runSingleStep();
    }

    function toggleAutoGeneration() {
        if (isAutoGenerating) {
            stopAutoGeneration();
        } else {
            startAutoGeneration();
        }
    }

    function startAutoGeneration() {
        isAutoGenerating = true;
        const btn = document.getElementById('btnPlayGen');
        btn.innerHTML = '<i class="fas fa-pause mr-1.5"></i> Pausar Geração';
        btn.classList.replace('bg-purple-600', 'bg-yellow-600');

        const speed = parseInt(document.getElementById('speedRange').value, 10);
        autoGenInterval = setInterval(() => {
            generateNextCharStep();
        }, speed);
    }

    function stopAutoGeneration() {
        isAutoGenerating = false;
        if (autoGenInterval) clearInterval(autoGenInterval);
        const btn = document.getElementById('btnPlayGen');
        btn.innerHTML = '<i class="fas fa-play mr-1.5"></i> Gerar Auto';
        btn.classList.replace('bg-yellow-600', 'bg-purple-600');
    }

    function toggleTraining() {
        if (isTraining) {
            stopTraining();
        } else {
            startTraining();
        }
    }

    function startTraining() {
        isTraining = true;
        const btn = document.getElementById('btnTrainToggle');
        btn.innerHTML = '<i class="fas fa-pause mr-1.5"></i> Pausar Treino';
        btn.classList.replace('bg-green-600', 'bg-yellow-600');

        trainInterval = setInterval(() => {
            const res = engine.trainEpoch();
            currentEpoch++;

            document.getElementById('epochCounter').textContent = currentEpoch;
            document.getElementById('lossVal').textContent = res.loss.toFixed(4);
            document.getElementById('accVal').textContent = res.accuracy.toFixed(1) + '%';

            charts.updateMetricsChart(engine.history);
        }, 100);
    }

    function stopTraining() {
        isTraining = false;
        if (trainInterval) clearInterval(trainInterval);
        const btn = document.getElementById('btnTrainToggle');
        btn.innerHTML = '<i class="fas fa-graduation-cap mr-1.5"></i> Treinar Modelo (Live)';
        btn.classList.replace('bg-yellow-600', 'bg-green-600');
    }

    function reinitWeights() {
        if (isTraining) stopTraining();
        currentEpoch = 0;
        document.getElementById('epochCounter').textContent = '0';
        document.getElementById('lossVal').textContent = '0.00';
        document.getElementById('accVal').textContent = '0%';

        engine.initWeights();
        charts.resetMetricsChart();
        resetGeneration();
    }

    function initTokenizerTable() {
        const container = document.getElementById('tokenizerContainer');
        if (!container) return;

        let html = `
            <div class="grid grid-cols-6 sm:grid-cols-9 gap-1.5 text-center text-xs font-mono">
                ${engine.vocab.map((c, i) => `
                    <div class="bg-slate-800 p-1.5 rounded border border-slate-700 hover:border-indigo-500 transition">
                        <div class="text-indigo-400 font-bold">${c === '\n' ? '\\n' : (c === ' ' ? '␣' : c)}</div>
                        <div class="text-[10px] text-slate-400">${i}</div>
                    </div>
                `).join('')}
            </div>
        `;

        container.innerHTML = html;
    }

    function updateMathFormulas() {
        const temp = parseFloat(document.getElementById('tempRange').value);

        const softFormula = `P(c_i \\mid \\text{contexto}) = \\frac{\\exp(z_i / ${temp.toFixed(2)})}{\\sum_{j=1}^{${engine.vocabSize}} \\exp(z_j / ${temp.toFixed(2)})}`;
        const lstmFormula = `f_t = \\sigma(W_f x_t + U_f h_{t-1} + b_f) \\quad C_t = f_t \\odot C_{t-1} + i_t \\odot \\tilde{C}_t`;

        if (window.katex) {
            window.katex.render(softFormula, document.getElementById('katexSoftmax'), { throwOnError: false, displayMode: true });
            window.katex.render(lstmFormula, document.getElementById('katexLSTM'), { throwOnError: false, displayMode: true });
        }
    }
});
