import csv
import sqlite3

CSV_DIR = "../../Dataset"


def db_connect():
	conn = sqlite3.connect("../customer_clear.db")

	return conn

def create_tables() -> None:
	conn = db_connect()
	curr = conn.cursor()

	curr.execute("""CREATE TABLE IF NOT EXISTS customer(
		customer_id INTEGER,
		churn INTEGER,
		tenure REAL,
		preferred_login_device VARCHAR(9),
		preferred_payment_mode VARCHAR(8),
		gender VARCHAR(8),
		number_of_device_registered INTEGER,
		satisfaction_score REAL,
		marital_status VARCHAR(7),
		complain BOOLEAN,
		coupon_used BOOLEAN,
		name_customer VARCHAR(64)
	)""")

	curr.execute("CREATE TABLE IF NOT EXISTS solds(invoice_no INTEGER, stock_code VARCHAR(6), description VARCHAR(42), quantity INTEGER, invoice_date TEXT, unitary_price FLOAT, customer_id INTEGER, country VARCHAR(14))")

	curr.close()
	conn.close()

def db_insert(query: str, thing_to_insert) -> None:
	fquery = f"INSERT INTO {query}"
	conn = db_connect()
	curr = conn.cursor()

	curr.execute(fquery, thing_to_insert)

	conn.commit()

	curr.close()
	conn.close()

def insert_data_into_customers() -> None:
	file_to_read = f"{CSV_DIR}/clientes_info_limpo.csv"

	with open(file_to_read) as file:
		reader = csv.reader(file, delimiter=',')

		next(reader, None)

		for data in reader:
			# checa se a linha está vazia
			# https://stackoverflow.com/questions/34192705/python-how-to-check-if-cell-in-csv-file-is-empty
			if(not data[4]):
				data[4] = None
			elif(not data[6]):
				data[6] = None
			elif(not data[8]):
				data[8] = None

			customer_id = data[0]
			churn = data[1]
			tenure = data[2]
			preferred_login_device = data[3]
			preferred_payment_mode = data[4]
			gender = data[5]
			number_of_device_registered = data[6]
			satisfaction_score = data[7]
			marital_status = data[8]
			complain = data[9]
			coupon_used = data[10]
			name_customer = data[11]

			data_to_insert = (customer_id, churn, tenure, preferred_login_device, preferred_payment_mode, gender, number_of_device_registered, satisfaction_score, marital_status, complain, coupon_used, name_customer,)

			db_insert("""customer(
				customer_id,
				churn,
				tenure,
				preferred_login_device,
				preferred_payment_mode,
				gender,
				number_of_device_registered,
				satisfaction_score,
				marital_status,
				complain,
				coupon_used,
				name_customer
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
			, data_to_insert)

def insert_data_into_solds() -> None:
	file_to_read = f"{CSV_DIR}/vendas_info_limpo.csv"

	with open(file_to_read) as file:
		reader = csv.reader(file, delimiter=',')

		next(reader, None)

		for data in reader:
			invoice_no = data[0]
			stock_code = data[1].strip()
			description = data[2].strip()
			quantity = data[3]
			invoice_date = data[4]
			unitary_price = data[5]
			customer_id = data[6]
			country = data[7].strip()

			data_to_insert = (invoice_no, stock_code, description, quantity, invoice_date, unitary_price, customer_id, country,)

			db_insert("""solds(
				invoice_no,
				stock_code,
				description,
				quantity,
				invoice_date,
				unitary_price,
				customer_id,
				country
			) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", 
			data_to_insert)

create_tables()
insert_data_into_customers()
insert_data_into_solds()
