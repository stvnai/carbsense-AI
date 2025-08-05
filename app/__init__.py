import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import User
from .db.user_queries import get_user_by_id
from flask import redirect, url_for


token= os.getenv("SECRET_KEY")
login_manager= LoginManager()
csrf= CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.secret_key= token
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes import main

    app.register_blueprint(main)
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(user_data[0], user_data[1])
        return None
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("main.login"))
    

    return app

