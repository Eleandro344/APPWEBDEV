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
    if username == "lucimara":
        username = username.capitalize()
    if  username == "eleandro":
        username = username.capitalize()
    if  username == "antonio":
        username = username.capitalize() 
    if  username ==  "taiane":
        username = username.capitalize()   
    if  username ==  "douglas":
        username = username.capitalize()  
    if  username ==  "caue":
        username = username.capitalize()                    
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
        html.I(className="fa fa-user", style={'font':'Arial','position': 'absolute', 'height': '220vh', 'top': '150px', 'right': '80px', 'font-size': '18px', 'color': '#222222', 'font-weight': 'bold'}),
        html.H1(f"Olá, {username}",className="text-user"),# style={'font-weight': 'bold','font-family': 'Bahnschrift','position': 'absolute', 'top': '150px', 'right': '110px', 'font-size': '16px', 'color': '#222222'}),
    html.Div([
        html.Iframe(
            src="https://lottie.host/embed/ed87547d-213b-4beb-81b1-084c75e27473/Hj9y7DHwau.json",
            style={'width': '500px', 'height': '400px', 'margin': 'auto', 'padding-top': '20px', 'display': 'block','margin-rigth': '50px'}),
        html.Iframe(
            src="https://lottie.host/embed/4f864203-b546-48b6-97e6-e98a8b74d293/RytEztFHFm.json",
            style={'width': '500px', 'height': '400px', 'margin': 'auto', 'padding-top': '20px', 'display': 'block','margin-left': '-70px', 'transform': 'scaleX(-1)'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    dbc.Button('Continuar para Menu Principal', id='/home', href='/home', class_name="text-button")
])



