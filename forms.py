from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")

class RegisterForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  password_repeat = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
  email = StringField("Email", validators=[DataRequired(), Email()])
  submit = SubmitField("Register")

class TaskForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  submit = SubmitField("Create Task")

class EditTaskForm(FlaskForm):
  id = HiddenField('id')
  new_title = StringField("Edited Title", validators=[DataRequired()])
  submit = SubmitField('Submit Changes')