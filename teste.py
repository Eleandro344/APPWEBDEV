from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)

# Execute a consulta SQL para selecionar todos os registros da tabela "Devolucao"
consulta = "SELECT * FROM devolucao"
client_df = pd.read_sql(consulta, con=mydb)

# Feche a conexão
mydb.close()


app = dash.Dash(__name__)

app.layout = dbc.Container(
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
                    html.H1("Devoluções cadastradas", style={'marginBottom': '20px', 'margin-top': '10px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
                    dash_table.DataTable(
                        id='client-table',
                        columns=[
                            {'name': col, 'id': col} for col in client_df.columns
                        ] + [
                            {'name': 'Excluir', 'id': 'delete-button', 'presentation': 'button'}
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
        ],
        fluid=True
    )

# Função para inserir dados no banco de dados
def insert_data_into_database(cliente, transporte, volumes, motivo):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "INSERT INTO devolucao (Cliente, Transporte, Volumes, Motivo) VALUES (%s, %s, %s, %s)"
    values = (cliente, transporte, volumes, motivo)

    cursor.execute(query, values)

    mydb.commit()
    mydb.close()

# Função para deletar uma devolução do banco de dados
def delete_devolucao(devolucao_id):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "DELETE FROM devolucao WHERE id = %s"
    values = (devolucao_id,)

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
    ],
)
def update_client_df(n_clicks, cliente, transporte, volumes, motivo):
    if n_clicks > 0 and all([cliente, transporte, volumes, motivo]):
        global client_df
        new_data = {'Cliente': [cliente], 'Transporte': [transporte], 'Volumes': [volumes], 'Motivo': [motivo]}
        client_df = pd.concat([client_df, pd.DataFrame(new_data)], ignore_index=True)

        insert_data_into_database(cliente, transporte, volumes, motivo)

    raise PreventUpdate

@app.callback(
    Output('client-table', 'data'),
    [Input('delete-button', 'n_clicks')],
    [State('client-table', 'derived_virtual_data')]
)
def delete_devolucao_row(n_clicks, rows):
    if n_clicks is None:
        raise PreventUpdate

    if not rows:
        raise PreventUpdate

    deleted_row_index = rows[-1]['id']

    # Assume que o ID da devolução está na primeira coluna
    devolucao_id = rows[deleted_row_index]['ID']

    delete_devolucao(devolucao_id)

    # Recarrega os dados da tabela após a exclusão
    # Isso também é necessário para atualizar a interface
    consulta = "SELECT * FROM devolucao"
    client_df = pd.read_sql(consulta, con=mydb)

    return client_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)