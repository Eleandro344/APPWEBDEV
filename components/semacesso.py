from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app


app.title = 'Trimed Financ'

# Layout do aplicativo
def layout():
    return html.Div([
        html.H4('Usuário sem acesso',className="text-semacesso"),
        html.Iframe(         
            src="https://lottie.host/embed/547da133-a45b-4ca3-b3a4-161e388df0c1/6afa9OZpOR.json",
            style={'width': '550px', 'height': '450px', 'margin': 'auto','padding-top': '20px', 'display': 'block'}
    )])


