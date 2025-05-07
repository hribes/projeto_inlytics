from Dataset.db.conexao_bd import conn

def list_all_customers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    customer = cursor.fetchall()
    conn.close
    
    return customer