import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Seu DataFrame
df = pd.DataFrame({
    'cod': [436288, 436289, 436290, 436291, 436292, 436293, 436294, 436295, 436296],
    'hora': ['10:39:48 AM', '10:50:10 AM', '10:50:29 AM', '10:50:47 AM', '10:53:24 AM', '11:11:21 AM', '11:13:14 AM', '11:34:20 AM', '11:36:12 AM'],
    'tot_venda': ['16,76', '323,34', '875,43', '2161,01', '169,9', '14,83', '4428,4', '369,77', '535,66'],
    'cliente': ['Bruno Hoppe Porto - Trimed', 'Solar Medic Ltda', 'Aline Venturini Dias Me', 'Sildomar S de Oliveira', 'Cema Prod Para Saude Eireli', 'Joao Pedro Mirapalheta - Trimed', 'Tm Farmacia Eireli', 'American Pharma Com Prod Farmaceuticos Eireli', 'Farmácia Caravágio Ltda'],
    'mc_b_': ['36,75', '42,16', '24', '38,95', '61,74', '41,67', '37,2', '28,66', '33,15'],
    'orig': ['1', '3', '3', '3', '1', '1', '5', '3', '5'],
    'flex_gc': ['', '', '', '', '2,67', '', '', '', ''],
    'gerou_flex': ['N', 'S', 'S', 'S', 'S', 'N', 'N', 'N', 'N']
})

# Convertendo a coluna tot_venda para tipo numérico
df['tot_venda'] = df['tot_venda'].str.replace(',', '').astype(float)

# Ordenando as horas corretamente
df['hora'] = pd.to_datetime(df['hora']).dt.strftime('%H:%M:%S')

# Inicialização do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(
                    id='bar-chart',
                    figure=px.bar(df, x='hora', y='tot_venda', title='Total de Vendas por Hora', labels={'tot_venda': 'Total de Vendas'})
                )
            )
        )
    ])
])

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
