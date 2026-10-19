# -*- coding: utf-8 -*-
"""
Geracao completa de grafos e visualizacoes SNA
Projeto: Vulnerabilidade da Cadeia de Suprimentos de Insumos Quimicos
FGV MBA - Grupo Paulista T16
"""

import pandas as pd
import networkx as nx
import networkx.algorithms.bipartite as bipartite
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import os

# â”€â”€ Paths â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BASE_DATA = r'C:\Users\fribeiro\OneDrive - Echostar Operating L.L.C\Documentos\lixo\FGV\materiais\SNA\trabalho em grupo\mods v2'
PROJ = os.path.join(BASE_DATA, 'Rede_Projeto_SNA_v2.xlsx')
OUT  = r'C:\Users\fribeiro\.gemini\antigravity\scratch\FLSRib_repo\SNA\grafos'

# â”€â”€ Paleta â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
COR_EXPOSTO   = '#E63946'
COR_SEGURO    = '#457B9D'
COR_UCRANIANO = '#FF6B35'
COR_INSUMO    = '#2A9D8F'
COR_EDGE_BASE = '#AAAAAA'
COR_BG        = '#F8F9FA'

plt.rcParams.update({
    'figure.facecolor': COR_BG,
    'axes.facecolor':   COR_BG,
    'font.family':      'sans-serif',
    'font.size':        9,
})

# â”€â”€ Carregar dados â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
df_one    = pd.read_excel(PROJ, sheet_name='matriz One-mode',   engine='openpyxl', index_col=0)
df_two    = pd.read_excel(PROJ, sheet_name='matriz Two-mode',   engine='openpyxl', index_col=0)
df_attr_p = pd.read_excel(PROJ, sheet_name='Atributos_Portos',  engine='openpyxl')

UCRANIANOS = [
    'Mariupol','Berdyansk','Kherson','Skadovsk','Mykolaiv',
    'Olvia','Chornomorsk','Pivdennyi','Bilhorod-Dnistrovskyi'
]

df_attr_p_clean = df_attr_p.dropna(subset=['Porto (linha)'])
expostos_set = set(df_attr_p_clean[df_attr_p_clean['Exposto? (1=sim)'] == 1]['Porto (linha)'])

G_base  = nx.from_pandas_adjacency(df_one)
df_stress = df_one.drop(index=UCRANIANOS, columns=UCRANIANOS)
G_stress  = nx.from_pandas_adjacency(df_stress)

def ok(nome):
    print('[OK] ' + nome)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 1 â€” One-Mode Baseline
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_one_mode_baseline():
    fig, ax = plt.subplots(figsize=(16, 12))
    pos = nx.spring_layout(G_base, seed=42, k=2.2)
    deg = dict(G_base.degree())

    node_colors, node_sizes = [], []
    for n in G_base.nodes():
        if n in UCRANIANOS:
            node_colors.append(COR_UCRANIANO)
        elif n in expostos_set:
            node_colors.append(COR_EXPOSTO)
        else:
            node_colors.append(COR_SEGURO)
        node_sizes.append(150 + deg[n] * 30)

    nx.draw_networkx_edges(G_base, pos, alpha=0.15, edge_color=COR_EDGE_BASE, ax=ax)
    nx.draw_networkx_nodes(G_base, pos, node_color=node_colors,
                           node_size=node_sizes, alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G_base, pos, font_size=6.5, font_weight='bold', ax=ax)

    patches = [
        mpatches.Patch(color=COR_UCRANIANO, label='Porto ucraniano (removido no estresse)'),
        mpatches.Patch(color=COR_EXPOSTO,   label='Porto exposto (Mar Negro/Ormuz/Mar Vermelho)'),
        mpatches.Patch(color=COR_SEGURO,    label='Porto nao exposto'),
    ]
    ax.legend(handles=patches, loc='lower left', fontsize=8, framealpha=0.85)
    ax.set_title('Rede One-Mode - Baseline (39 portos)\nTamanho do no proporcional ao grau',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '01_one_mode_baseline.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('01_one_mode_baseline.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 2 â€” One-Mode Cenario de Estresse
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_one_mode_estresse():
    fig, ax = plt.subplots(figsize=(15, 11))
    pos = nx.spring_layout(G_stress, seed=42, k=2.2)
    deg  = dict(G_stress.degree())
    betw = nx.betweenness_centrality(G_stress)

    node_colors = [COR_EXPOSTO if n in expostos_set else COR_SEGURO for n in G_stress.nodes()]
    node_sizes  = [150 + deg[n] * 35 for n in G_stress.nodes()]

    nx.draw_networkx_edges(G_stress, pos, alpha=0.18, edge_color=COR_EDGE_BASE, ax=ax)
    nx.draw_networkx_nodes(G_stress, pos, node_color=node_colors,
                           node_size=node_sizes, alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G_stress, pos, font_size=7, font_weight='bold', ax=ax)

    top3 = sorted(betw.items(), key=lambda x: -x[1])[:3]
    top3_nodes = {n: v for n, v in top3}
    nx.draw_networkx_nodes(G_stress, pos, nodelist=list(top3_nodes.keys()),
                           node_color='#FFD166',
                           node_size=[150 + deg[n]*35 + 200 for n in top3_nodes],
                           ax=ax, linewidths=2.5, edgecolors='#333')

    patches = [
        mpatches.Patch(color=COR_EXPOSTO, label='Porto exposto'),
        mpatches.Patch(color=COR_SEGURO,  label='Porto nao exposto'),
        mpatches.Patch(color='#FFD166',   label='Top 3 Betweenness'),
    ]
    ax.legend(handles=patches, loc='lower left', fontsize=8, framealpha=0.85)
    ax.set_title('Rede One-Mode - Cenario de Estresse (30 portos)\nTamanho proporcional ao grau | Amarelo = maior betweenness',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '02_one_mode_estresse.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('02_one_mode_estresse.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 3 â€” Two-Mode bipartido
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_two_mode():
    B = nx.Graph()
    portos  = list(df_two.index)
    insumos = list(df_two.columns)
    B.add_nodes_from(portos,  bipartite=0)
    B.add_nodes_from(insumos, bipartite=1)
    for p in portos:
        for ins in insumos:
            if df_two.loc[p, ins] == 1:
                B.add_edge(p, ins)

    pos = {}
    pos.update((n, (0, i * 1.1)) for i, n in enumerate(reversed(portos)))
    pos.update((n, (4, i * 1.4)) for i, n in enumerate(reversed(insumos)))

    fig, ax = plt.subplots(figsize=(14, 22))
    port_colors = [COR_EXPOSTO if p in expostos_set else COR_SEGURO for p in portos]
    port_sizes  = [df_two.loc[p].sum() * 25 + 100 for p in portos]

    exp_pct = {}
    for ins in insumos:
        total = df_two[ins].sum()
        exp   = df_two.loc[df_two.index.isin(expostos_set), ins].sum()
        exp_pct[ins] = exp / total if total > 0 else 0

    cmap_ins   = matplotlib.colormaps['RdYlGn_r']
    ins_colors = [mcolors.to_hex(cmap_ins(exp_pct[ins])) for ins in insumos]
    ins_sizes  = [df_two[ins].sum() * 20 + 100 for ins in insumos]

    nx.draw_networkx_edges(B, pos, alpha=0.12, edge_color=COR_EDGE_BASE, ax=ax)
    nx.draw_networkx_nodes(B, pos, nodelist=portos,  node_color=port_colors,
                           node_size=port_sizes, alpha=0.9, ax=ax)
    nx.draw_networkx_nodes(B, pos, nodelist=insumos, node_color=ins_colors,
                           node_size=ins_sizes, alpha=0.9, ax=ax, node_shape='s')
    nx.draw_networkx_labels(B, pos, font_size=7, font_weight='bold', ax=ax)

    patches = [
        mpatches.Patch(color=COR_EXPOSTO, label='Porto exposto (circulo)'),
        mpatches.Patch(color=COR_SEGURO,  label='Porto nao exposto (circulo)'),
        mpatches.Patch(color='#006d2c',   label='Insumo - baixa exposicao (quadrado)'),
        mpatches.Patch(color='#d73027',   label='Insumo - alta exposicao (quadrado)'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=8, framealpha=0.85)
    ax.set_title('Rede Two-Mode - 30 Portos x 21 Insumos\nCores dos insumos = % de portos expostos (verde->vermelho)',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '03_two_mode_bipartido.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('03_two_mode_bipartido.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 4 â€” Heatmap de Centralidades
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def heatmap_centralidades():
    deg  = dict(G_base.degree())
    betw = nx.betweenness_centrality(G_base)
    clos = nx.closeness_centrality(G_base)
    eig  = nx.eigenvector_centrality(G_base, max_iter=1000)

    df_cent = pd.DataFrame({
        'Degree':      deg,
        'Betweenness': betw,
        'Closeness':   clos,
        'Eigenvector': eig,
    })
    df_norm = (df_cent - df_cent.min()) / (df_cent.max() - df_cent.min())
    df_norm = df_norm.sort_values('Betweenness', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 14))
    im = ax.imshow(df_norm.values, aspect='auto', cmap='YlOrRd', vmin=0, vmax=1)

    ax.set_xticks(range(4))
    ax.set_xticklabels(df_norm.columns, fontsize=10, fontweight='bold')
    ax.set_yticks(range(len(df_norm)))
    ax.set_yticklabels(df_norm.index, fontsize=7)

    for i in range(len(df_norm)):
        for j, col in enumerate(df_norm.columns):
            val = df_cent.loc[df_norm.index[i], col]
            ax.text(j, i, f'{val:.3f}', ha='center', va='center', fontsize=5.5,
                    color='black' if df_norm.values[i, j] < 0.7 else 'white')

    plt.colorbar(im, ax=ax, label='Valor normalizado (0-1)', fraction=0.02, pad=0.02)
    ax.set_title('Heatmap de Centralidades - One-Mode Baseline (39 portos)\nOrdenado por Betweenness decrescente',
                 fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '04_heatmap_centralidades.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('04_heatmap_centralidades.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 5 â€” Betweenness Centrality colorida
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_betweenness():
    betw = nx.betweenness_centrality(G_base)
    pos  = nx.spring_layout(G_base, seed=42, k=2.2)

    fig, ax = plt.subplots(figsize=(16, 12))
    vals   = [betw[n] for n in G_base.nodes()]
    cmap   = matplotlib.colormaps['plasma']
    norm   = mcolors.Normalize(vmin=min(vals), vmax=max(vals))
    colors = [cmap(norm(v)) for v in vals]
    sizes  = [300 + betw[n] * 8000 for n in G_base.nodes()]

    nx.draw_networkx_edges(G_base, pos, alpha=0.12, edge_color='#CCCCCC', ax=ax)
    nx.draw_networkx_nodes(G_base, pos, node_color=colors,
                           node_size=sizes, alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G_base, pos, font_size=6.5, font_weight='bold', ax=ax)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Betweenness Centrality', fraction=0.025, pad=0.02)
    ax.set_title('Betweenness Centrality - One-Mode Baseline\nTamanho e cor proporcional a intermediacao estrutural',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '05_betweenness_centrality.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('05_betweenness_centrality.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 6 â€” Comparativo Degree Baseline vs Estresse
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def barras_degree_comparativo():
    deg_base   = dict(G_base.degree())
    deg_stress = dict(G_stress.degree())
    comuns = sorted(set(deg_base) & set(deg_stress))
    d_base = [deg_base[p]   for p in comuns]
    d_str  = [deg_stress[p] for p in comuns]
    delta  = [d_str[i] - d_base[i] for i in range(len(comuns))]

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    x = np.arange(len(comuns))
    w = 0.38
    axes[0].barh(x + w/2, d_base, w, label='Baseline (39)', color=COR_SEGURO,  alpha=0.85)
    axes[0].barh(x - w/2, d_str,  w, label='Estresse (30)', color=COR_EXPOSTO, alpha=0.85)
    axes[0].set_yticks(x)
    axes[0].set_yticklabels(comuns, fontsize=7)
    axes[0].set_xlabel('Grau (Degree)')
    axes[0].set_title('Degree: Baseline vs. Estresse', fontweight='bold')
    axes[0].legend()
    axes[0].invert_yaxis()
    axes[0].set_facecolor(COR_BG)

    cores_delta = ['#E63946' if d > 0 else '#457B9D' for d in delta]
    axes[1].barh(x, delta, color=cores_delta, alpha=0.85)
    axes[1].axvline(0, color='black', linewidth=0.8)
    axes[1].set_yticks(x)
    axes[1].set_yticklabels(comuns, fontsize=7)
    axes[1].set_xlabel('Variacao do Grau (Estresse - Baseline)')
    axes[1].set_title('Variacao do Grau apos remocao dos 9 portos\nVermelho = aumentou | Azul = diminuiu', fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].set_facecolor(COR_BG)

    plt.suptitle('Impacto do Cenario de Estresse no Grau dos Portos', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '06_degree_baseline_vs_estresse.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('06_degree_baseline_vs_estresse.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 7 â€” Exposicao por insumo (barras Two-Mode)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def barras_exposicao_insumos():
    exposicao = {}
    for ins in df_two.columns:
        total = df_two[ins].sum()
        exp   = df_two.loc[df_two.index.isin(expostos_set), ins].sum()
        pct   = (exp / total * 100) if total > 0 else 0
        exposicao[ins] = {'pct': round(pct, 1), 'exp': int(exp), 'total': int(total)}

    df_exp = pd.DataFrame(exposicao).T.sort_values('pct', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 9))
    cmap = matplotlib.colormaps['RdYlGn_r']
    norm = mcolors.Normalize(vmin=0, vmax=60)
    cores = [mcolors.to_hex(cmap(norm(v))) for v in df_exp['pct']]

    bars = ax.barh(df_exp.index, df_exp['pct'], color=cores, alpha=0.9,
                   edgecolor='white', linewidth=0.5)

    for bar, (ins, row) in zip(bars, df_exp.iterrows()):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{row['pct']}%  ({row['exp']}/{row['total']})",
                va='center', ha='left', fontsize=8)

    ax.axvline(x=40, color='#E63946', linewidth=1.5, linestyle='--', alpha=0.7, label='Limiar 40%')
    ax.set_xlabel('Exposicao (%)', fontsize=10)
    ax.set_xlim(0, 75)
    ax.set_title('Exposicao por Insumo - Rede Two-Mode\n% de portos associados classificados como expostos',
                 fontsize=13, fontweight='bold', pad=12)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '07_exposicao_por_insumo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('07_exposicao_por_insumo.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 8 â€” K-core decomposition
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_kcore():
    kcore = nx.core_number(G_base)
    pos   = nx.spring_layout(G_base, seed=42, k=2.2)

    fig, ax = plt.subplots(figsize=(16, 12))
    cmap   = matplotlib.colormaps['viridis']
    norm   = mcolors.Normalize(vmin=min(kcore.values()), vmax=max(kcore.values()))
    colors = [cmap(norm(kcore[n])) for n in G_base.nodes()]
    sizes  = [100 + kcore[n] * 45 for n in G_base.nodes()]

    nx.draw_networkx_edges(G_base, pos, alpha=0.12, edge_color='#CCCCCC', ax=ax)
    nx.draw_networkx_nodes(G_base, pos, node_color=colors,
                           node_size=sizes, alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G_base, pos, font_size=6.5, font_weight='bold', ax=ax)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='K-core (maior = mais central no nucleo)', fraction=0.025, pad=0.02)
    ax.set_title('K-core Decomposition - One-Mode Baseline\nViridis: escuro=periferia | claro=nucleo central',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '08_kcore_decomposition.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('08_kcore_decomposition.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 9 â€” Projecao bipartida: co-exposicao de insumos
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_projecao_bipartida():
    B = nx.Graph()
    portos  = list(df_two.index)
    insumos = list(df_two.columns)
    B.add_nodes_from(portos,  bipartite=0)
    B.add_nodes_from(insumos, bipartite=1)
    for p in portos:
        for ins in insumos:
            if df_two.loc[p, ins] == 1:
                B.add_edge(p, ins)

    proj_ins = bipartite.weighted_projected_graph(B, insumos)
    pos = nx.spring_layout(proj_ins, seed=42, k=1.8, weight='weight')

    fig, ax = plt.subplots(figsize=(14, 11))

    exp_pct = {}
    for ins in insumos:
        total = df_two[ins].sum()
        exp   = df_two.loc[df_two.index.isin(expostos_set), ins].sum()
        exp_pct[ins] = (exp / total * 100) if total > 0 else 0

    cmap   = matplotlib.colormaps['RdYlGn_r']
    norm   = mcolors.Normalize(vmin=0, vmax=60)
    colors = [mcolors.to_hex(cmap(norm(exp_pct[n]))) for n in proj_ins.nodes()]
    deg_proj = dict(proj_ins.degree(weight='weight'))
    sizes  = [200 + deg_proj[n] * 8 for n in proj_ins.nodes()]

    edges    = list(proj_ins.edges(data=True))
    edge_wts = [d['weight'] for _, _, d in edges]
    max_w    = max(edge_wts) if edge_wts else 1
    edge_list = [(u, v) for u, v, d in edges]

    nx.draw_networkx_edges(proj_ins, pos, edgelist=edge_list,
                           width=[w / max_w * 4 for w in edge_wts],
                           alpha=0.4, edge_color='#888888', ax=ax)
    nx.draw_networkx_nodes(proj_ins, pos, node_color=colors,
                           node_size=sizes, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(proj_ins, pos, font_size=7, font_weight='bold', ax=ax)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Exposicao do insumo (%)', fraction=0.025, pad=0.02)
    ax.set_title('Projecao Bipartida - Co-exposicao entre Insumos\nEspessura = portos em comum | Cor = exposicao individual',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '09_projecao_bipartida_insumos.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('09_projecao_bipartida_insumos.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 10 â€” Fragmentacao incremental
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def grafo_fragmentacao_incremental():
    betw_base = nx.betweenness_centrality(G_base)
    ordem = sorted(UCRANIANOS, key=lambda x: -betw_base.get(x, 0))

    passos      = ['Baseline\n(39 portos)']
    componentes = [1]
    arestas     = [G_base.number_of_edges()]
    densidades  = [nx.density(G_base)]

    G_temp = G_base.copy()
    for porto in ordem:
        G_temp.remove_node(porto)
        passos.append('-' + porto)
        componentes.append(nx.number_connected_components(G_temp))
        arestas.append(G_temp.number_of_edges())
        densidades.append(nx.density(G_temp))

    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    x = range(len(passos))
    cor_comp = ['#E63946' if c > 1 else '#457B9D' for c in componentes]

    axes[0].bar(x, componentes, color=cor_comp, alpha=0.85, edgecolor='white')
    axes[0].axhline(y=1, color='#333', linewidth=1, linestyle='--')
    axes[0].set_ylabel('Componentes')
    axes[0].set_title('Fragmentacao da Rede - Remocao Incremental dos 9 Portos Ucranianos\n(ordem: betweenness decrescente)',
                      fontsize=12, fontweight='bold')
    axes[0].set_facecolor(COR_BG)
    for i, v in enumerate(componentes):
        axes[0].text(i, v + 0.05, str(v), ha='center', fontsize=9, fontweight='bold')

    axes[1].plot(x, arestas, marker='o', color='#2A9D8F', linewidth=2.5, markersize=7)
    axes[1].fill_between(x, arestas, alpha=0.15, color='#2A9D8F')
    axes[1].set_ylabel('Arestas')
    axes[1].set_facecolor(COR_BG)

    axes[2].plot(x, densidades, marker='s', color='#E76F51', linewidth=2.5, markersize=7)
    axes[2].fill_between(x, densidades, alpha=0.15, color='#E76F51')
    axes[2].set_ylabel('Densidade')
    axes[2].set_xlabel('Passo de remocao')
    axes[2].set_facecolor(COR_BG)

    plt.xticks(list(x), passos, rotation=25, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '10_fragmentacao_incremental.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('10_fragmentacao_incremental.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# GRAFO 11 â€” Scatter: Degree vs Exposicao (Two-Mode)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def scatter_degree_exposicao():
    grau    = df_two.sum(axis=0)
    exp_pct = {}
    for ins in df_two.columns:
        total = df_two[ins].sum()
        exp   = df_two.loc[df_two.index.isin(expostos_set), ins].sum()
        exp_pct[ins] = (exp / total * 100) if total > 0 else 0

    fig, ax = plt.subplots(figsize=(12, 8))
    xs     = [grau[ins] for ins in df_two.columns]
    ys     = [exp_pct[ins] for ins in df_two.columns]
    labels = list(df_two.columns)

    cmap   = matplotlib.colormaps['RdYlGn_r']
    norm   = mcolors.Normalize(vmin=0, vmax=60)
    colors = [mcolors.to_hex(cmap(norm(y))) for y in ys]

    ax.scatter(xs, ys, c=colors, s=180, alpha=0.9, edgecolors='#444', linewidths=0.8)

    for label, x, y in zip(labels, xs, ys):
        nome = label.split('(')[0].strip()
        ax.annotate(nome, (x, y), textcoords='offset points', xytext=(6, 3), fontsize=7.5)

    ax.axhline(y=40, color='#E63946', linewidth=1.5, linestyle='--', alpha=0.7, label='Limiar 40% exposicao')
    ax.axvline(x=15, color='#457B9D', linewidth=1.5, linestyle='--', alpha=0.7, label='Limiar grau 15')

    ax.set_xlabel('Grau do Insumo (numero de portos associados)', fontsize=11)
    ax.set_ylabel('Exposicao (%)', fontsize=11)
    ax.set_title('Scatter: Grau x Exposicao por Insumo\nQuadrante sup-esq = risco escondido | Quadrante sup-dir = risco amplo',
                 fontsize=13, fontweight='bold', pad=12)
    ax.legend(fontsize=9)

    ax.text(3.2, 52, 'RISCO\nESCONDIDO', fontsize=9, color='#E63946', alpha=0.8, style='italic', fontweight='bold')
    ax.text(17,  52, 'RISCO\nAMPLO',     fontsize=9, color='#FF6B35', alpha=0.8, style='italic', fontweight='bold')
    ax.text(17,   3, 'RESILIENTE',        fontsize=9, color='#2A9D8F', alpha=0.8, style='italic', fontweight='bold')

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Exposicao (%)', fraction=0.025, pad=0.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '11_scatter_degree_exposicao.png'), dpi=150, bbox_inches='tight')
    plt.close()
    ok('11_scatter_degree_exposicao.png')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MAIN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if __name__ == '__main__':
    print('Gerando grafos SNA...\n')
    grafo_one_mode_baseline()
    grafo_one_mode_estresse()
    grafo_two_mode()
    heatmap_centralidades()
    grafo_betweenness()
    barras_degree_comparativo()
    barras_exposicao_insumos()
    grafo_kcore()
    grafo_projecao_bipartida()
    grafo_fragmentacao_incremental()
    scatter_degree_exposicao()
    print('\n[DONE] Todos os grafos salvos em: ' + OUT)

