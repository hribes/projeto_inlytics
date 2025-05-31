from Database.conexao_bd import conectar_db

#Dados do Usuario
def get_user_info():
    conn = conectar_db()
    cursor = conn.cursor()

    query_name = """ SELECT worker_name FROM inlytic_user WHERE id_inlytic_user = 1; """
    cursor.execute(query_name)

    nome_usuario_consulta = cursor.fetchone()
    
    nome_usuario = nome_usuario_consulta['worker_name'] if nome_usuario_consulta else ""
    
    
    query_sector = """ SELECT sector FROM inlytic_user WHERE id_inlytic_user = 1 """
    cursor.execute(query_sector)

    setor_usuario_consulta = cursor.fetchone()
    
    setor_usuario = setor_usuario_consulta['sector'] if setor_usuario_consulta else ""


    conn.close()
    
    return nome_usuario, setor_usuario

def get_all_customers():
    conn = conectar_db()
    cursor = conn.cursor()

    query = "SELECT * FROM customer"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_customers_with_lucro_rfm_churn():
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
    SELECT 
        c.customer_id,c.name,c.gender,c.tenure,c.preferred_payment_type,
        c.frequent_dispositive,c.satisfaction_score,c.marital_status,c.cupom_used,
        c.complained,c.dispositives_num,
        r.recency,r.frequencey,r.monetary,
        r.customer_classification,
        ch.loss_probabilty AS churn,
        COALESCE(SUM(sp.product_price * sp.quantity), 0) AS lucro
    FROM customer c
    LEFT JOIN rfm r ON c.customer_id = r.customer_id
    LEFT JOIN churn ch ON c.customer_id = ch.id_customer
    LEFT JOIN sold_products sp ON c.customer_id = sp.id_customer
    GROUP BY 
        c.customer_id, c.name, c.gender, c.tenure, c.preferred_payment_type,
        c.frequent_dispositive, c.satisfaction_score, c.marital_status,
        c.cupom_used, c.complained, c.dispositives_num,
        r.recency, r.frequencey, r.monetary, r.customer_classification,
        ch.loss_probabilty
    ORDER BY c.customer_id
    """

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results
def search_user_profile(perfil=None):
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
    SELECT 
        c.customer_id,c.name,c.gender,c.tenure,c.preferred_payment_type,
        c.frequent_dispositive,c.satisfaction_score,c.marital_status,c.cupom_used,
        c.complained,c.dispositives_num,
        r.recency,r.frequencey,r.monetary,
        r.customer_classification,
        ch.loss_probabilty AS churn,
        COALESCE(SUM(sp.product_price * sp.quantity), 0) AS lucro
    FROM customer c
    LEFT JOIN rfm r ON c.customer_id = r.customer_id
    LEFT JOIN churn ch ON c.customer_id = ch.id_customer
    LEFT JOIN sold_products sp ON c.customer_id = sp.id_customer
    """

    params = []
    if perfil:
        query += " WHERE r.customer_classification = %s "

        params.append(perfil)

    query += """
    GROUP BY 
        c.customer_id, c.name, c.gender, c.tenure, c.preferred_payment_type,
        c.frequent_dispositive, c.satisfaction_score, c.marital_status,
        c.cupom_used, c.complained, c.dispositives_num,
        r.recency, r.frequencey, r.monetary, r.customer_classification,
        ch.loss_probabilty
    ORDER BY c.customer_id
    LIMIT 50;
    """

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
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