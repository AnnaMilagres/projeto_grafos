import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def limpar_valor(valor):
    if pd.isna(valor):
        return valor
    valor = str(valor)
    valor = valor.replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return None

try:
    df = pd.read_csv('pagamentos-publicidade-2017.csv', delimiter=';', encoding='ISO-8859-1')
except UnicodeDecodeError:
    df = pd.read_csv('pagamentos-publicidade-2017.csv', delimiter=';', encoding='utf-16')

print("Nomes das colunas:", df.columns)

df.columns = df.columns.str.strip()

print("Nomes das colunas após limpeza:", df.columns)

try:
    df_clean = df[['Agencia', 'Subcontratado', 'Bruto PI']].dropna()
except KeyError as e:
    print(f"Erro: {e}")
    print("Certifique-se de que as colunas 'Agencia', 'Subcontratado' e 'Bruto PI' existem no DataFrame.")
    exit()

df_clean['Bruto PI'] = df_clean['Bruto PI'].apply(limpar_valor)

df_clean = df_clean.dropna(subset=['Bruto PI'])

G = nx.Graph()

for _, row in df_clean.iterrows():
    agencia = row['Agencia']
    subcontratado = row['Subcontratado']
    valor_bruto_pi = row['Bruto PI']
    
    G.add_edge(agencia, subcontratado, weight=valor_bruto_pi)

plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=100, node_color='lightblue', edge_color='pink', font_size=6)

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

plt.title('Grafo de Agências e Subcontratados')
plt.show()
