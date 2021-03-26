from flask import (
    Flask,
)
from flask_sqlalchemy import SQLAlchemy
from app.config import SECRET_KEY
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message_category = 'info'

from app import routes
