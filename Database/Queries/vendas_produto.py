from Database.conexao_bd import conectar_db
from datetime import date, timedelta

quinze_dias = date.today() - timedelta(days=15)
#print (quinze_dias)


def show_highlight_products():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """SELECT product_name, COUNT(*) AS produto_destaque
               FROM sold_products 
               WHERE bill_emission >= CURDATE() - INTERVAL 15 DAY
               GROUP BY id_product
               ORDER BY produto_destaque DESC"""   
    cursor.execute(query)
    customer = cursor.fetchall()
    produto_destaque = [row[0] for row in customer]
    conn.close()
    
    return produto_destaque


def last_sold_products():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """ SELECT sold_products, COUNT(*) AS qnt_total_vendas
    FROM customer
    WHERE time_as_client >= CURDATE() - INTERVAL 15 DAY
    GROUP BY customer_id
    """
    cursor.execute(query)
    aumento_clientes = cursor.fetchall()
    conn.close()
    
    return aumento_clientes
