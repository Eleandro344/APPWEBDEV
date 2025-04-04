import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
from components import agendamentos, avisos, home, faturamento,grafeno,avarias,banco,rastrear,ajusteboletos,santander,login,devolucao,sofisa,safra,semacesso,bemvindo,cemapaga,itau,sicoob,trocados
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from app import app  # Importa o objeto app do arquivo app.py
import dash_auth
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_auth
import globals
from dash import dcc
from flask import request   
from components.shared_variables import username
from dash import html, dcc, Input, Output, ctx, callback_context
from dash.exceptions import PreventUpdate
from flask import request
from components.shared_variables import username


# df = pd.read_excel('C:/Users/elean/Desktop/bancodedados/docs.xlsx')


sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src='/assets/logobranco.png', className="logo-img", style={'width': '100%'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        html.P("Bem-Vindo, colega!", className="welcome-text"),
        
        dbc.Nav(
            [
            dbc.NavLink(
                [
                html.I(className="fas fa-home me-2 fa-lg", style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                html.Span("Home", className="sidebar-info"),
                ],
                href="/home",
                active="exact",
                className="nav-link-beat"
            ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-map-location-dot fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span("Agendamentos",className="sidebar-info"),
                    ],
                    href="/agendamentos",
                    active="exact",
                    className="nav-link-beat"#<i class="fa-solid fa-map-location-dot"></i>
                ),    
                # dbc.NavLink(
                #     [
                #         html.I(className="fa-solid fa-map-location-dot fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                #         html.Span("Avarias",className="sidebar-info"),
                #     ],
                #     href="/avarias",
                #     active="exact",
                #     className="nav-link-beat"#<i class="fa-solid fa-map-location-dot"></i>
                # ),                    
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Itau",className="sidebar-info"),
                    ],
                    href="/itau",
                    active="exact",
                    className="nav-link-beat"
                ),       
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Grafeno",className="sidebar-info"),
                    ],
                    href="/grafeno",
                    active="exact",
                    className="nav-link-beat"
                ),                               
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Unicred",className="sidebar-info"),
                    ],
                    href="/rastrear",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Santander",className="sidebar-info"),                    ],
                    href="/santander",
                    active="exact",
                    className="nav-link-beat"
                ),  
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Sofisa",className="sidebar-info"),                    ],
                    href="/sofisa",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Sicoob",className="sidebar-info"),                    ],
                    href="/sicoob",
                    active="exact",
                    className="nav-link-beat"
                ),                      
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span(" Banco Safra",className="sidebar-info"),                    ],
                    href="/safra",
                    active="exact",
                    className="nav-link-beat"
                ),   
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-barcode fa-lg", style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span("Stratton ",className="sidebar-info"),                    ],
                    href="/banco",
                    active="exact",
                    className="nav-link-beat"
                ),                                          
                dbc.NavLink(    
                    [
                        html.I(className="fa-solid fa-sack-dollar fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span("Faturamento",className="sidebar-info"),                    ],
                    href="/faturamento",
                    active="exact",
                    className="nav-link-beat"
                ),
                dbc.NavLink(    
                    [
                        html.I(className="fa-solid fa-comments-dollar fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                        html.Span("Cema Paga",className="sidebar-info"),                    ],
                    href="/cemapaga",
                    active="exact",
                    className="nav-link-beat"
                ),            

                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-truck-fast fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                    html.Span("Devoluções",className="sidebar-info"),                    ],
                    href="/devolucao",
                    active="exact",
                    className="nav-link-beat"
                ),
                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-file-circle-exclamation fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                    html.Span("Situação Bancos",className="sidebar-info"),                    ],
                    href="/trocados",
                    active="exact",
                    className="nav-link-beat"
                ),
                    dbc.NavLink(
                    [
                    html.I(className="fa-solid fa-user fa-lg",  style={"color": "#FFFFFF", 'verticalAlign': 'middle'}),
                    html.Span("Login",className="sidebar-info"),                    ],
                    href="/login",
                    active="exact",
                    className="nav-link-beat",
                ),                                                                      
                html.Div(id='open-new-tab'),              
            ],
            vertical=True,
            pills=True,
        ),
        
    ],
    className="sidebar",
)
# avarias_lauout = avarias.layout()

cemapaga_layout = cemapaga.layout()
garfeno_layout = grafeno.layout()
# home_layout = home.layout()
semacesso_layout = semacesso.layout()
faturamento_layout = faturamento.layout()
banco_layout = banco.layout()
login_layout = login.layout()
devolucao_layout = devolucao.layout()
santander_layout = santander.layout()
# trocados_layout = trocados.layout()
sofisa_layout = sofisa.layout()
agendamentos_layout= agendamentos.layout()
safra_layout = safra.layout()
avisos_layout = avisos.layout()
itau_layout = itau.layout()
sicoob_layout = sicoob.layout()

bemvindo_layout = bemvindo.layout(username=username) 

app.layout = html.Div([ 
    sidebar,
    html.Div([
        dcc.Location(id="url", refresh=True),
        html.Div(id="page-content"),
    ], className="content"),
    
    # Adicione o código JavaScript aqui
    html.Script('''
        document.addEventListener('keydown', function(event) {
            if (event.key === "F5") {
                location.reload(true);
            }
        });
    ''')
])





# Dados de autenticação
VALID_USERNAME_PASSWORD_PAIRS = {
    'eleandro': '2323',
    'antonio':'2024',
    'lucimara':'2024',
    'taiane':'2024',
    'douglas':'2024',
    'caue':'2024',
    'andre':'2023'



}

# Definindo permissões
PERMISSIONS = {
    'eleandro': 0,
    'antonio': 0,
    'lucimara': 0,
    'taiane': 2, 
    'douglas':1,
    'caue':2,   
    'andre':6,    
}
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# Função para verificar as permissões e redirecionar conforme necessário
def check_permission(username, pathname):
    if username in PERMISSIONS:
        user_permission = PERMISSIONS[username]
        if user_permission == 9 and (pathname == "/faturamento" or pathname == "/banco"):       
            return "/semacesso"  # Redireciona usuários com permissão 1 da página de faturamento para a página inicial
        if user_permission ==9 and (pathname == "/devolucao" or pathname == "/banco"):
            return "/semacesso"  # Redireciona usuários com permissão 1 da página de faturamento para a página inicial
        if user_permission ==6 and (pathname == "/faturamento" or pathname == "/banco" or pathname == "/sicoob"
        or pathname == "/banco"   
        or pathname == "/santander"
        or pathname == "/safra"
        or pathname == "/itau"
        or pathname == "/grafeno"
        or pathname == "/rastrear"
        or pathname == "/trocados"
        or pathname == "/cemapaga"
        or pathname == "/sicoob"):
            return "/semacesso"  # Redireciona usuários com permissão 1 da página de faturamento para a página inicial        
        
    return pathname

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])


def display_page(pathname):
    auth = request.authorization
    if auth:
        username = auth.username
    else:
        return dcc.Location(id="url", pathname="/", refresh=True)
    if username:
        print("Usuário logado:", username)  # Imprime o nome de usuário que foi logado
        pathname = check_permission(username, pathname)
        if pathname == '/' or pathname == "/login":
            return dcc.Location(id="url", pathname="/bemvindo", refresh=True)  # Redireciona usuários já autenticados para a página inicial
        elif pathname == "/faturamento":
            return faturamento.layout()
        elif pathname == "/login":
            return login.layout()
        elif pathname == "/bemvindo":
            return bemvindo.layout(username=username)      
        elif pathname == "/home":
            return home.layout()
        elif pathname == "/devolucao":
            return devolucao.layout()
        elif pathname == "/sicoob":
            return sicoob.layout()      
        elif pathname == "/grafeno":    
            return grafeno.layout()           
        elif pathname == "/avarias":
                return avarias.layout()              
        elif pathname == "/banco":
            return banco.layout()
        elif pathname == "/santander":
            return santander.layout()
        elif pathname == "/semacesso":
            return semacesso.layout()
        elif pathname == "/safra":
            return safra.layout()
        elif pathname == "/sofisa":
            return sofisa.layout()
        elif pathname == "/itau":
            return itau.layout()        
        elif pathname == "/agendamentos":
            return agendamentos.layout()        
        elif pathname == "/rastrear":
            return rastrear.layout()
        elif pathname == "/avisos":
            return avisos.layout()
        elif pathname == "/trocados":
            return trocados.layout()
        elif pathname == "/cemapaga":
            return  cemapaga.layout()
    else:
        return dcc.Location(id="url", pathname="/login", refresh=True)
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050, dev_tools_hot_reload=False)
