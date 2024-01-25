# App layout
from dash import Dash

import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from app import app  # Importa o objeto app do arquivo app.py



def layout():
    return html.Div([
        html.H1(children='AQUI VAI SER O BANCO SANTANDER', style={'textAlign':'center'}),

    ])

