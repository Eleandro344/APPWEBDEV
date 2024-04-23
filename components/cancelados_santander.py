import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta


import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM remessa_santander" # SELECIONA A TABELA 
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
consulta = "SELECT * FROM retorno_santander" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()
remessa = remessa.loc[remessa['CODIGO DO DOC'] != 0]

remessa['CODIGO DO DOC'] = pd.to_numeric(remessa['CODIGO DO DOC'], errors='coerce').fillna(0)

# Converter a coluna para int
remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)

retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['Código de movimento remessa'] == 'Solicitaçã']
linhas_pedido_baixa = linhas_pedido_baixa[['Data da Gravação do Arquivo','Número de inscrição do Pagador','Código de movimento remessa','CODIGO DO DOC','Data de vencimento do boleto']]

numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']

docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]

docs_filtrados['Data da ocorrência'] = pd.to_datetime(docs_filtrados['Data da ocorrência'])

docs_filtrados = docs_filtrados[['CODIGO DO DOC','Data da ocorrência','Nome do Pagador','Nome do banco','Tipo de cobrança','Valor nominal do boleto','Código movimento retorno']]

df_sorted = docs_filtrados.sort_values(by='Data da ocorrência', ascending=False)

indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data da ocorrência'].idxmax()
docs_mais_recentes = df_sorted.loc[indices_mais_recentes]

resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')


data_de_hoje = datetime.now()

data_de_hoje = data_de_hoje - timedelta(days=0)

data_de_hoje = data_de_hoje.strftime('%d/%m/%y') 

resultado_merge['Data de vencimento do boleto'] = pd.to_datetime(resultado_merge['Data de vencimento do boleto'], format='%d/%m/%y')


df_ordenado = resultado_merge.sort_values(by='Data de vencimento do boleto')
resultado_merge = resultado_merge[resultado_merge['Data de vencimento do boleto'] >= data_de_hoje]
df_ordenado.loc[df_ordenado['Código de movimento remessa'] == 'Solicitaçã', 'Código de movimento remessa'] = "Solicitado Baixa"






# Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento

# Agora, vamos usar esses índices para selecionar os registros correspondentes

# Exibindo os documentos mais recentes





df_ordenado['Ordem'] = "Cema Paga"
df_ordenado.loc[df_ordenado['Código movimento retorno'] == 'Boleto Baixado Conforme Instrução', 'Ordem'] = "Não pagar"


df_ordenado = df_ordenado.drop(columns=['Data da Gravação do Arquivo'])
novos_nomes = {
    'Data da ocorrência': 'Data da Ocorrencia',
    'Código de movimento remessa': 'Ocorrencia',
    'Data de vencimento do boleto':'Vencimento',
    'Tipo de cobrança': 'Instrução de Origem',
    'Código movimento retorno':'Status Atual',
    'Nome do banco':'Banco',
    'Valor nominal do boleto':'Valor do Título',
    'Nome do Pagador':'Nome/Razão Social do Pagador',
    'Número de inscrição do Pagador':'CNPJ'


    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)

df_ordenadosantander = df_ordenado.drop(columns=['Instrução de Origem'])

df_ordenadosantander





