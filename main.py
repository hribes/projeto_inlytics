from flask import Flask, render_template
from Routes.api import clientes


app = Flask(__name__)
app.register_blueprint(clientes)


if __name__ == "__main__":
    app.run(debug=True)