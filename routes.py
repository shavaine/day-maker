from datetime import datetime
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from models import User, Task, Todo, Schedule, Template
from forms import LoginForm, RegisterForm, TaskForm, EditTaskForm, TemplateForm, TodoForm, ScheduleForm, EditTodoForm
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

@app.route('/delete_task/<task_title>')
@login_required
def delete_task(task_title):
    task = Task.query.filter_by(user_id=current_user.id, title=task_title).first()
    db.session.delete(task)
    db.session.commit()
    flash(f'Task: {task.title}, has been successfully deleted')
    return redirect(url_for('tasks'))     

@app.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
    form = TemplateForm()
    if form.validate_on_submit():
      template = Template(name=form.name.data, user_id=current_user.id)
      db.session.add(template)
      db.session.commit()
      flash('Template successfully added')
      return redirect(url_for('templates'))
    return render_template('my_templates.html', form=form)

@app.route('/view_template/<template>', methods=['GET', 'POST'])
@login_required
def view_template(template):
    current_template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    todos = Todo.query.filter_by(template_id=current_template.id).all()
    form = TodoForm()
    form.task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      todo = Todo(notes=form.notes.data, start_time=form.start_time.data, end_time=form.end_time.data, task_id=form.task.data, template_id=current_template.id)
      db.session.add(todo)
      db.session.commit()
      flash('Todo successfully added')
      return redirect(url_for('view_template', template=template))
    return render_template('view_template.html', template=current_template, form=form, todos=todos)

@app.route('/edit_todo/<template>/<todo>/<todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo, template, todo_id):
    current_template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    old = Todo.query.filter_by(id=todo_id, template_id=current_template.id).first()
    form = EditTodoForm(obj=old, new_notes=old.notes, new_start_time=old.start_time, new_end_time=old.end_time, new_task=old.task_id)
    form.new_task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      todo = Todo.query.filter_by(id=todo_id, template_id=current_template.id).first()
      todo.notes = form.new_notes.data
      todo.start_time = form.new_start_time.data
      todo.end_time = form.new_end_time.data
      todo.task_id = form.new_task.data
      db.session.commit()
      flash('Todo successfully updated')
      return redirect(url_for('view_template', template=current_template.name))
    return render_template('edit_todo.html', todo=todo, todo_id=todo_id, template=template, form=form)

@app.route('/create_schedule', methods=['GET', 'POST'])
@login_required
def create_schedule():
    form = ScheduleForm()
    form.template.choices = [(template.id, template.name) for template in Template.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      schedule = Schedule(date=form.date.data, template_id=form.template.data, user_id=current_user.id)
      db.session.add(schedule)
      db.session.commit()
      flash('Schedule successfully created')
      return redirect(url_for('dashboard'))
    return render_template('create_schedule.html', form=form)

@app.route('/schedule')
@login_required
def schedule():
    schedule = Schedule.query.filter_by(date=datetime.today().strftime("%Y-%m-%d"), user_id=current_user.id).first()
    if schedule is None:
      flash('No Schedule set for today')
      return redirect(url_for('dashboard'))
    current_template = Template.query.filter_by(id=schedule.template_id).first()
    todos = Todo.query.filter_by(template_id=current_template.id).all()
    return render_template('todays_schedule.html', todos=todos , template=current_template.name)