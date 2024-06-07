from dash import html
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import subprocess
import pandas as pd
import win32com.client as win32
import datetime as dt
import statistics
import numpy as np
import locale
from datetime import date
from app import app  # Importa o objeto app do arquivo app.py
from datetime import datetime
from components.cancelados_santander import df_ordenadosantander
from components.sofisa_cancelados import dfcanceladosofisa
from components.safra_cancelados import cancelados_safra
from components.antecipacao import df_antecipacao
from components.itau_cancelados import cancelados_itau

import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM unicredremessa" # SELECIONA A TABELA 
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
consulta = "SELECT * FROM retornounicred" # SELECIONA A TABELA 
retorno = pd.read_sql(consulta, con=mydb) # TRANSFORMA EM DATAFRAME 

# Feche a conexão
mydb.close()


remessa['CODIGO DO DOC'] = remessa['CODIGO DO DOC'].astype(int)
retorno['CODIGO DO DOC'] = retorno['CODIGO DO DOC'].astype(int)
linhas_pedido_baixa = remessa.loc[remessa['Identificação da Ocorrência'] == 'Pedido de ']


#REMESSA
linhas_pedido_baixa = linhas_pedido_baixa[['Data da Gravação do Arquivo','Nº Inscrição do Pagador','Nome do Banco por Extenso','Valor do Título','Nome/Razão Social do Pagador','Identificação da Ocorrência','CODIGO DO DOC','Data de vencimento do Título']]
numero_de_docs  = linhas_pedido_baixa['CODIGO DO DOC']
docs_filtrados = retorno[retorno['CODIGO DO DOC'].isin(numero_de_docs)]
docs_filtrados['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(docs_filtrados['DATA DA GERAÇÃO DO ARQUIVO'])
docs_filtrados = docs_filtrados[['CODIGO DO DOC','DATA DA GERAÇÃO DO ARQUIVO','TIPO DE INSTRUÇÃO ORIGEM','CÓDIGO DE MOVIMENTO']]


condicao = (docs_filtrados['TIPO DE INSTRUÇÃO ORIGEM'] == ' Pedido de Baixa') & (docs_filtrados['CÓDIGO DE MOVIMENTO'] == 'Instrução Confirmada')

# Atualizar o valor da coluna "Ocorrencia" para "boleto protestado" onde a condição for verdadeira
docs_filtrados.loc[condicao, 'CÓDIGO DE MOVIMENTO'] = 'Boleto Baixado'



# Primeiro, vamos ordenar o DataFrame pela coluna 'DATA DA GERAÇÃO DO ARQUIVO' para garantir que a data mais recente apareça primeiro
df_sorted = docs_filtrados.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO', ascending=False)

# Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento
indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['DATA DA GERAÇÃO DO ARQUIVO'].idxmax()

# Agora, vamos usar esses índices para selecionar os registros correspondentes
docs_mais_recentes = df_sorted.loc[indices_mais_recentes]

resultado_merge = pd.merge(linhas_pedido_baixa, docs_mais_recentes, on='CODIGO DO DOC', how='inner')








df_ordenado = resultado_merge.sort_values(by='Data de vencimento do Título')
#df_ordenado['Data da Gravação do Arquivo'] = pd.to_datetime(df_ordenado['Data da Gravação do Arquivo'])
# Converter a coluna 'Data da Ocorrencia' para o formato de data do pandas
#df_ordenado['Data da Gravação do Arquivo'] = pd.to_datetime(df_ordenado['Data da Gravação do Arquivo'], format='%d%m%y', errors='coerce')

# Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
#df_ordenado['Data da Gravação do Arquivo'] = df_ordenado['Data da Gravação do Arquivo'].dt.strftime('%d/%m/%Y')
df_ordenado.loc[df_ordenado['Identificação da Ocorrência'] == 'Pedido de ', 'Identificação da Ocorrência'] = "Solicitado Baixa"
df_ordenado['Ordem'] = "Cema Paga"
novos_nomes = {
    'Data da Gravação do Arquivo': 'Data da Ocorrencia',
    'Identificação da Ocorrência': 'Ocorrencia',
    'Data de vencimento do Título':'Vencimento',
    'DATA DA GERAÇÃO DO ARQUIVO': 'Ultima ocorrencia',
    'TIPO DE INSTRUÇÃO ORIGEM': 'Instrução de Origem',
    'CÓDIGO DE MOVIMENTO':'Status Atual',
    'Nome do Banco por Extenso':'Banco',
    'Nº Inscrição do Pagador':'CNPJ',
    
    # ... adicione os outros nomes conforme necessário
}
df_ordenado.rename(columns=novos_nomes, inplace=True)
df_ordenado = df_ordenado.drop(columns=['Ultima ocorrencia'])

df_ordenado.loc[df_ordenado['Status Atual'] == 'Protesto solicitado', 'Status Atual'] = "Enviado a Cartorio"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Título Descontável (título com desistênc', 'Status Atual'] = "Devolvido"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Instrução Confirmada', 'Status Atual'] = "Aceito"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Liquidação de Título Descontado', 'Status Atual'] = "Liquidação de Título Trocado"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Título Descontado', 'Status Atual'] = "Trocado"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Pago(Título protestado pago em cartório)', 'Status Atual'] = "Pago em Cartório"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Pedido de ', 'Status Atual'] = "Solicitação de Baixa"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Protesto Em cartório', 'Status Atual'] = "Em cartório"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Sustação solicitada', 'Status Atual'] = "Em cartório"

#df_remessa.loc[df_remessa['TIPO DE INSTRUÇÃO ORIGEM'] == 'Protesto Em cartório', 'TIPO DE INSTRUÇÃO ORIGEM'] = "Em cartório"

condicao = (df_ordenado['Instrução de Origem'] == 'Protestar') & (df_ordenado['Status Atual'] == 'Instrução Confirmada')

# Atualizar o valor da coluna "Ocorrencia" para "boleto protestado" onde a condição for verdadeira
df_ordenado.loc[condicao, 'Status Atual'] = 'Boleto Protestado'


df_ordenado = df_ordenado.drop(columns=['Instrução de Origem'])



df_ordenado.loc[df_ordenado['Status Atual'] == 'Liquidação de Título Trocado', 'Ordem'] = "Não pagar"
#df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento'])
df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento'], format='%d%m%y')
df_ordenado['Data da Ocorrencia'] = pd.to_datetime(df_ordenado['Data da Ocorrencia'], format='%d%m%y')





df_ordenado = pd.concat([df_ordenado, df_ordenadosantander], ignore_index=True)
df_ordenado = pd.concat([df_ordenado, dfcanceladosofisa], ignore_index=True)
df_ordenado = pd.concat([df_ordenado,cancelados_safra],ignore_index=True)
df_ordenado = pd.concat([df_ordenado,cancelados_itau],ignore_index=True)
df_ordenado.loc[df_ordenado['Status Atual'] == 'Liquidação Normal', 'Ordem'] = "Não pagar"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Em cartório', 'Ordem'] = "Não pagar"
df_ordenado.loc[df_ordenado['Status Atual'] == 'LIQUIDAÇÃO EM CARTÓRIO', 'Ordem'] = "Não pagar"
df_ordenado.loc[df_ordenado['Status Atual'] == 'Pago em Cartório', 'Ordem'] = "Não pagar"
df_ordenado.loc[df_ordenado['Status Atual'] == 'LIQUIDAÇÃO NORMAL', 'Ordem'] = "Não pagar"

df_ordenado.loc[df_ordenado['Status Atual'] == 'Boleto Baixado', 'Ordem'] = "Não pagar"



df_ordenado.loc[df_ordenado['Ocorrencia'] == 'Solicitaçã', 'Ocorrencia'] = "Solicitado Baixa"


from datetime import datetime, timedelta





data_hoje_menos_5_dias = pd.Timestamp.today().normalize() - timedelta(days=40)
df_ordenado = df_ordenado.loc[df_ordenado['Vencimento'] >= data_hoje_menos_5_dias]

df_ordenado = df_ordenado.sort_values(by='Vencimento')

hoje = datetime.now().date()
df_ordenado = df_ordenado[df_ordenado['Vencimento'] <= pd.to_datetime(hoje)]
df_ordenado = df_ordenado.loc[df_ordenado['Ordem'] =='Cema Paga']
# data_de_hoje = datetime.now()


# data_de_hoje = data_de_hoje - timedelta(days=5)

# data_de_hoje = data_de_hoje.strftime('%d/%m/%y') 
# df_ordenado = resultado_merge[df_ordenado['Vencimento'] >= data_de_hoje]


#df_ordenado['Nome/Razão Social do Pagador'] = df_ordenado['Nome/Razão Social do Pagador'].str.lower()

#df_ordenado['CNPJ'] = df_ordenado['CNPJ'].astype(str)
#
df_ordenado = pd.merge(df_ordenado, df_antecipacao, on='CNPJ', how='left')


df_ordenado.loc[df_ordenado['Status Atual'] == 'BAIXA COM TRANSFERÊNCIA PARA D', 'Status Atual'] = "DEVOLVIDO"




# Selecione apenas os dados a partir da data de hoje
# data_de_hoje = pd.Timestamp.today().normalize()  # Hoje à meia-noite
# df_ordenado = df_ordenado.loc[df_ordenado['Vencimento'] >= data_de_hoje]

# df_ordenado = df_ordenado.sort_values(by='Vencimento')

#df_ordenado['Vencimento'] = df_ordenado['Vencimento'].apply(lambda x: x.strftime("%d/%m/%Y"))

#data_atualteste = datetime.now()

# Data há cinco dias atrás
#data_5_dias_atras = data_atualteste - timedelta(days=5)

# Selecionar as linhas que estão dentro do intervalo de cinco dias atrás até a data atual
#df_ordenado = df_ordenado[(df_ordenado['Vencimento'] >= data_5_dias_atras) ]



# Obtendo a data de hoje
data_de_hoje = datetime.now()

# Adicionando um dia à data de hoje
data_de_hoje_mais_um_dia = data_de_hoje + timedelta(days=0)

# Convertendo a data para o formato desejado ('%Y-%m-%d')
data_de_hoje_mais_um_dia_formatada = data_de_hoje_mais_um_dia.strftime('%Y-%m-%d')

#df_ordenado['Vencimento'] = df_ordenado['Vencimento'].astype(str)

df_ordenado.loc[df_ordenado['IA'].isna(), 'IA'] = '0,0 %'

df_ordenado['Vencimento'] = df_ordenado['Vencimento'].dt.strftime('%d/%m/%Y')

#df_ordenado.to_excel("C:/Users/elean/Desktop/bancodedados/relatorioitau2205.xlsx")


# REMOVER DOCS ERRADOS
codigos_para_remover = [401326, 406866, 406858]
df_ordenado = df_ordenado[~df_ordenado['CODIGO DO DOC'].isin(codigos_para_remover)]


def layout():
    return dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H3('Boletos a pagar', className='text-titulo',style={'margin-top': '50px'}),
        ),
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker-range',
                display_format='DD/MM/YYYY',
                style={'margin-top': '15px', 'margin-bottom': '15px'}  # Adiciona espaço acima e abaixo do filtro
            ),
            width=3,  # Ajuste a largura da coluna para mover o componente para a direita
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='data-table',
                data=df_ordenado.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in df_ordenado.columns],
                # page_size=10,  # Defina o número de linhas por página
                style_table={'overflowX': 'auto', 'width': '150%', 'margin-top':'30px','margin-left': '-24%', 'margin-right': 'auto', 'z-index': '0','border': 'none'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold','color': 'Black','fontFamily': 'Arial'},
                style_cell={'textAlign': 'left','fontSize': '15px','minWidth': '100px', 'fontFamily': 'Arial'}, # Estilo das células
                        style_data_conditional=[
                    {  'if': {'row_index': 'odd'},
                       'backgroundColor': 'rgb(248, 248, 248)',
                    },
                       {
                         'if': {'column_id': 'Ordem'},
                        'backgroundColor': 'red',
                        'color': 'white',
                    },
                   # {
                    #    'if': {'column_id': 'Vencimento'},
                     #   'backgroundColor': 'Goldenrod',
                      #  'color': 'white',
                    #},
                    {
                         'if': {'column_id': 'Status Atual'},
                        'backgroundColor': 'red',
                        'color': 'white',
                    },   
                    {
                         'if': {'column_id': 'IA'},
                        'backgroundColor': 'LightCyan',
                        'color': 'black',
                    },                       

            #       {
            #     'if': {'column_id': 'Status Atual', 'filter_query': '{Status Atual} eq "Boleto Baixado Conforme Instrução"'},
            #     'backgroundColor': 'ForestGreen',
            #     'color': 'white',
            # },
                              {
                'if': {'column_id': 'Ordem', 'filter_query': '{Ordem} eq "Não pagar"'},
                'backgroundColor': 'ForestGreen',
                'color': 'white',
            },  
            {
                'if': {'column_id': 'Vencimento', 'filter_query': '{Vencimento} eq "' + data_de_hoje_mais_um_dia_formatada  + '"'},
                'backgroundColor': 'yellow',
                'color': 'black',
            },                             


                ],

            ),
        ),
    ]),
        dbc.Col(
            html.H3('(IA) Probabilidade de antecipação do titulo pelo Pagador', className='text-ia',style={'margin-top': '50px'}),
        ),
    ])

