from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app.models import User, Role
from app import db

from . import auth
from .forms import LoginForm, RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name='READER').first()
        user = User(name=form.username.data, password=form.password.data, email=form.email.data, userStats='A',
                    userRole=role.id)
        db.session.add(user)
        db.session.commit()
        flash('Usuário registrado com sucesso')
        return redirect(url_for('auth.login'))
    return render_template('auth/cadastro.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.userStats == "A":
                login_user(user)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Usuário Inativo !!')
        flash('Usuário ou senha inválidos !! ')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout feito com sucesso !! ')
    return redirect(url_for('main.index'))