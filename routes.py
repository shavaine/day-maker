from datetime import datetime
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from models import User, Task, Todo, Schedule, Template
from forms import LoginForm, RegisterForm, TaskForm, EditTaskForm, TemplateForm, TodoForm, ScheduleForm, EditTodoForm, EditScheduleForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import json

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
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    schedules_list = [{'title': Template.query.filter_by(id=schedule.template_id).first().name, 'start': str(schedule.date), 'url': url_for('day_view', schedule=schedule.id, template=Template.query.filter_by(id=schedule.template_id).first().name)} for schedule in schedules]
    return render_template('calendar.html', date=datetime.today(), schedules=json.dumps([schedule for schedule in schedules_list]))

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    EditForm = EditTaskForm()
    if form.validate_on_submit():
      task = Task(title=form.title.data, user_id=current_user.id)
      db.session.add(task)
      db.session.commit()
      flash('Task successfully added')
      return redirect(url_for('tasks'))
    return render_template('view_tasks.html', form=form, EditForm=EditForm)

@app.route('/edit_task/<task_title>', methods=['GET', 'POST'])
@login_required
def edit_task(task_title):
    EditForm = EditTaskForm()
    if EditForm.validate_on_submit():
      task = Task.query.filter_by(user_id=current_user.id, title=task_title).first()
      task.title = EditForm.new_title.data
      db.session.commit()
      flash('Title successfully Changed')
      return redirect(url_for('tasks'))
    return render_template('edit_task.html', Edit=EditForm, task_title=task_title)

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
    return render_template('templates.html', form=form)

@app.route('/view_template/<template>')
@login_required
def view_template(template):
    current_template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    todos = Todo.query.filter_by(template_id=current_template.id).all()
    EditForm = EditTodoForm()
    EditForm.new_task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    AddForm = TodoForm()
    AddForm.task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    return render_template('view_template.html', template=template, todos=todos, AddForm=AddForm, EditTodoForm=EditForm)

@app.route('/add_todo/<template>', methods=['POST'])
@login_required
def add_todo(template):
    current_template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    form = TodoForm()
    form.task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      todo = Todo(notes=form.notes.data, start_time=form.start_time.data, end_time=form.end_time.data, task_id=form.task.data, template_id=current_template.id)
      db.session.add(todo)
      db.session.commit()
      flash('Todo successfully added')
      return redirect(url_for('view_template', template=template))

@app.route('/delete_template/<template>')
@login_required
def delete_template(template):
    template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    db.session.delete(template)
    db.session.commit()
    flash('Template successfully deleted')
    return redirect(url_for('templates'))

@app.route('/edit_todo/<template>/<todo_id>', methods=['POST'])
@login_required
def edit_todo( template, todo_id):
    current_template = Template.query.filter_by(user_id=current_user.id, name=template).first()
    form = EditTodoForm()
    form.new_task.choices = [(task.id, task.title) for task in Task.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      todo = Todo.query.filter_by(id=todo_id, template_id=current_template.id).first()
      todo.notes = form.new_notes.data
      todo.start_time = form.new_start_time.data
      todo.end_time = form.new_end_time.data
      todo.task_id = form.new_task.data
      db.session.commit()
      flash('Todo successfully updated')
      return redirect(url_for('view_template', template=current_template.name,))
    else:
      flash(form.errors)
      return redirect(url_for('view_template', template=template))

@app.route('/create_schedule', methods=['POST'])
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

@app.route('/edit_schedule/<schedule>', methods=['POST'])
@login_required
def edit_schedule(schedule):
    form = EditScheduleForm()
    form.new_template.choices = [(template.id, template.name) for template in Template.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
      schedule = Schedule.query.get(int(schedule))
      schedule.date = form.new_date.data
      schedule.template_id = form.new_template.data
      db.session.commit()
      flash('Schedule successfully changed')
      return redirect(url_for('dashboard'))


@app.route('/delete_schedule/<schedule>')
@login_required
def delete_schedule(schedule):
    schedule = Schedule.query.filter_by(user_id=current_user.id, id=schedule).first()
    db.session.delete(schedule)
    db.session.commit()
    flash('Schedule successfully deleted')
    return redirect(url_for('dashboard'))

@app.route('/schedule')
@login_required
def schedule():
    form = ScheduleForm()
    form.template.choices = [(template.id, template.name) for template in Template.query.filter_by(user_id=current_user.id).all()]
    schedule = Schedule.query.filter_by(date=datetime.today().strftime("%Y-%m-%d"), user_id=current_user.id).first()
    if schedule is None:
      todos = []
      schedule = Schedule(date=datetime.today().strftime("%Y-%m-%d"), template_id=1, user_id=current_user.id, id=1)
      schedules_list = []
      deletable = False
    else:
      deletable = True
      current_template = Template.query.filter_by(id=schedule.template_id).first()
      todos = Todo.query.filter_by(template_id=schedule.template_id).all()
      schedules_list = [{'title': todo.task.title, 'start': str(schedule.date)+'T'+str(todo.start_time), 'end': str(schedule.date)+'T'+str(todo.end_time), 'url': url_for('day_view', schedule=schedule.id, template=Template.query.filter_by(id=schedule.template_id).first().name)} for todo in todos]
    return render_template('todays_schedule.html', date=schedule.date, schedules=json.dumps([schedule for schedule in schedules_list]), todos=todos, form=form, schedule=schedule.id, deletable=deletable)

@app.route('/day_view/<schedule>')
@login_required
def day_view(schedule):
    form = EditScheduleForm()
    form.new_template.choices = [(template.id, template.name) for template in Template.query.filter_by(user_id=current_user.id).all()]
    current_schedule = Schedule.query.filter_by(user_id=current_user.id, id=schedule).first()
    todos = Todo.query.filter_by(template_id=current_schedule.template_id).all()
    schedules_list = [{'title': todo.task.title, 'start': str(current_schedule.date)+'T'+str(todo.start_time), 'end': str(current_schedule.date)+'T'+str(todo.end_time), 'url': url_for('day_view', schedule=current_schedule.id, template=Template.query.filter_by(id=current_schedule.template_id).first().name)} for todo in todos]
    return render_template('day_view.html', date=current_schedule.date, schedules=json.dumps([schedule for schedule in schedules_list]), todos=todos, form=form, schedule=current_schedule.id)