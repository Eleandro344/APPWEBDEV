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
        consulta_remessa = "SELECT * FROM remessa_safra"
        remessasafra_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()
        
        new_order = [
        'Data da Gravação do Arquivo',
        'Cod. Ocorrência',
        'CODIGO DO DOC',
        'Valor Do Título', 
        'Vencimento',
        'Cod. Carteira',
        'Nome Do Pagador', 
        'Data De Emissão Do Título',
        'Valor Do Desconto Concedido',
        'dias protesto', 
        'cod. inscrição', 
        'Numero da Inscrição',
        'Cod. Empresa',
        'Nosso Número',
        'Código lof',




        'Bco. Deposit.', 
        'Ag. Depositária',
        'Cod. Aceite',
        'Primeira Instrução De Cobrança',
        'Segunda Instrução De Cobrança', 
        'Juros 1 Dia', 'Data Limite Para Desconto', 
        'Valor lof', 
        'Abatimento /Multa', 
        'Número de Inscrição do Pagador', 
        'Endereço Do Pagador',
        'Bairro Do Pagador',
        'Código De Endereçamento Postal Do Pagador',
        'Cidade Do Pagador',
        'Estado Do Pagador',
        'Nome do Sacador Avalista',
        'Banco Emitente do Boleto',
        'Numero Sequencial do Arquivo Remessa',
        'Número Sequenc. De Registro De Arquivo',
        'Nome do arquivo', 
        'Código do Registro header',
        'Código da Remessa',
        'Literal Remessa',
        'Código de Serviço', 
        'Literal Serviço', 
        'Código de Transmissão',
        'Nome da Empresa BENEFICIÁRIO',
        'Código do Banco',
        'Nome do Banco', 
        'Código do Registro',
        'Nº Sequencial do Arquivo', 
        'Nº Sequencial do Registro',
        'Código do Registro trailer',
        'Quantidade de registro no arquivo',
        'Valor Total dos boletos',
        'Número sequencial de registro no arquivo trailer'
        ]

        # Reordena as colunas do DataFrame
        remessasafra_bd = remessasafra_bd[new_order]



        remessasafra_bd = remessasafra_bd[new_order]
        remessasafra_bd = remessasafra_bd.sort_values(by='Data da Gravação do Arquivo', ascending=True)

        novos_nomes = {
            'Data da Gravação do Arquivo': 'Data da Ocorrencia',
            'Cod. Ocorrência': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        remessasafra_bd.rename(columns=novos_nomes, inplace=True)

        remessasafra_bd['Data da Ocorrencia'] = pd.to_datetime(remessasafra_bd['Data da Ocorrencia'])

        # Ordenar o DataFrame pela coluna 'Data da Ocorrência' de forma crescente
        #df_retorno = df_retorno.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO')
        remessasafra_bd = remessasafra_bd.sort_values(by=['Data da Ocorrencia', 'Número Sequenc. De Registro De Arquivo'], ascending=[True, True])
        return remessasafra_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None            

########################################################

def carregar_dados_retorno():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',  
            database='db_sabertrimed',
        )
        consulta_retorno = "SELECT * FROM retorno_safra"
        safraretorno_db = pd.read_sql(consulta_retorno, con=mydb)
        mydb.close()

        new_order = [
        'Data Da Ocorrência No Banco',   
        'Identifica  o Da Ocorrência (Retorno)',  
        'CODIGO DO DOC',
        'Identificação Do Tipo De Carteira', 
        'Valor Título',
        'Valor Líquido Pago Pelo Pagador',
        'Data De Vencimento Do Título',
        'Valor Do Desconto Concedido', 
        'Tarifa De Cobrança',
        'indica entrada do titulo no DDA',


        'Identificaçao Do Registro Transação', 
        'Tipo De Inscri ão Da Empresara', 
        'Número De Inscriçao Da Empresa',
        'Identifica  o Do Título No Banco',
        'Cod. Ocorrência Recebida No Arquivo REMESSA',
        'Código De Motivo De Rejeição', 

        'Data Da Geração Do Arquivo Retorno',

        'Identifica  o Do Título Na Empresa', 
        'Nosso Número',
        'Código Do Banco Encarregado Da Cobrança',
        'Agência Encarregada Da Cobrança',
        'Espécie', 
        'Valor De Outras Despesas',
        'lof',
        'Valor Abatimento Concedido Ou Cancelado',
        'Juros De Mora',
        'Valor De Outros Créditos',
        'Data De Crédito Para Ocorrências 06, 07, 15 e 41',
        'Código Beneficiario Transferido Ocorrência 21',
        'Meio de Liquida',
        'Seu Número', 
        'Número Seqüencial Geração Arq. Retorno',
        'Número Seqüencial Do Registro No Arquivo',
        'Nome do arquivo',
        'Identificação Registro Header',
        'Identificação Arquivo Retorno Header',
        'Identificação Arquivo Retorno P/ extenso',
        'Código Identificação Do Serviço Header',
        'Identificação Do Serviço P/ Extenso', 
        'Ident. Empresa No Banco', 
        'Nome Da Empresa Beneficiário',
        'Código De Identificação Do Banco',
        'Nome Do Banco Por Extenso',
        'Número Seqüencial De Geração Do Arquivo Header',
        'Número Seqüencial Do Registro No Arquivo Header',
        'Código do Registro trailer', 
        'Identificação Do Arquivo Retorno treiler', 
        'Código Identificação Do Serviço treiler',
        'Código De Identificação Do Banco treiler',
        'Quantidade De Títulos',
        'Valor Total Dos Títulos',
        'Número do aviso de cobrança',
        'Número Seqüencial Geração Arquivo Retorno treiler',
        'Número Seqüencial Do Registro No Arquivo treiler',
        ]

        safraretorno_db = safraretorno_db[new_order]

        novos_nomes = {
            'Data Da Ocorrência No Banco': 'Data da Ocorrencia',
            'Identifica  o Da Ocorrência (Retorno)': 'Ocorrencia',
            'Identificação Do Tipo De Carteira': 'Carteira',
            'Valor Líquido Pago Pelo Pagador':'Valor pago',
            'indica entrada do titulo no DDA':'Titulo no DDA',

            # ... adicione os outros nomes conforme necessário
        }

        safraretorno_db.rename(columns=novos_nomes, inplace=True)

        safraretorno_db['Data da Ocorrencia']  = pd.to_datetime(safraretorno_db['Data da Ocorrencia'])
        #df_retorno['Data De Vencimento Do Título']  = pd.to_datetime(df_retorno['Data De Vencimento Do Título'])


        safraretorno_db = safraretorno_db.sort_values(by=['Data da Ocorrencia', 'Número Seqüencial Do Registro No Arquivo'], ascending=[True, True])
            

        safraretorno_db.loc[safraretorno_db['Ocorrencia'] == 'REMESSA DE TÍTULOS', 'Ocorrencia'] = "ENVIADO"
        safraretorno_db['Data De Vencimento Do Título'] = pd.to_datetime(safraretorno_db['Data De Vencimento Do Título'], format='%d%m%y', errors='coerce')

        safraretorno_db['Data De Vencimento Do Título'] = safraretorno_db['Data De Vencimento Do Título'].dt.strftime('%d/%m/%Y')

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
                    html.Img(src='/assets/bancosafra.png', className="logo-img", style={'width': '15%', 'marginLeft': '500px','marginTop': '0px'}),
                    html.H3("Rastreamento de Boletos Safra",className="text-titulo"),# style={'marginBottom': '20px', 'margin-top': '0px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '0px'}),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),#)style={'margin-bottom': '20px'}),
                    create_data_table('data-table1-remessa4', df_remessa)
                    
                ]
            )

        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-table-retorno4', df_retorno)
                ]

                
            )
            
        ])



        
    ])
# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-table1-remessa4', 'data'),
     Output('data-table-retorno4', 'data')],
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

