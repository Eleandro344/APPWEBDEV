import pandas as pd

# Especifique o encoding correto ao ler o arquivo CSV
antecipados = pd.read_excel(r'C:\Users\elean\Desktop\bancodedados\pagosntecipados.xlsx')

# Verifique os primeiros registros para garantir que os dados foram carregados corretamente
antecipados['antecipado'] = antecipados['antecipado'].apply(lambda x: 0 if x >= 0 else x)

contagem_antecipado = antecipados[antecipados['antecipado'] < 0].groupby('Nome').size().reset_index(name='Total_de_Pedidos_Antecipados')

contagem_pedidos_cliente = antecipados.groupby('Nome').size().reset_index(name='Total_de_Pedidos')

merged_df = pd.merge(contagem_antecipado, contagem_pedidos_cliente, on='Nome', how='outer')

merged_df.fillna(0, inplace=True)

merged_df['Chance_de_Antecipacao(%)'] = (merged_df['Total_de_Pedidos_Antecipados'] / merged_df['Total_de_Pedidos']) * 100

merged_df['Chance_de_Antecipacao'] = (merged_df['Chance_de_Antecipacao(%)']).round(2)

merged_df['Chance_de_Antecipacao'] = merged_df['Chance_de_Antecipacao'].apply(lambda x: f'{x:.2f} %')

df_antecipacao = merged_df[['Nome','Chance_de_Antecipacao']]

novos_nomes = {
    'Nome': 'Nome/Razão Social do Pagador',
    'Chance_de_Antecipacao':'IA'

    
    # ... adicione os outros nomes conforme necessário
}
df_antecipacao.rename(columns=novos_nomes, inplace=True)
#df_antecipacao['Nome/Razão Social do Pagador'] = df_antecipacao['Nome/Razão Social do Pagador'].str.strip()

df_antecipacao['Nome/Razão Social do Pagador'] = df_antecipacao['Nome/Razão Social do Pagador'].str.replace('    ', '')

df_antecipacao['Nome/Razão Social do Pagador'] = df_antecipacao['Nome/Razão Social do Pagador'].str.upper()


#print(df_antecipacao)