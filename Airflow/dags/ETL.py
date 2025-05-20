import json
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine as eng
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


def transform(df_clients = None, df_sales = None, df_update = None):
    #Só ira transformar updates se existirem
    if df_update is not None and not df_update.empty:
        df_update['CustomerID'] = pd.to_numeric(df_update['CustomerID'], errors='coerce').astype('int')
        df_update['Tenure'] = pd.to_numeric(df_update['Tenure'], errors='coerce').astype('float')
        df_update.loc[df_update['Tenure'] <= 0, 'Tenure'] = 0
        df_update.loc[df_update['Tenure'].isnull(), 'Tenure'] = 0
        df_update.loc[df_update['Tenure'] > 99.9, 'Tenure'] = 99.9
        return
    
    #Transformações nas tabelas de clientes
    df_clients['CustomerID'] = pd.to_numeric(df_clients['CustomerID'], errors='coerce').astype('int')
    df_clients.loc[df_clients['Tenure'] <= 0, 'Tenure'] = 0
    df_clients.loc[df_clients['Tenure'].isnull(), 'Tenure'] = 0
    df_clients.loc[df_clients['Tenure'] > 99.9, 'Tenure'] = 99.9

    #Transformações nas tabelas de vendas
    df_sales['InvoiceNo'] = pd.to_numeric(df_sales['InvoiceNo'], errors='coerce').astype('int')
    df_sales['InvoiceDate'] = pd.to_datetime(df_sales['InvoiceDate'])
    df_sales['CustomerID'] = pd.to_numeric(df_sales['CustomerID'], errors='coerce').astype('int')
    df_sales['UnitPrice'] = pd.to_numeric(df_sales['UnitPrice'], errors='coerce').astype('float')


def update(clients_ids):
    
    df_update = extract(clients_ids)
    transform(None, None, df_update)

    df_update_mysql = df_update.rename(columns={
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

    #Executa os updates na tabela de clientes
    with mysql_eng.begin() as conn:
        for _, row in df_update_mysql.iterrows():
            conn.execute(
                text("""
                    UPDATE customer SET
                     name = :name,
                     churn = :churn,
                     gender = :gender,
                     tenure = :tenure,
                     preferred_payment_type = :preferred_payment_type,
                     frequent_dispositive = :frequent_dispositive,
                     satisfaction_score = :satisfaction_score,
                     cupom_used = :cupom_used,
                     complained = :complained,
                     dispositives_num = :dispositives_num,
                     marital_status = :marital_status
                    WHERE customer_id = :customer_id
                """),
                row.to_dict()
            )


def load(df_clients, df_sales):
    df_clients_mysql = df_clients.rename(columns={
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


#Váriaveis que vão ser responsáveis pelo transporte dos dataframes entre funções
df_clients_file = '/opt/airflow/data/df_clients.parquet'
df_sales_file = '/opt/airflow/data/df_sales.parquet'

#DAG
default_args = {
    'owner': 'Inlytic',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
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

        transform(df_clients, df_sales)


    def task_update(ti):
        clients_update = ti.xcom_pull(key='clients_update', task_ids='extract_data')

        if clients_update:
            update(clients_update)


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

    update_op = PythonOperator(
        task_id='update_clients',
        python_callable=task_update
    )

    load_op = PythonOperator(
        task_id='load_data',
        python_callable=task_load
    )

    extract_op >> transform_op >> update_op >> load_op
