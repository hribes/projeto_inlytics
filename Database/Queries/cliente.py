from Database.conexao_bd import conectar_db

#Listar todos os clientes
def list_all_clients():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    customer = cursor.fetchall()
    conn.close()
    
    return customer

#QNT total de clientes
def qnt_all_clients():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """ SELECT COUNT(*) FROM customer
    """
    cursor.execute(query)
    qnt_total_clientes = cursor.fetchone()[0]
    conn.close()
    print(qnt_total_clientes)
    return qnt_total_clientes
    
#QNT total de novos clientes por data    
def clients_increase():
    conn = conectar_db()
    cursor = conn.cursor()
    # query = """ SELECT customer_id, COUNT(*) AS novos_clientes
    # FROM customer
    # WHERE time_as_client >= CURDATE() - INTERVAL 15 DAY
    # GROUP BY customer_id
    # """
    
    query = """SELECT customer_id, COUNT(*) AS novos_clientes
     FROM customer
     WHERE tenure >= 1 
     GROUP BY customer_id
    """
    cursor.execute(query)
    aumento_clientes = cursor.fetchall()
    conn.close()
    
    return aumento_clientes
    
#  query = """SELECT product_name, COUNT(*) AS produto_destaque
#                FROM sold_products 
#                WHERE bill_emission >= CURDATE() - INTERVAL 15 DAY
#                GROUP BY id_product
#                ORDER BY produto_destaque DESC"""   