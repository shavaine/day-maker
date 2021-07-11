from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from models import User, Task, Todo, Schedule, Template
from forms import LoginForm, RegisterForm, TaskForm, EditTaskForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
        flash('Incorrect username or password')
        return redirect(url_for('login'))
      login_user(user)
      next_page = request.args.get('next')
      if not next_page or url_parse(next_page) != '':
        next_page = url_for('dashboard')
      return redirect(next_page)
    return render_template('login.html', LoginForm=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
      new_user = User(username=form.username.data, email=form.email.data)
      new_user.set_password(form.password.data)
      db.session.add(new_user)
      db.session.commit()
      flash('Registration successful!')
      return redirect(url_for('login'))
    return render_template('register.html', RegisterForm=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
      task = Task(title=form.title.data, user_id=current_user.id)
      db.session.add(task)
      db.session.commit()
      flash('Title successfully added')
      return redirect(url_for('tasks'))
    return render_template('view_tasks.html', form=form)

@app.route('/edit_task/<task_title>', methods=['GET', 'POST'])
@login_required
def edit_task(task_title):
    form = EditTaskForm()
    if form.validate_on_submit():
      task = Task.query.filter_by(user_id=current_user.id, title=task_title).first()
      task.title = form.new_title.data
      db.session.commit()
      flash('Title successfully Changed')
      return redirect(url_for('tasks'))
    return render_template('edit_task.html', form=form, task_title=task_title)