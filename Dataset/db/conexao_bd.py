import mysql.connector
from mysql.connector import errorcode

conn = None

# faz a conexão mais a checagem pra ver se está conectado
try:
    conn = mysql.connector.connect(
        user= "",
        password= "",
        database= "",
        host= ""
    )
except mysql.connector.Error as err:
    if(err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    # else:
    #     conn.close()
    
# faz a consulta
with conn.cursor() as cursor:
	#  manda pro banco de dados a consulta
    consulta = cursor.execute("SELECT * FROM rfm LIMIT 5")
# pega o que foi pedido
    rows = cursor.fetchall()
    
    print(rows)
# mostra o resultado
    for rows in rows:
        print(rows)
