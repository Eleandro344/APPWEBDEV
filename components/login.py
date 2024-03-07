from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
import dash_auth
import mysql.connector

app.title = 'Trimed Financ'

# Conexão Banco de Dados
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)
mycursor = mydb.cursor()
consultaSQL = 'SELECT usuario, senha FROM usuario'
mycursor.execute(consultaSQL)
myresult = mycursor.fetchall()
df_usuario = pd.DataFrame(myresult, columns=['usuario', 'Senha'])
usuariosBD = dict(myresult)

# Exemplo de usuários e senhas válidas
VALID_USERNAME_PASSWORD_PAIRS = usuariosBD

# Método de autenticação
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


def consultar_banco_de_dados():
    # Adicione sua lógica de consulta ao banco de dados aqui
    # Exemplo de consulta:
    consulta_sql = 'SELECT * FROM sua_tabela'
    mycursor.execute(consulta_sql)
    resultado_consulta = mycursor.fetchall()
    return resultado_consulta


# Layout do aplicativo

from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
import dash_auth
import mysql.connector

app.title = 'Trimed Financ'

# Conexão Banco de Dados
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)
mycursor = mydb.cursor()
consultaSQL = 'SELECT usuario, senha FROM usuario'
mycursor.execute(consultaSQL)
myresult = mycursor.fetchall()
df_usuario = pd.DataFrame(myresult, columns=['usuario', 'Senha'])
usuariosBD = dict(myresult)

# Exemplo de usuários e senhas válidas
VALID_USERNAME_PASSWORD_PAIRS = usuariosBD

# Método de autenticação
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)



# Layout do aplicativo
def layout():
    return  html.Div(style={'background-color': '#FFFFFF', 'height': '220vh', 'width': '100%'}, children=[
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
        html.Div([
            html.Iframe(
            src="https://lottie.host/embed/45af3a4c-75e6-42ba-b74b-c9a98e1639a3/r2rPa6bgO4.json",
            style={'width': '550px', 'height': '450px', 'margin': 'auto','padding-top': '20px', 'display': 'block'}
            )
        ]),
        dbc.Button('Continuar para Menu Principal', id='/home', href='/home',
                   style={'border-width': '3px', 'font-size': '14px', 'background-color': '#008B8B',
                          'margin-left': '43%', 'margin-top': '15px', 'padding-top': '10px'}
                   ),
        # Adicione um componente para exibir os dados do banco de dados
        html.Div(id='output_div'),
    ])

# Callback para atualizar os dados do layout ao carregar a página
@app.callback(
    Output('output_div', 'children'),
    [Input('login', 'n_clicks')]  # Pode ser um componente diferente que aciona a consulta
)
def carregar_dados_banco_de_dados(n_clicks):
    # Verifica se o callback foi acionado pelo botão 'login'
    if not ctx.triggered_id or ctx.triggered_id != 'login':
        raise PreventUpdate

    # Lógica de consulta ao banco de dados
    dados_do_banco = consultar_banco_de_dados()

    # Atualiza o layout com os novos dados
    return f"Dados do Banco de Dados: {dados_do_banco}"


