
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv('pagamentos-publicidade-2017.csv', encoding='ISO-8859-1', delimiter=';')

# Limpar e converter a coluna ' Bruto PI ' para float
df[' Bruto PI '] = df[' Bruto PI '].str.replace('.', '', regex=False)  # Remove o ponto dos milhares
df[' Bruto PI '] = df[' Bruto PI '].str.replace(',', '.', regex=False)  # Substitui vírgula por ponto para decimal
df[' Bruto PI '] = df[' Bruto PI '].astype(float)  # Converte para float

# Criar um grafo vazio
G = nx.Graph()

# Preencher o grafo com os dados
for _, row in df.iterrows():
    agencia = row['Agencia']
    subcontratado = row['Subcontratado']
    valor_bruto_pi = row[' Bruto PI ']
    
    # Adicionar a aresta com o peso correspondente ao valor da campanha
    G.add_edge(agencia, subcontratado, weight=valor_bruto_pi)

# Desenhar o grafo
plt.figure(figsize=(120,120))
pos = nx.spring_layout(G, k=0.15, seed=42)  # Define o layout para visualização e uma semente para reprodução consistente

# Desenhar nós
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')

# Desenhar arestas
nx.draw_networkx_edges(G, pos, edge_color='gray')

# Desenhar rótulos dos nós
nx.draw_networkx_labels(G, pos, font_size=8)

# Desenhar rótulos das arestas com pesos
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.show()
