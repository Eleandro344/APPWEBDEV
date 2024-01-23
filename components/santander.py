# App layout
from dash import Dash

import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from app import app  # Importa o objeto app do arquivo app.py



def layout():
    return html.Div([
        html.Iframe(
            src="https://lottie.host/embed/580b3172-98d5-4868-ba24-09d525f483fd/ZzflFlsYZU.json",
            style={'width': '500px', 'height': '500px', 'margin': 'auto', 'display': 'block'}
        )
    ])
