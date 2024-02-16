from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from config import Config
from models import db
from functools import wraps

import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Importação dos modelos (User, Campanha, Pessoa, Rifa, Sorteio)
from models import User, Campanha, Pessoa, Rifa, Sorteio

# Criação das tabelas se não existirem
with app.app_context():
    db.create_all()
    
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

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
@login_required
def index():
    # Cria o usuário padrão
    create_default_user()
    
    username = request.cookies.get('username')
    
    context = {
        'user': username,
    }
    
    print(context['user'])
    return render_template("templates-privados/index.html", context=context)

@app.route('/autenticacao', methods=['POST'])
def authenticate():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(email=username).first()

    if user and user.check_password(password):
        # Salva os dados do usuário em um cookie
        response = make_response(jsonify({'success': True, 'user': user.to_dict()}))
        response.set_cookie('user_id', str(user.id))
        response.set_cookie('username', user.username)
        return response
    else:
        return jsonify({'success': False, 'message': 'Login falhou. Verifique suas credenciais.'})


@app.route('/logout')
def logout():
    # Limpa os cookies de autenticação e redireciona para a página de login
    response = make_response(redirect(url_for('login')))
    response.set_cookie('user_id', '', expires=0)
    response.set_cookie('username', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
