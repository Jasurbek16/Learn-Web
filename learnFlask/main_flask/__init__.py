from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app = Flask(__name__)
# we instanciated the flask app in the "app" variable
# setting up a secret key
app.config["SECRET_KEY"] = 'c647aaa08100111e2cf2b392828dbc0f'
# ^ .config -- the configuration dictionary
# ^ could be set as an env var
# ^ The secret key is needed to keep the client-side sessions secure. You can generate some random key
# ^ # ! we need to put a secret key for our application --> protects modifying cookies, avoid forgery attacks
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
# /// are relative paths from the current file via sqlite
db = SQLAlchemy(app)
# ^ setting an instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# ^ setting the login route   ^ func name of our route like with url_for
login_manager.login_message_category = 'info'
# ^ adding a category for msgs

from main_flask import routes