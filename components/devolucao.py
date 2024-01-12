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
                                dbc.Label("Nome"),
                                dbc.Input(id="name-input", type="text", placeholder="Digite o nome"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Email"),
                                dbc.Input(id="email-input", type="email", placeholder="Digite o email"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Telefone"),
                                dbc.Input(id="phone-input", type="tel", placeholder="Digite o telefone"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Button("Cadastrar Cliente", id="submit-button", n_clicks=0, color="primary",
                                       className="mt-3")
                        )
                    ),
                ]
            ),
            html.Div(
                [
                    html.H2("Clientes Cadastrados"),
                    dash_table.DataTable(
                        id='client-table',
                        columns=[{'name': col, 'id': col} for col in client_df.columns],
                        data=client_df.to_dict('records'),
                    )
                ]
            ),
        ],
        fluid=True
    )


# Function to insert data into the database
def insert_data_into_database(name, email, phone):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    # Use placeholders to prevent SQL injection
    query = "INSERT INTO devolucao (Nome, Email, Telefone) VALUES (%s, %s, %s)"
    values = (name, email, phone)

    cursor.execute(query, values)

    # Commit the changes and close the connection
    mydb.commit()
    mydb.close()


# Callback to update the client DataFrame and insert data into the database
@app.callback(
    Output("submit-button", "n_clicks"),
    [Input("submit-button", "n_clicks")],
    [
        State("name-input", "value"),
        State("email-input", "value"),
        State("phone-input", "value"),
    ],
)
def update_client_df(n_clicks, name, email, phone):
    if n_clicks > 0 and all([name, email, phone]):
        global client_df
        new_data = {'Nome': [name], 'Email': [email], 'Telefone': [phone]}
        client_df = pd.concat([client_df, pd.DataFrame(new_data)], ignore_index=True)

        # Insert data into the database
        insert_data_into_database(name, email, phone)

    # Prevent updating the button's n_clicks property to avoid re-triggering the callback
    raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
