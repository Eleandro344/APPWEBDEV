import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM remessa_sofisa" # SELECIONA A TABELA 
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
consulta = "SELECT * FROM retorno_sofisa" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()

remessa['CODIGO DO DOC'] = pd.to_numeric(remessa['CODIGO DO DOC'], errors='coerce').fillna(0)

# Converter a coluna para int
remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)


retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['Código de movimento remessa'] == 'Solicitaçã']
linhas_pedido_baixa = linhas_pedido_baixa[['Data da Gravação do Arquivo','Número de inscrição do Pagador','Nome do Pagador','Código de movimento remessa','CODIGO DO DOC','Data de vencimento do boleto']]
numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']
docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]

docs_filtrados['Data da ocorrência'] = pd.to_datetime(docs_filtrados['Data da ocorrência'])

docs_filtrados = docs_filtrados[['CODIGO DO DOC','Data da ocorrência','Nome do banco','Tipo de cobrança','Valor nominal do boleto','Código movimento retorno']]
# Primeiro, vamos ordenar o DataFrame pela coluna 'DATA DA GERAÇÃO DO ARQUIVO' para garantir que a data mais recente apareça primeiro
df_sorted = docs_filtrados.sort_values(by='Data da ocorrência', ascending=False)

# Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento
indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data da ocorrência'].idxmax()

# Agora, vamos usar esses índices para selecionar os registros correspondentes
docs_mais_recentes = df_sorted.loc[indices_mais_recentes]

# Exibindo os documentos mais recentes
resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')

from datetime import datetime, timedelta
data_de_hoje = datetime.now()
data_de_hoje = data_de_hoje - timedelta(days=5)

data_de_hoje = data_de_hoje.strftime('%d/%m/%y') 

print(resultado_merge['Data de vencimento do boleto'])
resultado_merge['Data de vencimento do boleto'] = pd.to_datetime(resultado_merge['Data de vencimento do boleto'], format='%d/%m/%y')

#resultado_merge['Data de vencimento do Título'] = pd.to_datetime(resultado_merge['Data de vencimento do Título'], format='%d/%m/%y')
resultado_merge = resultado_merge[resultado_merge['Data de vencimento do boleto'] >= data_de_hoje]


df_ordenado = resultado_merge.sort_values(by='Data de vencimento do boleto')




df_ordenado.loc[df_ordenado['Código de movimento remessa'] == 'Solicitaçã', 'Código de movimento remessa'] = "Solicitado Baixa"

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
    'Número de inscrição do Pagador':'CNPJ',




    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)
dfcanceladosofisa = df_ordenado.drop(columns=['Instrução de Origem'])


dfcanceladosofisa.loc[dfcanceladosofisa['Status Atual'] == '28', 'Status Atual'] = "Débito de Tarifas/Custas – Correspondentes"
dfcanceladosofisa.loc[dfcanceladosofisa['Status Atual'] == '23', 'Status Atual'] = "Título enviado para cartório"
dfcanceladosofisa.loc[dfcanceladosofisa['Status Atual'] == '43', 'Status Atual'] = "Baixado por ter sido protestado"
#print(dfcanceladosofisa)