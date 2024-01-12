from dash import html
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import subprocess
import pandas as pd
import win32com.client as win32
import datetime as dt
import statistics
from datetime import datetime, timedelta
from app import app  # Importa o objeto app do arquivo app.py

import numpy as np
import locale
from datetime import date

tabela_docs = pd.read_excel('C:/Users/elean/Desktop/bancodedados/verificadocs.xlsx')
tabela_docs =  tabela_docs[['Cod_Doc','Status','Data','Nome_Carteira','CanceladoPor']]
tabela_docs.loc[tabela_docs['Status'] == 'Enviado', 'Status'] = "Problema com o Retorno"
tabela_docs.loc[tabela_docs['Status'] == 'Solic. Baixa', 'Status'] = "Nao atendido a Solicitação de baixa"
tabela_docs.loc[tabela_docs['Status'] == 'Não Enviado', 'Status'] = "Nao enviado a Remessa"
tabela_docs.loc[tabela_docs['CanceladoPor'] == 46, 'CanceladoPor'] =" Eleandro"
tabela_docs.loc[tabela_docs['CanceladoPor'] == 41, 'CanceladoPor'] = "Lucimara"
import pandas as pd
from datetime import datetime, timedelta

# Supondo que 'Data' seja do tipo string, converta para o tipo datetime
tabela_docs['Data'] = pd.to_datetime(tabela_docs['Data'], format='%Y-%m-%d')

# Obtenha a data de dois dias atrás
data_ontem = datetime.now() - timedelta(days=3)
data_ontem_str = data_ontem.strftime('%Y-%m-%d')

# Filtre os dados removendo 'Boletos Stratton Fidc Bradesco' da data de ontem
tabela_docs = tabela_docs[(tabela_docs['Data'].dt.date != data_ontem.date()) | (tabela_docs['Nome_Carteira'] != 'Boletos Stratton Fidc Bradesco')]

# Converta a coluna 'Data' de volta para o formato original, se necessário
tabela_docs['Data'] = tabela_docs['Data'].dt.strftime('%d/%m/%Y')

data_atual = datetime.now()

# Subtrair um dia
data_ontem = data_atual - timedelta(days=1)

# Converter para o formato desejado ('%d/%m/%Y')
data_ontem_formatada = data_ontem.strftime('%d/%m/%Y')
tabela_docs = tabela_docs[~((tabela_docs['Nome_Carteira'] == 'Boletos Stratton Fidc Bradesco') & (tabela_docs['Data'] == data_ontem_formatada))]




def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.H3("Boletos Não Finalizados", style={'marginBottom': '20px','margin-top': '10px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
                    dash_table.DataTable(
                        id='data-table',
                        data=tabela_docs.to_dict('records'),
                        columns=[{'name': col, 'id': col} for col in tabela_docs.columns],
                        #page_size=22,
                        style_table={'overflowX': 'auto', 'width': '100%', 'margin-left': 'px', 'z-index': '0'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'font-family': 'Calibri'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                            {'if': {'column_id': 'Status'}, 'backgroundColor': '#FF0000', 'color': 'white'},
                        ],
                    )
                ]
            )
        ]),
    ])
