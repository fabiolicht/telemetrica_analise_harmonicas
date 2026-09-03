#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:24:56 2026

@author: fabiolicht
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuração de estilo alinhada a padrões acadêmicos
sns.set_theme(style='whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    'Caracterização do Dataset do Data Center (UCO)',
    fontsize=14,
    fontweight='bold',
    y=1.03,
)

# Leitura do dataset .XLSX
df = pd.read_excel('Dataset_data_center.xlsx')

# Painel A: Distribuição e KDE da Potência Ativa Total (ptotal)
sns.histplot(
    df['ptotal'],
    kde=True,
    ax=ax1,
    color='#2b5c8f',
    bins=30,
    edgecolor='black',
    alpha=0.6,
)
ax1.set_title(
    'A) Distribuição da Potência Ativa Total ($P_{total}$ [W])',
    fontsize=11,
    fontweight='bold',
)
ax1.set_xlabel('Potência Ativa Total (W)', fontsize=10)
ax1.set_ylabel('Frequência Absoluta (Amostras)', fontsize=10)

# Painel B: Composição das Correntes RMS por Fase (irmsa, irmsb, irmsc)
currents_df = df[['irmsa', 'irmsb', 'irmsc']].melt(
    var_name='Fase', value_name='Corrente RMS (A)'
)
currents_df['Fase'] = currents_df['Fase'].replace(
    {'irmsa': 'Fase A', 'irmsb': 'Fase B', 'irmsc': 'Fase C'}
)
sns.boxplot(
    x='Fase',
    y='Corrente RMS (A)',
    data=currents_df,
    ax=ax2,
    palette=['#3b82f6', '#10b981', '#f59e0b'],
)
ax2.set_title(
    'B) Composição das Correntes RMS por Fase', fontsize=11, fontweight='bold'
)
ax2.set_xlabel('Fase do Sistema Trifásico', fontsize=10)
ax2.set_ylabel('Corrente RMS (A)', fontsize=10)

plt.tight_layout()
plt.savefig('dataset_caracterizacao_uco.png', dpi=300, bbox_inches='tight')
plt.show()

# Impressão de estatísticas descritivas para auxílio na discussão
print('--- Estatísticas Descritivas ---')
print(
    df[['ptotal', 'irmsa', 'irmsb', 'irmsc', 'thdva', 'thdia']].describe().loc[
        ['count', 'mean', 'std', 'min', 'max']
    ]
)