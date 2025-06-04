import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from conexao_bd import conectar_db
from sqlalchemy import create_engine as eng


conn = conectar_db()
load_dotenv()

eng = eng(f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}')


# Carregar o pipeline salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model', 'modelo_churn_final.pkl')
pipeline_carregado = joblib.load(model_path)

#Preciso que seja importado a tabela das vendas, dos clientes e do rfm
df_customer_user = pd.read_sql_query("""SELECT * FROM customer""", eng)
df_customer_sales = pd.read_sql_query("""SELECT * FROM sold_products""", eng)
df_rfm = pd.read_sql_query("""SELECT * FROM rfm""", eng)

# Junção das tabelas para ter mais dados relevantes para o modelo
df_customer_sales['InvoiceDate'] = pd.to_datetime(df_customer_sales['invoice_date'])
df_customer_sales['DateStartBase'] = df_customer_sales['InvoiceDate'].dt.strftime('%Y-%m-%d')
df_customer_min_invoice = df_customer_sales.groupby('id_customer')['DateStartBase'].agg('min').reset_index()
df_user_rfm = pd.merge(df_customer_user, df_rfm, on='customer_id', how='left')
df_all_data = pd.merge(df_user_rfm, df_customer_min_invoice, left_on='customer_id', right_on='id_customer', how='left')
df_all_data = df_all_data.drop(columns=['tenure'])

# Trocando os dados em formato de Datetime para em dias (de quando começou até o ultimo dia marcado na tabela)
data_referencia = pd.to_datetime('2011-12-09')
df_all_data['DateStartBase'] = pd.to_datetime(df_all_data['DateStartBase'])
df_all_data['DateStart_Days'] = (data_referencia - df_all_data['DateStartBase']).dt.days
dados_sem_null = df_all_data['DateStart_Days'].dropna()

df_all_data.drop(columns=['name', 'DateStartBase', 'churn'], inplace=True)
categorical_features = ['PreferredLoginDevice', 'PreferredPaymentMode', 'Gender', 'MaritalStatus']
numeric_features = [col for col in df_all_data.columns if col not in categorical_features + ['churn']]

df_all_data.rename(columns={
    'recency': 'Recency',
    'frequencey': 'Frequency',
    'monetary': 'Monetary',
    'r_score': 'R_Score',
    'f_score': 'F_Score',
    'm_score': 'M_Score',
    'gender': 'Gender',
    'marital_status': 'MaritalStatus',
    'complained': 'Complain',
    'cupom_used': 'CouponUsed',
    'preferred_payment_type': 'PreferredPaymentMode',
    'dispositives_num': 'NumberOfDeviceRegistered',
    'frequent_dispositive': 'PreferredLoginDevice',
    'satisfaction_score': 'SatisfactionScore'
}, inplace=True)

# Usar para prever novos dados
y_pred = pipeline_carregado.predict_proba(df_all_data)

customer_ids = df_all_data['customer_id'].copy()
y_proba = pipeline_carregado.predict_proba(df_all_data)[:, 1]


df_resultado = pd.DataFrame({
    'id_customer': customer_ids,
    'id_enterprise': 1,
    'loss_probabilty': y_proba
})

# DEVERÁ SER ENVIADO PARA O BANCO 'df_resultado'
df_resultado.to_sql('churn', con=eng, if_exists='append', index=False)
print(df_resultado.head())
