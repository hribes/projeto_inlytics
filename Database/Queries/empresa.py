from Database.conexao_bd import conectar_db

id_enterprise = 1

#Dados da empresa
def company_data():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """
        SELECT enterprise_name AS nome_empresa
        FROM enterprise
        WHERE id_enterprise = %s;
    """
    params = (id_enterprise,)
    
    cursor.execute(query, params)
    dados_empresa = cursor.fetchone()
    
    return dados_empresa


