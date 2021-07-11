from sqlalchemy.orm import backref
from app import  db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, index = True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    schedules = db.relationship('Schedule', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')
    templates = db.relationship('Template', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')
    tasks = db.relationship('Task', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    todos = db.relationship('Todo', lazy='dynamic', cascade='all, delete, delete-orphan')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notes = db.Column(db.String(200))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    task = db.relationship('Task')

class Template(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), index=True)
    todos = db.relationship('Todo', backref='template', lazy='dynamic', cascade='all, delete, delete-orphan')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))