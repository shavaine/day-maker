from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brownie101'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlight:///dayMakerDB.db'
app.config["SQLALCHEMY_TRACK_MODIFICAITONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import routes, models
 