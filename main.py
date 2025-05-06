from flask import Flask, render_template
from Dataset.db.conexao_bd import conn
from Dataset.db import services


app = Flask(__name__)

@app.route("/")
def home():
    customers = services.list_all_customers()
    return str(customers)


if __name__ == "__main__":
    app.run(debug=True)