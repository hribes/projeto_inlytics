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
    # dados_rfm = {linha['tipo_perfil']: linha[1] for linha in resultados}
    # print(dados_rfm)
    dados_rfm = {linha['customer_classification']: linha['quantidade_usuarios'] for linha in resultados}
    return dados_rfm
