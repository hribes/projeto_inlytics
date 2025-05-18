from flask import Blueprint, render_template
from Database.Queries.cliente import list_all_clients,clients_increase, qnt_all_clients
from Database.Queries.vendas_produto import show_highlight_products  
from Database.Queries.usuario import get_user_info
from Database.Queries.empresa import company_data

home = Blueprint("home", __name__)

#configurações das rotas

@home.route("/")
def home_page():
    
    return render_template("index.html")

  
    
@home.route("/dashboard")
def dashboard():
    nome_usuario, setor_usuario = get_user_info()
    produto_destaque = show_highlight_products()
    clientes_novos = len(clients_increase())
    clientes_totais = qnt_all_clients()
    empresa = company_data()
    
    if ((clientes_totais - clientes_novos) == 0):
        porcentagem_clientes_novos = 100
    else:
        porcentagem_clientes_novos = (clientes_novos / (clientes_totais-clientes_novos)) * 100
    
    return render_template("dashboard.html", produto_destaque=produto_destaque[0], clientes_novos=clientes_novos, porcentagem_clientes_novos=porcentagem_clientes_novos,nome_usuario=nome_usuario, setor_usuario=setor_usuario, empresa=empresa )
    #return str([clientes[0], customers,clientes_totais, porcentagem_clientes_novos ])



@home.route("/churn")
def churn():
    nome_usuario, setor_usuario = get_user_info()
    
    return render_template("churn.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario)



@home.route("/rfm")
def rfm():
    nome_usuario, setor_usuario = get_user_info()
    
    return render_template("rfm.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario)



@home.route("/sazonalidade")
def sazonalidade():
    nome_usuario, setor_usuario = get_user_info()

    return render_template("sazonalidade.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario)



@home.route("/usuario")
def usuario():
    nome_usuario, setor_usuario = get_user_info()
    
    return render_template("usuario.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario)