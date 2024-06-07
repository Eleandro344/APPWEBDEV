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

import time
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
        consulta_remessa = """
    SELECT 
        `DATA DE GERAÇÃO HEADER`,
        `CÓD. DE OCORRÊNCIA`,
        `CODIGO DO DOC`,
        `DATA DE EMISSÃO`,
        VENCIMENTO,
        NOME,
        `DESCONTO ATÉ`,
        `VALOR DO DESCONTO`,
        `VALOR DO IOF`,
        `VALOR DO TÍTULO`
    FROM remessa_itau
"""
        remessaunicred_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()
        
        novos_nomes = {
        'DATA DE GERAÇÃO HEADER': 'Data da Ocorrencia',
        'CÓD. DE OCORRÊNCIA': 'Ocorrencia',
        # ... adicione os outros nomes conforme necessário
        }
        remessaunicred_bd.rename(columns=novos_nomes, inplace=True)
        remessaunicred_bd = remessaunicred_bd.sort_values(by='Data da Ocorrencia', ascending=True)
        remessaunicred_bd['Data da Ocorrencia'] = pd.to_datetime(remessaunicred_bd['Data da Ocorrencia'])

        remessaunicred_bd = remessaunicred_bd.sort_values(by=['Data da Ocorrencia'], ascending=[True])

   
        remessaunicred_bd.loc[remessaunicred_bd['Ocorrencia'] == 'REMESSA DE TÍTULOS', 'Ocorrencia'] = "ENVIADO"


        #remessaunicred_bd['Data da Ocorrencia'] = pd.to_datetime(remessaunicred_bd['Data da Ocorrencia'].dt.strftime('%d/%m/%Y') ) 

        # # Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
        # remessaunicred_bd['Data da Ocorrencia'] = remessaunicred_bd['Data da Ocorrencia'].dt.strftime('%d/%m/%Y')        
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
        consulta_retorno = "SELECT * FROM retorno_itau"
        retornounicred_bd = pd.read_sql(consulta_retorno, con=mydb)
        mydb.close()
        new_column_order = [
            'DATA DE OCORRÊNCIA', 
            'CÓD. DE OCORRÊNCIA', 
            'CODIGO DO DOC', 
            'VALOR DO TÍTULO',
            'VALOR DO IOF',
            'VENCIMENTO', 
            'DESCONTOS', 
            'ERROS', 





            'Código do Registro',
            'CÓDIGO DE INSCRIÇÃO',
            'Nº de inscrição do beneficiário',
            'Código da agência beneficiário',
            'Conta movimento beneficiário', 
            'DAC',
            'USO DA EMPRESA',
            'NOSSO NÚMERO', 
            'CARTEIRA', 
            'DAC NOSSO NÚMERO',
            'NOSSO NÚMERO 2',
            'CÓDIGO DO BANCO', 
            'AGÊNCIA COBRADORA', 
            'DAC AG. COBRADORA', 
            'TARIFA DE COBRANÇA',
            'VALOR ABATIMENTO',
            'VALOR PRINCIPAL',
            'JUROS DE MORA/MULTA',
            'OUTROS CRÉDITOS',
            'BOLETO DDA',
            'DATA CRÉDITO',
            'INSTR.CANCELADA', 
            'NOME',
            'CÓD. DE LIQUIDAÇÃO', 
            'NÚMERO SEQUENCIAL',
            'Nome do arquivo',
            'TIPO DE REGISTRO HEADER',
            'CÓDIGO DE RETORNO', 
            'LITERAL DE RETORNO HEADER',
            'LITERAL DE SERVIÇO HEADER',
            'AGÊNCIA HEADER', 
            'CONTA HEADER', 
            'DAC HEADER',
            'NOME DA EMPRESA HEADER',
            'CODIGO DO BANCO HEADER',
            'NOME DO BANCO HEADER',
            'DATA DE GERAÇÃO HEADER',
            'NUMERO SEQUENCIAL HEADER', 
            'DENSIDADE', 'UNIDADE DE DENSID',
            'Nº SEQ. ARQUIVO RET', 
            'TIPO DE REGISTRO TRAILER',
            'CÓDIGO DE RETORNO TRAILER', 
            'CÓDIGO DE SERVIÇO TRAILER',
            'CÓDIGO DO BANCO TRAILER',
            'QTDE. DE TÍTULOS TRAILER', 
            'VALOR TOTAL TRAILER',
            'AVISO BANCÁRIO TRAILER',
            'CONTROLE DO ARQUIVO TRAILER',
            'QTDE DE DETALHES TRAILER', 
            'VLR TOTAL INFORMADO TRAILER', 
            'NÚMERO SEQUENCIAL TRAILER'
    ]

# Reorder the columns
        retornounicred_bd = retornounicred_bd[new_column_order]        
        retornounicred_bd['DATA DE OCORRÊNCIA'] = pd.to_datetime(retornounicred_bd['DATA DE OCORRÊNCIA']).dt.strftime('%Y%m%d')
        retornounicred_bd['DATA DE OCORRÊNCIA'] = pd.to_datetime(retornounicred_bd['DATA DE OCORRÊNCIA'])

        # # Ordenar o DataFrame pela coluna 'Data da Ocorrência' de forma crescente
      #  df_retorno = df_retorno.sort_values(by='DATA DE GERAÇÃO HEADER')
            


        novos_nomes = {
            'DATA DE OCORRÊNCIA': 'Data da Ocorrencia',
            'CÓD. DE OCORRÊNCIA': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        retornounicred_bd.rename(columns=novos_nomes, inplace=True)
        retornounicred_bd = retornounicred_bd.sort_values(by='Data da Ocorrencia', ascending=True)
       # retornounicred_bd['Data da Ocorrencia'] = pd.to_datetime(retornounicred_bd['Data da Ocorrencia'])

        retornounicred_bd = retornounicred_bd.sort_values(by=['Data da Ocorrencia', 'NÚMERO SEQUENCIAL'], ascending=[True, True])
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'BAIXA COM TRANSFERÊNCIA PARA D', 'Ocorrencia'] = "TROCADO"
       # retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'BAIXA COM TRANSFERÊNCIA PARA D', 'Ocorrencia'] = "DEVOLVIDO"






        # retornounicred_bd['DATA LIQUIDAÇÃO'] = pd.to_datetime(retornounicred_bd['DATA LIQUIDAÇÃO'], format='%d%m%y', errors='coerce')

        # # Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
        # retornounicred_bd['DATA LIQUIDAÇÃO'] = retornounicred_bd['DATA LIQUIDAÇÃO'].dt.strftime('%d/%m/%Y')
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
                html.Img(src='/assets/logoitau.png', className="logo-img", style={'width': '7%','border-radius': '10px', 'marginLeft': '450px','marginTop': '0px'}),
                html.H3("Rastreamento de Boletos Itau",className="text-titulo"),
                dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),
                html.Div(id='output-message', className='output-message'),  # Aplicar classe CSS
                    create_data_table('data-table-remessa8', df_remessa)
                    
                ]
            )

        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-table-retorno8', df_retorno)
                ]

                
            )
            
        ])



        
    ])

@app.callback(
    Output('output-message', 'children'),
    [Input('pesquisar-doc-button', 'n_clicks')]
)
def update_message(n_clicks):
    if n_clicks != 0:
        return "Buscando seu doc, aguarde!"
    else:
        return " "



# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-table-remessa8', 'data'),
     Output('data-table-retorno8', 'data')],
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