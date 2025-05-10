from flask import Blueprint, render_template
from Database.Queries.cliente import list_all_customers

clientes = Blueprint("clientes", __name__)


#configurações das rotas
@clientes.route("/")
def exibir_clientes():
    clientes = list_all_customers()
    return str(clientes)
