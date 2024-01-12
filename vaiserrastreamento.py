from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import dash
import mysql.connector
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app  # Importa o objeto app do arquivo app.py

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

consulta = "SELECT * FROM unicredremessa"
df = pd.read_sql(consulta, con=mydb)
mydb.close()

new_order = [
    'Nº do Documento (Seu número)',
    'Identificação da Ocorrência',
    'Data de emissão do Título',    
    'Data de vencimento do Título',    
    'Valor do Título',    
    'Nome/Razão Social do Pagador',  
    'Data Limite P/Concessão de Desconto',
    'Valor do Desconto',
    'Nº Sequencial do Registro remessa', 
    'Código do desconto',       
    'Identificação do Registro remessa',
    'Agência do BENEFICIÁRIO na UNICRED',
    'Data da Gravação do Arquivo',    
    'Dígito da Agência',
    'Conta Corrente',
    'Dígito da Conta Corrente',
    'Zero',
    'Código da Carteira',
    'zeros',
    'Nº Controle do Participante (Uso da empresa)',
    'Código do Banco na Câmara de Compensação',
    'zeross',
    'Brancoss',
    'Filler',
    'Código da Multa',
    'Valor/Percentual da Multa',
    'Tipo de Valor Mora',
    'Identificação de Título Descontável',
    'Brancossss',
    'Código para Protesto/Negativação',
    'Número de Dias para Protesto/Negativação',
    'Valor de Mora',
    'Nosso Número na UNICRED',
    'Valor do Abatimento a ser concedido',
    'Identificação do Tipo de Inscrição do Pagador',
    'Nº Inscrição do Pagador',
    'Endereço do Pagador',
    'Bairro do Pagador',
    'CEP do Pagador',
    'Cidade do Pagador',
    'UF do Pagador',
    'Pagador/Avalista',
    'Identificação do Registro',
    'Identificação do Arquivo Remessa',
    'Literal Remessa',
    'Código de Serviço',
    'Literal Serviço',
    'Código do Beneficiário',
    'Nome da Empresa BENEFICIÁRIO',
    'Número da UNICRED na Câmara de Compensação',
    'Nome do Banco por Extenso',
    'Código da Variação carteira da UNICRED',
    'Nº Sequencial do Arquivo',
    'Nº Sequencial do Registro',
    'Identificação do Registro treiler'
]

df = df[new_order]

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.H3("Rastreamento de Boletos", style={'marginBottom': '50px', 'margin-top': '20px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1', style={'margin-bottom': '20px'}),
                    dash_table.DataTable(
                        id='data-table',
                        data=df.to_dict('records'),
                        columns=[{'name': col, 'id': col} for col in df.columns],
                        page_size=80,
                        style_table={'overflowX': 'auto', 'width': '125%', 'margin-left': '-12%', 'margin-right': 'auto', 'z-index': '0'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'font-family': 'Calibri'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                            {'if': {'column_id': 'Identificação da Ocorrência'}, 'backgroundColor': '#006400', 'color': 'white'},
                            ],
                            
                    )
                ]
            )
        ]),
    ])

@app.callback(
    Output('data-table', 'data'),
    [Input('pesquisar-doc-button', 'n_clicks')],
    [State('numero-boleto-input', 'value')],
    allow_duplicate=True
)
def update_table(n_clicks_doc, numero_boleto):
    if not numero_boleto or n_clicks_doc == 0:
        return df.to_dict('records')
    
    ctx = dash.callback_context
    if ctx.triggered_id == 'pesquisar-doc-button':
        resultado_pesquisa = df[df['Nº do Documento (Seu número)'].astype(str) == numero_boleto]
        return resultado_pesquisa.to_dict('records')
    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
