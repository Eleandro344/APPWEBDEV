import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import mysql.connector
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app  # Importa o objeto app do arquivo app.py

from dotenv import load_dotenv
import os

load_dotenv()
import pandas as pd
import mysql.connector

# Função para carregar os dados da tabela de remessa
def carregar_dados_remessa():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        )

        # Consulta SQL apenas para as colunas desejadas
        consulta_remessa = """
            SELECT 
                `Data de Geração do Arquivo header`,
                Ocorrencia,
                `CODIGO DO DOC`,
                `Valor do Título`
            FROM remessa_sicoob
        """

        remessasafra_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()
        remessasafra_bd['Data de Geração do Arquivo header'] = pd.to_datetime(remessasafra_bd['Data de Geração do Arquivo header'], format='%d%m%Y')

        # safraretorno_db['Data da Ocorrencia']  = pd.to_datetime(safraretorno_db['Data da Ocorrencia'])


        remessasafra_bd = remessasafra_bd.sort_values(by=['Data de Geração do Arquivo header'], ascending=[True])
                    


    #     remessasafra_bd = remessasafra_bd[new_order]
        remessasafra_bd = remessasafra_bd.sort_values(by='Data de Geração do Arquivo header', ascending=True)

        novos_nomes = {
            'Data de Geração do Arquivo header': 'Data da Ocorrencia',
            'Ocorrencia': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        remessasafra_bd.rename(columns=novos_nomes, inplace=True)

    #     remessasafra_bd['Data da Ocorrencia'] = pd.to_datetime(remessasafra_bd['Data da Ocorrencia'])

    #     # Ordenar o DataFrame pela coluna 'Data da Ocorrência' de forma crescente
    #     #df_retorno = df_retorno.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO')
    #     remessasafra_bd = remessasafra_bd.sort_values(by=['Data da Ocorrencia', 'Número Sequenc. De Registro De Arquivo'], ascending=[True, True])
        return remessasafra_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None            

########################################################

def carregar_dados_retorno():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        )
        consulta_retorno = """
    SELECT 
        `Data de Geração do Arquivo header`,
        `Ocorrencia`,
        `CODIGO DO DOC`,
        Carteira,
        `Valor do Título`,
        Vencimento,
        `Nº do Registro`
    FROM retorno_sicoob
"""
        safraretorno_db = pd.read_sql(consulta_retorno, con=mydb)
        mydb.close()

        new_order = [
        'Data de Geração do Arquivo header',   
        'Ocorrencia',  
        'CODIGO DO DOC',
        'Carteira', 
        'Valor do Título',
        'Vencimento',
        'Nº do Registro',

        ]

        safraretorno_db = safraretorno_db[new_order]
        safraretorno_db['Data de Geração do Arquivo header'] = pd.to_datetime(safraretorno_db['Data de Geração do Arquivo header'], format='%d%m%Y')

        # safraretorno_db['Data da Ocorrencia']  = pd.to_datetime(safraretorno_db['Data da Ocorrencia'])
        safraretorno_db['Vencimento'] = pd.to_datetime(safraretorno_db['Vencimento'], format='%d%m%Y')


        safraretorno_db = safraretorno_db.sort_values(by=['Data de Geração do Arquivo header', 'Nº do Registro'], ascending=[True, True])
            

        # safraretorno_db.loc[safraretorno_db['Ocorrencia'] == 'REMESSA DE TÍTULOS', 'Ocorrencia'] = "ENVIADO"
        # safraretorno_db['Data De Vencimento Do Título'] = pd.to_datetime(safraretorno_db['Data De Vencimento Do Título'], format='%d%m%y', errors='coerce')

        # safraretorno_db['Data De Vencimento Do Título'] = safraretorno_db['Data De Vencimento Do Título'].dt.strftime('%d/%m/%Y')

        return safraretorno_db
    
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
                    html.Img(src='/assets/sicoob.png', className="logo-img", style={'width': '12%','border-radius': '10px', 'marginLeft': '500px','marginTop': '0px'}),
                    html.H3("Rastreamento de Boletos Safra",className="text-titulo"),# style={'masrginBottom': '20px', 'margin-top': '0px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '0px'}),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),#)style={'margin-bottom': '20px'}),
                    html.Div(id='output-message9', className='output-message'),  # Aplicar classe CSS
                    create_data_table('data-table1-remessa9', df_remessa)
                    
                ]
            )

        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-table-retorno9', df_retorno)
                ]

                
            )
            
        ])



        
    ])
@app.callback(
    Output('output-message9', 'children'),
    [Input('pesquisar-doc-button', 'n_clicks')]
)
def update_message(n_clicks):
    if n_clicks != 0:
        return "Buscando seu doc, aguarde!"
    else:
        return " "

# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-table1-remessa9', 'data'),
     Output('data-table-retorno9', 'data')],
    [Input('pesquisar-doc-button', 'n_clicks')],
    [State('numero-boleto-input', 'value')],
    allow_duplicate=True
)
def update_table(n_clicks_doc, numero_boleto):
    ctx = dash.callback_context
    if not numero_boleto or n_clicks_doc == 0:
        df_remessa = carregar_dados_remessa()
        df_retorno = carregar_dados_retorno()
        return df_remessa.head(10).to_dict('records'), df_retorno.head(10).to_dict('records')

    if ctx.triggered_id == 'pesquisar-doc-button':
        df_remessa = carregar_dados_remessa()
        df_retorno = carregar_dados_retorno()
        resultado_pesquisa_remessa = df_remessa[df_remessa['CODIGO DO DOC'].astype(str) == numero_boleto]
        resultado_pesquisa_retorno = df_retorno[df_retorno['CODIGO DO DOC'].astype(str) == numero_boleto]
        return resultado_pesquisa_remessa.head(10).to_dict('records'), resultado_pesquisa_retorno.head(10).to_dict('records')
    else:
        raise PreventUpdate

