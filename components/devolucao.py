from dash import html, Input, Output, State, dcc, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from app import app
import json
import dash
from dotenv import load_dotenv
import os

load_dotenv()
# Função para carregar os dados da tabela de remessa
def carregar_dados_remessa():
    try:
        # Conexão com o banco de dados
        mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        )
        # Execute a consulta SQL para selecionar todos os registros da tabela "devolucao"
        consulta = "SELECT * FROM devolucao"
        client_df = pd.read_sql(consulta, con=mydb)

        mydb.close()
        client_df2 = client_df
        client_df2['dia_chegou'] = pd.to_datetime(client_df2['dia_chegou'], format='%d/%m/%y')

        data_hoje_menos_5_dias = pd.Timestamp.today().normalize() - timedelta(days=0)



        #TEMPO A CAMINHO 

        client_df2['Tempo(a caminho)'] = (client_df2['Data'] - data_hoje_menos_5_dias).dt.days




        client_df['Tempo(a caminho)']  = client_df2['Tempo(a caminho)']

        client_df['Data'] = pd.to_datetime(client_df['Data'])
        client_df['dia_chegou'] = pd.to_datetime(client_df['dia_chegou'])
        client_df['chegou'] = client_df['chegou'].astype(str) 
        client_df['chegou'] = "Sim"        
        client_df.loc[client_df['Data'] != 0, 'em_transito'] = 'Sim'

        # TEMPO DE CONFERENCIA

        client_df['Tempo(conferida)'] = (client_df['dia_chegou'] - data_hoje_menos_5_dias).dt.days

        client_df.loc[client_df['dia_chegou'].isna(), 'Tempo(conferida)'] = 'Não chegou'

        # client_df.loc[client_df['conferida']!= "none",'Tempo(conferida)' = 'Conferida']
        client_df.loc[client_df['conferida'].notna(), 'Tempo(conferida)'] = 'Conferida'





        # Data atual
        data_hoje = pd.Timestamp.today().normalize()
        # Calculando 'Tempo(a caminho)' e 'Tempo(No estoque)'
        client_df['Tempo(a caminho)'] = (data_hoje - client_df['Data']).dt.days

        client_df['dia_chegou'] = client_df['dia_chegou'].dt.strftime('%d/%m/%y')
        # client_df.loc[client_df['finalizado']!= "Não", 'Tempo(No estoque)'] = 'Concluida'
        client_df.loc[~client_df['dia_chegou'].isna(), 'Tempo(a caminho)'] = 'ja Chegou'

        # client_df['conferida'] = client_df['conferida'].dt.strftime('%d/%m/%y')


        #TEMPO LANÇAMENTO

        client_df2['conferida'] = pd.to_datetime(client_df2['conferida'], format='%d/%m/%y')

        client_df['Tempo(lançado)'] = (client_df['conferida'] - data_hoje_menos_5_dias).dt.days


        # client_df.loc[client_df['finalizado']!= "Não",'Tempo(lançado)'= 'Concluida']
        client_df.loc[(client_df['finalizado'] != 'Não') & (client_df['finalizado'].notna()), 'Tempo(lançado)'] = 'Concluida'

        # client_df.loc[client_df['conferida'].notna(), 'Tempo(conferida)'] = 'Conferida'






        client_df.loc[client_df['dia_chegou'].isna(), 'chegou'] = 'Não'
        client_df.loc[client_df['finalizado'].isna(), 'finalizado'] = 'Não'

        client_df.loc[~client_df['dia_chegou'].isna(), 'Tempo(a caminho)'] = 'ja Chegou'
        client_df['Tempo(conferida)'] = client_df['Tempo(conferida)'].apply(lambda x: abs(float(x)) if isinstance(x, (int, float)) else x)

        client_df['Tempo(lançado)'] = client_df['Tempo(lançado)'].apply(lambda x: abs(float(x)) if isinstance(x, (int, float)) else x)
        client_df['conferida'] = pd.to_datetime(client_df['conferida'], errors='coerce')
        client_df['conferida'] = client_df['conferida'].dt.strftime('%d/%m/%y')
        # client_df['Data'] = pd.to_datetime(client_df['Data'], errors='coerce')
        # client_df['Data'] = client_df['Data'].dt.strftime('%d/%m/%y')        


        client_df['delete-button'] = [
            f'<button class="btn btn-danger" type="button" id="delete-button-{index}">Deletar</button>'
            for index in range(len(client_df))
        ]


        return client_df
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None

# Carregar os dados da tabela de remessa
client_df = carregar_dados_remessa()
client_df = client_df.drop(columns=["delete-button"])


def layout():
    # Carregar os dados da tabela de remessa
    client_df = carregar_dados_remessa()
    client_df = client_df.drop(columns=["delete-button"])

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
                                dbc.Label("Pre_nota"),
                                dbc.Input(id="Prenota-input", type="text", placeholder="Digite a Prenota"),
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
                      html.H4("Estoque preencha as colunas (Amarelas)", className="text-devolucao2"),
                      html.H4("Financeiro preencha as colunas (Azul)", className="text-devolucao3"),
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
                                {'name': col, 'id': col, 'editable': True if col in ['em_transito', 'chegou','dia_chegou', 'conferida','finalizado'] else False}
                                for col in client_df.columns
                            ] + [
                                {'name': 'Deletar', 'id': 'delete-button', 'type': 'text', 'presentation': 'markdown'},
                            ],
                            data=client_df.to_dict('records'),
                            markdown_options={"html": True},
                            style_table={'overflowX': 'auto', 'width': '100%', 'margin-top': '30px', 'margin-left': '-2%', 'margin-right': 'auto', 'z-index': '0', 'border': 'none', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'color': '#0e0e0d','font-size ':'12px' ,'fontFamily': 'Poppins, Arial', 'borderBottom': '1px solid #00aaff'},
                                style_cell={
                                    'textAlign': 'left',
                                    'fontFamily': 'Poppins, Arial',
                                    'font-size': '13px',  # Reduza o tamanho da fonte
                                    'minWidth': '100px',   # Reduza a largura mínima
                                    'maxWidth': '130px',  # Defina a largura máxima
                                    'padding': '5p',
                                    'whiteSpace': 'normal' 
          # Permite quebra de linha

                                },
                                style_data_conditional=[
                                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                                {'if': {'column_id': 'finalizado'}, 'backgroundColor': '#00FFFF','color': 'Black'},
                                {'if': {'column_id': 'dia_chegou'}, 'backgroundColor': '#f3ef1d','color': 'Black'},
                                {'if': {'column_id': 'conferida'}, 'backgroundColor': '#f3ef1d','color': 'Black'},


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

def insert_data_into_database(cliente, transporte, Pre_nota, volumes, motivo, data):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "INSERT INTO devolucao (Cliente, Transporte, Pre_nota, Volumes, Motivo, Data) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (cliente, transporte, Pre_nota, volumes, motivo, data)

    cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    mydb.close()

def delete_data_from_database(cliente, transporte,Pre_nota, volumes, motivo, data):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "DELETE FROM devolucao WHERE Cliente = %s AND Transporte = %s AND Pre_nota = %s AND Volumes = %s AND Motivo = %s AND Data = %s"
    values = (cliente, transporte, Pre_nota, volumes, motivo, data)

    cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    mydb.close()
    

@app.callback(
    Output('client-table', 'data', allow_duplicate=True),
    [Input('submit-button', 'n_clicks')],
    [
        State('cliente-input', 'value'),
        State('transporte-input', 'value'),
        State('Prenota-input', 'value'),
        State('volumes-input', 'value'),
        State('motivo-input', 'value'),
        State('data-input', 'value'),
        State('client-table', 'data'),
    ],
    prevent_initial_call=True  # Adiciona prevent_initial_call aqui
)
def adicionar_remessa(n_clicks, cliente, transporte, Pre_nota, volumes, motivo, data, rows):
    if n_clicks > 0:
        nova_linha = {'Cliente': cliente, 'Transporte': transporte, 'Pre_nota': Pre_nota, 'Volumes': volumes, 'Motivo': motivo, 'Data': data}
        rows.append(nova_linha)
        insert_data_into_database(cliente, transporte, Pre_nota, volumes, motivo, data)
    return rows


@app.callback(
    Output('client-table', 'data', allow_duplicate=True),
    Input('client-table', 'active_cell'),
    State('client-table', 'data'),
    prevent_initial_call=True

)
def deletar_linha(active_cell, rows):
    if active_cell and active_cell['column_id'] == 'delete-button':
        row_id = active_cell['row']
        linha = rows.pop(row_id)
        delete_data_from_database(linha['Cliente'], linha['Transporte'], linha['Pre_nota'], linha['Volumes'], linha['Motivo'], linha['Data'])
    return rows

@app.callback(
    Output('client-table', 'data', allow_duplicate=True),
    [Input('save-changes-button', 'n_clicks')],
    [State('client-table', 'data')],
    prevent_initial_call=True

)
def salvar_alteracoes(n_clicks, rows):
    if n_clicks > 0:
        mydb = mysql.connector.connect(
            host='db_sabertrimed.mysql.dbaas.com.br',
            user='db_sabertrimed',
            password='s@BRtR1m3d',
            database='db_sabertrimed',
        )
        cursor = mydb.cursor()

        for row in rows:
            query = """
            UPDATE devolucao
            SET em_transito = %s, chegou = %s, dia_chegou = %s, conferida = %s, finalizado = %s
            WHERE Cliente = %s AND Transporte = %s AND Pre_nota = %s AND Volumes = %s AND Motivo = %s AND Data = %s
            """
            values = (row['em_transito'], row['chegou'], row['dia_chegou'], row['conferida'], row['finalizado'], row['Cliente'], row['Transporte'], row['Pre_nota'], row['Volumes'], row['Motivo'], row['Data'])
            cursor.execute(query, values)

        mydb.commit()
        cursor.close()
        mydb.close()

    return rows

@app.callback(
    Output('client-table', 'data', allow_duplicate=True),
    [Input({'type': 'delete-button', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State('client-table', 'data')],
    prevent_initial_call=True
)
def delete_row(delete_buttons, table_data):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    triggered = ctx.triggered[0]
    if 'delete-button' in triggered['prop_id']:
        delete_index = json.loads(triggered['prop_id'].split('.')[0])['index']
        row_to_delete = table_data[delete_index]

        delete_data_from_database(
            row_to_delete['Cliente'],
            row_to_delete['Transporte'],
            row_to_delete['Transporte'],
            row_to_delete['Pre_nota'],
            row_to_delete['Volumes'],
            row_to_delete['Motivo'],
            row_to_delete['Data']
        )

        del table_data[delete_index]

    return table_data




@app.callback(
    Output('client-table', 'data'),
    [
        Input('filter-cliente', 'value'),
        Input('filter-em_transito', 'value'),
        Input('filter-chegou', 'value'),
        Input('filter-finalizado', 'value'),
    ]
)
def filtrar_dados(cliente, em_transito, chegou, finalizado):
    # Carregar os dados da tabela de remessa
    client_df = carregar_dados_remessa()

    # Aplicar os filtros conforme os valores selecionados
    if cliente:
        client_df = client_df[client_df['Cliente'] == cliente]
    if em_transito:
        client_df = client_df[client_df['em_transito'] == em_transito]
    if chegou:
        client_df = client_df[client_df['chegou'] == chegou]
    if finalizado:
        client_df = client_df[client_df['finalizado'] == finalizado]

    return client_df.to_dict('records')



