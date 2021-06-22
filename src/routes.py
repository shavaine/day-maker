from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from models import User, Task, Todo, Schedule, Template
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
def home():
    return render_template('home.html')