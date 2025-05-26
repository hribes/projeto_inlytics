from Database.conexao_bd import conectar_db
from datetime import date, timedelta

quinze_dias = date.today() - timedelta(days=15)
#print (quinze_dias)

#Produto em destaque
def show_highlight_products():
    conn = conectar_db()
    cursor = conn.cursor()

    query = """SELECT product_desc, COUNT(*) AS produto_destaque
               FROM sold_products 
               WHERE invoice_date >= CURDATE() - INTERVAL 30 DAY
               GROUP BY stock_code, product_desc
               ORDER BY produto_destaque DESC
               LIMIT 1"""
       
    cursor.execute(query)
    customer = cursor.fetchall()

    #produto_destaque = [row[0] for row in customer]
    produto_destaque = [row['product_desc'] for row in customer]
    conn.close()
    
    if produto_destaque:
        return produto_destaque
    else:
        return {'product_desc': 'Nenhum produto vendido', 'quantidade_vendida': 0}


#?????
# def last_sold_products():
#     conn = conectar_db()
#     cursor = conn.cursor()
#     query = """ SELECT sold_products, COUNT(*) AS qnt_total_vendas
#     FROM customer
#     WHERE time_as_client >= CURDATE() - INTERVAL 15 DAY
#     GROUP BY customer_id
#     """
#     cursor.execute(query)
#     aumento_clientes = cursor.fetchall()
#     conn.close()
    
#     return aumento_clientes
