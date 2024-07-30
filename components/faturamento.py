from dash import dash_table
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
from dash import html, Input, Output, State, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from app import app
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
import mysql.connector
import plotly.express as px

from dash_table import DataTable

def carregar_dados_remessa():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',
            database='db_sabertrimed',
        )

        # Consultas de remessas
        remessa_santander = pd.read_sql("SELECT * FROM remessa_santander", con=mydb)
        rememessa_uncired = pd.read_sql("SELECT * FROM unicredremessa", con=mydb)
        remessa_safra = pd.read_sql("SELECT * FROM remessa_safra", con=mydb)
        remessa_sofisa = pd.read_sql("SELECT * FROM remessa_sofisa", con=mydb)
        remessa_itau = pd.read_sql("SELECT * FROM remessa_itau", con=mydb)
        remessa_sicoob = pd.read_sql("SELECT * FROM remessa_sicoob", con=mydb)

        # Data de ontem
        hoje = datetime.now()
        if hoje.weekday() == 0:
            ontem = hoje - timedelta(days=3)
        else:
            ontem = hoje - timedelta(days=1)
        ontem = ontem.strftime('%Y-%m-%d')

        # Processamento das remessas
        santander = remessa_santander[remessa_santander['Código de movimento remessa'] == 'Enviado']
        santander = santander[santander['Nº de inscrição do beneficiário'] != 0]
        santander['Valor nominal do boleto'] = santander['Valor nominal do boleto'].str.replace(',', '.').astype(float)
        santander['Data de emissão do boleto'] = pd.to_datetime(santander['Data de emissão do boleto'], format='%d/%m/%y', errors='coerce')
        santander = santander[santander['Data de emissão do boleto'] == ontem]
        santandertotal = santander['Valor nominal do boleto'].sum()

        remessa_itau = remessa_itau[["DATA DE GERAÇÃO HEADER","DATA DE EMISSÃO","CÓD. DE OCORRÊNCIA", "NOME DO BANCO HEADER","VALOR DO TÍTULO"]]
        remessa_itau['DATA DE EMISSÃO'] = pd.to_datetime(remessa_itau['DATA DE EMISSÃO'], format='%d/%m/%y')
        remessa_itau= remessa_itau[remessa_itau['CÓD. DE OCORRÊNCIA'] =='REMESSA DE TÍTULOS']   
        itauontem = remessa_itau[remessa_itau['DATA DE EMISSÃO'] == ontem]
        itauontem['VALOR DO TÍTULO'] = itauontem['VALOR DO TÍTULO'].str.replace(',', '.').astype(float)

        itautotal = itauontem['VALOR DO TÍTULO'].sum()


        sicoob = remessa_sicoob[remessa_sicoob['Ocorrencia'] == 'Enviado']
        sicoob['Data Emissão do Título'] = pd.to_datetime(sicoob['Data Emissão do Título'], format='%d%m%Y', errors='coerce')
        sicoobontem = sicoob[sicoob['Data Emissão do Título'] == ontem]
        sicoobontem['Valor do Título'] = sicoobontem['Valor do Título'].str.replace(',', '.').astype(float)
        sicoobtotal = sicoobontem['Valor do Título'].sum()

        unicred = rememessa_uncired[rememessa_uncired['Identificação da Ocorrência'] == 'Enviado']
        unicred['Data de emissão do Título'] = pd.to_datetime(unicred['Data de emissão do Título'], format='%d/%m/%y', errors='coerce')
        unicred = unicred[unicred['Data de emissão do Título'] == ontem]
        unicred['Valor do Título'] = unicred['Valor do Título'].str.replace(',', '.').astype(float)
        totalunicred = unicred['Valor do Título'].sum()






        safra = remessa_safra[remessa_safra['Cod. Ocorrência'] == 'REMESSA DE TÍTULOS']
        safra['Nome do Banco'] = "SAFRA"        
        safra['Data De Emissão Do Título'] = pd.to_datetime(safra['Data De Emissão Do Título'], format='%d/%m/%y', errors='coerce')
        safra = safra[safra['Data De Emissão Do Título'] == ontem]
        safra['Valor Do Título'] = safra['Valor Do Título'].str.replace(',', '.').astype(float)
        safratotal = safra['Valor Do Título'].sum()

        sofisa = remessa_sofisa[remessa_sofisa['Código de movimento remessa'] == 'Enviado']
        sofisa['Data de emissão do boleto'] = pd.to_datetime(sofisa['Data de emissão do boleto'], format='%d/%m/%y', errors='coerce')
        sofisa = sofisa[sofisa['Data de emissão do boleto'] == ontem]
        sofisa['Valor nominal do boleto'] = sofisa['Valor nominal do boleto'].str.replace(',', '.').astype(float)
        total_sofisa = sofisa['Valor nominal do boleto'].sum()

        # Criação da tabela completa
        santander = santander.rename(columns={'Data de emissão do boleto': 'Emissao Doc', 'Valor nominal do boleto': 'Valor', 'Código de movimento remessa': 'Ocorrencia', 'Nome do Banco': 'Nome do Banco'})
        itauontem = itauontem.rename(columns={'DATA DE EMISSÃO': 'Emissao Doc', 'VALOR DO TÍTULO': 'Valor', 'CÓD. DE OCORRÊNCIA': 'Ocorrencia', 'NOME DO BANCO HEADER': 'Nome do Banco'})
        sicoobontem = sicoobontem.rename(columns={'Data Emissão do Título': 'Emissao Doc', 'Valor do Título': 'Valor', 'Ocorrencia': 'Ocorrencia', 'Nome do Banco': 'Nome do Banco'})
        unicred = unicred.rename(columns={'Data de emissão do Título': 'Emissao Doc', 'Valor do Título': 'Valor', 'Identificação da Ocorrência': 'Ocorrencia', 'Nome do Banco por Extenso': 'Nome do Banco'})
        safra = safra.rename(columns={'Data De Emissão Do Título': 'Emissao Doc', 'Valor Do Título': 'Valor', 'Cod. Ocorrência': 'Ocorrencia', 'Nome do Banco': 'Nome do Banco'})
        sofisa = sofisa.rename(columns={'Data de emissão do boleto': 'Emissao Doc', 'Valor nominal do boleto': 'Valor', 'Código de movimento remessa': 'Ocorrencia', 'Nome do Banco': 'Nome do Banco'})

        tabelacompleta = pd.concat([santander, itauontem, sicoobontem, unicred, safra, sofisa], ignore_index=True)
        tabelacompleta['Quantidade de Titulos'] = 1

        total_por_banco = tabelacompleta.groupby(['Emissao Doc', 'Nome do Banco'])[['Quantidade de Titulos', 'Valor']].sum().reset_index()
        total_por_banco = total_por_banco.rename(columns={'Valor': 'Total'})
    
        total_por_banco['Emissao Doc'] = pd.to_datetime(total_por_banco['Emissao Doc'])
        total_por_banco['Emissao Doc'] = total_por_banco['Emissao Doc'].dt.strftime('%d/%m/%Y')
        grafico = total_por_banco



        total_por_banco['Total'] = total_por_banco['Total'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_vazio = total_por_banco['Quantidade de Titulos'].astype(int)
        if df_vazio.empty:
            exibicao = "nao"
        else:
            exibicao = "sim"

        return total_por_banco, exibicao,santandertotal, grafico,totalunicred, safratotal, total_sofisa, itautotal, sicoobtotal

    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None, None
    


def layout():
    total_por_banco, exibicao, santandertotal, grafico, totalunicred, safratotal, total_sofisa, itautotal, sicoobtotal = carregar_dados_remessa()

    if total_por_banco is None:
        return html.Div("Erro ao carregar dados da tabela de remessa.")

    if exibicao == "nao":
        return html.Div([
            html.H4('Faturamento não contabilizado ainda, aguarde!',className="text-semacesso2"),
            html.Iframe(         
                src="https://lottie.host/embed/547da133-a45b-4ca3-b3a4-161e388df0c1/6afa9OZpOR.json",
                style={'width': '550px', 'height': '450px', 'margin': 'auto','padding-top': '20px', 'display': 'block'}
        )])
    else:
        grafico["Total"] = grafico["Total"].str.replace("R$", "").str.replace(".", "").str.replace(",", ".").astype(float)
        grafico['Total'] = grafico['Total'].astype(float)
        total_bruto = grafico['Total'].sum()
        # Create a modern bar chart for the total values per bank
        fig = go.Figure(data=[
            go.Bar(
                x=grafico['Nome do Banco'],
                y=grafico['Total'],
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            )
        ])
        fig.update_layout(
            title='Total por Banco',
            xaxis_title='Nome do Banco',
            yaxis_title='Total',
            template='plotly_white',
            font=dict(family='Poppins, Arial', size=14)
        )


        return dbc.Container([
            dbc.Row([
                dbc.Col(html.H3('Auditoria de Boletos', className='text-titulo', style={'margin-top': '50px'})),
                dbc.Col(dcc.DatePickerRange(
                    id='date-picker-range',
                    display_format='DD/MM/YYYY',
                    style={'margin-top': '50px'}
                ), width=3),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Santander'),
                            html.H5(f'R$ {santandertotal:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px','transition': '300ms','overflow': 'hidden'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Itau'),
                            html.H5(f'R$ {itautotal:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Sicoob'),
                            html.H5(f'R$ {sicoobtotal:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Unicred'),
                            html.H5(f'R$ {totalunicred:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Safra'),
                            html.H5(f'R$ {safratotal:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend('Sofisa'),
                            html.H5(f'R$ {total_sofisa:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), id='card-title', style={}),
                        ], className='card-quantidade-atendimentos card-style'),
                        dbc.Card(
                            html.Div(className='fa fa-university card-icon'),
                            color='success', style={'maxWidth': 75, 'height': 150, 'margin-left': '-10px'}
                        ),
                    ], style={'width': '100%'})
                ], width=2),
            ], style={'margin-top': '50px'}),
            dbc.Row([
                dbc.Col(
                    DataTable(
                        id='datatable',
                        columns=[
                            {'name': i, 'id': i} for i in total_por_banco.columns
                        ],
                        data=total_por_banco.to_dict('records'),
                        style_table={'overflowX': 'auto', 'width': '100%', 'margin-top': '30px', 'margin-left': 'auto', 'margin-right': 'auto', 'z-index': '0', 'border': 'none', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black', 'fontFamily': 'Poppins, Arial', 'borderBottom': '2px solid #00aaff'},
                        style_cell={'textAlign': 'left', 'fontSize': '15px', 'minWidth': '100px', 'fontFamily': 'Poppins, Arial', 'padding': '10px', 'border': 'none'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                            {'if': {'column_id': 'Total'}, 'backgroundColor': 'rgb(232, 243, 230)', 'color': 'Black'},
                            {'if': {'column_id': 'CET'}, 'backgroundColor': 'red', 'color': 'white'},
                            {'if': {'state': 'active'}, 'backgroundColor': 'rgba(0, 170, 255, 0.3)', 'border': 'none'},
                            {'if': {'state': 'selected'}, 'backgroundColor': 'rgba(0, 170, 255, 0.1)', 'border': 'none'}
                        ],
                        style_as_list_view=True
                    ),
                ),
            ], style={'flex': '1 1 0', 'margin-top': '50px', 'height': 'auto'}),
            dbc.Row([
            dbc.Col(html.H4(f'Total bruto R$ {total_bruto:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."),className='text-titulototal'))]),   
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='bar-chart',
                        figure=fig
                    )
                )
                
            ], style={'margin-top': '50px'})
        ], fluid=True, style={'width': '100%', 'height': '100vh', 'padding': '0px', 'margin': '0px'})
