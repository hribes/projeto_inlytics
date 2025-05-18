from mysql.connector import connect, errorcode, Error
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
		conn = None

		# faz a conexão mais a checagem pra ver se está conectado
		try:
			conn = connect(
				user= os.getenv("DB_USER"),
				password= os.getenv("DB_PASSWORD"),
				database= os.getenv("DB_DATABASE"),
				host= os.getenv("DB_HOST"),
				port= os.getenv("DB_PORT")
			)
		except Error as err:
			if(err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
				print("Something is wrong with your username or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)

		return conn
