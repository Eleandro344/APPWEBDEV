from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate



# Layout do aplicativo
def layout():
    return  html.Div(style={'background-color': '#FFFFFF', 'height': '220vh', 'width': '100%'}, children=[
        html.Header(
        ),
        html.Div([
            html.H1(children='Safra habilitado, Aproveite!!', style={'textAlign':'center'}),
            html.Iframe(
            src="https://lottie.host/embed/a328be23-d331-49db-be88-82960c3dd7e6/gmUePOLO8U.json",
            style={'width': '550px', 'height': '450px', 'margin': 'auto','padding-top': '20px', 'display': 'block'}
            )
        ]),#<iframe src="https://lottie.host/embed/a328be23-d331-49db-be88-82960c3dd7e6/gmUePOLO8U.json"></iframe>#<iframe src="https://lottie.host/embed/33b4316d-45e1-462c-ab40-02457e206854/6uJldcuFus.json"></iframe>
    ])#<iframe src="https://lottie.host/embed/00551b35-071e-47c7-ab41-ff68d814802f/8AbOMQuSMc.json"></iframe>