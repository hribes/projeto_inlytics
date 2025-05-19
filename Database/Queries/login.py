from Database.conexao_bd import conectar_db
from werkzeug.security import check_password_hash

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_inlytic_user, worker_name, worker_email, sector, photo_url):
        self.id = id_inlytic_user
        self.worker_name = worker_name
        self.worker_email = worker_email
        self.sector = sector
        self.photo_url = photo_url

    def get_id(self):
        return str(self.id)
    
    
def find_by_email_password(email, password):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM inlytic_user WHERE worker_email = %s LIMIT 1"
    cursor.execute(query, (email,))
    
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['login_password'], password):
        return user 
    else:
        return None
    
def load_user(user_id):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM inlytic_user WHERE id_inlytic_user = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(
            id_inlytic_user=user_data['id_inlytic_user'],
            worker_name=user_data['worker_name'],
            worker_email=user_data['worker_email'],
            sector=user_data['sector'],
            photo_url=user_data['photo_url']
        )
    return None

def find_user_by_id(user_id):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM inlytic_user WHERE id_inlytic_user = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return user

# def find_by_email_password(email, password):
#     conn = conectar_db()
#     cursor = conn.cursor(dictionary=True)
    
#     query = """SELECT * FROM inlytic_user WHERE worker_email = %s LIMIT 1"""   
#     cursor.execute(query,(email, ))
    
#     user = cursor.fetchone()
#     conn.close()

#     if user and check_password_hash(user['login_password'], password):
#         return True
#     else:
#         return False
    
