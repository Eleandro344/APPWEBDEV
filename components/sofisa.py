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
        consulta_remessa = """
    SELECT 
            `Data da Gravação do Arquivo`,
            `Código de movimento remessa`,   
            `CODIGO DO DOC`,     
            `Data de vencimento do boleto`,    
            `Valor nominal do boleto`,    
            `Nome do Pagador`,    
            `Data Limite para concessão do desconto`,
            `Valor do desconto a ser concedido`,
            `Nº Sequencial do Registro`,
            `Primeira instrução`,
            `Segunda instrução`,
            `Data de emissão do boleto`,
            `Valor de Mora dia`,
            `Percentual do IOF a ser recolhido`,
            `Valor do abatimento ou Valor do segundo desconto`,
            `Número de dias corridos para Protesto`,
            `Número sequencial do registro no arquivo`,
            `Número sequencial de registro no arquivo trailer`
          FROM remessa_sofisa
                """
        remessasofisa_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()


        novos_nomes = {
            'Data da Gravação do Arquivo': 'Data da Ocorrencia',
            'Código de movimento remessa': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        remessasofisa_bd.rename(columns=novos_nomes, inplace=True)
        remessasofisa_bd = remessasofisa_bd.sort_values(by='Data da Ocorrencia', ascending=True)
        return remessasofisa_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None




# Função para carregar os dados da tabela de remessa
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
            `Data da ocorrência`,
            `Código movimento retorno`,        
            `CODIGO DO DOC`,
            `Tipo de cobrança`, 
            `Data de vencimento do boleto`,   
            `Valor nominal do boleto`,   
            `Valor total recebido`,       
            `Valor do juros de mora`,   
            `Valor da tarifa cobrada`,
            `Valor de outras despesas`,
            `Valor de juros de atraso`,
            `Valor de IOF recolhido`,
            `Valor do abatimento concedido`,
            `Valor do desconto concedido`,
            `Código de erro 1`,
            `Código de erro 2`,
            `Código de erro 3`,
            `Data de vencimento do boleto`,
            `Valor de outros créditos`,
            `Valor do IOF em outra unidade`,
            `Número Sequencial do registro do arquivo corpo`,
            `Número Sequencial do registro no arquivo cabeacrio`,
            `Número Sequência do arquivo trailer`,
            `Número Sequência do arquivo corpo`
          FROM retorno_sofisa
                """
        retornosofisa_db = pd.read_sql(consulta_retorno, con=mydb)
        mydb.close()
        retornosofisa_db['Data da ocorrência'] = pd.to_datetime(retornosofisa_db['Data da ocorrência'])

        novos_nomes = {
            'Data da ocorrência': 'Data da Ocorrencia',
            'Código movimento retorno': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }



        retornosofisa_db.rename(columns=novos_nomes, inplace=True)

        retornosofisa_db = retornosofisa_db.sort_values(by=['Data da Ocorrencia', 'Número Sequência do arquivo corpo'], ascending=[True, True])


        retornosofisa_db.loc[retornosofisa_db['Ocorrencia'] == '28', 'Ocorrencia'] = "Débito Tarifas/Custas Correspondentes"

        retornosofisa_db.loc[retornosofisa_db['Tipo de cobrança'] == '4', 'Tipo de cobrança'] = "Título Descontado"
        retornosofisa_db.loc[retornosofisa_db['Tipo de cobrança'] == '2', 'Tipo de cobrança'] = "Cobrança Vinculada"
        retornosofisa_db.loc[retornosofisa_db['Tipo de cobrança'] == '3', 'Tipo de cobrança'] = "Cobrança Caucionada"



        return retornosofisa_db
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
          #  {'if': {'column_id': 'TIPO DE INSTRUÇÃO ORIGEM'}, 'backgroundColor': '#A52A2A', 'color': 'white'},
           # {'if': {'column_id': 'CÓDIGO DE MOVIMENTO'}, 'backgroundColor': '#006400', 'color': 'white'},
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
                    html.Img(src='/assets/Sofisaimagem.png', className="logo-img", style={'width': '10%', 'marginLeft': '500px','marginTop': '0px'}),
                    html.H3("Rastreamento de Boletos Banco Sofisa",className="text-titulo"),# style={'marginBottom': '20px', 'margin-top': '0px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '0px'}),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),#)style={'margin-bottom': '20px'}),
                    html.Div(id='output-message5', className='output-message'),  # Aplicar classe CSS
                    create_data_table('data-table2-remessa', df_remessa)
                    
                ]
            )

        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-table2-retorno', df_retorno)
                ]

                
            )
            
        ])



        
    ])
@app.callback(
    Output('output-message5', 'children'),
    [Input('pesquisar-doc-button', 'n_clicks')]
)
def update_message(n_clicks):
    if n_clicks != 0:
        return "Buscando seu doc, aguarde!"
    else:
        return " "
# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-table2-remessa', 'data'),
     Output('data-table2-retorno', 'data')],
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

