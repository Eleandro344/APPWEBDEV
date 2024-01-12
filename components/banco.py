# App layout
from dash import Dash

import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from app import app  # Importa o objeto app do arquivo app.py

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')


def layout():
    return html.Div([
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
        dcc.Dropdown(
            id='dropdown-selection',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value='Canada'
        ),
        dcc.Graph(id='graph-content')
    ])

@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df['country'] == value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.layout = layout()  # Chama a função layout para configurar o layout do aplicativo
    app.run_server(debug=True)
