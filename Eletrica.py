#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:24:56 2026

@author: fabiolicht
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 300
})

def analisar_dataset_metadados(caminho_csv):
    if not os.path.exists(caminho_csv):
        print(f"Erro: O arquivo {caminho_csv} não foi encontrado no diretório atual.")
        return
        
    # Carregamento do dataset
    df = pd.read_csv(caminho_csv)
    
    print("\n" + "="*50)
    print("RESUMO ESTATÍSTICO DO DATASET DE HARMÔNICAS")
    print("="*50)
    print(f"Total de registros catalogados: {len(df)}")
    print(f"Colunas disponíveis: {', '.join(df.columns)}")
    
    if 'tone_frequency_hz' in df.columns:
        freq_stats = df['tone_frequency_hz'].describe()
        print("\nEstatísticas da Frequência de Tom (Hz):")
        print(freq_stats.round(2))
        
    print("="*50)

    # Criação da grade de gráficos para o artigo
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Caracterização do Dataset de Sinais Harmônicos', fontweight='bold', fontsize=16)
    
    # Gráfico 1: Histograma das Frequências
    if 'tone_frequency_hz' in df.columns:
        sns.histplot(data=df, x='tone_frequency_hz', bins=40, kde=True, ax=axes[0], color='tab:blue')
        axes[0].set_title('A) Distribuição das Frequências (Hz)')
        axes[0].set_xlabel('Frequência de Injeção (Hz)')
        axes[0].set_ylabel('Frequência Absoluta (Amostras)')
    
    # Gráfico 2: Contagem de anomalias por categoria
    if 'category1' in df.columns:
        sns.countplot(data=df, y='category1', ax=axes[1], palette='viridis', order=df['category1'].value_counts().index)
        axes[1].set_title('B) Composição das Categorias de Sinais')
        axes[1].set_xlabel('Quantidade de Amostras')
        axes[1].set_ylabel('Categoria / Tipo de Onda')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('Caracterizacao_Dataset_Harmonicas.png', bbox_inches='tight')
    plt.show()
    
    print("\nProcessamento concluído. O gráfico 'Caracterizacao_Dataset_Harmonicas.png' foi gerado para anexação ao artigo.")

if __name__ == "__main__":
    ARQUIVO_METADADOS = 'harmonic_signals_dataset_metadata.csv'
    analisar_dataset_metadados(ARQUIVO_METADADOS)