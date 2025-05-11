from flask import Blueprint, render_template
from Database.Queries.cliente import list_all_customers,customers_increase, qnt_all_customers
from Database.Queries.vendas_produto import show_highlight_products  

clientes = Blueprint("clientes", __name__)

#configurações das rotas
@clientes.route("/")
def exibir_clientes():
    clientes = show_highlight_products()
    customers = len(customers_increase())
    clientes_totais = qnt_all_customers()
    porcentagem_clientes_novos = (customers / (clientes_totais-customers)) * 100
    
    return str([clientes[0], customers,clientes_totais, porcentagem_clientes_novos ])


