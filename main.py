from flask import Flask, render_template
from Routes.api import home
from flask_login import LoginManager
from Database.Queries.login import User, find_user_by_id

app = Flask(__name__)
app.register_blueprint(home)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.home_page'

@login_manager.user_loader
def load_user(user_id):
    user_data = find_user_by_id(user_id)
    if user_data:
        return User(
            id_inlytic_user=user_data['id_inlytic_user'],
            worker_name=user_data['worker_name'],
            worker_email=user_data['worker_email'],
            sector=user_data['sector'],
            photo_url=user_data['photo_url']
        )
    return None

if __name__ == "__main__":
    app.run(debug=True)
