from dash import html
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import dash
from app import app  # Importa o objeto app do arquivo app.py

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
        # Execute a consulta SQL para selecionar todos os registros da tabela "cema_paga1"
        consulta = "SELECT * FROM cema_paga1"
        df_ordenado = pd.read_sql(consulta, con=mydb)
        mydb.close()
        new_column_order = [
	    "Data da Ocorrencia",
        "CNPJ",
        "Banco",
        "Valor do Título",
        "Nome/Razão Social do Pagador",
        "OBS",        
        "Ocorrencia",
        "CODIGO DO DOC",
        "Vencimento",
        "Status Atual",
        "Ordem",
        "IA",
            ]
                                                                                
        df_ordenado = df_ordenado[new_column_order]  
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Liquidação Normal', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Em cartório', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'LIQUIDAÇÃO EM CARTÓRIO', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Pago em Cartório', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Pago', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'LIQUIDAÇÃO NORMAL', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Boleto Baixado', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Baixado', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'BAIXA SIMPLES', 'Ordem'] = "Não pagar"
        df_ordenado.loc[df_ordenado['Status Atual'] == 'Liquidação de Título Trocado', 'Ordem'] = "Não pagar"



        df_ordenado.loc[df_ordenado['Ocorrencia'] == 'Solicitaçã', 'Ocorrencia'] = "Solicitado Baixa"

        df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento'], format='%Y-%m-%d')

        data_hoje_menos_5_dias = pd.Timestamp.today().normalize() - timedelta(days=30)
        df_ordenado = df_ordenado.loc[df_ordenado['Vencimento'] >= data_hoje_menos_5_dias]

        df_ordenado = df_ordenado.sort_values(by='Vencimento')
        df_ordenado = df_ordenado.drop(columns=['Ocorrencia'])
        df_ordenado = df_ordenado.drop(columns=['Data da Ocorrencia','CNPJ'])
        # df_ordenado = df_ordenado.loc[df_ordenado['Ordem'] == 'Cema Paga']
        df_ordenado['Vencimento'] = pd.to_datetime(df_ordenado['Vencimento']).dt.strftime('%d/%m/%Y')

        return df_ordenado
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None

# Layout da aplicação

def layout():
    # Carregar os dados da tabela de remessa
    df_ordenado = carregar_dados_remessa()
    if df_ordenado is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de remessa.")

    return dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H3('Boletos a pagar', className='text-titulo', style={'margin-top': '50px'}),
            ),
            dbc.Col(
                dcc.DatePickerRange(
                    id='date-picker-range',
                    display_format='DD/MM/YYYY',
                    style={'margin-top': '15px', 'margin-bottom': '15px'}  # Adiciona espaço acima e abaixo do filtro
                ),
                width=8,  # Ajuste a largura da coluna para mover o componente para a direita
            ),
        ]),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                id="filter-Ordem",
                                options=[
                                    {"label": Ordem, "value": Ordem} for Ordem in df_ordenado["Ordem"].unique()
                                ],
                                placeholder="Filtrar por Pagar",
                                multi=True, # Permitir múltiplas seleções
                            ),
                            )]),
                          
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    id='data-table',
                    data=df_ordenado.to_dict('records'),
                    columns=[{'name': col, 'id': col, 'editable': True if col == 'OBS' else False} for col in df_ordenado.columns],
                    # page_size=10,  # Defina o número de linhas por página
                    style_table={ 'width': '100%', 'margin-top': '30px', 'margin-left': '-20%', 'border': 'none', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'},
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'color': '#0e0e0d','font-size ':'12px' ,'fontFamily': 'Poppins, Arial', 'borderBottom': '1px solid #00aaff'},
                    style_cell= {                                   
                    'textAlign': 'left',
                    'fontFamily': 'Poppins, Arial',
                    'font-size': '14px',  # Reduza o tamanho da fonte
                    'minWidth': '180px',   # Reduza a largura mínima
                    'maxWidth': '200px',  # Defina a largura m  áxima
                    'padding': '5p',
                    'whiteSpace': 'normal' }  ,# Estilo das células
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                        {'if': {'column_id': 'Ordem'}, 'backgroundColor': 'red', 'color': 'white'},
                        {'if': {'column_id': 'Status Atual'}, 'backgroundColor': 'red', 'color': 'white'},
                        {'if': {'column_id': 'IA'}, 'backgroundColor': 'LightCyan', 'color': 'black'},
                        {'if': {'column_id': 'Ordem', 'filter_query': '{Ordem} eq "Não pagar"'}, 'backgroundColor': 'ForestGreen', 'color': 'white'},
                        {'if': {'column_id': 'Vencimento', 'filter_query': '{Vencimento} eq "' + datetime.now().strftime('%Y-%m-%d') + '"'}, 'backgroundColor': 'yellow', 'color': 'black'},
                    ],
                ),
            ),
        ]),
        dbc.Row([
            dbc.Button("Salvar OBS", id="salvar-obs-button", color="primary", className="mr-2", style={'margin-top': '15px'})
        ]),
        dbc.Col(
            html.H3('(IA) Probabilidade de antecipação do titulo pelo Pagador', className='text-ia', style={'margin-top': '50px'}),
        ),
    ])

@app.callback(
    Output('data-table', 'data'),
    [Input('salvar-obs-button', 'n_clicks')],
    [State('data-table', 'data')]
)
def salvar_observacoes(n_clicks, data):
    if n_clicks is None:
        return dash.no_update
    
    print("Botão 'Salvar OBS' clicado. Dados recebidos:", data)
    
    try:
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',
            database='db_sabertrimed',
        )
        print("Conexão com o banco de dados estabelecida.")
        
        cursor = mydb.cursor()
        for row in data:
            obs = row.get('OBS')
            codigo = row.get('CODIGO DO DOC')  # Assuming this is the correct column name
            cursor.execute("UPDATE cema_paga1 SET OBS = %s WHERE `CODIGO DO DOC` = %s", (obs, codigo))
        mydb.commit()
        mydb.close()
        return data
    except mysql.connector.Error as e:
        return dash.no_update
    
@app.callback(
    Output('data-table', 'data', allow_duplicate=True),
    [Input('filter-Ordem', 'value')],
    prevent_initial_call=True
)
def filtrar_dados(Ordem):
    # Carregar os dados da tabela de remessa
    df_ordenado = carregar_dados_remessa()

    # Verifica se o DataFrame está vazio
    if df_ordenado is None or df_ordenado.empty:
        return dash.no_update

    # Aplicar o filtro conforme o valor selecionado
    if Ordem:
        df_ordenado = df_ordenado[df_ordenado['Ordem'].isin(Ordem)]

    return df_ordenado.to_dict('records')
