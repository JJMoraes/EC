from flask import session, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from app import db
from .forms import SearchForm
from app.models import Article, User, Category, Permission

from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    principais = db.session.query(Article, User, Category).join(User, Article.author == User.id).join(Category, Category.id == Article.category).order_by(Article.date.desc()).all()
    sections = {'Principais':principais[:4]}
    for section in principais:
        if section[2].name in list(sections.keys()):
            sections[section[2].name].append(section)
        else:
            sections[section[2].name] = [section]
    return render_template('index.html', sections=sections)

@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        datas = request.form
        articlesPagination = db.session.query(Article.title, Article.image, Article.date, Article.subtitle, User.name).join(
            User, Article.author == User.id
        ).filter(
            Article.text.like('%{}%'.format(datas['textSearch']))
        ).paginate(
            page, per_page=5, error_out=False
        )
        posts = articlesPagination.items
    return render_template('searchPage.html', posts=posts, search=datas['textSearch'], pagination=articlesPagination)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template('contact.html', mensagem=True)

    return render_template('contact.html', mensagem=False)

@main.route('/categories/<categoryName>', methods=['GET', 'POST'])
def categories(categoryName):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(name=categoryName).first()
    pagination = db.session.query(Article, User.name).join(User, Article.author == User.id).filter(Article.category==category.id).order_by(
        Article.date.desc()
    ).paginate(
        page, per_page=5, error_out=False
    )
    posts = pagination.items

    return render_template('categories.html', categoryName=categoryName, posts=posts, pagination=pagination)


@main.route('/openArticle/<string:title>', methods=['GET', 'POST'])
def openArticle(title):
    title = title.replace('_', ' ')
    article = Article.query.filter_by(title=title).first()
    if article is None:
        flash('Matéria inválida !')
        return redirect(url_for('main.index'))
    author = User.query.filter_by(id=Article.author).first()
    return render_template('openArticle.html', article=article, author=author.name)

@main.route('/authors', methods=['GET', 'POST'])
def authors():
    page = request.args.get('page', 1, type=int)
    authorsPagination = User.query.paginate(
        page, per_page=5, error_out=False
    )
    usersAuthors = authorsPagination.items
    authors = [user for user in usersAuthors if user.has_permission(Permission.WRITE)]
    return render_template('authors.html', authors=authors, pagination=authorsPagination)