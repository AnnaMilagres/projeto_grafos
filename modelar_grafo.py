import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def limpar_valor(valor):
    if pd.isna(valor):
        return valor
    valor = str(valor)
    valor = valor.replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return None

df_trends = pd.read_csv('multiTimeline.csv', header=1)  
df_trends['Data'] = pd.to_datetime(df_trends['Semana'])

try:
    df_pagamentos = pd.read_csv('pagamentos-publicidade-2017.csv', delimiter=';', encoding='ISO-8859-1')
except UnicodeDecodeError:
    df_pagamentos = pd.read_csv('pagamentos-publicidade-2017.csv', delimiter=';', encoding='utf-16')

df_pagamentos.columns = df_pagamentos.columns.str.strip()

df_clean = df_pagamentos[['Agencia', 'Subcontratado', 'Bruto PI']].dropna()
df_clean['Bruto PI'] = df_clean['Bruto PI'].apply(limpar_valor)
df_clean = df_clean.dropna(subset=['Bruto PI'])

threshold = 300000

df_filtered = df_clean[df_clean['Bruto PI'] >= threshold]

df_correio_braziliense = df_filtered[df_filtered['Subcontratado'].str.contains('Correio Braziliense', case=False, na=False)]

G = nx.Graph()

for i in range(len(df_trends)):
    data = df_trends['Data'].iloc[i]
    popularidade = df_trends[df_trends.columns[1]].iloc[i]
    G.add_node(data, type='trends', popularity=popularidade)

for _, row in df_correio_braziliense.iterrows():
    agencia = row['Agencia']
    valor_bruto_pi = row['Bruto PI']
    
    G.add_node(agencia, type='pagamento', valor=valor_bruto_pi)
    
    for data in df_trends['Data']:
        G.add_edge(data, agencia, weight=valor_bruto_pi)

node_colors = []
node_sizes = []

for node in G.nodes():
    if G.nodes[node]['type'] == 'trends':
        node_colors.append(G.nodes[node].get('popularity', 0))
        node_sizes.append(G.nodes[node].get('popularity', 0) * 0.1)
    else:
        node_colors.append(0)
        node_sizes.append(G.nodes[node].get('valor', 0) * 0.1)

node_sizes = [max(size, 20) for size in node_sizes]

plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, seed=42)

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap='coolwarm', node_shape='o')
edges = nx.draw_networkx_edges(G, pos)
labels = nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=8)

cbar_ax = plt.gca().inset_axes([0.85, 0.1, 0.03, 0.8])
sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
sm.set_array([])
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('Popularidade')

plt.title('Grafo de Popularidade do Google Trends e Pagamentos ao Correio Braziliense')
plt.show()
