import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
from components import avisos, home, faturamento, banco,rastrear,ajusteboletos,santander,login,devolucao,sofisa,safra
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from app import app  # Importa o objeto app do arquivo app.py

import globals
from dash import dcc



df = pd.read_excel('C:/Users/elean/Desktop/bancodedados/docs.xlsx')


sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src='/assets/logobranco.png', className="logo-img", style={'width': '100%'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        html.P("Bem-Vindo, colega Trimed!", className="welcome-text"),
        
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2 fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span(" HOME", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/home",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span(" Banco Unicred", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/rastrear",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span(" Banco Santander", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/santander",
                    active="exact",
                    className="nav-link-beat"
                ),  
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span(" Banco Sofisa", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/sofisa",
                    active="exact",
                    className="nav-link-beat"
                ),   
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span("Banco Safra", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/safra",
                    active="exact",
                    className="nav-link-beat"
                ),                             
                dbc.NavLink(    
                    [
                        html.I(className="fa-solid fa-sack-dollar fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span(" Faturamento", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/faturamento",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-building-columns fa-lg", style={'verticalAlign': 'middle'}),
                        html.Span("Banco", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/banco",
                    active="exact",
                    className="nav-link-beat"
                ),
                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-truck-fast fa-lg", style={'verticalAlign': 'middle'}),
                    html.Span(" Cadastrar devoluções", style={'verticalAlign': 'middle', 'marginLeft': '0px'}),
                    ],
                    href="/devolucao",
                    active="exact",
                    className="nav-link-beat"
                ),
                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-file-circle-exclamation fa-lg", style={'verticalAlign': 'middle'}),
                    html.Span("Titulos com Problema", style={'verticalAlign': 'middle', 'marginLeft': '0px'}),
                    ],
                    href="/ajusteboletos",
                    active="exact",
                    className="nav-link-beat"
                ),
                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-file-circle-exclamation fa-lg", style={'verticalAlign': 'middle'}),
                    html.Span("login", style={'verticalAlign': 'middle', 'marginLeft': '0px'}),
                    ],
                    href="/login",
                    active="exact",
                    className="nav-link-beat"
                ),  
                dbc.NavLink(
                    [
                        #html.I(className="fa-solid fa-barcode fa-lg", style={'verticalAlign': 'middle'}),
                        #html.Span("Banco Safra", style={'verticalAlign': 'middle', 'marginLeft': '30px'}),
                    ],
                    href="/avisos",
                    active="exact",
                    className="nav-link-beat"
                ),                                                                     
                html.Div(id='open-new-tab'),              
            ],
            vertical=True,
            pills=True,
        ),
        
    ],
    className="sidebar",
)

home_layout = home.layout()
faturamento_layout = faturamento.layout()
banco_layout = banco.layout()
login_layout = login.layout()
devolucao_layout = devolucao.layout()
santander_layout = santander.layout()
ajusteboletoslayout = ajusteboletos.layout()
sofisa_layout = sofisa.layout()
safra_layout = safra.layout()
avisos_layout = avisos.layout()

app.layout = html.Div([
    sidebar,
    html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ], className="content"),
])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == '/' or pathname == "/login":
        return avisos.layout()   
    if pathname == "/faturamento":
        return faturamento.layout()
    if pathname == "/home":
        return home.layout()
    if pathname == "/devolucao":
        return devolucao.layout()    
    if pathname == "/banco":
        return banco.layout()       
    if pathname == "/santander":
        return santander.layout()    
    if pathname == "/safra":
        return safra.layout()    
    if pathname == "/sofisa":
        return sofisa.layout()      
    if pathname == "/rastrear":
        return rastrear.layout()
    if pathname == "/safra":
        return avisos.layout()
    if pathname == "/ajusteboletos":
        return ajusteboletos.layout()
    
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True, host='10.1.1.23', port=8050, dev_tools_hot_reload=True)
   # app.run_server(debug=False, use_reloader=True, host='0.0.0.0', port=8040, dev_tools_hot_reload=True)
