from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, login_user, logout_user
from Database.Queries.cliente import list_all_clients,clients_increase, qnt_all_clients, increase_simbol
from Database.Queries.vendas_produto import show_highlight_products, monthly_sales_data, monthly_sales_volume, qnt_products_month, most_frequent_country, total_profit, top3_monthly_sales
from Database.Queries.usuario import get_user_info, get_all_customers, search_user_profile, get_all_customers_with_lucro_rfm_churn
from Database.Queries.empresa import company_data
from Database.Queries.login import find_by_email_password, User, load_user
from Database.Queries.rfm import type_and_qnt_perfil

home = Blueprint("home", __name__)

#configurações das rotas

@home.route("/")
def home_page():
    if logout_user() == True:
        return render_template("index.html")
    else:
        logout_user()
        return render_template("index.html")


@home.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home_page"))


@home.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        logout_user()
        return render_template('index.html')
    else: 
        email = request.form['emailFORM']
        senha = request.form['passwordFORM']
        user_data = find_by_email_password(email, senha)
        if user_data:
            user = User(
                id_inlytic_user=user_data['id_inlytic_user'],
                worker_name=user_data['worker_name'],
                worker_email=user_data['worker_email'],
                sector=user_data['sector'],
                photo_url=user_data['photo_url']
            )
            login_user(user)
            return redirect(url_for('home.dashboard'))
        else:
            return render_template('index.html', error=True)

# @home.route("/login", methods=["POST"])
# def login():
#     email = request.form['emailFORM']
#     senha = request.form['passwordFORM']
    
#     if find_by_email_password(email, senha):
#         return redirect(url_for('home.dashboard'))
#     else:
#         return render_template('index.html')
    

  
@home.route("/dashboard")
@login_required
def dashboard():
    nome_usuario, setor_usuario = get_user_info()
    produto_destaque = show_highlight_products()

    if produto_destaque and len(produto_destaque) > 0:
        produto_destaque = produto_destaque[0]
    else:
        produto_destaque = {}

    clientes_novos = len(clients_increase())
    clientes_totais = qnt_all_clients()
    empresa = company_data()
    dados_faturamento = monthly_sales_data()
    qnt_produtos = qnt_products_month()
    pais_destaque = most_frequent_country()
    lucro_total = total_profit()
    
    if ((clientes_totais - clientes_novos) == 0):
        porcentagem_clientes_novos = 100
    else:
        porcentagem_clientes_novos = (clientes_novos / (clientes_totais - clientes_novos)) * 100
    
    return render_template("dashboard.html", produto_destaque=produto_destaque, clientes_novos=clientes_novos, 
        porcentagem_clientes_novos=porcentagem_clientes_novos, nome_usuario=nome_usuario,
        setor_usuario=setor_usuario, empresa=empresa, dados_faturamento=dados_faturamento, qnt_produtos=qnt_produtos,pais_destaque=pais_destaque, lucro_total=lucro_total)

@home.route("/api/faturamento_mensal")
def faturamento_mensal():
    dados = monthly_sales_data()
    return jsonify(dados)


@home.route("/churn")
@login_required
def churn():
    nome_usuario, setor_usuario = get_user_info()
    empresa = company_data()
    empresa = company_data()
    
    return render_template("churn.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario, empresa=empresa)


@home.route("/rfm")
@login_required
def rfm():
    enterprise_id = 1
    empresa = company_data()
    nome_usuario, setor_usuario = get_user_info()
    quantidades_rfm = type_and_qnt_perfil(enterprise_id)
    qnt_total_clientes = qnt_all_clients()
    
    print(qnt_all_clients)
    return render_template("rfm.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario, quantidades_rfm=quantidades_rfm, qnt_total_clientes=qnt_total_clientes, empresa=empresa)



@home.route("/sazonalidade")
@login_required
def sazonalidade():
    empresa = company_data()
    nome_usuario, setor_usuario = get_user_info()

    return render_template("sazonalidade.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario, empresa=empresa)



@home.route("/usuario")
@login_required
def usuario():
    empresa = company_data()
    nome_usuario, setor_usuario = get_user_info()
    perfil = request.args.get('perfil')
    
    if perfil:
        clientes = search_user_profile(perfil)
    else:
        clientes = get_all_customers_with_lucro_rfm_churn()
        
    
    return render_template("usuario.html", nome_usuario=nome_usuario, setor_usuario=setor_usuario, clientes = clientes, empresa=empresa)


@home.route("/teste")
def grafico():
    grafico_volume = top3_monthly_sales()
    #resultado_final = format_data_for_chart(grafico_volume)
    grafico_faturamento = monthly_sales_data()
    return [grafico_volume]



        