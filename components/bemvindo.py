from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
import dash_auth
import mysql.connector
from components.shared_variables import username

app.title = 'Trimed Financ'
favicon = 'money_upico.ico'

app.server.favicon = favicon

def layout(username):
    if username in ["lucimara", "eleandro", "antonio", "taiane", "douglas", "caue"]:
        username = username.capitalize()

    return html.Div(className='pagina-initial', children=[
        html.Header(
            children=[
                html.Img(src='/assets/logobranco.png', className="logo-img"),
                html.Div(className="header-title", children="Trimed Financ"),
            ],
            className="main-header"
        ),
        html.I(className="fa fa-user", style={'position': 'absolute', 'top': '150px', 'right': '80px', 'font-size': '18px', 'color': '#222222', 'font-weight': 'bold'}),
        html.H1(f"Olá, {username}", className="text-user"),
        html.H1(f"Grafeno disponivel!", className="text-mensage"),

        html.Div([
            html.Iframe(className='animation3',
                         src="https://lottie.host/embed/4a38ddaf-5b65-4a65-b537-a7be7ce54a49/x7ymJTtuXu.json"),
        # html.Div([<iframe src="https://lottie.host/embed/45af3a4c-75e6-42ba-b74b-c9a98e1639a3/r2rPa6bgO4.json"></iframe>
        #     html.Ifr<iframe src="https://lottie.host/embed/45af3a4c-75e6-42ba-b74b-c9a98e1639a3/r2rPa6bgO4.jsoname(className='animation1',
        #                 src="https://lottie.host/embed/ed87547d-213b-4beb-81b1-084c75e27473/Hj9y7DHwau.json"),
        #     html.Iframe(className='animation2',
        #                 src="https://lottie.host/embed/4f864203-b546-48b6-97e6-e98a8b74d293/RytEztFHFm.json")
         ], className='animation-container'),
        html.Div([
            dbc.Button('Continuar para Menu Principal', id='/home', href='/home', className="text-button"),
        ]),
        html.Footer(
            children=[
                html.Span("© 2024 Trimed Financ. Todos os direitos reservados.", className="footer-left"),
                html.Span("Desenvolvido por Eleandro S. Martins", className="footer-right")
            ],
            className="text-footer"
        ),
      ])
# Example of a basic callback
