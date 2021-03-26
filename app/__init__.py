from flask import (
    Flask,
)
from flask_sqlalchemy import SQLAlchemy
from app.config import SECRET_KEY

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from app import routes
