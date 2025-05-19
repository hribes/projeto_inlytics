from Database.conexao_bd import conectar_db

def type_and_qnt_perfil(enterprise_id):
    conn = conectar_db()
    cursor = conn.cursor()
    query = """ 
        SELECT customer_classification, COUNT(*) AS quantidade_usuarios
        FROM rfm
        WHERE enterprise_id = %s
        GROUP BY customer_classification
    """
    cursor.execute(query, (enterprise_id,))
    resultados = cursor.fetchall()
    conn.close()

    # Transforma os resultados em dicionário: {"Campeões": 10, "Em risco": 5, ...}
    dados_rfm = {linha[0]: linha[1] for linha in resultados}
    print(dados_rfm)
    return dados_rfm
