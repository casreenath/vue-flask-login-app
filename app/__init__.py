from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['LDAP_PROVIDER_URL'] = 'ldap://ldap-master.certesnetworks.com:389/'
    db.init_app(app)
    from .views import main as main_bp
    app.register_blueprint(main_bp)
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    logging.basicConfig(level=logging.DEBUG, filename='app.log',
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    CORS(app)
    # db.create_all()
    return app
