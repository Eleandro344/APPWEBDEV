import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import mysql.connector
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app  # Importa o objeto app do arquivo app.py
from dash import dcc, html


import pandas as pd
import mysql.connector

# Função para carregar os dados da tabela de remessa
def carregar_dados_remessa():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',  
            database='db_sabertrimed',
        )
        consulta_remessa = "SELECT * FROM unicredremessa"
        remessaunicred_bd = pd.read_sql(consulta_remessa, con=mydb)
        # Ordenar e renomear colunas conforme necessário
        return remessaunicred_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None

# Função para carregar os dados da tabela de retorno
def carregar_dados_retorno():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',  
            database='db_sabertrimed',
        )
        consulta_retorno = "SELECT * FROM retornounicred"
        retornounicred_bd = pd.read_sql(consulta_retorno, con=mydb)
        # Ordenar e renomear colunas conforme necessário
        return retornounicred_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None

# Função para criar a tabela de dados
def create_data_table(id, data):
    return dash_table.DataTable(
        id=id,
        data=data.head(10).to_dict('records'),
        columns=[{'name': col, 'id': col} for col in data.columns],
        page_size=80,
        style_table={'overflowX': 'auto', 'width': '150%', 'margin-top':'30px','margin-left': '-25%', 'margin-right': 'auto', 'z-index': '0','border': 'none'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold','color': 'Black','fontFamily': 'Arial'},
        style_cell={'textAlign': 'left','fontSize': '15px','minWidth': '100px', 'fontFamily': 'Arial'},  # Mudança da fonte para Arial
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
            {'if': {'column_id': 'Ocorrencia'}, 'backgroundColor': '#006400', 'color': 'white'},
            {'if': {'column_id': 'TIPO DE INSTRUÇÃO ORIGEM'}, 'backgroundColor': '#A52A2A', 'color': 'white'},
            {'if': {'column_id': 'CÓDIGO DE MOVIMENTO'}, 'backgroundColor': '#006400', 'color': 'white'},
        ],
    )

# Função para criar o layout da aplicação
def layout():
    # Carregar os dados da tabela de remessa
    df_remessa = carregar_dados_remessa()
    if df_remessa is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de remessa.")
    
    # Carregar os dados da tabela de retorno
    df_retorno = carregar_dados_retorno()
    if df_retorno is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de retorno.")
    
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.Img(src='/assets/unicredimagem.png', className="logo-img", style={'width': '10%', 'marginLeft': '450px','marginTop': '0px'}),
                    html.H3("Rastreamento de Boletos Unicred",className="text-titulo"),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),
                    create_data_table('data-table-remessa3', df_remessa)
                ]
            )
        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-table-retorno3', df_retorno)
                ]
            )
        ])
    ])


