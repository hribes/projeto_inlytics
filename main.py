from flask import Flask, render_template
from Routes.api import home


app = Flask(__name__)
app.register_blueprint(home)


if __name__ == "__main__":
    app.run(debug=True)