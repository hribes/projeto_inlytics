from Database.conexao_bd import conectar_db
from datetime import date, timedelta, datetime

quinze_dias = date.today() - timedelta(days=15)
#print (quinze_dias)

#Produto em destaque
def show_highlight_products():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """SELECT product_desc, COUNT(*) AS produto_destaque
               FROM sold_products 
               WHERE invoice_date >= CURDATE() - INTERVAL 15 DAY
               GROUP BY stock_code
               ORDER BY produto_destaque DESC"""   
    cursor.execute(query)
    customer = cursor.fetchall()
    produto_destaque = [row[0] for row in customer]
    conn.close()
    
    return produto_destaque


def completa_anos_meses_simples(dados):
    # Dicionário de meses em português
    meses = {
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
        '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
    }
    
    # Encontrar o ano mais recente nos dados
    anos = [item['data'].split()[-1] for item in dados]
    ano_mais_recente = max(anos)
    
    # Criar lista com todos os meses do ano mais recente
    dados_completos = []
    for mes_num in range(1, 13):
        mes_str = f"{mes_num:02d}"  # Ex: '01', '02', etc.
        nome_mes = f"{meses[mes_str]} {ano_mais_recente}"  # Ex: "Janeiro 2025"
        
        # Verificar se o mês existe nos dados
        valor = 0
        for item in dados:
            if item['data'] == nome_mes:
                valor = item['valor']
                break
        
        dados_completos.append({'data': nome_mes, 'valor': valor})
    
    return dados_completos



# def monthly_sales_data():
#     conn = conectar_db()
#     cursor = conn.cursor()
    
#     query = """
#         SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
#         SUM(product_price) AS faturamento_total
#         FROM sold_products
#         GROUP BY mes
#         ORDER BY mes;
#     """
    
#     cursor.execute(query)
#     resultado = cursor.fetchall()
#     conn.close()
    
#     dados = [(row[0], round(float(row[1]), 2)) for row in resultado]
    
#     # Exemplo de função opcional que completa os meses vazios
#     dados_completos = completa_anos_meses_simples(dados)

#     return dados_completos

def monthly_sales_data():
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
        SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
        SUM(product_price) AS faturamento_total
        FROM sold_products
        GROUP BY mes
        ORDER BY mes;
    """
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    
    # Dicionário para mapear números dos meses para nomes em português
    meses = {
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
        '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
    }
    
    # Converter os dados brutos e incluir nomes dos meses
    dados = []
    for row in resultado:
        ano_mes = row[0]  # Formato 'YYYY-MM'
        ano, mes = ano_mes.split('-')
        nome_mes = f"{meses[mes]} {ano}"  # Ex: "Janeiro 2025"
        dados.append({'data': nome_mes, 'valor': round(float(row[1]), 2)})
    
    # Completar os meses vazios com a função existente
    dados_completos = completa_anos_meses_simples(dados)
    
    return dados_completos

#?????
# def last_sold_products():
#     conn = conectar_db()
#     cursor = conn.cursor()
#     query = """ SELECT sold_products, COUNT(*) AS qnt_total_vendas
#     FROM customer
#     WHERE time_as_client >= CURDATE() - INTERVAL 15 DAY
#     GROUP BY customer_id
#     """
#     cursor.execute(query)
#     aumento_clientes = cursor.fetchall()
#     conn.close()
    
#     return aumento_clientes
