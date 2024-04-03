import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM remessa_safra" # SELECIONA A TABELA 
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
consulta = "SELECT * FROM retorno_safra" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()

#remessa['CODIGO DO DOC'] = pd.to_numeric(remessa['CODIGO DO DOC'], errors='coerce').fillna(0)

# Converter a coluna para int
remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)


retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['Cod. Ocorrência'] == 'PEDIDO DE BAIXA']
linhas_pedido_baixa = linhas_pedido_baixa[['Data da Gravação do Arquivo','Nome Do Pagador','Número de Inscrição do Pagador','Cod. Ocorrência','CODIGO DO DOC','Vencimento']]
numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']
docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]
docs_filtrados = docs_filtrados[['CODIGO DO DOC','Data Da Ocorrência No Banco','Nome Do Banco Por Extenso','Valor Título','Identifica  o Da Ocorrência (Retorno)']]
# Certifique-se de que a coluna de datas é do tipo datetime
docs_filtrados['Data Da Ocorrência No Banco'] = pd.to_datetime(docs_filtrados['Data Da Ocorrência No Banco'])

# Ordene o DataFrame pela coluna de datas para garantir que a data mais recente apareça primeiro
df_sorted = docs_filtrados.sort_values(by='Data Da Ocorrência No Banco', ascending=False)

# Identifique os índices dos registros com a data mais recente para cada número de documento
indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data Da Ocorrência No Banco'].idxmax()

# Use esses índices para selecionar os registros correspondentes
docs_mais_recentes = df_sorted.loc[indices_mais_recentes]

# Exiba os documentos mais recentes

df_ordenado = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')
from datetime import datetime

data_de_hoje = datetime.now().strftime('%d/%m/%y')
df_ordenado['Ordem'] = "Cema Paga"
df_ordenado.loc[df_ordenado['Cod. Ocorrência'] == 'LIQUIDAÇÃO NORMAL', 'Ordem'] = "Não pagar"
novos_nomes = {
    'Data da Gravação do Arquivo': 'Data da Ocorrencia',
    'Cod. Ocorrência': 'Ocorrencia',
    'Vencimento':'Vencimento',
    'Identifica  o Da Ocorrência (Retorno)':'Status Atual',
    'Nome Do Banco Por Extenso':'Banco',
    'Valor Título':'Valor do Título',
    'Nome Do Pagador':'Nome/Razão Social do Pagador',
    'Número de Inscrição do Pagador':'CNPJ',

    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)
cancelados_safra = df_ordenado.drop(columns=['Data Da Ocorrência No Banco'])

#print(cancelados_safra)