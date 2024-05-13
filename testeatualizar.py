import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dd
from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import mysql.connector
import pandas as pd
from app import app


mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)



app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


def consultar_banco_dados():
    try:
        consulta = "SELECT * FROM devolucao"
        client_df = pd.read_sql(consulta, con=mydb)
        return client_df
    except mysql.connector.Error as e:
        print("Erro ao conectar-se ao banco de dados:", e)
        # Tentar reconectar-se ao banco de dados
        mydb.reconnect(attempts=3, delay=5)

colocar o retsnte aq



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    # Consultar o banco de dados para obter os dados atualizados
    client_df = consultar_banco_dados()
    
    # Retornar o layout da página com os dados atualizados
    return html.Div([
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
    ])

if __name__ == '__main__':
   app.run_server(debug=False, use_reloader=True, host='10.1.1.6', port=8040, dev_tools_hot_reload=True)
