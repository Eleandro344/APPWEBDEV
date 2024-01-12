from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from app import app
import mysql.connector
from dash import dcc
import dash
import dash_bootstrap_components as dbc
from dash import html, Dash, dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
import mysql.connector
from dash import dcc
from app import app  # Importa o objeto app do arquivo app.py

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

def layout():
    return dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Cadastro de Cliente"), className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Label("Nome do Cliente", className="form-label"),
                        dbc.Input(id="input-nome", type="text", placeholder="Digite o nome do cliente"),
                    ]),
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Label("Email do Cliente", className="form-label"),
                        dbc.Input(id="input-email", type="email", placeholder="Digite o email do cliente"),
                    ]),
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Label("Telefone do Cliente", className="form-label"),
                        dbc.Input(id="input-telefone", type="tel", placeholder="Digite o telefone do cliente"),
                    ]),
                ], className="mb-3"),
            ]),
            dbc.Button("Cadastrar Cliente", id="btn-cadastrar", color="primary", className="mt-3"),
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id="div-mensagem"),
        ], className="mt-4"),
    ]),
])

# Callback para cadastrar cliente no banco de dados
# Callback para cadastrar cliente no banco de dados
@app.callback(
    Output("div-mensagem", "children"),
    Input("btn-cadastrar", "n_clicks"),
    State("input-nome", "value"),
    State("input-email", "value"),
    State("input-telefone", "value"),
)
def cadastrar_cliente(n_clicks, nome, email, telefone):
    if n_clicks is not None:
        try:
            # Conectar ao banco de dados
            mydb = mysql.connector.connect(
                host='db_sabertrimed.mysql.dbaas.com.br',
                user='db_sabertrimed',
                password='s@BRtR1m3d',
                database='db_sabertrimed',
            )

            # Executar a consulta SQL para inserir um novo cliente
            consulta = f"INSERT INTO devolucao (nome, email, telefone) VALUES ('{nome}', '{email}', '{telefone}')"
            cursor = mydb.cursor()
            cursor.execute(consulta)
            mydb.commit()

            mensagem = html.Div("Cliente cadastrado com sucesso!", className="alert alert-success")
        except Exception as e:
            mensagem = html.Div(f"Erro ao cadastrar cliente: {str(e)}", className="alert alert-danger")

        finally:
            # Fechar a conexão
            mydb.close()

        return mensagem
    return None

if __name__ == '__main__':
    app.run_server(debug=True)