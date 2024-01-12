from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dash_table
import mysql.connector
from app import app  # Importa o objeto app do arquivo app.py

# Conectar ao banco de dados
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Criação do aplicativo Dash

# Layout da aplicação
def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H4('Consultar Boletos', style={'margin-top': '10px', 'fontSize': 30, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'})),
        ]),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Input(
                        id='doc-number-input',
                        type='text',
                        placeholder='Digite o número do documento',
                        className="mb-3",
                            style={
                        'width': '100%',
                        'padding': '10px',
                        'font-size': '16px',
                        'border-radius': '5px',
                        'border': '1px solid #ced4da',
                        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.7)'  # Adiciona uma sombra
                    }
                    ),
                    dbc.Button('Consultar', id='btn-consultar', n_clicks=0, color="primary", className="mb-3"),
                    html.Div(id='consulta-output'),
                ]
            ),
        ]),
    ])

# Callback para executar a consulta quando o botão for clicado
@app.callback(
    Output('consulta-output', 'children'),
    [Input('btn-consultar', 'n_clicks')],
    [State('doc-number-input', 'value')]
)
def consultar_titulo(n_clicks, doc_number):
    try:
        if n_clicks > 0:
            # Realizar a consulta no banco de dados
            consulta = f"SELECT * FROM unicredremessa WHERE `Nº do Documento (Seu número)` = {doc_number}"
            cursor = mydb.cursor()
            cursor.execute(consulta)
            result = cursor.fetchall()

            if result:
                # Exibir o resultado da consulta
                table_header = [
                    html.Thead(html.Tr([html.Th(col) for col in cursor.column_names]))
                ]
                table_body = [
                    html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in result])
                ]

                return dbc.Table(
                    table_header + table_body,
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    className="mt-4"
                )
            else:
                return dbc.Alert("Nenhum título encontrado para o número do documento informado.", color="danger")

    except Exception as e:
        print(f"Error in consultar_titulo callback: {str(e)}")
        return dbc.Alert(f"Error: {str(e)}", color="danger")


if __name__ == '__main__':
    app.run_server(debug=True)