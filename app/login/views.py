from flask import session, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from app.decorators import admin_required, permission_required
from app import db
from datetime import datetime
from .forms import EditProfileForm, EditProfileAdminForm, RoleForm, ToPostForm
from app.models import User, Role, Article

from . import login

@login.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('login/profile.html', user=user)

@login.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('login/users.html', users=users)

@login.route('/roles', methods=['GET', 'POST'])
@login_required
@admin_required
def roles():
    form = RoleForm()
    roles = Role.query.all()
    if form.validate_on_submit():
        new_role = Role()
        perms = sum([int(permission) for permission in form.permissions.data])
        new_role.name = form.name.data
        new_role.permissions = perms
        db.session.add(new_role)
        db.session.commit()
        flash('Função cadastrada com sucesso.')
        return redirect(url_for('login.roles'))
    return render_template('login/roles.html', form=form, roles=roles)

@login.route('/topost', methods=['GET', 'POST'])
@login_required
def topost():
    if not(current_user.has_permission(4)):
        flash("Acesso não permitido")
        return redirect(url_for('main.index'))
    form = ToPostForm()
    if form.validate_on_submit():
         artigo = Article(
                title= form.title.data,
                date= datetime.now(),
         )
         db.session.add(artigo)
         db.session.commit()
         return redirect(url_for('login.articles'))
    return render_template('login/topost.html', form=form)


@login.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.name = form.username.data
        user.email = form.email.data
        if form.password.data is not None:
            user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Perfil editado com sucesso!')
        return redirect(url_for('.user', username=current_user.name))
    form.username.data = current_user.name
    form.email.data = current_user.email
    return render_template('login/editProfile.html', form=form, username=current_user.name)


@login.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.userRole = Role.query.get(form.role.data).id
        user.userStats = form.status.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário editado com sucesso!')
        return redirect(url_for('.user', username=user.name))
    form.role.data = user.userRole
    form.status.data = user.userStats
    return render_template('login/editProfile.html', form=form, username=user.name)

