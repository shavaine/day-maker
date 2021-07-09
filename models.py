from app import  db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, index = True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notes = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))

class Template(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    date = db.Column(db.DateTime, index = True)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))