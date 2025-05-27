from Database.conexao_bd import conectar_db
from datetime import date, timedelta

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
    anos = set()
    for mes_ano, total in dados:
        ano = mes_ano.split('-')[0]
        anos.add(ano)
    
    anos = sorted(list(anos))
    
    dict_dados = {}
    for mes_ano, total in dados:
        dict_dados[mes_ano] = total
    
    resultado = []
    for ano in anos:
        for mes in range(1, 13):
            mes_str = str(mes).zfill(2)
            chave = f"{ano}-{mes_str}"
            total = dict_dados.get(chave, 0)
            resultado.append({"data": chave, "valor": total})
    
    return resultado



def monthly_sales_data():
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
        SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
        SUM(quantity * product_price) AS faturamento_total
        FROM sold_products
        GROUP BY mes
        ORDER BY mes;
    """
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    
    # dados = lista de tuplas (mes, total)
    dados = [(row[0], round(float(row[1]), 2)) for row in resultado]
    
    # Completa meses/anos faltantes
    dados_completos = completa_anos_meses_simples(dados)
    
    print("FATURAMENTO DO PRODUTOS POR MES - GRAFICO")
    print(dados_completos)
    
    return dados_completos

def monthly_sales_volume():
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
        SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
        SUM(quantity) AS total_vendas
        FROM sold_products
        GROUP BY mes
        ORDER BY mes;
    """
    
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    
    # dados = lista de tuplas (mes, total de vendas)
    dados = [(row[0], int(row[1])) for row in resultado]
    
    # Completa meses/anos faltantes
    dados_completos = completa_anos_meses_simples(dados)
    
    print("QUANTIDADE DE VENDAS POR MÊS - GRÁFICO")
    print(dados_completos)
    
    return dados_completos

def qnt_products_month():
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """SELECT SUM(quantity) AS qnt_produtos
    FROM sold_products
    WHERE invoice_date >= CURDATE() - INTERVAL 30 DAY;
    """
    cursor.execute(query)
    qnt_total_produtos = cursor.fetchall()
    cursor.close()
    
    
    if qnt_total_produtos and qnt_total_produtos[0][0] is not None:
        return int(qnt_total_produtos[0][0])
    else:
        return 0


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
