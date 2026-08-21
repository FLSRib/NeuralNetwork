/**
 * Playground Charts - Gráficos Chart.js para Distribuição Softmax e Métricas de Treino
 */

class PlaygroundCharts {
    constructor() {
        this.softmaxChart = null;
        this.metricsChart = null;
        this.initSoftmaxChart();
        this.initMetricsChart();
    }

    initSoftmaxChart() {
        const ctx = document.getElementById('softmaxChartCanvas').getContext('2d');
        this.softmaxChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Probabilidade Softmax P(c)',
                    data: [],
                    backgroundColor: '#ec4899',
                    borderColor: '#f472b6',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 150 },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', font: { size: 10 } }
                    },
                    y: {
                        min: 0,
                        max: 1.0,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `Probabilidade: ${(context.raw * 100).toFixed(2)}%`
                        }
                    }
                }
            }
        });
    }

    initMetricsChart() {
        const ctx = document.getElementById('metricsChartCanvas').getContext('2d');
        this.metricsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Perda (Loss)',
                        data: [],
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        yAxisID: 'yLoss'
                    },
                    {
                        label: 'Acurácia (%)',
                        data: [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        yAxisID: 'yAcc'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    yLoss: {
                        type: 'linear',
                        position: 'left',
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#ef4444' }
                    },
                    yAcc: {
                        type: 'linear',
                        position: 'right',
                        min: 0,
                        max: 100,
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#10b981' }
                    }
                },
                plugins: {
                    legend: { labels: { color: '#e2e8f0' } }
                }
            }
        });
    }

    updateSoftmaxChart(vocab, probs, sampledIdx = -1) {
        const labels = vocab.map(c => c === '\n' ? '\\n' : (c === ' ' ? '␣' : c));
        this.softmaxChart.data.labels = labels;
        this.softmaxChart.data.datasets[0].data = probs;

        // Destaque de cor no caractere sorteado
        const colors = probs.map((_, i) => i === sampledIdx ? '#10b981' : '#ec4899');
        this.softmaxChart.data.datasets[0].backgroundColor = colors;

        this.softmaxChart.update();
    }

    updateMetricsChart(history) {
        const labels = history.loss.map((_, idx) => idx + 1);
        this.metricsChart.data.labels = labels;
        this.metricsChart.data.datasets[0].data = history.loss;
        this.metricsChart.data.datasets[1].data = history.accuracy;
        this.metricsChart.update('none');
    }

    resetMetricsChart() {
        this.metricsChart.data.labels = [];
        this.metricsChart.data.datasets[0].data = [];
        this.metricsChart.data.datasets[1].data = [];
        this.metricsChart.update();
    }
}

window.PlaygroundCharts = PlaygroundCharts;
