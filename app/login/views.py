from flask import session, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from app.decorators import admin_required, permission_required
from app import db
from .forms import EditProfileForm, EditProfileAdminForm, RoleForm, ToPostForm, EditPost
from app.models import User, Role, Article, Follow, Permission
import os
from . import login

@login.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    following = len(user.followed.all())
    followers = len(user.followers.all())
    return render_template('login/profile.html', user=user, followers=followers, following=following)

@login.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    usersPagination = db.session.query(User, Role).join(Role, User.userRole == Role.id).paginate(
        page, per_page=10, error_out=False
    )
    users = usersPagination.items
    return render_template('login/users.html', users=users, pagination=usersPagination)

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
@permission_required(Permission.WRITE)
def topost():
    if not(current_user.has_permission(4)):
        flash("Acesso não permitido")
        return redirect(url_for('main.index'))
    form = ToPostForm()
    if form.validate_on_submit():
        file = form.image.data
        imageName = str(hash(file.filename[:-4])) + file.filename[-4::]
        file.save(os.path.join('app/static/images/', imageName))
        article = Article(
            title=form.title.data,
            image=imageName,
            subtitle=form.subtitle.data,
            lide=form.lide.data,
            text=form.text.data,
            author=current_user.id,
            category=form.categories.data
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('login.articles'))
    return render_template('login/topost.html', form=form, nome='Escrever Artigo')


@login.route('/articles/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE)
def editArticle(id):
    article = Article.query.filter_by(id=id).first()
    form = EditPost()
    if form.validate_on_submit():
        if form.image.data.filename != article.image and not(form.image.data.filename == ''):
            file = form.image.data
            imageName = str(hash(file.filename[:-4])) + file.filename[-4::]
            file.save(os.path.join('app/static/images/', imageName))
            article.image = imageName
        article.subtitle = form.subtitle.data
        article.title = form.title.data
        article.lide = form.lide.data
        article.category = form.categories.data
        article.text = form.text.data
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('login.articles'))
    form.title.data = article.title
    form.lide.data = article.lide
    form.subtitle.data = article.subtitle
    form.text.data = article.text
    return render_template("login/topost.html", form=form, nome='Editar Artigo - %s'%article.title)


@login.route('/articles', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE)
def articles():
    page = request.args.get('page', 1, type=int)
    articlesPagination = db.session.query(User.name, Article.id, Article.title, Article.date).join(
        Article, User.id == Article.author
    ).paginate(
        page, per_page=5, error_out=False
    )
    articles = articlesPagination.items

    return render_template('login/articles.html', articles=articles, pagination=articlesPagination)


@login.route('/following/<name>', methods=['GET', 'POST'])
@login_required
def following(name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('User inválid')
        return redirect(url_for('login.profile', name=current_user.name))
    followersPagination = user.followed.paginate(
        page, per_page=10, error_out=False
    )
    followers = followersPagination.items
    userFollowers = [User.query.filter_by(id=user.followed_id).first() for user in followers]
    return render_template('login/follow.html', users=userFollowers, titulo='Following', pagination=followersPagination, name=name)

@login.route('/followers/<name>', methods=['GET', 'POST'])
@login_required
def followers(name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('User inválid')
        return redirect(url_for('login.profile', name=current_user.name))
    followingPagination = user.followers.paginate(
        page, per_page=10, error_out=False
    )
    following = followingPagination.items
    userFollowing = [User.query.filter_by(id=user.follower_id).first() for user in following]
    return render_template('login/follow.html', users=userFollowing, titulo='Followers', pagination=followingPagination, name=name)


@login.route('/follow/<name>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def follow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid User')
        return redirect(url_for('login.user', name=current_user.name))
    if current_user.is_following(user):
        flash('Você já está seguindo esse usuário')
        return redirect(url_for('.user', name=name))
    current_user.follow(user)
    flash('Agora você já está seguindo esse usuário')
    return redirect(url_for('.user', name=user.name))


@login.route('/unfollow/<name>', methods=['GET', 'POST'])
@login_required
def unfollow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid User !')
        return redirect(url_for('login.user', name=current_user.name))
    if not current_user.is_following(user):
        flash('Você ainda não segue esse usuário !')
        return redirect(url_for('.user', name=current_user.name))
    current_user.unfollow(user)
    flash('Agora você já não segue mais esse usuário !')
    return redirect(url_for('.user', name=name))


@login.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        if form.avatar.data.filename != user.avatar and not(form.avatar.data.filename == ''):
            file = form.avatar.data
            avatarName = str(hash(file.filename[:-4])) + file.filename[-4::]
            file.save(os.path.join('app/static/images/', avatarName))
            user.avatar = avatarName
        user.about_me = form.about_me.data
        user.name = form.username.data
        user.email = form.email.data
        print(form.password.data)
        if form.password.data != '':
            input("Erro na senha !!")
            user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Perfil editado com sucesso!')
        return redirect(url_for('.user', name=current_user.name))
    form.username.data = current_user.name
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me
    return render_template('login/editProfile.html', form=form, name=current_user.name)


@login.route('/edit-profile/<int:idUser>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(idUser):
    user = User.query.get_or_404(idUser)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.userRole = Role.query.get(form.role.data).id
        user.userStats = form.status.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário editado com sucesso!')
        return redirect(url_for('.user', name=user.name))
    form.role.data = user.userRole
    form.status.data = user.userStats
    return render_template('login/editProfile.html', form=form, name=user.name)

