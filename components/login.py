from dash import Dash, html, dcc, Input, Output, dash, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
from dash import callback_context
import dash_auth
import mysql.connector



app.title= 'Trimed Financ'

### Conexão Banco de Dados
# Cria um dataframe contendo todos os usuários e senhas para ser iterada
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',
    database='db_sabertrimed',
)
mycursor = mydb.cursor()
consultaSQL = 'SELECT usuario, senha  FROM usuario'
mycursor.execute(consultaSQL)
myresult = mycursor.fetchall()
# Transforma o resultado da Query no BD em um dataframe
df_usuario = pd.DataFrame(myresult, columns = ['usuario', 'Senha'])
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
        html.Header(
            html.Img(src='/assets/logobranco.png', className="logo-img", style={'width': '15%'}),
            style={
                'background-color': '#008B8B',  # Cor de fundo azul
                'padding': '15px',  # Espaçamento interno
                'text-align': 'center',  # Alinhamento centralizado
                'font-family': 'Arial, sans-serif',
                'text-shadow': '2px 2px 4px rgba(0, 0, 0, 0.3)',  # Sombra de texto suave
                'letter-spacing': '2px',  # Espaçamento entre letras
            }
        ),
        html.Div([
            html.Iframe(
                src="https://lottie.host/embed/580b3172-98d5-4868-ba24-09d525f483fd/ZzflFlsYZU.json",
                style={'width': '550px', 'height': '550px', 'margin': 'auto', 'display': 'block'}
            )
        ]),
        html.Div(dbc.Button('Continuar para Menu Principal', id='login', href='/home',
                            style={'border-width': '3px', 'font-size': '14px','background-color': '#008B8B', 'margin-left': '43%', 'margin-top': '15px', 'padding-top': '10px'})
        ),
    ])
