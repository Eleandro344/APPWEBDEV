import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import mysql.connector
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app  # Importa o objeto app do arquivo app.py


import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
    
load_dotenv() 
def carregar_dados_remessa():
    try:
        mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
        )
        consulta_remessa = "SELECT * FROM basestratton"
        remessasafra_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()
        novos_nomes = {
            'NºTit.': 'CODIGO DO DOC',


            # ... adicione os outros nomes conforme necessário
        }

        remessasafra_bd.rename(columns=novos_nomes, inplace=True)   
        df = remessasafra_bd 

        return df
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None                            

def create_data_table(id, data):
    return dash_table.DataTable(
        id=id,
        data=data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in data.columns],
        style_table={'overflowX': 'auto', 'width': '150%', 'margin-top':'30px','margin-left': '-25%', 'margin-right': 'auto', 'z-index': '0','border': 'none'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold','color': 'Black','fontFamily': 'Arial'},
        style_cell={'textAlign': 'left','fontSize': '15px','minWidth': '100px', 'fontFamily': 'Arial'},   # Mudança da fonte para Arial
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
            {'if': {'column_id': 'Situação'}, 'backgroundColor': '#006400', 'color': 'white'},
            {'if': {'column_id': 'TIPO DE INSTRUÇÃO ORIGEM'}, 'backgroundColor': '#A52A2A', 'color': 'white'},

            {'if': {'column_id': 'Ocorrência'}, 'backgroundColor': '#006400', 'color': 'white'},
            

        ],
        
    )

def layout():
    # Carregar os dados da tabela de remessa
    df = carregar_dados_remessa()
    if df is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de remessa.")
    
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.Img(src='/assets/stratton.png', className="logo-img", style={'width': '25%', 'marginLeft': '500px','marginTop': '0px'}),
                    html.H3("Stratton",className="text-titulo"),# style={'marginBottom': '20px', 'margin-top': '10px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
                    dbc.Input(id='numero-boleto-input', type='text' ,placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),#)style={'margin-bottom': '20px'}),
                    create_data_table('data-table8-remessa', df)
                ]
            )
        ])
    ])

@app.callback(
    Output('data-table8-remessa', 'data'),
    [Input('pesquisar-doc-button', 'n_clicks')],
    [State('numero-boleto-input', 'value')],
    allow_duplicate=True
)
def update_table(n_clicks_doc, numero_boleto):
    ctx = dash.callback_context
    if not numero_boleto or n_clicks_doc == 0:
        df = carregar_dados_remessa()
        return df.to_dict('records')  # Exibe apenas as 5 primeiras linhas se não houver pesquisa

    if ctx.triggered_id == 'pesquisar-doc-button':
        df = carregar_dados_remessa()
        resultado_pesquisa_remessa = df[df['CODIGO DO DOC'].astype(str) == numero_boleto]
        return resultado_pesquisa_remessa.to_dict('records')
    else:
        raise PreventUpdate

#print(df)
