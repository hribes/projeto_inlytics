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

    print(f"[DEBUG] Resultados do SELECT: {resultados}")  # 👈 Print dos resultados crus do banco

    conn.close()

    dados_rfm = {
        linha['customer_classification']: int(linha['quantidade_usuarios'])
        for linha in resultados
    }

    print(f"[DEBUG] Dicionário gerado: {dados_rfm}")  # 👈 Print do dicionário final

    return dados_rfm
