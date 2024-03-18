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


tabela_docs = pd.read_excel('C:/Users/elean/Desktop/bancodedados/docs.xlsx')

tabela_docs.loc[tabela_docs['Banco'] == 'Itau', 'Banco']= "Itau"
tabela_docs.loc[tabela_docs['Banco'] == 'Bradesco', 'Banco']= "Stratton"
tabela_docs = tabela_docs[tabela_docs['Status']!='Cancelado']
tabela_docs.loc[tabela_docs['Banco'] != 'Itau', 'TAC'] = 0
#Cria taxa de boleto
tabela_docs['Taxa de boleto'] = 0
tabela_docs.loc[tabela_docs['Banco'] == 'Itau', 'Taxa de boleto']= 0.00
tabela_docs.loc[tabela_docs['Banco'] == 'Santander', 'Taxa de boleto']= 1.35
tabela_docs.loc[tabela_docs['Banco'] == 'Unicred ES', 'Taxa de boleto']= 1.30
tabela_docs.loc[tabela_docs['Banco'] == 'Stratton', 'Taxa de boleto']= 2.00
tabela_docs = tabela_docs[tabela_docs['Status']!='Cancelado']
tabela_docs = tabela_docs[tabela_docs['Status']!='Solic. Baixa']
def contagemboletos(tabela_docs):
    # Filtra os boletos com valor igual a 'larca' na coluna 'Banco'
    boletos_larca = tabela_docs.loc[tabela_docs['Banco'] == 'Itau', 'Com Registro']

    # Verifica se há boletos com valor 'larca'
    if not boletos_larca.empty:
        contagem = boletos_larca.value_counts().values[0]
    else:
        contagem = 0

    return contagem
contagem = contagemboletos(tabela_docs)

if contagem != 0:
    valortac = 195.00 / contagem
else:
    valortac = 0.0

# Define o valor da coluna 'TAC' no DataFrame
tabela_docs['TAC'] = valortac
#tabela_docs['TAC'] = valortac.astype(float)
tabela_docs['TAC'] = tabela_docs['TAC'].round(2)

tabela_docs.loc[tabela_docs['Banco'] != 'Itau', 'TAC'] = 0

#SOMA TAXA DE BOLETO DOCS
total = tabela_docs['Com Registro'].sum()
taxaboleto = total * 1.95
taxaboleto.astype(float)

#CRIA MINHA TABELA AGRUPADA POR BANCO
faturamento = tabela_docs[['Banco','%Desc','Status','Com Registro','Valor']].groupby('Banco').sum()

# CRIA VARIAVEL HOJE COM DATA DE HOJE
hoje = dt.datetime.now()
hoje.strftime("%d/%m/%Y")
tabela_docs[["datadehoje"]] =dt.datetime.now() 
hoje.strftime("%d/%m/%Y")
from datetime import date

#data_atual = date.today()
#tabela_docs[["datadehoje"]] = data_atual = date.today()
from datetime import date

data_atual = date.today()
tabela_docs[["datadehoje"]] = data_atual = date.today()
tabela_docs['IOF'] = 0
#CRIA COLUNA MEDIA DE DIAS PARA PAGAMENTO
tabela_docs['media_pagamento'] = (tabela_docs['DtVenc'] - dt.datetime.now()).dt.days + 1  #method 11
somaunicred = tabela_docs.loc[tabela_docs['Banco'] == 'Unicred ES', 'Valor'].sum()
#CADASTRA TAXA DE JUROS
#AO DIA
tabela_docs.loc[tabela_docs['Banco'] == 'Unicred ES', 'taxa_juros']= 0.0496666666666667
tabela_docs.loc[tabela_docs['Banco'] == 'Itau', 'taxa_juros']= 0.073333
tabela_docs.loc[tabela_docs['Banco'] == 'Santander', 'taxa_juros']= 0.05248011
tabela_docs.loc[tabela_docs['Banco'] == 'Stratton', 'taxa_juros']= 0.056
#zera nan da coluna taxajuros
tabela_docs ['taxa_juros'] = tabela_docs ['taxa_juros']. fillna (0)
#tabela_docs.head(50)
#zera nan da coluna taxajuros
tabela_docs ['TAC'] = tabela_docs ['TAC'].astype(float)

#CALCULA A TAXA DE JUROS
tabela_docs ['taxa_total'] = tabela_docs['taxa_juros'] * tabela_docs['media_pagamento']

#DESCONTO DA TAXA EM VALOR R$
tabela_docs ['desctaxa'] =  tabela_docs ['taxa_total'] * tabela_docs ['Valor'] / 100 

#cria o Desagio - desagio = valor  - desconto da taxa somente
tabela_docs ['Deságio'] = tabela_docs ['Valor'] - tabela_docs['desctaxa'] 


#AJUSTES
tabela_docs['Deságio'] = tabela_docs['Deságio'].astype(float)
tabela_docs['taxa_total'] = tabela_docs['taxa_total'].round(2)

#SE MEU DESCONTO DA TAXA FOR 0 MEU DESAGIO VAI SER 0 TAMBEM
tabela_docs.loc[tabela_docs['desctaxa'] == 0, 'Deságio'] = 0
#RENOMEIA COLUNAS
mapeamento = { 'taxa_total': 'taxa total','desctaxa': 'descontado','Deságio': 'liquido' }

# Renomear as colunas usando o método rename()
tabela_docs = tabela_docs.rename(columns=mapeamento)

tabela_docs['liquido'] = tabela_docs['liquido'].astype(float)
tabela_docs['liquido'] = tabela_docs['liquido'].apply(lambda x: round(x, 3))
tabela_docs['descontado'] = tabela_docs['descontado'].round(2)
faturamento1 = tabela_docs
faturamento1 = faturamento1.reset_index()
faturamento1  = tabela_docs[['Banco','Com Registro','media_pagamento','liquido']].groupby('Banco').mean()
faturamento1['media_pagamento'] = faturamento1['media_pagamento'].astype(int)
faturamento  = tabela_docs[['Banco','Status','Com Registro','Valor','TAC','Taxa de boleto','descontado','liquido']].groupby('Banco').sum()
faturamento= faturamento.reset_index()
#ADICIONAR IOF
faturamento['IOF'] = faturamento['Valor'] * 0.0055376
faturamento['IOF']= faturamento['IOF'].round(2)

#SOMENTE SANTANDER RECEBE IOF
faturamento.loc[faturamento['Banco'] != 'Santander', 'IOF']= 0.00
#ADICIONA A RECOMPRA LARCA
faturamento['Recompra'] = 0
faturamento = faturamento.merge(faturamento1['media_pagamento'], left_on='Banco', right_index=True)
faturamento = faturamento.reindex(columns=['Banco', 'Com Registro', 'Valor','TAC','Taxa de boleto','Recompra','IOF','descontado','liquido','media_pagamento'])
faturamento['liquido']= faturamento ['Valor'] - faturamento['TAC'] - faturamento['Taxa de boleto'] - faturamento ['IOF'] - faturamento['Recompra'] - faturamento['descontado']
faturamento['CET'] = faturamento ['Valor'] - faturamento['TAC'] - faturamento ['IOF'] - faturamento['descontado']
faturamento['CET']  = faturamento ['Valor'] - faturamento ['CET']
faturamento.loc[faturamento['Banco'] == 'Itau', 'CET'] = faturamento ['Valor'] - faturamento['TAC'] - faturamento ['IOF'] - faturamento['descontado'] 
faturamento.loc[faturamento['Banco'] == 'Itau', 'CET'] = faturamento ['Valor'] - faturamento ['CET']
faturamento.loc[faturamento['Banco'] == 'Unicred ES', 'IOF'] = faturamento['Valor'] * 0.3841 /100
faturamento.loc[faturamento['Banco'] == 'Unicred ES', 'CET'] = faturamento['IOF'] + faturamento['descontado']
faturamento['CET'] = faturamento['CET'] * 100 / faturamento['Valor']
faturamento['CET'] = faturamento['CET'].astype(float)
faturamento['CET'] = faturamento['CET'].round(3)
faturamento['CET'] = faturamento['CET'] / 100
faturamento['CET'] = faturamento['CET'].map('{:.2%}'.format)
# Filtrar os dados para o banco "larca"
larca_df = tabela_docs[tabela_docs['Banco'] == 'Itau']

# Calcular a média ponderada
soma_produto = (larca_df['media_pagamento'] * larca_df['Valor']).sum()
soma_valores = larca_df['Valor'].sum()
media_ponderada_larca = soma_produto / soma_valores
media_ponderada_larca
media_ponderada_larca = media_ponderada_larca.round(2)
faturamento.loc[faturamento['Banco'] == 'Itau', 'media_pagamento'] = media_ponderada_larca
# Filtrar os dados para o banco "santander"
santanderdf = tabela_docs[tabela_docs['Banco'] == 'Santander']

# Calcular a média ponderada
soma_produto = (santanderdf['media_pagamento'] * santanderdf['Valor']).sum()
soma_valores = santanderdf['Valor'].sum()
media_ponderada_santander = soma_produto / soma_valores

media_ponderada_santander = media_ponderada_santander.round(2)
faturamento.loc[faturamento['Banco'] == 'Santander', 'media_pagamento'] = media_ponderada_santander
faturamento.loc[faturamento['Banco'] == 'Santander', 'liquido'] = faturamento['IOF'] + faturamento['descontado'] 
faturamento.loc[faturamento['Banco'] == 'Santander', 'liquido'] = faturamento['Valor'] -  faturamento['liquido']
faturamento.loc[faturamento['Banco'] == 'Unicred ES', 'liquido'] = faturamento['Valor'] - faturamento['descontado'] 
faturamento['IOF'] = faturamento['IOF'].round(2)
faturamento['Taxa de boleto'] = faturamento['Taxa de boleto'].round(2)

faturamentototal= faturamento['liquido'].sum()
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# 
# Formatar o número
faturamentototal = locale.currency(faturamentototal, grouping=True, symbol=None)


# Formatar os valores na coluna 'Valor' para o formato de moeda
faturamento['descontado'] = faturamento['descontado'].map(lambda x: locale.currency(x, grouping=True))

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Formatar os valores na coluna 'Valor' para o formato de moeda
faturamento['liquido'] = faturamento['liquido'].map(lambda x: locale.currency(x, grouping=True))

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# Formatar os valores na coluna 'Valor' para o formato de moeda
faturamento['Valor'] = faturamento['Valor'].map(lambda x: locale.currency(x, grouping=True))

#RENOMEIA COLUNAS
mapeamento = { 'descontado': 'Deságio','liquido': 'Valor Liquido', 'media_pagamento': 'Prazo Medio' }


# Renomear as colunas usando o método rename()
faturamento = faturamento.rename(columns=mapeamento)
faturamento['Prazo Medio'] = faturamento['Prazo Medio'].round(2)
#faturamento['Deságio'] = faturamento['Deságio'].round(2)
faturamento.loc[faturamento['CET'] == '0.00%', 'TAC']= "Falta"
faturamento.loc[faturamento['CET'] == '0.00%', 'Taxa de boleto']= "Falta"
faturamento.loc[faturamento['CET'] == '0.00%', 'Deságio']= "Falta"
faturamento.loc[faturamento['CET'] == '0.00%', 'IOF']= "Falta"
faturamento.loc[faturamento['CET'] == '0.00%', 'CET']= "Falta"
faturamento['Data']=dt.datetime.now() 
hoje.strftime("%d/%m/%Y")
# Formatando a coluna 'Data' no formato 'dd/mm/yyyy'
faturamento['Data'] = faturamento['Data'].dt.strftime('%d/%m/%Y')
colunas = ['Data'] + [coluna for coluna in faturamento.columns if coluna != 'Data']
faturamento = faturamento[colunas]


#IMPORTANDO PARA O SISTEMA
# App layout
def layout():
    return dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H3('Auditoria de Boletos', className='text-titulo',style={'margin-top': '50px'}),
        ),
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker-range',
                display_format='DD/MM/YYYY',
                start_date=faturamento['Data'].min(),
                end_date=faturamento['Data'].max(),
                style={'margin-top': '15px', 'margin-bottom': '15px'}  # Adiciona espaço acima e abaixo do filtro
            ),
            width=3,  # Ajuste a largura da coluna para mover o componente para a direita
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='data-table',
                data=faturamento.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in faturamento.columns],
                # page_size=10,  # Defina o número de linhas por página
                style_table={'overflowX': 'auto', 'width': '125%', 'margin-top':'30px','margin-left': '-15%', 'margin-right': 'auto', 'z-index': '0','border': 'none'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold','color': 'Black','fontFamily': 'Arial'},
                style_cell={'textAlign': 'left','fontSize': '15px','minWidth': '100px', 'fontFamily': 'Arial'}, # Estilo das células
                        style_data_conditional=[
                    {  'if': {'row_index': 'odd'},
                       'backgroundColor': 'rgb(248, 248, 248)',
                    },
                       {
                         'if': {'column_id': 'Valor Liquido'},
                        'backgroundColor': 'green',
                        'color': 'white',
                    },
                    {
                        'if': {'column_id': 'CET'},
                        'backgroundColor': 'red',
                        'color': 'white',
                    },
                ],
            ),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H3(f'Receita Liquida R$ {faturamentototal}', style={'margin-top': '20px', 'fontSize': 20, 'fontFamily': 'Calibri', 'color': 'black', 'text-align': 'right', 'fontWeight': 'bold'}),
            width={'size': 5, 'offset': 6}  # Adiciona um offset para mover o componente para a direita
        ),
    ]),
])

# Callback para atualizar a tabela com base nas datas selecionadas
#@app.callback(Output('data-table', 'data'),
 #             [Input('date-picker-range', 'start_date'),
  #             Input('date-picker-range', 'end_date')])
#def update_table(start_date, end_date):
 #   filtered_df = faturamento[(faturamento['Data'] >= start_date) & (faturamento['Data'] <= end_date)]
  #  return filtered_df.to_dict('records')

