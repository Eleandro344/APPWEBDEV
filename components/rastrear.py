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

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Consulta na tabela unicredremessa
consulta_remessa = "SELECT * FROM unicredremessa"
df_remessa = pd.read_sql(consulta_remessa, con=mydb)

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

df_remessa = df_remessa[new_order]
df_remessa = df_remessa.sort_values(by='Data da Gravação do Arquivo', ascending=True)

novos_nomes = {
    'Data da Gravação do Arquivo': 'Data da Ocorrencia',
    'Identificação da Ocorrência': 'Ocorrencia',
    # ... adicione os outros nomes conforme necessário
}
df_remessa.rename(columns=novos_nomes, inplace=True)


# Supondo que 'data da ocorrencia' seja a coluna que precisa ser formatada
#df_remessa['Data da Ocorrencia'] = pd.to_datetime(df_remessa['Data da Ocorrencia'], format='%y%m%d')
#df_remessa['Data da Ocorrencia'] = df_remessa['Data da Ocorrencia'].dt.strftime('%d/%m/%Y')


#04/12/2050



# Consulta na tabela unicredretorno
consulta_retorno = "SELECT * FROM retornounicred"
df_retorno = pd.read_sql(consulta_retorno, con=mydb)

#df_retorno = df_retorno.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO', ascending=True)

#df_retorno['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(df_retorno['DATA DA GERAÇÃO DO ARQUIVO'], format='%d/%m/%Y')
df_retorno['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(df_retorno['DATA DA GERAÇÃO DO ARQUIVO'])

# Ordenar o DataFrame pela coluna 'Data da Ocorrência' de forma crescente
#df_retorno = df_retorno.sort_values(by='DATA DA GERAÇÃO DO ARQUIVO')
df_retorno = df_retorno.sort_values(by=['DATA DA GERAÇÃO DO ARQUIVO', 'SEQUENCIAL DO REGISTRO'], ascending=[True, True])
    

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
df_retorno = df_retorno[new_order]

novos_nomes = {
    'DATA DA GERAÇÃO DO ARQUIVO': 'Data da Ocorrencia',
    'CÓDIGO DE MOVIMENTO': 'Ocorrencia',
    # ... adicione os outros nomes conforme necessário
}
df_retorno.rename(columns=novos_nomes, inplace=True)
#df_retorno.loc[df_retorno['Ocorrencia'] == 'Protesto solicitado', 'Ocorrencia'] = "Enviado a Cartorio"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Protesto solicitado', 'Ocorrencia'] = "Enviado a Cartorio"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Título Descontável (título com desistênc', 'Ocorrencia'] = "Devolvido"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Instrução Confirmada', 'Ocorrencia'] = "Instrução Confirmada"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Liquidação de Título Descontado', 'Ocorrencia'] = "Liquidação de Título Trocado"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Título Descontado', 'Ocorrencia'] = "Trocado"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Pago(Título protestado pago em cartório)', 'Ocorrencia'] = "Pago em Cartório"
df_remessa.loc[df_remessa['Ocorrencia'] == 'Pedido de ', 'Ocorrencia'] = "Solicitação de Baixa"
df_retorno.loc[df_retorno['Ocorrencia'] == 'Protesto Em cartório', 'Ocorrencia'] = "Em cartório"
#df_remessa.loc[df_remessa['TIPO DE INSTRUÇÃO ORIGEM'] == 'Protesto Em cartório', 'TIPO DE INSTRUÇÃO ORIGEM'] = "Em cartório"

condicao = (df_retorno['TIPO DE INSTRUÇÃO ORIGEM'] == 'Protestar') & (df_retorno['Ocorrencia'] == 'Instrução Confirmada')

# Atualizar o valor da coluna "Ocorrencia" para "boleto protestado" onde a condição for verdadeira
df_retorno.loc[condicao, 'Ocorrencia'] = 'Boleto Protestado'



# Fechar a conexão com o banco de dados
mydb.close()



# Converter a coluna 'Data da Ocorrencia' para o formato de data do pandas
df_remessa['Data da Ocorrencia'] = pd.to_datetime(df_remessa['Data da Ocorrencia'], format='%d%m%y', errors='coerce')

# Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
df_remessa['Data da Ocorrencia'] = df_remessa['Data da Ocorrencia'].dt.strftime('%d/%m/%Y')

# Converter a coluna 'Data da Ocorrencia' para o formato de data do pandas

# Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
#df_retorno['Data da Ocorrencia'] = df_retorno['Data da Ocorrencia'].dt.strftime('%d/%m/%Y')


df_retorno['DATA LIQUIDAÇÃO'] = pd.to_datetime(df_retorno['DATA LIQUIDAÇÃO'], format='%d%m%y', errors='coerce')

# Formatar a coluna 'Data da Ocorrencia' no novo formato desejado
df_retorno['DATA LIQUIDAÇÃO'] = df_retorno['DATA LIQUIDAÇÃO'].dt.strftime('%d/%m/%Y')


def create_data_table(id, data):
    return dash_table.DataTable(
        id=id,
        data=data.head(10).to_dict('records'),
        columns=[{'name': col, 'id': col} for col in data.columns],
        page_size=80,
        style_table={'overflowX': 'auto', 'width': '125%', 'margin-left': '-12%', 'margin-right': 'auto', 'z-index': '0','border': 'none'},
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
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    html.Img(src='/assets/unicredimagem.png', className="logo-img", style={'width': '10%', 'marginLeft': '450px','marginTop': '0px'}),
                    html.H3("Rastreamento de Boletos Unicred",className="text-titulo"),# ' style={'font':'Bahnschrift','marginBottom': '20px', 'margin-top': '0px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '0px'}),
                    dbc.Input(id='numero-boleto-input', type='text', placeholder='Digite o número do boleto'),
                    dbc.Button('Pesquisar por Nº do Documento', id='pesquisar-doc-button', n_clicks=0, color='primary', className='mr-1', style={'margin-bottom': '20px'}),
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
        return df_remessa.head(10).to_dict('records'), df_retorno.head(10).to_dict('records')  # Exibe apenas as 5 primeiras linhas se não houver pesquisa

    if ctx.triggered_id == 'pesquisar-doc-button':
        resultado_pesquisa_remessa = df_remessa[df_remessa['CODIGO DO DOC'].astype(str) == numero_boleto]
        resultado_pesquisa_retorno = df_retorno[df_retorno['CODIGO DO DOC'].astype(str) == numero_boleto]
        return resultado_pesquisa_remessa.head(10).to_dict('records'), resultado_pesquisa_retorno.head(10).to_dict('records')
    else:
        raise PreventUpdate

