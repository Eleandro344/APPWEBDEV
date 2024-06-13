from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector
import pandas as pd
from dash import Dash, dcc
from app import app
from datetime import datetime, timedelta

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


        data_hoje_menos_5_dias = pd.Timestamp.today().normalize() - timedelta(days=0)

        client_df['Tempo(dias)'] = (client_df['Data'] - data_hoje_menos_5_dias).dt.days
        client_df['Tempo(dias)']
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
                                       className="mt-3")
                        )
                    ),
                ]
            ), 
        
            html.Div(
                [
                    html.H1("Devoluções cadastradas", className="text-devolucao"),
                    dash_table.DataTable(
                        id='client-table',
                        columns=[
                            {'name': col, 'id': col, 'editable': True if col in ['em_transito', 'chegou', 'finalizado'] else False} 
                            for col in client_df.columns
                        ],
                        data=client_df.to_dict('records'),
                        style_table={'overflowX': 'auto', 'width': '100%', 'margin-left': '0%', 'margin-right': 'auto', 'z-index': '0'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'font-family': 'Calibri'},
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                        ],
                    )
                ]
            ),
            
            html.Div(
                [
                    dbc.Button("Salvar Alterações", id="save-changes-button", color="primary", className="mt-3"),
                ]
            ),
        ]
    )

def insert_data_into_database(cliente, transporte, volumes, motivo, data):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "INSERT INTO devolucao (Cliente, Transporte, Volumes, Motivo, Data) VALUES (%s, %s, %s, %s, %s)"
    values = (cliente, transporte, volumes, motivo, data)

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
def update_client_df(n_clicks, cliente, transporte, volumes, motivo, data):
    if n_clicks > 0 and all([cliente, transporte, volumes, motivo, data]):
        global client_df
        new_data = {'Cliente': [cliente], 'Transporte': [transporte], 'Volumes': [volumes], 'Motivo': [motivo], 'Data': [data]}
        client_df = pd.concat([client_df, pd.DataFrame(new_data)], ignore_index=True)

        insert_data_into_database(cliente, transporte, volumes, motivo, data)

    raise PreventUpdate

@app.callback(
    Output('client-table', 'data'),
    [Input('client-table', 'loading_state')]
)
def reload_table_data(loading_state):
    # Verifica se o callback foi acionado pelo carregamento inicial da página
    if loading_state is None:
        raise PreventUpdate

    # Realiza uma nova consulta ao banco de dados
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    consulta = "SELECT * FROM devolucao"
    client_df = pd.read_sql(consulta, con=mydb)

    # Fecha a conexão
    mydb.close()

    # Retorna os dados da tabela atualizados
    return client_df.to_dict('records')

def update_data_in_database(cliente, em_transito, chegou, finalizado):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "UPDATE devolucao SET em_transito = %s, chegou = %s, finalizado = %s WHERE Cliente = %s"
    values = (em_transito, chegou, finalizado, cliente)

    cursor.execute(query, values)

    mydb.commit()
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

            # Atualize os valores no banco de dados
            update_data_in_database(cliente, em_transito, chegou, finalizado)

    return n_clicks or 0  # Retorna n_clicks se não for None, caso contrário, retorna 0
