from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SUPER_SECRET') or 'brownie101'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace("://", "ql://", 1) or 'sqlite:///dayMaker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# attach to DATABASE_URL for production
# .replace("://", "ql://", 1)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import routes, models
 