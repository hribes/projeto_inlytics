from Database.conexao_bd import conectar_db
from werkzeug.security import check_password_hash

def find_by_email_password(email, password):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    query = """SELECT * FROM inlytic_user WHERE worker_email = %s LIMIT 1"""   
    cursor.execute(query,(email, ))
    
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['login_password'], password):
        return True
    else:
        return False
    
