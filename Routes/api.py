from flask import Blueprint, render_template
from Database.Queries.cliente import list_all_customers,customers_increase, qnt_all_customers
from Database.Queries.vendas_produto import show_highlight_products  

home = Blueprint("home", __name__)

#configurações das rotas


@home.route("/")
def exibir_clientes():
    produto_destaque = show_highlight_products()
    clientes = len(customers_increase())
    clientes_totais = qnt_all_customers()
    porcentagem_clientes_novos = (clientes / (clientes_totais-clientes)) * 100
    
    return render_template("rfm.html", produto_destaque=produto_destaque[0], clientes=clientes, porcentagem_clientes_novos=porcentagem_clientes_novos )
    #return str([clientes[0], customers,clientes_totais, porcentagem_clientes_novos ])


