import pandas as pd
from app import app  
from components.bancodedados import retornosantander_bd
from components.bancodedados import retornounicred_bd   
from components.bancodedados import retornosfra_bd
from components.bancodedados import retornosofisa_bd
import re







from dash import html, dcc, Input, Output, ctx



df_remessa1 =retornosantander_bd
df_remessa1[['Número Sequência do arquivo trailer','Data da ocorrência']]

df_remessa1.rename(columns={'Data da Gravação do Arquivo': 'Data da ocorrência', 'Número sequencial de registro no arquivo trailer': 'Número Sequência do arquivo trailer'}, inplace=True)

# Agrupe os dados por 'Data da ocorrência' e 'Número Sequência do arquivo trailer' e conte o número de ocorrências em cada grupo
agrupados = df_remessa1.groupby(['Data da ocorrência', 'Número Sequência do arquivo trailer']).size().reset_index(name='counts')

agrupados = agrupados.sort_values(by=[ 'Número Sequência do arquivo trailer'])
agrupados= agrupados.reset_index()
ultima_sequencia = agrupados['Número Sequência do arquivo trailer'].max()
penultima_linhasantader = agrupados['Número Sequência do arquivo trailer'].iloc[-2]
#o proximo arquivo vai ser !
tem_que_sersantander = penultima_linhasantader + 1



if ultima_sequencia == tem_que_sersantander:
    mensagem_santander = f'Último arquivo processado: {penultima_linhasantader}, e o atual {tem_que_sersantander}. Retorno Santander Ok! '
    class_css1 = 'mensagemok' 
else:
    mensagem_santander = "Arquivo sanatander com erro, verifique!"
    class_css1 = 'mensagemerro' 







# UNICRED

df_remessa1 = retornounicred_bd
df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'])

df_remessa1 = df_remessa1[df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'].dt.year == 2024]

df_remessa1[['SEQUENCIAL DO RETORNO','DATA DA GERAÇÃO DO ARQUIVO']]
df_remessa1.rename(columns={'DATA DA GERAÇÃO DO ARQUIVO': 'Data da ocorrência', 'SEQUENCIAL DO RETORNO': 'Número Sequência do arquivo trailer'}, inplace=True)

# Agrupe os dados por 'Data da ocorrência' e 'Número Sequência do arquivo trailer' e conte o número de ocorrências em cada grupo
agrupados = df_remessa1.groupby(['Data da ocorrência', 'Número Sequência do arquivo trailer']).size().reset_index(name='counts')
agrupados['Número Sequência do arquivo trailer'] = agrupados['Número Sequência do arquivo trailer'].astype(int) 
agrupados = agrupados.sort_values(by=['Número Sequência do arquivo trailer'])
agrupados= agrupados[:-8]

ultima_sequenciaunicred = agrupados['Número Sequência do arquivo trailer'].max()
#arquivo anterior
penultima_linhasunidred = agrupados['Número Sequência do arquivo trailer'].iloc[-2]

#o proximo arquivo vai ser !
tem_que_serunicred = penultima_linhasunidred + 1


if ultima_sequenciaunicred == tem_que_serunicred:
    mensagem_unicred = f'Último arquivo processado: {penultima_linhasunidred}, e o atual {tem_que_serunicred}. Retorno Unicred Ok! '
    class_css2 = 'mensagemok' 
else:
    mensagem_unicred = "Arquivo Santander com erro, verifique!"
    class_css2 = 'mensagemerro' 



#SAFRA 

df_remessa1 = retornosfra_bd

df_remessa1['Número Seqüencial Geração Arq. Retorno'] = df_remessa1['Número Seqüencial Geração Arq. Retorno'].astype(int)
df_remessa1[['Número Seqüencial Geração Arq. Retorno','Data Da Ocorrência No Banco','Nome do arquivo','Identificação Do Tipo De Carteira']]
agrupados = df_remessa1.groupby(['Data Da Ocorrência No Banco','Identificação Do Tipo De Carteira','Número Seqüencial Geração Arq. Retorno','Nome do arquivo']).size().reset_index(name='counts')
agrupados = agrupados.sort_values(by=[ 'Data Da Ocorrência No Banco'])
cobranca_simples = agrupados.loc[agrupados['Identificação Do Tipo De Carteira'] == 'cobrança simples']

cobranca_simples = agrupados.loc[agrupados['Identificação Do Tipo De Carteira'] == 'cobrança simples']



cobranca_descontada = agrupados.loc[agrupados['Identificação Do Tipo De Carteira'] == 'Cobrança descontada']


ul_safra_descontada = cobranca_descontada['Número Seqüencial Geração Arq. Retorno'].max()
penu_safra__descontada = cobranca_descontada['Número Seqüencial Geração Arq. Retorno'].iloc[-2]
#o proximo arquivo vai ser 
tem_que_ser_descontadasafra = penu_safra__descontada + 1



ul_safra_simples = cobranca_simples['Número Seqüencial Geração Arq. Retorno'].max()
penu_safra__simples= cobranca_simples['Número Seqüencial Geração Arq. Retorno'].iloc[-2]
#o proximo arquivo vai ser !
tem_que_ser_simplessafra = penu_safra__simples + 1


#MENSAGEM SIMPLES
# if ul_safra_simples == tem_que_ser_simplessafra:
#     mensagem_safrasimples = f'Último arquivo processado: {penu_safra__simples}, e o atual {tem_que_ser_simplessafra}. Retorno Safra cart.Simpes Ok! '
#     class_css = 'mensagemok' 

# else:
#     mensagem_safrasimples = "Arquivo safra Cart.Simples com erro, verifique!"
#     class_css = 'mensagemerro' 


if ul_safra_simples == tem_que_ser_simplessafra:
    mensagem_safrasimples = f'Último arquivo processado: {penu_safra__simples}, e o atual {tem_que_ser_simplessafra}. Retorno Safra Cart.Simples Ok!'
    class_css4 = 'mensagemok'  # Usar classe de estilo para mensagem de sucesso
else:
    mensagem_safrasimples = 'Arquivo Safra com erro, verifique'
    class_css4 = 'mensagemerro'  # Usar classe de estilo para mensagem de erro

#MENSAGEM DESCONTADA
if ul_safra_descontada == tem_que_ser_descontadasafra:
    mensagem_safradescontada = f'Último arquivo processado: {penu_safra__descontada}, e o atual {tem_que_ser_descontadasafra}. Retorno Safra Cart.Descontada Ok!'
    class_css3 = 'mensagemok' 
else:
    mensagem_safradescontada = "Arquivo safra Cart.Descontada com erro, verifique!"
    class_css3 = 'mensagemerro' 

#SOFISA
df_remessa1 =  retornosofisa_bd
df_remessa1['Data da ocorrência'] = pd.to_datetime(df_remessa1['Data da ocorrência'])

df_remessa1['Código do beneficiário'] = df_remessa1['Código do beneficiário'].apply(lambda x: re.sub("[^0-9]", "", str(x)))


df_remessa1['Código do beneficiário'] = df_remessa1['Código do beneficiário'].astype(int)

df_remessa1['Data da ocorrência'] = pd.to_datetime(df_remessa1['Data da ocorrência'])

df_remessa1 = df_remessa1[df_remessa1['Data da ocorrência'].dt.year == 2024]

df_remessa1[['Código do beneficiário','Tipo de cobrança','Data da geração do arquivo','Nome do arquivo']]
agrupados = df_remessa1.groupby(['Código do beneficiário','Nome do arquivo']).size().reset_index(name='counts')
agrupados = agrupados.sort_values(by=['Código do beneficiário'])

ultima_sequenciasofisa = agrupados['Código do beneficiário'].max()

penultima_linhasofisa = agrupados['Código do beneficiário'].iloc[-2]

tem_que_sersofisa = penultima_linhasofisa + 1



if ultima_sequenciasofisa == tem_que_sersofisa:
    mensagemsofisa = f'Último arquivo processado: {penultima_linhasofisa}, e o atual {tem_que_sersofisa}. Retorno Sofisa Ok!'
    class_css5 = 'mensagemok'  # Usar classe de estilo para mensagem de sucesso
else:
    mensagemsofisa = 'Arquivo Sofisa com erro, verifique'
    class_css5 = 'mensagemerro'  # Usar classe de estilo para mensagem de erro








def layout():
    return html.Div([
        html.H1("Auditoria de Arquivos Cnab",className="text-titulo", style={'margin-top': '30px'}),#'margin-top': '10px', 'fontSize': 25, 'fontFamily': 'Calibri', 'fontWeight': 'bold', 'color': 'black', 'textAlign': 'left', 'marginBottom': '20px'}),
        html.Img(src='/assets/santanderimagem.png', className="logo-imgz"),#, style={'width': '10%', 'marginLeft': '500px','marginTop': '0px'}),
        html.H3((mensagem_santander), className=class_css1),
        html.Img(src='/assets/unicredimagem.png', className="logo-imgz", style={'width': '8%'}),
        html.H3((mensagem_unicred), className=class_css2),
        html.Img(src='/assets/bancosafra.png', className="logo-imgz", style={'width': '8%'}),
        html.H3((mensagem_safradescontada), className=class_css3),
        html.H3((mensagem_safrasimples), className=class_css4),
        html.Img(src='/assets/Sofisaimagem.png', className="logo-imgz", style={'width': '8%'}),
        html.H3((mensagemsofisa), className=class_css5),


    ])


































# UNICRED

# df_remessa1 = remessaunicred_bd
# df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'] = pd.to_datetime(df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'])

# df_remessa1 = df_remessa1[df_remessa1['DATA DA GERAÇÃO DO ARQUIVO'].dt.year == 2024]

# df_remessa1[['SEQUENCIAL DO RETORNO','DATA DA GERAÇÃO DO ARQUIVO']]
# df_remessa1.rename(columns={'DATA DA GERAÇÃO DO ARQUIVO': 'Data da ocorrência', 'SEQUENCIAL DO RETORNO': 'Número Sequência do arquivo trailer'}, inplace=True)

# # Agrupe os dados por 'Data da ocorrência' e 'Número Sequência do arquivo trailer' e conte o número de ocorrências em cada grupo
# agrupados = df_remessa1.groupby(['Data da ocorrência', 'Número Sequência do arquivo trailer']).size().reset_index(name='counts')
# agrupados['Número Sequência do arquivo trailer'] = agrupados['Número Sequência do arquivo trailer'].astype(int) 
# agrupados = agrupados.sort_values(by=['Número Sequência do arquivo trailer'])
# agrupados= agrupados[:-8]
# ultima_sequenciaunicred = agrupados['Número Sequência do arquivo trailer'].max()
# #arquivo anterior
# penultima_linhasunidred = agrupados['Número Sequência do arquivo trailer'].iloc[-2]

# #o proximo arquivo vai ser !
# tem_que_serunicred = penultima_linhasunidred + 1


# if ultima_sequencia == tem_que_serunicred:
#     print(f'ultimo arquivo processado: {penultima_linhasunidred}, e o atual {tem_que_serunicred}. Retorno Unicred ok!'  )
# else:
#     print("Erro")


