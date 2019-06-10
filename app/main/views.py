from flask import session, redirect, url_for, flash, render_template
from . import main
from .forms import SearchForm

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/search', methods=['GET', 'POST'])
def busca():
    return render_template('paginaBusca.html')

@main.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

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


@main.route('/admin')
def admin():
    return render_template('index.html')