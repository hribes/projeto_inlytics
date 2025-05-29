import json
import pandas as pd
from sqlalchemy import text, MetaData, Table
from sqlalchemy import create_engine as eng
from sqlalchemy.dialects.mysql import insert
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


#Credenciais do db
sql_user = 'root'
sql_pass = 'airfwDB9090'
sql_host = 'db'
port = 3306
db_name = 'Inlytics'

#Conexão com os bancos de dados e arquivos JSON
sqlite_eng = eng('sqlite:////opt/airflow/data/empresa_cliente_db.db')
mysql_eng = eng(f'mysql+pymysql://{sql_user}:{sql_pass}@{sql_host}:{port}/{db_name}')

json_archive = '/opt/airflow/data/data.json'

#Tabelas alvo
metadata = MetaData()
customer_table = Table('customer', metadata, autoload_with=mysql_eng)
sold_products_table = Table('sold_products', metadata, autoload_with=mysql_eng)


#Funções auxiliares
def read_json_clients():
    with open(json_archive,'r') as js:
        save_points = json.load(js)

    return save_points['clients_data']['last_clients_line'], save_points['clients_update']


def save_json_clients(line, update):
    with open(json_archive, 'r') as js:
        save_points = json.load(js)

    save_points['clients_data']['last_clients_line'] = line
    save_points['clients_update'] = update

    with open(json_archive, 'w') as js:
        json.dump(save_points, js, indent=4)


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


#Funções ETL
def extract(update = None):
    if update:
        return pd.DataFrame.from_dict(update, orient='index')
    
    clients_starting_line, clients_updates = read_json_clients()
    sales_starting_line = read_json_sales()

    df_clients = pd.read_sql('SELECT * FROM customer_user', sqlite_eng).iloc[clients_starting_line:]
    df_sales = pd.read_sql('SELECT * FROM customer_sales', sqlite_eng).iloc[sales_starting_line:]

    return df_clients, df_sales, clients_updates, clients_starting_line, sales_starting_line


def transform(df_clients = None, df_sales = None):

    #Transformações nas tabelas de clientes
    if df_clients is not None:
        df_clients = df_clients.copy()
        '''
        df_clients['CustomerID'] = pd.to_numeric(df_clients['CustomerID'], errors='coerce').astype('Int64')
        df_clients['Tenure'] = pd.to_numeric(df_clients['Tenure'], errors='coerce').fillna(0).clip(lower=0, upper=99.9)
        '''
        df_clients['CustomerID'] = pd.to_numeric(df_clients['CustomerID'], errors='coerce').astype(int)
        df_clients['NomeCustomer'] = df_clients['NomeCustomer'].fillna(' ')
        df_clients['Churn'] = pd.to_numeric(df_clients['Churn'], errors='coerce').fillna(0).astype(float)
        df_clients['Gender'] = df_clients['Gender'].fillna(' ')
        df_clients['Tenure'] = pd.to_numeric(df_clients['Tenure'], errors='coerce').fillna(0).astype(float).clip(lower=0, upper=99.9)
        df_clients['PreferredPaymentMode'] = df_clients['PreferredPaymentMode'].fillna(' ')
        df_clients['PreferredLoginDevice'] = df_clients['PreferredLoginDevice'].fillna(' ')
        df_clients['SatisfactionScore'] = pd.to_numeric(df_clients['SatisfactionScore'], errors='coerce').fillna(0).astype(float)
        df_clients['MaritalStatus'] = df_clients['MaritalStatus'].fillna(' ')
        df_clients['CouponUsed'] = pd.to_numeric(df_clients['CouponUsed'], errors='coerce').fillna(0).astype(int)
        df_clients['Complain'] = pd.to_numeric(df_clients['Complain'], errors='coerce').fillna(0).astype(int)
        df_clients['NumberOfDeviceRegistered'] = pd.to_numeric(df_clients['NumberOfDeviceRegistered'], errors='coerce').fillna(0).astype(int)
        #df_clients['id_enterprise'] = pd.to_numeric(df_clients['id_enterprise'], errors='coerce').fillna(0).astype(int)

    #Transformações nas tabelas de vendas
    if df_sales is not None:
        df_sales =  df_sales.copy()
        '''
        df_sales['InvoiceNo'] = pd.to_numeric(df_sales['InvoiceNo'], errors='coerce').astype('Int64')
        df_sales['InvoiceDate'] = pd.to_datetime(df_sales['InvoiceDate'])
        df_sales['CustomerID'] = pd.to_numeric(df_sales['CustomerID'], errors='coerce').astype('Int64')
        df_sales['UnitPrice'] = pd.to_numeric(df_sales['UnitPrice'], errors='coerce').fillna(0).astype('float')
        '''
        df_sales['InvoiceNo'] = pd.to_numeric(df_sales['InvoiceNo'], errors='coerce').fillna(0).astype(int)
        df_sales['StockCode'] = df_sales['StockCode'].fillna(' ')
        df_sales['Description'] = df_sales['Description'].fillna(' ')
        df_sales['Quantity'] = pd.to_numeric(df_sales['Quantity'], errors='coerce').fillna(0).astype(int)
        df_sales['InvoiceDate'] = pd.to_datetime(df_sales['InvoiceDate'], errors='coerce').fillna(datetime(1970, 1, 1))
        df_sales['UnitPrice'] = pd.to_numeric(df_sales['UnitPrice'], errors='coerce').fillna(0).astype(float)
        df_sales['CustomerID'] = pd.to_numeric(df_sales['CustomerID'], errors='coerce').fillna(0).astype(int)
        df_sales['Country'] = df_sales['Country'].fillna(' ')

    
    return df_clients, df_sales


def rename_columns(df_clients, df_sales):
    rename_clients = {
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
    }

    rename_sales = {
        'InvoiceNo': 'invoice',
        'CustomerID': 'id_customer',
        'Description': 'product_desc',
        'UnitPrice': 'product_price',
        'StockCode': 'stock_code',
        'InvoiceDate': 'invoice_date',
        'Quantity': 'quantity',
        'Country': 'country'
    }

    df_clients_renamed = df_clients.rename(columns=rename_clients)
    df_sales_renamed = df_sales.rename(columns=rename_sales)

    return df_clients_renamed, df_sales_renamed


def upsert_dataframe(table, df, key):
    '''
    with mysql_eng.begin() as conn:
        insert_stmt = insert(table)
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{col: insert_stmt.inserted[col] for col in df.columns if col != key}
        )
        conn.execute(update_stmt, df.to_dict(orient='records'))
    '''
    df = df.where(pd.notnull(df), None)  # Converte NaN para None
    with mysql_eng.begin() as conn:
        insert_stmt = insert(table)
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{col: insert_stmt.inserted[col] for col in df.columns if col != key}
        )
        conn.execute(update_stmt, df.to_dict(orient='records'))


def validate_dataframe(df):
    if 'tenure' in df.columns and (df['tenure'] < 0).any():
        raise ValueError("Dados inválidos: 'tenure' contém valores negativos")
    if 'UnitPrice' in df.columns and (df['UnitPrice'] < 0).any():
        raise ValueError("Dados inválidos: 'UnitPrice' contém valores negativos")


def load(df_clients, df_sales):
    validate_dataframe(df_clients)
    validate_dataframe(df_sales)

    df_clients_mysql = df_clients.rename(columns={
        'CustomerID': 'customer_id',
        'NomeCustomer': 'name',
        'Churn': 'churn',
        #'Churn': 'teste',
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

    df_clients_mysql = df_clients_mysql.where(pd.notnull(df_clients_mysql), None)
    df_sales_mysql = df_sales_mysql.where(pd.notnull(df_sales_mysql), None)

    df_clients_mysql.to_sql('customer', con=mysql_eng, if_exists='append', index=False)
    df_sales_mysql.to_sql('sold_products', con=mysql_eng, if_exists='append', index=False)

    '''
    upsert_dataframe(customer_table, df_clients_mysql, 'customer_id')
    upsert_dataframe(sold_products_table, df_sales_mysql, 'invoice')

    with mysql_eng.begin() as conn:
        for _, row in df_clients_mysql.iterrows():
            stmt = insert('customer').values(**row.to_dict())
            stmt = stmt.on_duplicate_key_update(**{
                col: stmt.inserted[col] for col in row.index if col != 'customer_id'
            })
            conn.execute(stmt)

        for _, row in df_sales_mysql.iterrows():
            stmt = insert('sold_products').values(**row.to_dict())
            stmt = stmt.on_duplicate_key_update(**{
                col: stmt.inserted[col] for col in row.index if col != 'invoice'
            })
            conn.execute(stmt)
    '''

#Váriaveis que vão ser responsáveis pelo transporte dos dataframes entre funções
df_clients_file = '/opt/airflow/data/df_clients.parquet'
df_sales_file = '/opt/airflow/data/df_sales.parquet'
transformed_clients_file = '/opt/airflow/transformed_clients.parquet'
transformed_sales_file = '/opt/airflow/transformed_sales.parquet'

#DAG
default_args = {
    'owner': 'Inlytic',
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    dag_id = 'ETL',
    default_args = default_args,
    description = 'ETL que extrai arquivos do banco SQLite e os armazena no MYSQL',
    schedule = '0 0 * * *',     #'(p/ min) (p/ hora) (p/ dia) (p/mes) (p/ano)'
    start_date = datetime(2025, 1, 1),
    catchup = False
) as dag:
    

    def task_extract(ti):
        df_clients, df_sales, clients_update, clients_starting_line, sales_starting_line = extract()

        df_clients.to_parquet(df_clients_file)
        df_sales.to_parquet(df_sales_file)
        
        ti.xcom_push(key='clients_update', value=clients_update)
        ti.xcom_push(key='clients_starting_line', value=clients_starting_line)
        ti.xcom_push(key='sales_starting_line', value=sales_starting_line)


    def task_transform(ti):
        df_clients = pd.read_parquet(df_clients_file)
        df_sales = pd.read_parquet(df_sales_file)

        df_clients, df_sales = transform(df_clients, df_sales)

        df_clients.to_parquet(transformed_clients_file)
        df_clients.to_parquet(transformed_sales_file)


    def task_load(ti):
        df_clients = pd.read_parquet(df_clients_file)
        df_sales = pd.read_parquet(df_sales_file)

        load(df_clients, df_sales)

        clients_starting_line = ti.xcom_pull(key='clients_starting_line', task_ids='extract_data')
        sales_starting_line = ti.xcom_pull(key='sales_starting_line', task_ids='extract_data')
        
        save_json_clients(clients_starting_line + len(df_clients), {})
        save_json_sales(sales_starting_line + len(df_sales))


    extract_op = PythonOperator(
        task_id='extract_data',
        python_callable=task_extract
    )

    transform_op = PythonOperator(
        task_id='transform_data',
        python_callable=task_transform
    )
    
    load_op = PythonOperator(
        task_id='load_data',
        python_callable=task_load
    )

    extract_op >> transform_op >> load_op
