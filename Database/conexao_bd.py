from mysql.connector import connect, errorcode, Error
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
		conn = None

		# faz a conexão mais a checagem pra ver se está conectado
		try:
			conn = connect(
				user= os.getenv("USER"),
				password= os.getenv("PASSWORD"),
				database= os.getenv("DATABASE"),
				host= os.getenv("HOST")
			)
		except Error as err:
			if(err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
				print("Something is wrong with your username or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)

		return conn
