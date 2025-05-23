import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conexao = sqlite3.connect('dados_vendas.db')

cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas1 (
id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
data_venda DATE,
produto TEXT,
categoria TEXT,
valor_venda REAL
)
''')

cursor.execute('''
INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda) VALUES
('2023-01-01', 'Produto A', 'Eletrônicos', 1500.00),
('2023-01-05', 'Produto B', 'Roupas', 350.00),
('2023-02-10', 'Produto C', 'Eletrônicos', 1200.00),
('2023-03-15', 'Produto D', 'Livros', 200.00),
('2023-03-20', 'Produto E', 'Eletrônicos', 800.00),
('2023-04-02', 'Produto F', 'Roupas', 400.00),
('2023-05-05', 'Produto G', 'Livros', 150.00),
('2023-06-10', 'Produto H', 'Eletrônicos', 1000.00),
('2023-07-20', 'Produto I', 'Roupas', 600.00),
('2023-08-25', 'Produto J', 'Eletrônicos', 700.00),
('2023-09-30', 'Produto K', 'Livros', 300.00),
('2023-10-05', 'Produto L', 'Roupas', 450.00),
('2023-11-15', 'Produto M', 'Eletrônicos', 900.00),
('2023-12-20', 'Produto N', 'Livros', 250.00);
''')

conexao.commit()

df = pd.read_sql_query("SELECT * FROM vendas1", conexao)
df['data_venda'] = pd.to_datetime(df['data_venda'])

# Adicionar colunas auxiliares, para mes e colocamos a coluna mes_nome no formato de dada
df['mes'] = df['data_venda'].dt.month
df['mes_nome'] = df['data_venda'].dt.strftime('%b')

# Usamos o groupby para agrupar valores das colunas categoria e valor_de_vendas e somamos resetando os index
vendas_categoria = df.groupby('categoria')['valor_venda'].sum().reset_index()

# Usamos o gruupby para agrupar a coluna mes_nome e valor de venda somando e indexando com os nomes dos meses 
vendas_mes = df.groupby('mes_nome')['valor_venda'].sum().reindex(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
)

# Usamos o loc para selecionar a coluna valor venda e filtrar o produto com maior e menor valor de venda
produto_max = df.loc[df['valor_venda'].idxmax()]
produto_min = df.loc[df['valor_venda'].idxmin()]

# Gráfico Total de vendas por categoria
plt.figure(figsize=(8,5))
sns.barplot(data=vendas_categoria, x='categoria', y='valor_venda', palette='pastel')
plt.title('Total de Vendas por Categoria')
plt.ylabel('Valor (R$)')
plt.xlabel('Categoria')
plt.tight_layout()
plt.show()

# Gráfico Total de vendas por mês
plt.figure(figsize=(10,5))
vendas_mes.plot(kind='bar', color='skyblue')
plt.title('Total de Vendas por Mês')
plt.ylabel('Valor (R$)')
plt.xlabel('Mês')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico Tendência de vendas ao longo do ano
plt.figure(figsize=(10,5))
sns.lineplot(data=df, x='data_venda', y='valor_venda', marker='o')
plt.title('Tendência de Vendas ao Longo do Ano')
plt.ylabel('Valor (R$)')
plt.xlabel('Data da Venda')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Fechar a conexão
conexao.close()
