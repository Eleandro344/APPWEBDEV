import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from app import app  # Importa o objeto app do arquivo app.py

# Dados de exemplo para autenticação de usuário
USERS = {'username': 'password'}


# Layout da tela de login
def layout():
    return dbc.Container([
        dbc.Row(dbc.Col(html.H1("Tela de Login"))),
        dbc.Row(dbc.Col(html.Div("Por favor, faça o login para acessar o aplicativo."))),
        dbc.Row([
            dbc.Col(html.Div("Usuário:")),
            dbc.Col(dcc.Input(id='username-input', type='text', placeholder='Digite seu usuário')),
        ]),
        dbc.Row([
            dbc.Col(html.Div("Senha:")),
            dbc.Col(dcc.Input(id='password-input', type='password', placeholder='Digite sua senha')),
        ]),
        dbc.Row([
            dbc.Col(html.Button('Login', id='login-button', n_clicks=0)),
            html.Div(id='login-status')
        ]),
    ])

# Callback para autenticar o usuário e redirecionar para a página '/home'
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('username-input', 'value'),
     State('password-input', 'value')]
)
def display_page(pathname, username, password):
    if pathname == '/home':
        if username in USERS and USERS[username] == password:
            return html.H1('Página Home')
        else:
            return html.H1('404 - Página não encontrada')
    else:
        return html.H1('Página de Login')

@app.callback(
    Output('login-status', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')]
)
def authenticate_user(n_clicks, username, password):
    if n_clicks > 0:
        if username in USERS and USERS[username] == password:
            return dcc.Location(href='/home', id='redirect')
        else:
            return html.Div('Usuário ou senha incorretos. Tente novamente.')


