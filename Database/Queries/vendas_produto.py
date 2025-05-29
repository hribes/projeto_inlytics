from Database.conexao_bd import conectar_db
from datetime import date, timedelta, datetime

quinze_dias = date.today() - timedelta(days=15)
#print (quinze_dias)

#Produto em destaque
def show_highlight_products():
    conn = conectar_db()
    cursor = conn.cursor()

    query = """SELECT product_desc, COUNT(*) AS quantidade_vendida
               FROM sold_products 
               WHERE invoice_date >= '2011-12-01'
               GROUP BY stock_code, product_desc
               ORDER BY quantidade_vendida DESC
               LIMIT 1"""
       
    cursor.execute(query)
    resultado = cursor.fetchall()  # lista de dicts

    conn.close()
    
    if resultado:
        return resultado  # retorna lista com 1 dict
    else:
        # retorna lista com 1 dict indicando "nenhum produto"
        return [{'product_desc': 'Nenhum produto vendido', 'quantidade_vendida': 0}]




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
    
    meses = {
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
        '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
    }
    
    dados = []
    for row in resultado:
        ano_mes = row['mes']  # usa chave 'mes'
        faturamento = row['faturamento_total']  # usa chave do alias do SELECT
        ano, mes = ano_mes.split('-')
        nome_mes = f"{meses[mes]} {ano}"
        dados.append({'data': nome_mes, 'valor': round(float(faturamento), 2)})
    
    dados_completos = completa_anos_meses_simples(dados)
    
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
    
    meses = {
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
        '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
    }
    
    dados = []
    for row in resultado:
        ano_mes = row[0]  # 'YYYY-MM'
        total_vendas = row[1]
        ano, mes = ano_mes.split('-')
        nome_mes = f"{meses[mes]} {ano}"  # Exemplo: "Jan 2025"
        dados.append({'data': nome_mes, 'valor': int(total_vendas)})
    
    dados_completos = completa_anos_meses_simples(dados)
    
    return dados_completos




def qnt_products_month():
    conn = conectar_db()
    cursor = conn.cursor()
    
    
    query = """
    SELECT 
    DATE_FORMAT(invoice_date, '%Y-%m') AS mes,
    SUM(quantity) AS qnt_produtos
    FROM sold_products
    WHERE invoice_date BETWEEN '2011-12-01' AND '2011-12-31'
    GROUP BY mes
    ORDER BY mes;
    """
    cursor.execute(query)
    qnt_total_produtos = cursor.fetchall()
    cursor.close()
    conn.close()

    if qnt_total_produtos and qnt_total_produtos[0]['qnt_produtos'] is not None:
        return int(qnt_total_produtos[0]['qnt_produtos'])
    else:
        return 0

#Puxa o país que mais comprou
def most_frequent_country():
    
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
    SELECT country, COUNT(*) AS most_freq
    FROM sold_products
    GROUP BY country
    ORDER BY most_freq DESC
    LIMIT 1"""

    cursor.execute(query)
    countries = cursor.fetchall()

    cursor.close()
    conn.close()

    return countries[0]['country']

def total_profit():
    conn = conectar_db()
    cursor = conn.cursor()

    #year = datetime.datetime.today().year
    year = 2011

    query = f"""
    SELECT SUM(product_price) AS total_profit
    FROM sold_products
    WHERE YEAR(invoice_date) = {year}"""

    cursor.execute(query)
    profit = cursor.fetchone()['total_profit']
    form = lambda num: f"{num:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

    return f'R$ {form(profit)}'

# def qnt_products_month():
#     conn = conectar_db()
#     cursor = conn.cursor()
    
#     query = """SELECT SUM(quantity) AS qnt_produtos
#     FROM sold_products
#     WHERE invoice_date >= CURDATE() - INTERVAL 30 DAY;
#     """
#     cursor.execute(query)
#     qnt_total_produtos = cursor.fetchall()
#     cursor.close()
    
    
#     if qnt_total_produtos and qnt_total_produtos[0][0] is not None:
#         return int(qnt_total_produtos[0][0])
#     else:
#         return 0


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



# def monthly_sales_data():
#     conn = conectar_db()
#     cursor = conn.cursor()
    
#     query = """
#         SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
#                SUM(product_price) AS faturamento_total
#         FROM sold_products
#         GROUP BY mes
#         ORDER BY mes;
#     """
    
#     cursor.execute(query)
#     resultado = cursor.fetchall()
#     conn.close()
    
#     meses = {
#         '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
#         '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
#         '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
#     }
    
#     dados = []
#     for row in resultado:
#         ano_mes = row[0]  # 'YYYY-MM'
#         faturamento = row[1]
#         ano, mes = ano_mes.split('-')
#         nome_mes = f"{meses[mes]} {ano}"  # Ex: "Jan 2025"
#         dados.append({'data': nome_mes, 'valor': round(float(faturamento), 2)})
    
#     dados_completos = completa_anos_meses_simples(dados)
    
#     return dados_completos




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
    
#     # Dicionário para mapear números dos meses para nomes em português
#     meses = {
#         '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
#         '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
#         '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
#     }
    
#     # Converter os dados brutos e incluir nomes dos meses
#     dados = []
#     for row in resultado:
#         ano_mes = row[0]  # Formato 'YYYY-MM'
#         ano, mes = ano_mes.split('-')
#         nome_mes = f"{meses[mes]} {ano}"  # Ex: "Janeiro 2025"
#         dados.append({'data': nome_mes, 'valor': round(float(row[1]), 2)})
    
#     # Completar os meses vazios com a função existente
#     dados_completos = completa_anos_meses_simples(dados)
    
#     return dados_completos




# def monthly_sales_volume():
#     conn = conectar_db()
#     cursor = conn.cursor()
    
#     query = """
#         SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS mes, 
#         SUM(quantity) AS total_vendas
#         FROM sold_products
#         GROUP BY mes
#         ORDER BY mes;
#     """
    
#     cursor.execute(query)
#     resultado = cursor.fetchall()
#     conn.close()
    
#     # dados = lista de tuplas (mes, total de vendas)
#     dados = [(row[0], int(row[1])) for row in resultado]
    
#     # Completa meses/anos faltantes
#     dados_completos = completa_anos_meses_simples(dados)
    
#     print("QUANTIDADE DE VENDAS POR MÊS - GRÁFICO")
#     print(dados_completos)
    
#     return dados_completos
