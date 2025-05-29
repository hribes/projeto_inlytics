from Database.conexao_bd import conectar_db
from flask import jsonify

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
    qnt_total_clientes = cursor.fetchone()['COUNT(*)']
    conn.close()

    print(qnt_total_clientes)
    return qnt_total_clientes
    
#QNT total de novos clientes por data    
def clients_increase():
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
        SELECT customer_id
        FROM customer
        WHERE tenure <= 0
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

#Define a seta da variação de clientes
def increase_simbol():
    conn = conectar_db()
    cursor = conn.cursor()

    query = """ SELECT customer_id FROM customer WHERE tenure > 1 """

    cursor.execute(query)
    old_clients = len(cursor.fetchall())

    query = """ SELECT customer_id FROM customer WHERE tenure = 1 """

    cursor.execute(query)
    new_clients = len(cursor.fetchall())

    percentage = (new_clients - old_clients) // 100

    if percentage > 0:
        return True
    
    else:
        return False

    '''
    1 coisa: Pegar os valores dos tenures iguais ou maiores que 2
    
    2 coisa: Pegar os valores dos tenures iguais a 1
    
    3 coisa: Fazer a porcentagem (se for maior: seta p/ cima, se for menor: seta p/ baixo)
    
    Retornar o sentido da seta para a API
    '''