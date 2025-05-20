from Database.conexao_bd import conectar_db

#Dados do Usuario
def get_user_info():
    conn = conectar_db()
    cursor = conn.cursor()
    query_name = """ SELECT worker_name FROM inlytic_user WHERE id_inlytic_user = 1; """
    cursor.execute(query_name)
    nome_usuario_consulta = cursor.fetchone()
    
    nome_usuario = nome_usuario_consulta[0] if nome_usuario_consulta else ""
    
    
    query_sector = """ SELECT sector FROM inlytic_user WHERE id_inlytic_user = 1 """
    cursor.execute(query_sector)
    setor_usuario_consulta = cursor.fetchone()
    setor_usuario = setor_usuario_consulta[0] if setor_usuario_consulta else ""


    conn.close()
    
    return nome_usuario, setor_usuario

def get_all_customers():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM customer"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
    
#  conn = conectar_db()
#     cursor = conn.cursor()
#     query = """ SELECT sold_products, COUNT(*) AS qnt_total_vendas
#     FROM customer
#     WHERE time_as_client >= CURDATE() - INTERVAL 15 DAY
#     GROUP BY customer_id
#     """
#     cursor.execute(query)
#     aumento_clientes = cursor.fetchall()
#     conn.close()