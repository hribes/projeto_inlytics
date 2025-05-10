from flask import Flask, render_template
import Database 


app = Flask(__name__)

@app.route("/")
def home():
    customers = Database.list_all_customers()
    return str(customers)


if __name__ == "__main__":
    app.run(debug=True)