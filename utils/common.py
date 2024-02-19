from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for, Blueprint
from flask_migrate import Migrate, upgrade
from flask_cors import CORS
from config import Config
from models import db
from functools import wraps
from sqlalchemy import desc
import os


# Importação dos modelos (User, Campanha, Pessoa, Rifa, Sorteio)
from models import User, Campanha, Pessoa, Rifa, Sorteio

def paginate(query, page=1, per_page=10):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    items = query.slice(start_index, end_index).all()
    return items
    
def create_default_user():
    # Verifica se o usuário já existe
    existing_user = User.query.filter_by(username='admin').first()

    if not existing_user:
        # Se o usuário não existir, cria um novo usuário padrão
        default_user = User(username='admin', email='admin@administrador.com', password='adminpassword')
        db.session.add(default_user)
        db.session.commit()
        
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        username = request.cookies.get('username')

        if user_id and username:
            user = User.query.filter_by(id=user_id, username=username).first()
            if user:
                # Adiciona o usuário à requisição para ser acessado nas rotas protegidas
                request.user = user
                return f(*args, **kwargs)
            
        # Redireciona para a página de login se o usuário não estiver autenticado
        return redirect(url_for('login'))

    return decorated_function

def navegacao(pagina):
    # 'NOME DA PAGINA NO FRONT' : ['ROTA DA PAGINA', 'PAGINA ATIVA OU NÃO']
    paginas = {
        'Inicio': ['index', ''],
        'Campanhas': ['campanhas.pag_campanhas',''],
        'Rifas': ['',''],
        'Pessoas': ['pessoas.pag_pessoas',''],
    }
    
    paginas[f'{pagina}'][1] = 'uk-active'
    """
    print(paginas)
    for item in paginas:
        print(paginas[item])
    """
        
    return paginas

