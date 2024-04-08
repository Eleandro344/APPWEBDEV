
import pandas as pd
import mysql.connector
# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host='db_sabertrimed.mysql.dbaas.com.br',
    user='db_sabertrimed',
    password='s@BRtR1m3d',  
    database='db_sabertrimed',
)

#REMESSA SANTANDER      
consulta_remessa = "SELECT * FROM remessa_santander"
remessaantader_bd = pd.read_sql(consulta_remessa, con=mydb)

#RETORNO SANTANDER
consulta_retorno = "SELECT * FROM retorno_santander"
retornosantander_bd = pd.read_sql(consulta_retorno, con=mydb)

#REMESSA UNICRED
consulta_remessa = "SELECT * FROM unicredremessa"
remessaunicred_bd = pd.read_sql(consulta_remessa, con=mydb)

#RETORNO UNICRED
consulta_retorno = "SELECT * FROM retornounicred"
retornounicred_bd = pd.read_sql(consulta_retorno, con=mydb)

#RETORNO SAFRA
consulta_retorno = "SELECT * FROM retorno_safra"
retornosfra_bd = pd.read_sql(consulta_retorno, con=mydb)

#REMESSA SAFRA
consulta_remessa = "SELECT * FROM remessa_safra"
remessasafra_bd = pd.read_sql(consulta_remessa, con=mydb)

#REMESSA SOFISA
consulta_remessa = "SELECT * FROM remessa_sofisa"
remessasofisa_bd = pd.read_sql(consulta_remessa, con=mydb)
#RETORNO SOFISA
consulta_retorno = "SELECT * FROM retorno_sofisa"
retornosofisa_bd = pd.read_sql(consulta_retorno, con=mydb)
mydb.close()


