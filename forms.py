from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime

class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")

class RegisterForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  password_repeat = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
  email = StringField("Email", validators=[DataRequired(), Email()])
  submit = SubmitField("Register")

class TaskForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  submit = SubmitField("Create Task")

class EditTaskForm(FlaskForm):
  id = HiddenField('id')
  new_title = StringField("Change Title:", validators=[DataRequired()])
  submit = SubmitField('Submit')

class TemplateForm(FlaskForm):
  name = StringField("Template Name", validators=[DataRequired()])
  submit = SubmitField("Create Template")

class TodoForm(FlaskForm):
  notes = TextAreaField("Notes")
  start_time = TimeField("Start Time", validators=[DataRequired()])
  end_time = TimeField("End Time", validators=[DataRequired()])
  task = SelectField(u"Pick Task", coerce=int)
  submit = SubmitField("Add Todo")

class ScheduleForm(FlaskForm):
  date = DateField("Select Date", validators=[DataRequired()], format='%Y-%m-%d', default=datetime.now())
  template = SelectField(u"Pick Template", coerce=int)
  submit = SubmitField("Create Schedule")

class EditScheduleForm(FlaskForm):
  id = HiddenField('id')
  new_date = DateField("Select Date", validators=[DataRequired()], format='%Y-%m-%d', default=datetime.now())
  new_template = SelectField(u"Pick Template", coerce=int)
  submit = SubmitField("Submit Changes")

class EditTodoForm(FlaskForm):
  id = HiddenField('id')
  new_notes = TextAreaField("Notes")
  new_start_time = TimeField("Start Time", validators=[DataRequired()])
  new_end_time = TimeField("End Time", validators=[DataRequired()])
  new_task = SelectField(u"Change Task", coerce=int)
  submit = SubmitField("Submit Changes")