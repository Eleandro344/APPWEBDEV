import dash
from datetime import datetime, timedelta
from dash import dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import mysql.connector
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
        # Execute a consulta SQL para selecionar todos os registros da tabela "agendamentos"
        consulta = "SELECT fornecedor, transporte, nota, volumes, entrega, status FROM agendamentos"
        client_df = pd.read_sql(consulta, con=mydb)
        mydb.close()

        # Obter a data de hoje
        hoje = datetime.now()
        # Verificar se hoje é segunda-feira (weekday() retorna 0 para segunda-feira)
        hoje = hoje.strftime('%Y-%m-%d')
        client_df['entrega'] = client_df['entrega'].astype(str)
        
        # entregashoje = client_df.loc[client_df['status'] !=  'concluído']
        entregashoje = client_df.loc[client_df['entrega'] == hoje]

        atrasados = client_df.loc[(client_df['status'] == 'pendente') & (client_df['entrega'] < hoje)]
        atrasados = atrasados.loc[atrasados['status'] == 'pendente'] 
        atrasados['status'] = 'atrasado'
        client_df.loc[(client_df['status'] == 'pendente') & (client_df['entrega'] < hoje), 'status'] = 'atrasado'
        entregashoje = pd.concat([entregashoje, atrasados])
        client_df['entrega'] = pd.to_datetime(client_df['entrega']).dt.strftime('%d/%m/%Y')
        entregashoje['entrega'] = pd.to_datetime(entregashoje['entrega']).dt.strftime('%d/%m/%Y')
        client_df['status_order'] = client_df['status'].apply(lambda x: 0 if x == 'pendente' else 1)    
        
        # Ordenar o DataFrame pela coluna temporária de ordem de status
        client_df = client_df.sort_values(by=['status_order', 'status'], ascending=[True, True])

        # Remover a coluna temporária de ordem de status
        client_df = client_df.drop(columns=['status_order'])


        # client_df = client_df.loc[client_df['entrega'] == ]

        return client_df, entregashoje
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        return None, None

# Carregar os dados da tabela de remessa
def layout():
    client_df, entregashoje = carregar_dados_remessa()
    
    if client_df is None or entregashoje is None:
        return html.Div("Erro ao carregar dados da tabela de remessa.")
    
    return html.Div(
        className="container-fluid",
        children=[
            dbc.CardGroup(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Fornecedor"),
                                dbc.Input(id="fornecedor-input", type="text", placeholder="Digite o Fornecedor"),
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
                                dbc.Label("Nota"),
                                dbc.Input(id="nota-input", type="text", placeholder="Digite a Prenota"),
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
                                dbc.Label("Data da Entrega"),
                                dbc.Input(id="entrega-input", type="date", placeholder="Data"),
                            ]
                        )
                    ),
                
            dbc.Card(
                dbc.CardBody(
                    dbc.Button("agendar", id="submit-button", n_clicks=0, color="primary",
                               className='mr-1')
                        )
                    ),

            dbc.Card(
                dbc.CardBody(
                    dbc.Button("Marcar como Entregue", id="mark-delivered-button", n_clicks=0, color="success",
                               className='mr-1')
                )
            ),
                ]
            ),            
            html.Div(
                [
                    html.H1("Entregas para hoje", className="text-devolucao4"),
                    dash_table.DataTable(
                        id='client-table2',
                        columns=[
                            {'name': col, 'id': col} for col in entregashoje.columns
                        ] + [],
                        data=entregashoje.to_dict('records'),
                        markdown_options={"html": True},
                        style_table={
                            'overflowX': 'auto',
                            'width': '100%',
                            'margin-top': '30px',
                            'margin-left': '-2%',
                            'margin-right': 'auto',
                            'z-index': '0',
                            'border': 'none',
                            'border-radius': '10px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'color': '#0e0e0d',
                            'font-size': '14px',
                            'fontFamily': 'Poppins, Arial',
                            'borderBottom': '1px solid #00aaff'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'fontFamily': 'Poppins, Arial',
                            'font-size': '14px',
                            'minWidth': '120px',
                            'maxWidth': '130px',
                            'padding': '5px',
                            'whiteSpace': 'normal'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                            {'if': {'column_id': 'finalizado'}, 'backgroundColor': '#00FFFF', 'color': 'Black'},
                            {'if': {'column_id': 'dia_chegou'}, 'backgroundColor': '#f3ef1d', 'color': 'Black'},
                            {'if': {'column_id': 'conferida'}, 'backgroundColor': '#f3ef1d', 'color': 'Black'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "concluído"'}, 'backgroundColor': 'ForestGreen', 'color': 'white'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "pendente"'}, 'backgroundColor': 'yellow', 'color': 'black'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "atrasado"'}, 'backgroundColor': 'red', 'color': 'white'},

                        ],
                        row_selectable='single',  # Permitir a seleção de uma linha por vez
                    ),
                    html.H1("Próximas entregas", className="text-devolucao4"),
                    dash_table.DataTable(
                        id='entregas-table2',
                        columns=[
                            {'name': col, 'id': col} for col in client_df.columns
                        ] + [],
                        data=client_df.to_dict('records'),
                        markdown_options={"html": True},
                        style_table={
                            'overflowX': 'auto',
                            'width': '100%',
                            'margin-top': '30px',
                            'margin-left': '-2%',
                            'margin-right': 'auto',
                            'z-index': '0',
                            'border': 'none',
                            'border-radius': '10px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'color': '#0e0e0d',
                            'font-size': '14px',
                            'fontFamily': 'Poppins, Arial',
                            'borderBottom': '1px solid #00aaff'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'fontFamily': 'Poppins, Arial',
                            'font-size': '14px',
                            'minWidth': '120px',
                            'maxWidth': '130px',
                            'padding': '5px',
                            'whiteSpace': 'normal'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                            {'if': {'column_id': 'finalizado'}, 'backgroundColor': '#00FFFF', 'color': 'Black'},
                            {'if': {'column_id': 'dia_chegou'}, 'backgroundColor': '#f3ef1d', 'color': 'Black'},
                            {'if': {'column_id': 'conferida'}, 'backgroundColor': '#f3ef1d', 'color': 'Black'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "concluído"'}, 'backgroundColor': 'ForestGreen', 'color': 'white'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "pendente"'}, 'backgroundColor': 'yellow', 'color': 'black'},
                             {'if': {'column_id': 'status', 'filter_query': '{status} eq "atrasado"'}, 'backgroundColor': 'red', 'color': 'white'},
                        ],
                    ),
                ]
            ),
        ]
    )

def insert_data_into_database(fornecedor, transporte, nota, volumes, entrega, status):
    mydb = mysql.connector.connect(
        host='db_sabertrimed.mysql.dbaas.com.br',
        user='db_sabertrimed',
        password='s@BRtR1m3d',
        database='db_sabertrimed',
    )

    cursor = mydb.cursor()

    query = "INSERT INTO agendamentos (fornecedor, transporte, nota, volumes, entrega, status) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (fornecedor, transporte, nota, volumes, entrega, status)

    cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    mydb.close()

@app.callback(
    Output('client-table2', 'data', allow_duplicate=True),
    [Input('submit-button', 'n_clicks')],
    [
        State('fornecedor-input', 'value'),
        State('transporte-input', 'value'),
        State('nota-input', 'value'),
        State('volumes-input', 'value'),
        State('entrega-input', 'value'),
        State('client-table2', 'data'),
    ],
    prevent_initial_call=True  # Adiciona prevent_initial_call aqui
)
def adicionar_remessa(n_clicks, fornecedor, transporte, nota, volumes, entrega, rows):
    if n_clicks > 0:
        nova_linha = {
            'Fornecedor': fornecedor,
            'Transporte': transporte,
            'Nota': nota,
            'Volumes': volumes,
            'Entrega': entrega,
            'Status': 'pendente'  # Adiciona status inicial
        }
        rows.append(nova_linha)
        insert_data_into_database(fornecedor, transporte, nota, volumes, entrega, status="pendente")
    return rows

@app.callback(
    Output('client-table2', 'data'),
    [Input('mark-delivered-button', 'n_clicks')],
    [
        State('client-table2', 'data'),
        State('client-table2', 'selected_rows'),
    ],
    prevent_initial_call=True
)
def marcar_como_entregue(n_clicks, rows, selected_rows):
    if n_clicks > 0 and selected_rows:
        selected_index = selected_rows[0]  # Pega o índice da linha selecionada
        if selected_index < len(rows):
            # Atualiza o status da linha selecionada
            rows[selected_index]['Status'] = 'concluído'

            # Atualiza o banco de dados
            mydb = mysql.connector.connect(
                host='db_sabertrimed.mysql.dbaas.com.br',
                user='db_sabertrimed',
                password='s@BRtR1m3d',
                database='db_sabertrimed',
            )
            cursor = mydb.cursor()
            
            # Identifica o valor da nota para atualização
            nota = rows[selected_index]['nota']

            query = "UPDATE agendamentos SET status = %s WHERE nota = %s"
            values = ('concluído', nota)
            
            cursor.execute(query, values)
            mydb.commit()
            cursor.close()
            mydb.close()

    return rows
