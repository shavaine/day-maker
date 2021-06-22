from app import  db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, index = True)
    password = db.Column(db.String(128))

    def set_passsword(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True)

class Todo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notes = db.Column(db.String(200))
    start_time = db.Column(db.Datetime)
    end_time = db.Column(db.Datetime)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))

class Template(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))

class Schedule(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    date = db.Column(db.Datetime, index = True)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))