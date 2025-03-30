# from dash import html, dcc, callback
# from dash.dependencies import Input, Output, State
# from datetime import date, datetime, timedelta
# import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import calendar
# import mysql.connector
# from dash_table import DataTable
# import locale

# from app import app

# card_icon = {
#     'color': 'white',
#     'textAlign': 'center',
#     'fontSize': 30,
#     'margin': 'auto',
# }

# mydb = mysql.connector.connect(
#     host=os.getenv('DB_HOST'),
#     user=os.getenv('DB_USER'),
#     password=os.getenv('DB_PASSWORD'),
#     database=os.getenv('DB_NAME'),
# # )

# consulta = "SELECT * FROM vendas"
# df = pd.read_sql(consulta, con=mydb)
# mydb.close()
# #df = df[df['oper_'] == 'Venda']
# #df['tot_venda'] = pd.to_numeric(df['tot_venda'].str.replace(',', '.'), errors='coerce')
# df['mc_b_'] = pd.to_numeric(df['mc_b_'].str.replace(',', '.'), errors='coerce')


# df = pd.read_excel("C:/Users/elean/Desktop/bancodedados/vendas12.xlsx")
# df = df[df['Oper.'] == 'Venda']



# #df['Tot_Venda'] = pd.to_numeric(df['Tot_Venda'].str.replace(',', '.'), errors='coerce')
# df['MC_B%'] = pd.to_numeric(df['MC_B%'].str.replace(',', '.'), errors='coerce')
# vendas = df[["Oper.","COD", "Hora", "Tot_Venda", "Cliente", "Cond. Pgto", "Orig", "MC_B%", "$FlexVe", "Gerou Flex","Nome_Cidade"]]
# total = df['Tot_Venda'].sum()
# mctotal = df['MC_B%'].mean()

# mctotal = round(mctotal, 2)

# # Formata como uma string com o símbolo de porcentagem
# mctotal = '{:.2f}%'.format(mctotal)




# total = '{:,.2f}'.format(total)

# # Adiciona o símbolo da moeda, se necessário
# total = 'R$ ' + total
# total = total.replace(',', '|')

# # Substitua os pontos por vírgulas
# ttotalemp = total.replace('.', ',')

# # Substitua o caractere temporário por pontos
# total = total.replace('|', '.')

# total
# # Exibe o valor formatado



# def layout():
#     return dbc.Col([
#         dbc.Row([
#             dbc.Col([
#                 dbc.CardGroup([
#                     dbc.Card([
#                         html.Legend("Vendas"),
#                         html.H5(total, id="p-saldo-dashboards", style={}),
#                     ], style={"padding-left": "20px", "padding-top": "10px"}),
#                     dbc.Card(
#                         html.Div(className="fa fa-university", style=card_icon),
#                         color="warning",
#                         style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
#                     )
#                 ])
#             ], width=4),
#             dbc.Col([
#                 dbc.CardGroup([
#                     dbc.Card([
#                         html.Legend("MC"),
#                         html.H5(mctotal, id="p-receita-dashboards", style={}),
#                     ], style={"padding-left": "20px", "padding-top": "10px"}),
#                     dbc.Card(
#                         html.Div(className="fa fa-smile-o", style=card_icon),
#                         color="success",
#                         style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
#                     )
#                 ])
#             ], width=4),
#             dbc.Col([
#                 dbc.CardGroup([
#                     dbc.Card([
#                         html.Legend("Devoluções"),
#                         html.H5("R$ 0,00", id="p-despesa-dashboards", style={}),
#                     ], style={"padding-left": "20px", "padding-top": "10px"}),
#                     dbc.Card(
#                         html.Div(className="fa fa-meh-o", style=card_icon),
#                         color="danger",
#                         style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
#                     )
#                 ])
#             ], width=4),
#         ], style={"margin": "10px"}),

#         dbc.Row([
#             dbc.Col(
#                 dbc.Card(
#                     dcc.Graph(
#                         id='graph1',
#                         figure=px.bar(df, x='Hora', y='Tot_Venda', title='Vendas do dia', labels={'Tot_Venda': 'Valor da venda'})
#                     )
#                 )
#             )
#         ]),

#         dbc.Row([
#             dbc.Col(
#                 [
#                     DataTable(
#                         id='data-table',
#                         data=vendas.to_dict('records'),
#                         columns=[{'name': col, 'id': col} for col in vendas.columns],
#                         page_size=400,
#                         style_table={'overflowX': 'auto', 'width': '100%', 'margin-left': 'px', 'z-index': '0'},
#                         style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
#                         style_cell={'textAlign': 'left', 'minWidth': '100px', 'font-family': 'Calibri'},
#                         style_data_conditional=[
#                             {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
#                             {'if': {'column_id': 'Tot_Venda'}, 'backgroundColor': '#006400', 'color': 'white'},
#                             {'if': {'column_id': 'MC_B%'}, 'backgroundColor': '#FF0000', 'color': 'white'},

#                         ],
#                     )
#                 ]
#             )
#         ]),
#     ])


# @app.callback(
#     Output('graph1', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = vendas[vendas.country == value]
#     return px.line(dff, x='Tot_Venda', y='Hora')

