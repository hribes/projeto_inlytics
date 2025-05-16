import json
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine as eng

sql_user = ''
sql_pass = ''
sql_host = ''
port = 0000
db_name = ''

sqlite_eng = eng('sqlite:///../../Dataset/db_cliente_sqlite/empresa_cliente_db.db')
mysql_eng = eng(f'mysql+pymysql://{sql_user}:{sql_pass}@{sql_host}:{port}/{db_name}')

json_archive = './data.json'

def read_json_sales():
    with open(json_archive, 'r') as js:
        sales_data = json.load(js)

    return sales_data['sales_data']['last_sales_line']

def save_json_sales(line):
    with open(json_archive, 'r') as js:
        sales_data = json.load(js)

    sales_data['sales_data']['last_sales_line'] = line

    with open(json_archive, 'w') as js:
        json.dump(sales_data, js, indent = 4)

def extract():
    sales_starting_line = read_json_sales()

    df_clients = pd.read_sql('SELECT * FROM customer_user', sqlite_eng)
    df_sales = pd.read_sql('SELECT * FROM customer_sales', sqlite_eng).iloc[sales_starting_line:]

    return df_clients, df_sales

def transform(df_clients, df_sales):
    #Transformações nas tabelas de clientes
    df_clients['CustomerID'] = pd.to_numeric(df_clients['CustomerID'], errors='coerce').astyper('int')
    df_clients.loc[df_clients['Tenure'] <= 0, 'Tenure'] = 0
    df_clients.loc[df_clients['Tenure'].isnull(), 'Tenure'] = 0

    #Transformações nas tabelas de vendas
    df_sales['InvoiceNo'] = pd.to_numeric(df_sales['InvoiceNo'], errors='coerce').astype('int')
    df_sales['InvoiceDate'] = pd.to_datetime(df_sales['InvoiceDate'])
    df_sales['CustomerID'] = pd.to_numeric(df_sales['CustomerID'], errors='coerce').astype('int')
    df_sales['UnitPrice'] = pd.to_numeric(df_sales['UnitPrice'], errors='coerce').astype('float')

def load(df_clients, df_sales):
    df_clients_mysql = df_clients.raname(columns={
        'CustomerID': 'customer_id',
        'NomeCustomer': 'name',
        'Churn': 'churn',
        'Gender': 'gender',
        'Tenure': 'tenure',
        'PreferredPaymentMode': 'preferred_payment_type',
        'PreferredLoginDevice': 'frequent_dispositive',
        'SatisfactionScore': 'satisfaction_score',
        'CouponUsed': 'cupom_used',
        'Complain': 'complained',
        'NumberOfDeviceRegistered': 'dispositives_num',
        'MaritalStatus': 'marital_status'
    })

    df_sales_mysql = df_sales.rename(columns={
        'InvoiceNo': 'invoice',
        'CustomerID': 'id_customer',
        'Description': 'product_desc',
        'UnitPrice': 'product_price',
        'StockCode': 'stock_code',
        'InvoiceDate': 'invoice_date',
        'Quantity': 'quantity',
        'Country': 'country'
    })

    df_clients_mysql.to_sql('customer', con=mysql_eng, if_exists='append', index=False)
    df_sales_mysql.to_sql('sold_products', con=mysql_eng, if_exists='append', index=False)

def main():
    df_clients, df_sales = extract()

    transform(df_clients, df_sales)
    load(df_clients, df_sales)

    save_json_sales(read_json_sales() + len(df_sales))


if __name__ == '__main__':
    main()
