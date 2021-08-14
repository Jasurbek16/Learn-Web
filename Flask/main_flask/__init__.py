from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from main_flask.config import Config


# setting up a secret key

db = SQLAlchemy()
# ^ setting an instance
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# ^ setting the login route   ^ func name of our route like with url_for
login_manager.login_message_category = 'info'
# ^ adding a category for msgs

# app.config['MAIL_DEFAULT_SENDER'] = 'demo@sender.com'
# # ^ adds the sender as 'from' for each email 
# app.config['MAIL_MAX_EMAILS'] = os.environ.get('EMAIL_PASS')
# # prevent too many sending of mails
# app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('EMAIL_PASS')

# app.config['MAIL_ASCII_ATTACHMENTS'] = os.environ.get('EMAIL_PASS')

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from main_flask.users.routes import users
    from main_flask.posts.routes import posts
    from main_flask.main.routes import main
    from main_flask.errors.handlers import errors
    # registering imported blueprint 
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app