from flask import Blueprint, render_template
from Database.Queries.cliente import list_all_customers,customers_increase, qnt_all_customers
from Database.Queries.vendas_produto import show_highlight_products  

home = Blueprint("home", __name__)

#configurações das rotas

@home.route("/")
def home_page():
    
    return render_template("index.html")

    
    
@home.route("/dashboard")
def dashboard():
    produto_destaque = show_highlight_products()
    clientes_novos = len(customers_increase())
    clientes_totais = qnt_all_customers()
    porcentagem_clientes_novos = (clientes_novos / (clientes_totais-clientes_novos)) * 100
    
    return render_template("dashboard.html", produto_destaque=produto_destaque[0], clientes_novos=clientes_novos, porcentagem_clientes_novos=porcentagem_clientes_novos )
    #return str([clientes[0], customers,clientes_totais, porcentagem_clientes_novos ])


@home.route("/churn")
def churn():
    
    return render_template("churn.html")


@home.route("/rfm")
def rfm():
    
    return render_template("rfm.html")


@home.route("/sazonalidade")
def sazonalidade():
    
    return render_template("sazonalidade.html")

@home.route("/usuario")
def usuario():
    
    return render_template("usuario.html")