/**
 * Network Visualizer - Renderização Gráfica Interativa da Arquitetura do Mini-LLM no Canvas
 * Desenha os blocos de Tokenização, Embedding (16 dims), Portas da Célula LSTM e Distribuição de Saída.
 */

class NetworkVisualizer {
    constructor(canvasElement) {
        this.canvas = canvasElement;
        this.ctx = canvasElement.getContext('2d');

        this.activeStepData = null;
        this.particles = [];
        this.animationId = null;

        this.resize();
        this.bindEvents();
        this.startAnimationLoop();
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width || 800;
        this.canvas.height = rect.height || 450;
    }

    bindEvents() {
        window.addEventListener('resize', () => this.resize());
    }

    setStepData(stepData, logits, probs, temp) {
        this.activeStepData = stepData;
        this.logits = logits;
        this.probs = probs;
        this.temp = temp;
        this.triggerPulseParticles();
    }

    triggerPulseParticles() {
        this.particles = [];
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Criar partículas fluindo da esquerda (Input/Embedding) para a direita (LSTM e Softmax)
        for (let i = 0; i < 15; i++) {
            this.particles.push({
                x: w * 0.15,
                y: h * 0.4 + (Math.random() - 0.5) * 60,
                targetX: w * 0.5,
                targetY: h * 0.45 + (Math.random() - 0.5) * 80,
                progress: 0.0,
                speed: 0.02 + Math.random() * 0.02,
                color: '#6366f1'
            });
            this.particles.push({
                x: w * 0.5,
                y: h * 0.45 + (Math.random() - 0.5) * 80,
                targetX: w * 0.85,
                targetY: h * 0.5 + (Math.random() - 0.5) * 100,
                progress: 0.0,
                speed: 0.02 + Math.random() * 0.02,
                color: '#ec4899'
            });
        }
    }

    startAnimationLoop() {
        const drawFrame = () => {
            this.draw();
            this.animationId = requestAnimationFrame(drawFrame);
        };
        requestAnimationFrame(drawFrame);
    }

    draw() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        this.ctx.clearRect(0, 0, w, h);

        // Fundo com grade sutil
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        this.ctx.lineWidth = 1;
        const step = 30;
        for (let x = 0; x < w; x += step) {
            this.ctx.beginPath(); this.ctx.moveTo(x, 0); this.ctx.lineTo(x, h); this.ctx.stroke();
        }
        for (let y = 0; y < h; y += step) {
            this.ctx.beginPath(); this.ctx.moveTo(0, y); this.ctx.lineTo(w, y); this.ctx.stroke();
        }

        // Posições dos Blocos Principais
        const bInput = { x: w * 0.05, y: h * 0.25, w: w * 0.18, h: h * 0.5 };
        const bLSTM  = { x: w * 0.32, y: h * 0.15, w: w * 0.36, h: h * 0.7 };
        const bDense = { x: w * 0.75, y: h * 0.25, w: w * 0.20, h: h * 0.5 };

        // Linhas de Conexão de Sinal entre Blocos
        this.ctx.beginPath();
        this.ctx.moveTo(bInput.x + bInput.w, bInput.y + bInput.h / 2);
        this.ctx.lineTo(bLSTM.x, bLSTM.y + bLSTM.h / 2);
        this.ctx.strokeStyle = 'rgba(99, 102, 241, 0.5)';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.moveTo(bLSTM.x + bLSTM.w, bLSTM.y + bLSTM.h / 2);
        this.ctx.lineTo(bDense.x, bDense.y + bDense.h / 2);
        this.ctx.strokeStyle = 'rgba(236, 72, 153, 0.5)';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        // 1. Desenha Bloco 1: Entrada / Tokenizador & Embedding (16 dims)
        this.drawCardBlock(bInput, '1. Token & Embedding', '#3b82f6');
        this.drawEmbeddingValues(bInput);

        // 2. Desenha Bloco 2: Célula Recorrente LSTM (Portas e Estados)
        this.drawCardBlock(bLSTM, '2. Célula LSTM (Hidden State h_t)', '#8b5cf6');
        this.drawLSTMGates(bLSTM);

        // 3. Desenha Bloco 3: Camada Densa & Softmax com Temperatura
        this.drawCardBlock(bDense, '3. Softmax (Temperatura τ)', '#ec4899');
        this.drawSoftmaxOutputs(bDense);

        // Desenha Partículas Animadas
        this.drawParticles();
    }

    drawCardBlock(rect, title, accentColor) {
        this.ctx.save();
        this.ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        this.ctx.strokeStyle = accentColor;
        this.ctx.lineWidth = 2;
        this.ctx.shadowColor = accentColor;
        this.ctx.shadowBlur = 10;

        this.ctx.beginPath();
        this.ctx.roundRect(rect.x, rect.y, rect.w, rect.h, 12);
        this.ctx.fill();
        this.ctx.stroke();
        this.ctx.restore();

        // Título do Bloco
        this.ctx.fillStyle = '#f8fafc';
        this.ctx.font = 'bold 12px Inter, sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(title, rect.x + rect.w / 2, rect.y + 22);
    }

    drawEmbeddingValues(rect) {
        if (!this.activeStepData) {
            this.ctx.fillStyle = '#64748b';
            this.ctx.font = '11px Inter, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('Nenhum passo ativo', rect.x + rect.w / 2, rect.y + rect.h / 2);
            return;
        }

        const char = this.activeStepData.char === '\n' ? '\\n' : this.activeStepData.char;
        this.ctx.fillStyle = '#60a5fa';
        this.ctx.font = 'bold 14px Inter, sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`Char: "${char}" (ID: ${this.activeStepData.charIdx})`, rect.x + rect.w / 2, rect.y + 45);

        // Renderiza barras do vetor de embedding d=16
        const emb = this.activeStepData.embedding;
        const startY = rect.y + 60;
        const barWidth = (rect.w - 20) / 16;

        for (let d = 0; d < 16; d++) {
            const val = emb[d] || 0;
            const h = Math.abs(val) * 35;
            const x = rect.x + 10 + d * barWidth;
            const y = startY + 40 - (val > 0 ? h : 0);

            this.ctx.fillStyle = val >= 0 ? '#3b82f6' : '#ef4444';
            this.ctx.fillRect(x, y, barWidth - 1, Math.max(2, h));
        }

        this.ctx.fillStyle = '#94a3b8';
        this.ctx.font = '10px Inter, sans-serif';
        this.ctx.fillText('Vetor Denso (d=16)', rect.x + rect.w / 2, rect.y + rect.h - 15);
    }

    drawLSTMGates(rect) {
        if (!this.activeStepData) {
            this.ctx.fillStyle = '#64748b';
            this.ctx.font = '11px Inter, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('Aguardando execução...', rect.x + rect.w / 2, rect.y + rect.h / 2);
            return;
        }

        const data = this.activeStepData;
        const avg = arr => (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(3);

        const gates = [
            { name: 'Forget Gate (f_t)', val: avg(data.f), color: '#ef4444' },
            { name: 'Input Gate (i_t)', val: avg(data.i), color: '#10b981' },
            { name: 'Output Gate (o_t)', val: avg(data.o), color: '#f59e0b' },
            { name: 'Cell Memory (C_t)', val: avg(data.c_next), color: '#3b82f6' }
        ];

        const startY = rect.y + 45;
        const gapY = (rect.h - 60) / gates.length;

        gates.forEach((g, idx) => {
            const y = startY + idx * gapY;

            // Rótulo
            this.ctx.fillStyle = '#cbd5e1';
            this.ctx.font = '11px Inter, sans-serif';
            this.ctx.textAlign = 'left';
            this.ctx.fillText(g.name, rect.x + 15, y);

            // Valor Numérico
            this.ctx.fillStyle = g.color;
            this.ctx.font = 'bold 11px Fira Code, monospace';
            this.ctx.textAlign = 'right';
            this.ctx.fillText(g.val, rect.x + rect.w - 15, y);

            // Barra de ativação
            const valNum = parseFloat(g.val);
            const fillW = Math.max(4, Math.min(1.0, (valNum + 1) / 2) * (rect.w - 30));
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
            this.ctx.fillRect(rect.x + 15, y + 6, rect.w - 30, 6);
            this.ctx.fillStyle = g.color;
            this.ctx.fillRect(rect.x + 15, y + 6, fillW, 6);
        });
    }

    drawSoftmaxOutputs(rect) {
        if (!this.probs) {
            this.ctx.fillStyle = '#64748b';
            this.ctx.font = '11px Inter, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('Aguardando amostragem...', rect.x + rect.w / 2, rect.y + rect.h / 2);
            return;
        }

        this.ctx.fillStyle = '#f472b6';
        this.ctx.font = 'bold 12px Inter, sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`Temp (τ): ${this.temp !== undefined ? this.temp.toFixed(2) : '0.70'}`, rect.x + rect.w / 2, rect.y + 45);

        // Pega os 4 caracteres mais prováveis
        const topProbs = this.probs
            .map((p, idx) => ({ idx, p, char: window.miniEngine.idx2char[idx] }))
            .sort((a, b) => b.p - a.p)
            .slice(0, 4);

        const startY = rect.y + 60;
        topProbs.forEach((item, i) => {
            const y = startY + i * 28;
            const charDisp = item.char === '\n' ? '\\n' : (item.char === ' ' ? 'ESPAÇO' : `"${item.char}"`);

            this.ctx.fillStyle = i === 0 ? '#10b981' : '#e2e8f0';
            this.ctx.font = '10px Inter, sans-serif';
            this.ctx.textAlign = 'left';
            this.ctx.fillText(`${charDisp}`, rect.x + 12, y);

            this.ctx.textAlign = 'right';
            this.ctx.fillText(`${(item.p * 100).toFixed(1)}%`, rect.x + rect.w - 12, y);
        });
    }

    drawParticles() {
        for (const p of this.particles) {
            p.progress += p.speed;
            if (p.progress >= 1.0) p.progress = 0.0;

            const currX = p.x + (p.targetX - p.x) * p.progress;
            const currY = p.y + (p.targetY - p.y) * p.progress;

            this.ctx.save();
            this.ctx.shadowColor = p.color;
            this.ctx.shadowBlur = 8;

            this.ctx.beginPath();
            this.ctx.arc(currX, currY, 3, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.fill();

            this.ctx.restore();
        }
    }
}

window.NetworkVisualizer = NetworkVisualizer;
