from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
import dash_auth
import mysql.connector

app.title = 'Trimed Financ'

# Layout do aplicativo
def layout():
    return html.Div(style={'background-color': '#FFFFFF', 'height': '220vh', 'width': '100%'}, children=[
        html.Header(
            html.Img(src='/assets/logobranco.png', className="logo-img", style={'width': '15%',}),
            style={
                'background-color': '#008B8B',
                'padding': '15px',
                'text-align': 'center',
                'font-family': 'Arial, sans-serif',
                'text-shadow': '2px 2px 4px rgba(0, 0, 0, 0.3)',
                'letter-spacing': '2px',
            }
        ),
        html.Div("Bem-vindo,olaaa usuário", style={'position': 'absolute', 'top': '10px', 'right': '10px', 'font-size': '16px', 'color': 'black'}),
        html.Div([
            html.Iframe(
                src="https://lottie.host/embed/299f41f5-0bd5-46e6-9aec-06fb86fc4d6b/G0XK8lIPMb.json",
                style={'width': '550px', 'height': '450px', 'margin': 'auto', 'padding-top': '20px', 'display': 'block'}
            )#<iframe src="https://lottie.host/embed/299f41f5-0bd5-46e6-9aec-06fb86fc4d6b/G0XK8lIPMb.json"></iframe>
        ]),
        dbc.Button('Continuar para Menu Principal', id='/home', href='/home',
                   style={'border-width': '3px', 'font-size': '14px', 'background-color': '#008B8B',
                          'margin-left': '43%', 'margin-top': '15px', 'padding-top': '10px'}
                   ),
    ])

