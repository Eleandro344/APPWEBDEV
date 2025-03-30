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
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',  
            database='db_sabertrimed',
        )
# Consulta na tabela unicredremessa
        consulta_remessa = "SELECT * FROM remessa_grafeno"
        remessasantander_bd = pd.read_sql(consulta_remessa, con=mydb)
        mydb.close()
        new_order = [
            'Data de gravação do arquivo cabeçalho',
            'Identificação da ocorrência',
            'CODIGO DO DOC',
            'Data da emissão do título',
            'Cliente',
            'Data do vencimento',
            'desconto ate',
            'Desconto',
            'Identificação da empresa beneficiária no banco',
            'Número de controle do participante',
            'Código do banco a ser debitado na câmara de compensação',
            'Campo de multa',
            'Percentual multa',
            'Identificação do título no banco',
            'Dígito de auto conferência do número bancário',
            'Quantidade de pagamentos possíveis',
            'Valor',
            'Banco',
            'Agência depositária',
            'Identificação',
            'Valor a ser cobrado por dia de atraso',
            'Valor do desconto',
            'Valor do IOF',
            'Valor do abatimento a ser concedido ou cancelado',
            'cnpj pagador',
            'endereco',
            'Número sequencial do registro',
            'Nome do arquivo',
            'TIPO DE REGISTRO HEADER cabeçalho',
            'Identificação do arquivo remessa cabeçalho',
            'Literal remessa cabeçalho',
            'Código do serviço cabeçalho',
            'Nome da empresa cabeçalho',
            'Número do Banco cabeçalho',
            'Nome do banco cabeçalho',
            'Identificação do sistema cabeçalho',
            'Número sequencial de remessa cabeçalho',
            'Número sequencial do registro cabeçalho',
            'Identificação do registro trailer',
            'Número sequencial de registro trailer',
            'Identificação do registro',

        ]


        remessasantander_bd = remessasantander_bd[new_order]


        novos_nomes = {
            'Data de gravação do arquivo cabeçalho': 'Data da Ocorrencia',
            'Identificação da ocorrência': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        remessasantander_bd.rename(columns=novos_nomes, inplace=True)
        remessasantander_bd['Data da Ocorrencia'] = pd.to_datetime(remessasantander_bd['Data da Ocorrencia'])
        remessasantander_bd = remessasantander_bd.sort_values(by='Data da Ocorrencia', ascending=True)       

        return remessasantander_bd
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None




def carregar_dados_retorno():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        )
        consulta_retorno = "SELECT * FROM retorno_grafeno"
        retornosantander_bd = pd.read_sql(consulta_retorno, con=mydb)
        mydb.close()
        # retornosantander_bd['Número sequencial de remessa cabeçalho'] = pd.to_datetime(retornosantander_bd['Número sequencial de remessa cabeçalho'])
        # retornosantander_bd = retornosantander_bd.sort_values(by='Número sequencial de remessa cabeçalho')
        new_order = [
            'Data de gravação do arquivo cabeçalho',
            'Identificação da ocorrência',

            'CODIGO DO DOC',
            'Valor do título',
            'Data de vencimento do título',
            'Valor pago',
            'Juros de mora',            
            'Número de inscrição da empresa',
            'Identificação da empresa beneficiária no banco',
            'Número de controle do participante',
            'Identificação do título no banco',
            'Data do ocorrência no banco',
            'Banco cobrador',
            'Agência Cobrança',
            'Despesas de cobrança',
            'Valor abatimento concedido',
            'Outros créditos',
            'Data do crédito',
            'Origem do pagamento',
            'Motivos de rejeição',
            'Número sequencial de registro',
            'Nome do arquivo',
            'TIPO DE REGISTRO HEADER cabeçalho',
            'Identificação do arquivo remessa cabeçalho',
            'Literal remessa cabeçalho',
            'Código do serviço cabeçalho',
            'Nome da empresa cabeçalho',
            'Número do Banco cabeçalho',
            'Nome do banco cabeçalho',
            'Identificação do sistema cabeçalho',
            'Número sequencial de remessa cabeçalho',
            'Número sequencial do registro cabeçalho',
            'Identificação do registro trailer',
            'Número sequencial de registro trailer',
            'Identificação do registro',

        ]

        retornosantander_bd = retornosantander_bd[new_order]

        novos_nomes = {
            'Data de gravação do arquivo cabeçalho': 'Data da Ocorrencia',

            'Identificação da ocorrência': 'Ocorrencia',
        }
        retornosantander_bd.rename(columns=novos_nomes, inplace=True)


        docsativos = retornosantander_bd[['Data da Ocorrencia','Nome da empresa cabeçalho','Ocorrencia','Valor do título','CODIGO DO DOC','Valor pago',]]
        docsativos['Data da Ocorrencia'] = pd.to_datetime(docsativos['Data da Ocorrencia'])

        # Primeiro, vamos ordenar o DataFrame pela coluna 'DATA DA GERAÇÃO DO ARQUIVO' para garantir que a data mais recente apareça primeiro
        df_sorted = docsativos.sort_values(by='Data da Ocorrencia', ascending=False)

        # Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento
        indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data da Ocorrencia'].idxmax()

        # Agora, vamos usar esses índices para selecionar os registros correspondentes
        docsativos = df_sorted.loc[indices_mais_recentes]

        # Exibindo os documentos mais recentes


        naopago = docsativos.loc[docsativos['Valor pago'] == 0.0]
        baixados = naopago.loc[naopago['Ocorrencia'] == 'Baixado co']  
        naopago = naopago.loc[naopago['Ocorrencia'] != 'Baixado co']  

        pagos = docsativos.loc[docsativos['Valor pago'] != 0.0]
        return retornosantander_bd

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
    df_retorno  = carregar_dados_retorno()
    if df_retorno is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de retorno.")
    
    
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.Img(src='/assets/grafeno.png', className="logo-img", style={'width': '30%', 'marginLeft': '500px','marginTop': '0px'}),
                    html.H3(id="total-pagos", className="text-titulo"),
                    html.H3(id="total-naopago", className="text-titulo"),
                    html.H3(id="total-baixado", className="text-titulo"),

                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1'),#)style={'margin-bottom': '20px'}),
                    html.Div(id='output-messagef1', className='output-message'),  # Aplicar classe CSS

                    create_data_table('data-tablef1-remessa', df_remessa)
                    
                ]
            )

        ]),
        dbc.Row([
            dbc.Col(
                [
                    create_data_table('data-tablef1-retorno', df_retorno)
                ]

                
            )
            
        ])



        
    ])

# Callback para atualizar os valores de 'pagos' e 'naopago'
@app.callback(
    [Output('total-pagos', 'children'),
     Output('total-naopago', 'children'),
     Output('total-baixado', 'children')],
    [Input('pesquisar-doc-button', 'n_clicks')]
)
def atualizar_totais(n_clicks):
    # Carregar dados (substitua pelo seu carregamento de dados real)
    retornosantander_bd = carregar_dados_retorno()
    
    # Filtrar os dados
    # docsativos = retornosantander_bd[['Data da Ocorrencia', 'Nome da empresa cabeçalho', 'Ocorrencia', 'Valor do título', 'CODIGO DO DOC', 'Valor pago']]
    # naopago = docsativos[docsativos['Valor pago'] == 0.0]

    # pagos = docsativos.loc[docsativos['Valor pago'] != 0.0]
    retornosantander_bd['Data da Ocorrencia'] = pd.to_datetime(retornosantander_bd['Data da Ocorrencia'])
    retornosantander_bd = retornosantander_bd.sort_values(by='Data da Ocorrencia', ascending=True) 

    docsativos = retornosantander_bd[['Data da Ocorrencia','Nome da empresa cabeçalho','Ocorrencia','Valor do título','CODIGO DO DOC','Valor pago',]]
    docsativos['Data da Ocorrencia'] = pd.to_datetime(docsativos['Data da Ocorrencia'])

    # Primeiro, vamos ordenar o DataFrame pela coluna 'DATA DA GERAÇÃO DO ARQUIVO' para garantir que a data mais recente apareça primeiro
    df_sorted = docsativos.sort_values(by='Data da Ocorrencia', ascending=False)

    # Em seguida, vamos identificar os índices dos registros com a data mais recente para cada número de documento
    indices_mais_recentes = df_sorted.groupby('CODIGO DO DOC')['Data da Ocorrencia'].idxmax()

    # Agora, vamos usar esses índices para selecionar os registros correspondentes
    docsativos = df_sorted.loc[indices_mais_recentes]

    # Exibindo os documentos mais recentes


    naopago = docsativos.loc[docsativos['Valor pago'] == 0.0]
    baixados = naopago.loc[naopago['Ocorrencia'] == 'Baixado co']  
    naopago = naopago.loc[naopago['Ocorrencia'] != 'Baixado co']  
    pagos = docsativos.loc[docsativos['Valor pago'] != 0.0]

    naopago['Valor do título'] = naopago['Valor do título'].str.replace(',', '.').astype(float)
    pagos['Valor do título'] = pagos['Valor do título'].str.replace(',', '.').astype(float)
    baixados['Valor do título'] = baixados['Valor do título'].str.replace(',', '.').astype(float)

    # Obter os totais
    total_pagos = pagos['Valor do título'].sum()
    total_naopago = naopago['Valor do título'].sum()
    baixados = baixados['Valor do título'].sum()

    # Formatando os valores para o formato correto com ponto para milhares e vírgula para decimais
    total_pagos = f"{total_pagos:,.2f}".replace('.', 'v').replace(',', '.').replace('v', ',')
    total_naopago = f"{total_naopago:,.2f}".replace('.', 'v').replace(',', '.').replace('v', ',')
    baixados = f"{baixados:,.2f}".replace('.', 'v').replace(',', '.').replace('v', ',')


    # Atualizar o conteúdo dos elementos H3
    return f'Total de títulos pagos: {total_pagos}', f'Total de titulos a pagar: {total_naopago}', f'Total de titulos baixados: {baixados}'

@app.callback(
    Output('output-messagef1', 'children'),
    [Input('pesquisar-doc-button', 'n_clicks')]
)
def update_message(n_clicks):
    if n_clicks != 0:
        return "Buscando seu doc, aguarde!"
    else:
        return " "

# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-tablef1-remessa', 'data'),
     Output('data-tablef1-retorno', 'data')],
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

