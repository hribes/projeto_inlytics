# Acrescentar todas as importanções necessárias
from conexao_bd import conectar_db
from sqlalchemy import create_engine as eng
from dotenv import load_dotenv
import pandas as pd
import os

conn = conectar_db()
load_dotenv()

engine = eng(f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}')


df_vendas = pd.read_sql_query("SELECT * FROM sold_products", engine)


# Colocando os dados da coluna InvoiceDate no formato datetime para poder manipular datas
print(df_vendas.head())
df_vendas['InvoiceDate'] = pd.to_datetime(df_vendas['invoice_date'])

# Removendo os dados com CustomerID nulo
df_vendas = df_vendas[df_vendas['id_customer'].notnull()]

# Removendo as transações com Quantity <= 0 para que não haja erro
df_vendas = df_vendas[df_vendas['quantity'] > 0]

# Calculamos o total por cada linha
df_vendas['TotalPrice'] = df_vendas['quantity'] * df_vendas['product_price']

# Definimos a data de referência para Recência
data_ref = df_vendas['InvoiceDate'].max() + pd.Timedelta(days=1)

# Calculo do RFM
rfm = df_vendas.groupby('id_customer').agg({
    'InvoiceDate': lambda x: (data_ref - x.max()).days,
    'invoice': 'nunique',
    'TotalPrice': 'sum'
}).reset_index()

# Nomeando as colunas
rfm.columns = ['id_customer', 'Recency', 'Frequency', 'Monetary']

# Criação dos Scores para R, F e M com base em quintis
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)  # Recência: menor valor melhor (mais recente)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)  # Frequência: maior melhor
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)  # Monetário: maior melhor


# Função para segmentar clientes com base em R, F e M
def rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] >= 4 and row['F_Score'] <= 2 and row['M_Score'] >= 3:
        return 'Potential Loyalist'
    elif row['R_Score'] >= 2 and row['F_Score'] >= 4 and row['M_Score'] <= 2:
        return 'Recent Customers'
    elif row['R_Score'] == 1 and row['F_Score'] >= 4 and row['M_Score'] >= 3:
        return 'Promising'
    elif row['R_Score'] == 1 and row['F_Score'] <= 2 and row['M_Score'] <= 2:
        return 'Needs Attention'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2 and row['M_Score'] <= 2:
        return 'At Risk'
    elif row['R_Score'] == 3 and row['F_Score'] == 1 and row['M_Score'] <= 2:
        return 'About To Sleep'
    elif row['R_Score'] == 2 and row['F_Score'] == 1 and row['M_Score'] <= 2:
        return 'Hibernating'
    elif row['R_Score'] == 1 and row['F_Score'] == 1 and row['M_Score'] == 1:
        return 'Lost'
    else:
        return 'Others'

# Aplicação da função nos dados
rfm['Segment'] = rfm.apply(rfm_segment, axis=1)


# Ordenação para melhor visualização
rfm = rfm.sort_values(by=['R_Score', 'F_Score', 'M_Score'], ascending=[False, False, False])
print(rfm.head())

#....
def load():
    rfm['enterprise_id'] = 1  
    dados_rfm = rfm.rename(columns={
        'R_Score': 'r_score',
        'F_Score': 'f_score',
        'M_Score': 'm_score',
        'id_rfm': 'id_rfm',
        'Recency': 'recency', 
        'Frequency': 'frequencey', 
        'Monetary': 'monetary', 
        'Segment':'customer_classification', 
        'id_customer': 'customer_id', 
        'enterprise_id': 'enterprise_id'
    }) 
          


    dados_rfm.to_sql('rfm', con=engine, if_exists='append', index=False)

load()