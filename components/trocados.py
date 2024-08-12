from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app

import pandas as pd
from dash import html, dcc, Input, Output, ctx
# Função para carregar os dados da tabela de remessa
def carregar_dados_remessa():
        dados=pd.read_excel(r"C:\Users\elean\Desktop\bancodedados\situacaodocs.xlsx")
        dados = dados.loc[dados['CodDoc'] != 0]

        itau = dados.loc[dados['Forma_Pg']=='Boletos Itaú']
        itautrocados =itau.loc[itau['Sit2'] == 'T']
        itautrocados =itautrocados['(Pend+Desp)'].sum()
        itautrocados = itautrocados.round(2)

        Ntrocadoitau = itau[itau["Sit2"].isna()]
        Ntrocadoitau = Ntrocadoitau['(Pend+Desp)'].sum()
        Ntrocadoitau = Ntrocadoitau.round(2)
        santander = dados.loc[dados['Forma_Pg']=="Boletos Santander"]
        santandertrocados = santander.loc[santander['Sit2'] == 'T']
        santandertrocados = santandertrocados['(Pend+Desp)'].sum()
        santandertrocados = santandertrocados.round(2)
        Ntrocado_sant = santander[santander["Sit2"].isna()]
        Ntrocado_sant = Ntrocado_sant['(Pend+Desp)'].sum()
        Ntrocado_sant = Ntrocado_sant.round(2)
        unicred = dados.loc[dados['Forma_Pg']=="Boletos Unicred"]
        unicredtrocados = unicred.loc[unicred['Sit2'] == 'T']
        unicredtrocados=unicredtrocados['(Pend+Desp)'].sum()
        unicredtrocados=unicredtrocados.round(2)
        Ntrocadounicred = unicred[unicred["Sit2"].isna()]
        Ntrocadounicred =Ntrocadounicred['(Pend+Desp)'].sum()
        Ntrocadounicred = Ntrocadounicred.round(2)
        stratton = dados.loc[dados['Forma_Pg']=="Boletos Stratton Fidc Bradesco"]
        Strattontrocados = stratton.loc[stratton['Sit2'] == 'T']
        stratton=stratton['(Pend+Desp)'].sum()
        stratton = stratton.round(2)
        # Ntrocadostratton = stratton[stratton["Sit2"].isna()]
        # Ntrocadostratton=Ntrocadostratton['(Pend+Desp)'].sum()

        sicoob = dados.loc[dados['Forma_Pg']=="Boletos Sicoob"]
        sicoobtrocados = sicoob.loc[sicoob['Sit2'] == 'T']
        sicoobtrocados = sicoobtrocados['(Pend+Desp)'].sum()
        sicoobtrocados=sicoobtrocados.round(2)
        Ntrocadossicoob = sicoob[sicoob["Sit2"].isna()]
        Ntrocadossicoob= Ntrocadossicoob['(Pend+Desp)'].sum()
        Ntrocadossicoob = Ntrocadossicoob.round(2)
        sofisa = dados.loc[dados['Forma_Pg']=="Boletos Sofisa"]
        sofisatrocados = sofisa.loc[sofisa['Sit2'] == 'T']
        sofisatrocados =sofisatrocados['(Pend+Desp)'].sum()
        sofisatrocados = sofisatrocados.round(2)
        Ntrocadossofisa = sofisa[sofisa["Sit2"].isna()]
        Ntrocadossofisa=Ntrocadossofisa['(Pend+Desp)'].sum()
        Ntrocadossofisa= Ntrocadossofisa.round(2)
        safra = dados.loc[dados['Forma_Pg']=="Boletos Safra"]
        safratrocados = safra.loc[safra['Sit2'] == 'T']
        safratrocados =safratrocados['(Pend+Desp)'].sum()
        safratrocados = safratrocados.round(2)
        Ntrocadossafra = safra[safra["Sit2"].isna()]
        Ntrocadossafra=Ntrocadossafra['(Pend+Desp)'].sum()
        Ntrocadossafra=Ntrocadossafra.round(2)
        # print(Ntrocadossafra)
        import locale

        # Configurar a localidade para português do Brasil
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        santandertrocados = locale.currency(santandertrocados, grouping=True)
        # Configurar a localidade para português do Brasil
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocado_sant = locale.currency(Ntrocado_sant, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        itautrocados = locale.currency(itautrocados, grouping=True)


        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocadoitau = locale.currency(Ntrocadoitau, grouping=True)


        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        unicredtrocados = locale.currency(unicredtrocados, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocadounicred = locale.currency(Ntrocadounicred, grouping=True)


        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        stratton = locale.currency(stratton, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        sicoobtrocados = locale.currency(sicoobtrocados, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocadossicoob = locale.currency(Ntrocadossicoob, grouping=True)



        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        sofisatrocados = locale.currency(sofisatrocados, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocadossofisa = locale.currency(Ntrocadossofisa, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        safratrocados = locale.currency(safratrocados, grouping=True)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        Ntrocadossafra = locale.currency(Ntrocadossafra, grouping=True)
        return Ntrocadossafra,safratrocados,unicredtrocados,Ntrocadossofisa,sofisatrocados,santandertrocados,Ntrocadossicoob,sicoobtrocados,stratton,Ntrocadounicred,Ntrocado_sant,Ntrocadoitau,itautrocados,





def layout():
    Ntrocadossafra,safratrocados,Ntrocadossofisa,unicredtrocados,sofisatrocados,santandertrocados,Ntrocadossicoob,sicoobtrocados,stratton,Ntrocadounicred,Ntrocado_sant,Ntrocadoitau,itautrocados = carregar_dados_remessa()

    

    return html.Div([
    html.H1("Situação Bancos com vencimento a partir da data de hoje (Incluido Garantia de OP)",className="text-titulo", style={'margin-top': '30px','margin-left':'20px'}),#'margin-top': '10px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
    html.Img(src='/assets/santanderimagem.png', className="logo-imgz"),#, style={'width': '10%', 'marginLeft': '500px','marginTop': '0px'}),
    html.H3(f'Trocados Santander R$ {santandertrocados}', className='class_css2'),
    html.H3(f'Não trocados santander R$ {Ntrocado_sant}', className='class_css1'),
    html.Img(src='/assets/logoitau.png', className="logo-imgz", style={'width': '3%'}),
    html.H3(f'Trocados Itau R$ {itautrocados}', className='class_css2'),
    html.H3(f'Não trocados Itau R$ {Ntrocadoitau}', className='class_css1'),
    html.Img(src='/assets/unicredimagem.png', className="logo-imgz", style={'width': '8%'}),
    html.H3(f'Trocados Unicred R$ {unicredtrocados}', className='class_css2'),
    html.H3(f'Não Trocados unicred R$ {Ntrocadounicred}', className='class_css1'),
    html.Img(src='/assets/stratton.png', className="logo-imgz", style={'width': '8%'}),
    html.H3(f'Trocados Stratton R$ {stratton}', className='class_css2'),
    html.Img(src='/assets/sicoob.png', className="logo-imgz", style={'width': '4%'}),
    html.H3(f'Trocados Sicoob R$ {sicoobtrocados}', className='class_css2'),
    html.H3(f'Não Trocados Sicoob R$ {Ntrocadossicoob}', className='class_css1'),
    html.Img(src='/assets/Sofisaimagem.png', className="logo-imgz", style={'width': '8%'}),
    html.H3(f'Trocados Sofisa R$ {sofisatrocados}', className='class_css2'),
    html.H3(f'Não Trocados Sofisa R$ {Ntrocadossofisa}', className='class_css1'),   
    html.Img(src='/assets/bancosafra.png', className="logo-imgz", style={'width': '8%'}),
    html.H3(f'Trocados Safra R$ {safratrocados}', className='class_css2'),
    html.H3(f'Não Trocados Safra R$ {Ntrocadossafra}', className='class_css1'),

    
])



        # html.Img(src='/assets/unicredimagem.png', className="logo-imgz", style={'width': '8%'}),
        # html.H3((mensagem_unicred), className=class_css2),
        # html.Img(src='/assets/bancosafra.png', className="logo-imgz", style={'width': '8%'}),
        # html.H3((mensagem_safradescontada), className=class_css3),
        # html.H3((mensagem_safrasimples), className=class_css4),
        # html.Img(src='/assets/Sofisaimagem.png', className="logo-imgz", style={'width': '8%'}),
        # html.H3((mensagemsofisa), className=class_css5),


