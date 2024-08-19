import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Carregar o DataFrame com o delimitador correto e codificação apropriada
try:
    df = pd.read_csv('pagamentos-publicidade-2017.csv', encoding='ISO-8859-1')
except UnicodeDecodeError:
    df = pd.read_csv('pagamentos-publicidade-2017.csv', encoding='utf-16')

# Verificar os nomes das colunas
print("Nomes das colunas:", df.columns)

# Limpar espaços e caracteres especiais nos nomes das colunas
df.columns = df.columns.str.strip()

# Verificar novamente os nomes das colunas após a limpeza
print("Nomes das colunas após limpeza:", df.columns)

# Selecionar as colunas e remover linhas com valores ausentes
try:
    df_clean = df[['Agencia', 'Subcontratado', 'Bruto PI']].dropna()
except KeyError as e:
    print(f"Erro: {e}")
    print("Certifique-se de que as colunas 'Agencia', 'Subcontratado' e 'Bruto PI' existem no DataFrame.")
    exit()

# Converter valores da coluna 'Bruto PI' para float, substituindo vírgulas por pontos
df_clean['Bruto PI'] = df_clean['Bruto PI'].str.replace(',', '.').astype(float)

# Criar o grafo
G = nx.Graph()

# Adicionar arestas ao grafo
for _, row in df_clean.iterrows():
    agencia = row['Agencia']
    subcontratado = row['Subcontratado']
    valor_bruto_pi = row['Bruto PI']
    
    G.add_edge(agencia, subcontratado, weight=valor_bruto_pi)

# Desenhar o grafo
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', edge_color='gray')

# Adicionar rótulos das arestas
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

plt.title('Grafo de Agências e Subcontratados')
plt.show()
