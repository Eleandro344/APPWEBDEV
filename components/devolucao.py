import dash_bootstrap_components as dbc
from dash import html
from dash import Dash, dcc, html
from dash import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app  # Importa o objeto app do arquivo app.py

import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Notas_Fiscais"
consulta = "SELECT * FROM devolucao"  # SELECIONA A TABELA
client_df = pd.read_sql(consulta, con=mydb)  # TRANSFORMA EM DATAFRAME

# Feche a conexão
mydb.close()


def layout():
    return dbc.Container(
        [
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
                            dbc.Button("Cadastrar devolução", id="submit-button", n_clicks=0, color="primary",
                                       className="mt-3")
                        )
                    ),
                ]
            ),
         html.Div(
                [
                        html.H2("Devoluções cadastradas"),
                        dash_table.DataTable(
                            id='client-table',
                            columns=[{'name': col, 'id': col} for col in client_df.columns],
                            data=client_df.to_dict('records'),
                            style_table={'overflowX': 'auto', 'maxHeight': '500px', 'overflowY': 'auto'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                            style_cell={
                                'textAlign': 'left',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                        },
                    )
                ]
            ),
        ],
        fluid=True
    )


# Function to insert data into the database
def insert_data_into_database(cliente, transporte, volumes, motivo):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    # Use placeholders to prevent SQL injection
    query = "INSERT INTO devolucao (Cliente, Transporte, Volumes, Motivo) VALUES (%s, %s, %s, %s)"
    values = (cliente, transporte, volumes, motivo)

    cursor.execute(query, values)

    # Commit the changes and close the connection
    mydb.commit()
    mydb.close()


# Callback to update the client DataFrame and insert data into the database
@app.callback(
    Output("submit-button", "n_clicks"),
    [Input("submit-button", "n_clicks")],
    [
        State("cliente-input", "value"),
        State("transporte-input", "value"),
        State("volumes-input", "value"),
        State("motivo-input", "value"),
    ],
)
def update_client_df(n_clicks, cliente, transporte, volumes, motivo):
    if n_clicks > 0 and all([cliente, transporte, volumes, motivo]):
        global client_df
        new_data = {'Cliente': [cliente], 'Transporte': [transporte], 'Volumes': [volumes], 'Motivo': [motivo]}
        client_df = pd.concat([client_df, pd.DataFrame(new_data)], ignore_index=True)

        # Insert data into the database
        insert_data_into_database(cliente, transporte, volumes, motivo)

    # Prevent updating the button's n_clicks property to avoid re-triggering the callback
    raise PreventUpdate



