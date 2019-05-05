from flask import session, redirect, url_for, flash, render_template
from . import main
from .forms import NameForm

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login')
def login():
    if session.get('user') is not None:
        return redirect(url_for('index'))
    return render_template('login.html')

@main.route('/admin')
def admin():
    return render_template('index.html')