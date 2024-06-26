from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for, Blueprint
from flask_migrate import Migrate, upgrade
from flask_cors import CORS
from config import Config
from models import db
from functools import wraps
from sqlalchemy import desc, func
import os

# Importação dos modelos (User, Campanha, Pessoa, Rifa, Sorteio)
from models import DimTipoCampanha, User, Campanha, Pessoa, Rifa, Sorteio, Talao

def paginate(query, page=1, per_page=10):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    items = query.slice(start_index, end_index).all()
    return items
    
def create_default_user():
    # Verifica se o usuário já existe
    existing_user = User.query.filter_by(username='admin').first()
    
    existing_types = DimTipoCampanha.query.filter_by(id=1).first()

    if not existing_user:
        # Se o usuário não existir, cria um novo usuário padrão
        default_user = User(username='admin', email='admin@administrador.com', password='adminpassword', permissions={"admin":"sudo"})
        db.session.add(default_user)
        db.session.commit()
    
    if not existing_types:
        default_type = DimTipoCampanha(nome='Rifa')
        db.session.add(default_type)
        default_type = DimTipoCampanha(nome='Arrecadação')
        db.session.add(default_type)
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

def navegacao(pagina, rule):
    # 'NOME DA PAGINA NO FRONT' : ['ROTA DA PAGINA', 'PAGINA ATIVA OU NÃO']
    
    if rule == "admin":
        paginas = {
            'Inicio': ['index', ''],
            'Campanhas': ['campanhas.pag_campanhas',''],
            'Rifas': ['rifas.pag_rifas',''],
            'Pessoas': ['pessoas.pag_pessoas',''],
            'Admin': ['admin.pag_admin','']
        }
    elif rule == "user":
        paginas = {
            'Inicio': ['index', ''],
            'Campanhas': ['campanhas.pag_campanhas',''],
            'Rifas': ['rifas.pag_rifas',''],
            'Pessoas': ['pessoas.pag_pessoas',''],
        }
    
    paginas[f'{pagina}'][1] = 'uk-active'
    
    """
    print(paginas)
    for item in paginas:
        print(paginas[item])
    """
        
    return paginas

@login_required
def check_campanhas():
    campanhas_sem_rifas = []

    # Obter IDs das campanhas com rifas
    campanhas_com_rifas = set(rifa.id_campanha for rifa in Rifa.query.distinct(Rifa.id_campanha))

    # Varrer campanhas
    campanhas = Campanha.query.filter(Campanha.tipo.has(nome='Rifa')).all()

    # Checar uma a uma
    for campanha in campanhas:
        if campanha.id not in campanhas_com_rifas:
            campanhas_sem_rifas.append({'id': campanha.id, 'nome': campanha.nome})
            
    
    return campanhas_sem_rifas

@login_required
def check_rifas():
    rifas = []

    # Obter IDs das campanhas com rifas
    campanhas_com_rifas = set(rifa.id_campanha for rifa in Rifa.query.distinct(Rifa.id_campanha))

    # Varrer campanhas
    campanhas = Campanha.query.filter(Campanha.tipo.has(nome='Rifa')).all()

    # Checar uma a uma
    for campanha in campanhas:
        if campanha.id in campanhas_com_rifas:
            rifas.append({'id': campanha.id, 'nome': campanha.nome})
            
    
    return rifas


