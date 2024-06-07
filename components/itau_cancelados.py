import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM remessa_itau" # SELECIONA A TABELA 
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
consulta = "SELECT * FROM retorno_itau" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()

remessa['CODIGO DO DOC'] = pd.to_numeric(remessa['CODIGO DO DOC'], errors='coerce').fillna(0)

# Converter a coluna para int
remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)

retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['CÓD. DE OCORRÊNCIA'] == 'PEDIDO DE BAIXA']


linhas_pedido_baixa = linhas_pedido_baixa[['DATA DE GERAÇÃO HEADER','VALOR DO TÍTULO','NOME DO BANCO HEADER','NOME','CÓD. DE OCORRÊNCIA','CODIGO DO DOC','VENCIMENTO','NÚMERO DE INSCRIÇÃO']]
numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']
docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]

docs_filtrados = docs_filtrados[['CODIGO DO DOC','DATA DE OCORRÊNCIA','CÓD. DE OCORRÊNCIA']]
docs_filtrados['DATA DE OCORRÊNCIA'] = pd.to_datetime(docs_filtrados['DATA DE OCORRÊNCIA']).dt.strftime('%Y%m%d')
docs_filtrados['DATA DE OCORRÊNCIA'] = pd.to_datetime(docs_filtrados['DATA DE OCORRÊNCIA'])


# Ordenar o DataFrame pela coluna 'DATA DE OCORRÊNCIA' para garantir que a data mais recente apareça primeiro
df_sorted = docs_filtrados.sort_values(by='DATA DE OCORRÊNCIA', ascending=False)

# Identificar os índices dos registros com 'BAIXA SIMPLES' para cada número de documento
indices_baixa_simples = df_sorted[df_sorted['CÓD. DE OCORRÊNCIA'] == 'BAIXA SIMPLES'].groupby('CODIGO DO DOC')['DATA DE OCORRÊNCIA'].idxmax()

# Identificar os índices dos registros mais recentes para cada número de documento
indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['DATA DE OCORRÊNCIA'].idxmax()

# Combine os dois conjuntos de índices, garantindo que 'BAIXA SIMPLES' tenha prioridade
indices_combined = indices_baixa_simples.combine_first(indices_mais_recentes)

# Selecionar os registros correspondentes
docs_mais_recentes = df_sorted.loc[indices_combined]

# Exibindo os documentos finais

# Exibindo os documentos mais recentes
resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')
from datetime import datetime
data_de_hoje = datetime.now().strftime('%d/%m/%y')
df_ordenado = resultado_merge
df_ordenado.loc[df_ordenado['CÓD. DE OCORRÊNCIA_x'] == 'PEDIDO DE BAIXA', 'CÓD. DE OCORRÊNCIA_x'] = "Solicitado Baixa"

df_ordenado['Ordem'] = "Cema Paga"
df_ordenado.loc[df_ordenado['CÓD. DE OCORRÊNCIA_y'] == 'BAIXA SIMPLES', 'Ordem'] = "Não pagar"
df_ordenado = df_ordenado.drop(columns=['DATA DE GERAÇÃO HEADER'])

novos_nomes = {
    'DATA DE OCORRÊNCIA': 'Data da Ocorrencia',
    'CÓD. DE OCORRÊNCIA_x': 'Ocorrencia',
    'VENCIMENTO':'Vencimento',
    'CÓD. DE OCORRÊNCIA_y':'Status Atual',
    'NOME DO BANCO HEADER':'Banco',
    'VALOR DO TÍTULO':'Valor do Título',    
    'NOME':'Nome/Razão Social do Pagador',
    'NÚMERO DE INSCRIÇÃO':'CNPJ',

    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)
df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento'], format='%d/%m/%y')

cancelados_itau = df_ordenado

cancelados_itau