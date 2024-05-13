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
        mydb.close()

        new_order = [
            'Data da Gravação do Arquivo',    
            'Identificação da Ocorrência',
            'CODIGO DO DOC',    
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

        remessaunicred_bd = remessaunicred_bd[new_order]
        remessaunicred_bd = remessaunicred_bd.sort_values(by='Data da Gravação do Arquivo', ascending=True)

        novos_nomes = {
            'Data da Gravação do Arquivo': 'Data da Ocorrencia',
            'Identificação da Ocorrência': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        remessaunicred_bd.rename(columns=novos_nomes, inplace=True)
        remessaunicred_bd['Data da Ocorrencia'] = pd.to_datetime(remessaunicred_bd['Data da Ocorrencia'], format='%d%m%y', errors='coerce')

        # Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
        remessaunicred_bd['Data da Ocorrencia'] = remessaunicred_bd['Data da Ocorrencia'].dt.strftime('%d/%m/%Y')        
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
        mydb.close()
        retornounicred_bd['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(retornounicred_bd['DATA DA GERAÇÃO DO ARQUIVO'])

        # Ordenar o DataFrame pela coluna 'Data da Ocorrência' de forma crescente
        #df_retorno = df_retorno.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO')
        retornounicred_bd = retornounicred_bd.sort_values(by=['DATA DA GERAÇÃO DO ARQUIVO', 'SEQUENCIAL DO REGISTRO'], ascending=[True, True])
            

        new_order = [
            'DATA DA GERAÇÃO DO ARQUIVO',   
            'TIPO DE INSTRUÇÃO ORIGEM',
            'CÓDIGO DE MOVIMENTO',
            'CODIGO DO DOC',
            'COMPLEMENTO DO MOVIMENTO',
            'DATA LIQUIDAÇÃO',
            'CANAL DE LIQUIDAÇÃO',
            'VALOR DO TÍTULO',
            'VALOR ABATIMENTO',
            'VALOR PAGO',
            'JUROS DE MORA',
            'VALOR LÍQUIDO',
            'TIPO DE INSCRIÇÃO DA EMPRESA',
            'NÚMERO DE INSCRIÇÃO DA EMPRESA',
            'NÚMERO DA AGÊNCIA',
            'DÍGITO VERIFICADOR DA AGÊNCIA',
            'CONTA CORRENTE DO BENEFICIÁRIO',
            'DÍGITO VERIFICADOR DA CONTA DO BENEFICIÁRIO',
            'CÓDIGO DO BENEFICIÁRIO',
            'NOSSO NÚMERO',
            'FIXO',
            'FIXO2',
            'FIXO3',
            'DATA DE VENCIMENTO',
            'CÓDIGO DO BANCO RECEBEDOR',
            'PREFIXO DA AGÊNCIA RECEBEDORA',
            'DV-PREFIXO AGÊNCIA RECEBEDORA',
            'DATA PROGRAMADA PARA REPASSE',
            'VALOR DA TARIFA',
            'DATA DE DEBITO DA TARIFA',
            'VALOR DESCONTO CONCEDIDO',
            'SEQUENCIAL DO REGISTRO',
            'FIXO cabecario',
            'FIXO2 cabecario',
            'FIXO3 cabecario',
            'FIXO4',
            'FIXO5',
            'NÚMERO DA AGÊNCIA CABECARIO',
            'DÍGITO VERIFICADOR DA AGÊNCIA CABECARIO',
            'CONTA CORRENTE DO BENEFICIÁRIO CABECARIO',
            'DÍGITO VERIFICADOR DA CONTA DO BENEFICIÁRIO CABECARIO',
            'NOME DO BENEFICIÁRIO',
            'FIXO6',
            'SEQUENCIAL DO RETORNO',
            'CÓDIGO DO BENEFICIÁRIO CABECARIO',
            'FIXO7',
            'Identificação do Registro treiler',
            'Nome do arquivo',
        ]
        retornounicred_bd = retornounicred_bd[new_order]

        novos_nomes = {
            'DATA DA GERAÇÃO DO ARQUIVO': 'Data da Ocorrencia',
            'CÓDIGO DE MOVIMENTO': 'Ocorrencia',
            # ... adicione os outros nomes conforme necessário
        }
        retornounicred_bd.rename(columns=novos_nomes, inplace=True)
        #df_retorno.loc[df_retorno['Ocorrencia'] == 'Protesto solicitado', 'Ocorrencia'] = "Enviado a Cartorio"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Protesto solicitado', 'Ocorrencia'] = "Enviado a Cartorio"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Título Descontável (título com desistênc', 'Ocorrencia'] = "Devolvido"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Instrução Confirmada', 'Ocorrencia'] = "Instrução Confirmada"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Liquidação de Título Descontado', 'Ocorrencia'] = "Liquidação de Título Trocado"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Título Descontado', 'Ocorrencia'] = "Trocado"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Pago(Título protestado pago em cartório)', 'Ocorrencia'] = "Pago em Cartório"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Pedido de ', 'Ocorrencia'] = "Solicitação de Baixa"
        retornounicred_bd.loc[retornounicred_bd['Ocorrencia'] == 'Protesto Em cartório', 'Ocorrencia'] = "Em cartório"
        #df_remessa.loc[df_remessa['TIPO DE INSTRUÇÃO ORIGEM'] == 'Protesto Em cartório', 'TIPO DE INSTRUÇÃO ORIGEM'] = "Em cartório"

        condicao = (retornounicred_bd['TIPO DE INSTRUÇÃO ORIGEM'] == 'Protestar') & (retornounicred_bd['Ocorrencia'] == 'Instrução Confirmada')

        # Atualizar o valor da coluna "Ocorrencia" para "boleto protestado" onde a condição for verdadeira
        retornounicred_bd.loc[condicao, 'Ocorrencia'] = 'Boleto Protestado'
        retornounicred_bd['DATA LIQUIDAÇÃO'] = pd.to_datetime(retornounicred_bd['DATA LIQUIDAÇÃO'], format='%d%m%y', errors='coerce')

        # Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
        retornounicred_bd['DATA LIQUIDAÇÃO'] = retornounicred_bd['DATA LIQUIDAÇÃO'].dt.strftime('%d/%m/%Y')
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
# Callback para atualizar as tabelas com base no botão de pesquisa
@app.callback(
    [Output('data-table-remessa3', 'data'),
     Output('data-table-retorno3', 'data')],
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

