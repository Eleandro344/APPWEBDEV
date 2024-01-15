from dash import Dash, html, dcc, Input, Output, dash, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app





# import do dash_ autentication
import dash_auth

# lib conexão MySQL
import mysql.connector

### Import das Variaveis Controle ###
import variaveisControle

### Variáveis de conexão com o banco de dados ###
host = variaveisControle.host
user = variaveisControle.user
password = variaveisControle.password
database = variaveisControle.database


### Conexão Banco de Dados
# Cria um dataframe contendo todos os usuários e senhas para ser iterada
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
# Transforma o resultado da Query no BD em um dataframe
df_usuario = pd.DataFrame(myresult, columns = ['Usuario', 'Senha'])
# Trasforma o resultado da Query no BD em um Dict
usuariosBD = dict(myresult)





# Exemplo de usuários e senhas válidas - manter isto em um arquivo a parte ou em um banco de dados para evitar problemas.
VALID_USERNAME_PASSWORD_PAIRS = usuariosBD


# Método de autenticação
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS  
)




def layout():
    return html.Div([
    html.H1('Bem vindo ao Sistema Financeiro', style={'border-width':'3px',
                                                            'margin-left':'35%',
                                                            'margin-top': '5px',
                                                            'padding-top':'10px'}),
    html.H3('Login realizado com sucesso!', style={'border-width':'3px',
                                                            'margin-left':'35%',
                                                            'margin-top': '5px',
                                                            'padding-top':'10px'}),
    html.Div(children = html.Img(src='/assets/logo.png', 
            style={'background-color': 'transparent', 
                        'border-color':'transparent', 
                        'height':'25%', 
                        'width':'25%', 
                        'margin-left':'41.8%',
                        'margin-top':'100px',})
    ),
    html.Div(
        dbc.Button('Continuar para Menu Principal', id='login', href='/home', style={'border-width':'3px',
                                                                                        'font-size':'14px', 
                                                                                        'margin-left':'45%',
                                                                                        'margin-top': '5px',
                                                                                        'padding-top':'10px'})),
])