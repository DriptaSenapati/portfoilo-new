from flask import Flask
#import secrets
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
# login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfoliodata.db'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    #app.config['SESSION_COOKIE_SECURE'] = True
    db.init_app(app)
    login_manager.init_app(app)

    from portfolio.routes import main
    app.register_blueprint(main, url_prefix='/')

    @app.template_filter('autoversion')
    def autoversion_filter(filename):
        fullpath = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), filename[1:])
        try:
            timestamp = str(os.path.getmtime(fullpath))
        except OSError:
            return filename
        newfilename = "{0}?v={1}".format(filename, timestamp)
        return newfilename

    return app
