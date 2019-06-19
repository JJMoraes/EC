from flask import session, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from app import db
from .forms import SearchForm
from app.models import Article

from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/search', methods=['GET', 'POST'])
def busca():
    if request.method == 'POST':
        dados = request.form
        posts = Article.query.filter(Article.text.like('%{}%'.format(dados['textoBusca'])))
        print(posts)
    return render_template('paginaBusca.html')

@main.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        return render_template('contato.html', mensagem=True)

    return render_template('contato.html', mensagem=False)

@main.route('/sobre', methods=['GET', 'POST'])
def sobre():
    return render_template('sobre.html')

@main.route('/categoria', methods=['GET', 'POST'])
def categoria():
    return render_template('links.html')

@main.route('/materia', methods=['GET', 'POST'])
def materiaAberta():
    return render_template('materiaAberta.html')

@main.route('/autores', methods=['GET', 'POST'])
def autores():
    return render_template('autores.html')