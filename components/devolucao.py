from dash import html, Input, Output, State, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from app import app

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
        consulta = "SELECT * FROM devolucao"
        client_df = pd.read_sql(consulta, con=mydb)

        mydb.close()
        client_df2 = client_df
        client_df2['dia_chegou'] = pd.to_datetime(client_df2['dia_chegou'], format='%d/%m/%y')


        data_hoje_menos_5_dias = pd.Timestamp.today().normalize() - timedelta(days=0)
        # client_df2['dia_chegou'] = pd.to_datetime(client_df2['dia_chegou'], errors='coerce')

        client_df2['Tempo(a caminho)'] = (client_df2['Data'] - data_hoje_menos_5_dias).dt.days
        client_df2['Tempo(No estoque)'] = (client_df2['dia_chegou'] - data_hoje_menos_5_dias).dt.days
        client_df['Tempo(a caminho)']  =   client_df2['Tempo(a caminho)']
        client_df['Tempo(No estoque)']  =  client_df2['Tempo(No estoque)'] 
        client_df['Data'] = pd.to_datetime(client_df['Data'])
        client_df['dia_chegou'] = pd.to_datetime(client_df['dia_chegou'])

        # Data atual
        data_hoje = pd.Timestamp.today().normalize()

        # Calculando 'Tempo(a caminho)' e 'Tempo(No estoque)'
        client_df['Tempo(a caminho)'] = (data_hoje - client_df['Data']).dt.days
        client_df['Tempo(No estoque)'] = (data_hoje - client_df['dia_chegou']).dt.days

        # Função para parar de contar 'Tempo(No estoque)' quando 'finalizado' é 'Sim'
        def manter_tempo_no_estoque(row, valor_anterior):
            if row['finalizado'] == 'Sim':
                return valor_anterior
            else:
                return (data_hoje - row['dia_chegou']).days

        # Aplicando a função
        valor_anterior = None
        for index, row in client_df.iterrows():
            if index == 0:
                valor_anterior = client_df.loc[index, 'Tempo(No estoque)']
            else:
                valor_anterior = manter_tempo_no_estoque(row, valor_anterior)
                client_df.at[index, 'Tempo(No estoque)'] = valor_anterior

        client_df        
        client_df['dia_chegou'] = client_df['dia_chegou'].dt.strftime('%d/%m/%y') 
        return client_df
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None

# Carregar os dados da tabela de remessa
client_df = carregar_dados_remessa()

def layout():
    # Carregar os dados da tabela de remessa
    client_df = carregar_dados_remessa()
    if client_df is None:
        # Se houve um erro ao carregar os dados, retornar uma mensagem de erro
        return html.Div("Erro ao carregar dados da tabela de remessa.")

    return html.Div(
        className="container-fluid",
        children=[
            dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Cliente"),
                                dbc.Input(id="cliente-input", type="text", placeholder="Digite o Cliente"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Transporte"),
                                dbc.Input(id="transporte-input", type="text", placeholder="Digite o Transporte"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Volumes"),
                                dbc.Input(id="volumes-input", type="text", placeholder="Quantidade de volumes"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Motivo"),
                                dbc.Input(id="motivo-input", type="text", placeholder="Motivo"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Data"),
                                dbc.Input(id="data-input", type="date", placeholder="data"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Button("Cadastrar devolução", id="submit-button", n_clicks=0, color="primary",
                                     className='mr-1')
                        )
                    ),
                ]
            ),
            html.Div(
                [
                    html.H1("Devoluções cadastradas", className="text-devolucao"),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    id="filter-cliente",
                                    options=[
                                        {"label": cliente, "value": cliente} for cliente in client_df["Cliente"].unique()
                                    ],
                                    placeholder="Filtrar por Cliente",
                                ),
                                width=3,className="filtros"
                              #  style={'background-color': '#28a745', 'padding': '10px', 'border-radius': '5px'}
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="filter-em_transito",
                                    options=[
                                        {"label": "Sim", "value": "Sim"},
                                        {"label": "Não", "value": "Não"},
                                    ],
                                    placeholder="Filtrar por Em Trânsito",
                                ),
                                width=3,className="filtros"
                              #  style={'background-color': '#28a745', 'padding': '10px', 'border-radius': '5px'}
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="filter-chegou",
                                    options=[
                                        {"label": "Sim", "value": "Sim"},
                                        {"label": "Não", "value": "Não"},
                                    ],
                                    placeholder="Filtrar por Chegou",
                                ),
                                width=3,className="filtros"
                               # style={'background-color': '#28a745', 'padding': '10px', 'border-radius': '5px'}
                            ),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="filter-finalizado",
                                    options=[
                                        {"label": "Sim", "value": "Sim"},
                                        {"label": "Não", "value": "Não"},
                                    ],
                                    placeholder="Filtrar por Finalizado",
                                ),
                                width=3,className="filtros"
                                #style={'background-color': '#28a745', 'padding': '10px', 'border-radius': '5px'}
                            ),
                        ],
                        style={'margin-bottom': '20px'}
                    ),
                    dash_table.DataTable(
                        id='client-table',
                        columns=[
                            {'name': col, 'id': col, 'editable': True if col in ['em_transito', 'chegou','dia_chegou' ,'finalizado'] else False}
                            for col in client_df.columns
                        ],
                        data=client_df.to_dict('records'),
                        style_table={'overflowX': 'auto', 'width': '100%', 'margin-left': '0%', 'margin-right': 'auto', 'z-index': '0'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'font-family': 'Calibri'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                        ],
                    ),
                ]
            ),
            html.Div(
                [
                    dbc.Button("Salvar Alterações", id="save-changes-button", color="primary", className='mr-1'),
                ]
            ),
        ]
    )

def insert_data_into_database(cliente, transporte, volumes, motivo, data,):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "INSERT INTO devolucao (Cliente, Transporte, Volumes, Motivo, Data) VALUES (%s, %s, %s, %s, %s)"
    values = (cliente, transporte, volumes, motivo, data,)

    cursor.execute(query, values)

    mydb.commit()
    mydb.close()

@app.callback(
    Output("submit-button", "n_clicks"),
    [Input("submit-button", "n_clicks")],
    [
        State("cliente-input", "value"),
        State("transporte-input", "value"),
        State("volumes-input", "value"),
        State("motivo-input", "value"),
        State("data-input", "value"),
    ],
)
def update_client_df(n_clicks, cliente, transporte, volumes, motivo, data,):
    if n_clicks > 0 and all([cliente, transporte, volumes, motivo, data]):
        global client_df
        new_data = {'Cliente': [cliente], 'Transporte': [transporte], 'Volumes': [volumes], 'Motivo': [motivo], 'Data': [data]}
        client_df = pd.concat([client_df, pd.DataFrame(new_data)], ignore_index=True)

        insert_data_into_database(cliente, transporte, volumes, motivo, data)

    raise PreventUpdate

@app.callback(
    Output('client-table', 'data'),
    [
        Input('filter-cliente', 'value'),
        Input('filter-em_transito', 'value'),
        Input('filter-chegou', 'value'),
        Input('filter-finalizado', 'value')
    ]
)
def filter_table_data(cliente_filter, em_transito_filter, chegou_filter, finalizado_filter):
    # Realiza uma nova consulta ao banco de dados
    client_df = carregar_dados_remessa()

    if cliente_filter:
        client_df = client_df[client_df['Cliente'] == cliente_filter]

    if em_transito_filter:
        client_df = client_df[client_df['em_transito'] == em_transito_filter]

    if chegou_filter:
        client_df = client_df[client_df['chegou'] == chegou_filter]

    if finalizado_filter:
        client_df = client_df[client_df['finalizado'] == finalizado_filter]

    return client_df.to_dict('records')

def update_data_in_database(cliente, em_transito, chegou, finalizado, dia_chegou):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "UPDATE devolucao SET em_transito = %s, chegou = %s, finalizado = %s, dia_chegou = %s WHERE Cliente = %s"
    values = (em_transito, chegou, finalizado, dia_chegou, cliente,)

    cursor.execute(query, values)

    mydb.commit()
    mydb.close()
    mydb.close()

@app.callback(
    Output("save-changes-button", "n_clicks"),
    [Input("save-changes-button", "n_clicks")],
    [State("client-table", "data")],
)
def save_table_changes(n_clicks, table_data):
    if n_clicks is not None and n_clicks > 0:
        # Atualize o banco de dados com os dados alterados na tabela
        for row in table_data:
            cliente = row["Cliente"]
            em_transito = row.get("em_transito", "Não")  # Se a coluna estiver vazia, defina como "Não"
            chegou = row.get("chegou", "Não")
            finalizado = row.get("finalizado", "Não")
            dia_chegou = row.get("dia_chegou", None)  # Obtém a nova data de chegada

            # Atualize os valores no banco de dados
            update_data_in_database(cliente, em_transito, chegou, finalizado, dia_chegou)

    return n_clicks or 0  #

