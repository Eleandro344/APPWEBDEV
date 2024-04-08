import pandas as pd
from app import app  
from components.bancodedados import retornosantander_bd
from components.bancodedados import remessaunicred_bd


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
    mensagem = "f'ultimo arquivo processado: {penultima_linhasantader}, e o atual {tem_que_sersantander}. Retorno Santander ok!' " 
else:
    print("Erro")





























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







def layout():
    return html.Div([
        html.H1("teste", style={'textAlign':'center'}),
    ])