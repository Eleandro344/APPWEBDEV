import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM remessa_sicoob" # SELECIONA A TABELA 
remessa = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()

import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM retorno_sicoob" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()

remessa['CODIGO DO DOC'] = pd.to_numeric(remessa['CODIGO DO DOC'], errors='coerce').fillna(0)

# Converter a coluna para int
remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)


retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['Ocorrencia'] == 'Solicitação de Baixa']


linhas_pedido_baixa = linhas_pedido_baixa[['Data de Geração do Arquivo header','Valor do Título','Nome do Banco','Ocorrencia','CODIGO DO DOC','Vencimento','Numero sequencial Header']]
numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']
docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]

docs_filtrados = docs_filtrados[['CODIGO DO DOC','Data de Geração do Arquivo header','Cnpj','Nome','Ocorrencia']]
docs_filtrados['Data de Geração do Arquivo header'] = pd.to_datetime(docs_filtrados['Data de Geração do Arquivo header'], format='%d%m%Y')

# Primeiro, vamos ordenar o DataFrame pela coluna 'DATA DA GERAÇÃO DO ARQUIVO' para garantir que a data mais recente apareça primeiro
df_sorted = docs_filtrados.sort_values(by='Data de Geração do Arquivo header', ascending=False)

# Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento
indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data de Geração do Arquivo header'].idxmax()

# Agora, vamos usar esses índices para selecionar os registros correspondentes
docs_mais_recentes = df_sorted.loc[indices_mais_recentes]

resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')

resultado_merge['Vencimento'] = pd.to_datetime(resultado_merge['Vencimento'], format='%d%m%Y')

resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')
from datetime import datetime
df_ordenado = resultado_merge
df_ordenado.loc[df_ordenado['Ocorrencia_x'] == 'PEDIDO DE BAIXA', 'Ocorrencia_x'] = "Solicitação de Baixa"

df_ordenado['Ordem'] = "Cema Paga"
df_ordenado.loc[df_ordenado['Ocorrencia_y']== 'BAIXA SIMPLES', 'Ordem'] = "Não pagar"
df_ordenado = df_ordenado.drop(columns=['Numero sequencial Header'])
df_ordenado = df_ordenado.drop(columns=['Data de Geração do Arquivo header_x'])

novos_nomes = {
    'Data de Geração do Arquivo header_y': 'Data da Ocorrencia',
    'Ocorrencia_x': 'Ocorrencia',
    'Vencimento':'Vencimento',
    'Ocorrencia_y':'Status Atual',
    'Nome do Banco':'Banco',
    'Valor do Título':'Valor do Título',
    'Nome':'Nome/Razão Social do Pagador',
    'Cnpj':'CNPJ',



    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)
df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento'], format='%d%m%Y')

cancelados_sicoob = df_ordenado
