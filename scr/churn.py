import joblib
import pandas as pd

# Carregar o pipeline salvo
pipeline_carregado = joblib.load('scr/model/modelo_churn_final.pkl')

#Preciso que seja importado a tabela das vendas, dos clientes e do rfm
df_customer_user = pd.read_sql_query('')
df_customer_sales = pd.read_sql_query('')
df_rfm = pd.read_sql_query('')

# Junção das tabelas para ter mais dados relevantes para o modelo
df_customer_sales['InvoiceDate'] = pd.to_datetime(df_customer_sales['InvoiceDate'])
df_customer_sales['DateStartBase'] = df_customer_sales['InvoiceDate'].dt.strftime('%Y-%m-%d')
df_customer_min_invoice = df_customer_sales.groupby('CustomerID')['DateStartBase'].agg('min').reset_index()
df_user_rfm = pd.merge(df_customer_user, df_rfm, on='CustomerID', how='left')
df_all_data = pd.merge(df_user_rfm, df_customer_min_invoice, on='CustomerID', how='left')
df_all_data = df_all_data.drop(columns=['Tenure', 'Segment'])

# Trocando os dados em formato de Datetime para em dias (de quando começou até o ultimo dia marcado na tabela)
data_referencia = pd.to_datetime('2011-12-09')
df_all_data['DateStartBase'] = pd.to_datetime(df_all_data['DateStartBase'])
df_all_data['DateStart_Days'] = (data_referencia - df_all_data['DateStartBase']).dt.days
dados_sem_null = df_all_data['DateStart_Days'].dropna()

df_all_data.drop(columns=['CustomerID', 'NomeCustomer', 'DateStartBase', 'Churn'], inplace=True)
categorical_features = ['PreferredLoginDevice', 'PreferredPaymentMode', 'Gender', 'MaritalStatus']
numeric_features = [col for col in df_all_data.columns if col not in categorical_features + ['Churn']]

# Usar para prever novos dados
y_pred = pipeline_carregado.predict_proba(df_all_data)

customer_ids = df_all_data['CustomerID'].copy()
y_proba = pipeline_carregado.predict_proba(df_all_data)[:, 1]

df_resultado = pd.DataFrame({
    'CustomerID': customer_ids,
    'Probabilidade_Churn': y_proba
})

# DEVERÁ SER ENVIADO PARA O BANCO 'df_resultado'