from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from flask_migrate import Migrate, upgrade
from flask_cors import CORS
from config import Config
from models import db
from functools import wraps
from sqlalchemy import desc
import os

# Importação dos modelos (User, Campanha, Pessoa, Rifa, Sorteio)
from models import User, Campanha, Pessoa, Rifa, Sorteio

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

CORS(app) 

migrate = Migrate(app, db)

def paginate(query, page=1, per_page=10):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    items = query.slice(start_index, end_index).all()
    return items

def run_migrations():
    # Cria as tabelas se não existirem
    with app.app_context():
        db.create_all()

    # Aplica as migrações ao banco de dados
    with app.app_context():
        upgrade()
    
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
        'Campanhas': ['',''],
        'Rifas': ['',''],
        'Pessoas': ['pag_pessoas',''],
    }
    
    paginas[f'{pagina}'][1] = 'uk-active'
    """
    print(paginas)
    for item in paginas:
        print(paginas[item])
    """
        
    return paginas

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
        'navegacao': navegacao('Inicio')
    }
    
    #print(context['user'])
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
@login_required
def logout():
    # Limpa os cookies de autenticação e redireciona para a página de login
    response = make_response(redirect(url_for('login')))
    response.set_cookie('user_id', '', expires=0)
    response.set_cookie('username', '', expires=0)
    return response

@app.route('/pag_pessoas')
@login_required
def pag_pessoas():
    username = request.cookies.get('username')
    
    context = {
       'user': username,
       'navegacao': navegacao('Pessoas')
    }
    
    return render_template('templates-privados/pessoas.html', context=context)

@app.route('/pessoas', methods=['GET'])
@login_required
def pessoas():
    # Obtem os parâmetros da consulta da URL
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    pessoas = paginate(Pessoa.query.order_by(desc(Pessoa.id)), page, per_page)

    # Converte as instâncias da classe Pessoa para dicionários usando o método to_dict
    pessoas_serializadas = [pessoa.to_dict() for pessoa in pessoas]

    # Informações sobre a paginação
    total_items = Pessoa.query.count()
    total_pages = (total_items + per_page - 1) // per_page

    paginacao = {
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'current_page': page,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None,
        'pages': [i for i in range(1, total_pages + 1)],
    }

    # Retorna os dados e informações de paginação em formato JSON
    return jsonify({'pessoas': pessoas_serializadas, 'paginacao': paginacao})

@app.route('/buscar_pessoas', methods=['GET'])
@login_required
def buscar_pessoas():
    # Obtenha o termo de busca da URL
    search_term = request.args.get('search', default='', type=str)

    # Use o filtro para pesquisar pessoas com base no termo de busca
    query = Pessoa.query.filter(Pessoa.nome.ilike(f'%{search_term}%'))

    # Converte as instâncias da classe Pessoa para dicionários usando o método to_dict
    pessoas_serializadas = [pessoa.to_dict() for pessoa in query]

    # Retorna os dados encontrados em formato JSON
    return jsonify({'pessoas': pessoas_serializadas})

@app.route('/add_pessoa', methods=['POST'])
@login_required
def add_pessoa():
    data = request.get_json()  # Obtém os dados do JSON na solicitação

    # Cria uma nova instância da classe Pessoa
    nova_pessoa = Pessoa(
        nome=data['nome'],
        telefone=data.get('telefone'),
        cidade=data.get('cidade'),
        estado=data.get('estado', 'Pernambuco'),  # Define um valor padrão se não fornecido
        pais=data.get('pais', 'Brasil')  # Define um valor padrão se não fornecido
    )

    # Adiciona a nova pessoa ao banco de dados
    db.session.add(nova_pessoa)
    db.session.commit()

    return jsonify({'message': 'Pessoa adicionada com sucesso!'}), 201

@app.route('/pessoa/<int:id>', methods=['GET'])
@login_required
def pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    #print(pessoa)
    return jsonify(pessoa.to_dict())

@app.route('/updt_pessoa/<int:id>', methods=['POST'])
@login_required
def updt_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    
    #Dados atualizados
    att = request.get_json()
    
    #Atribuindo dados novos
    pessoa.nome = att['nome']
    pessoa.telefone = att['telefone']
    pessoa.cidade = att['cidade']
    pessoa.estado = att['estado']
    pessoa.pais = att['pais']
    
    #Confirmando transação
    db.session.commit()
    
    #print(pessoa)
    return jsonify({'message': 'Pessoa atualizada com sucesso!'}), 201

if __name__ == '__main__':
    # Executa as migrações antes de iniciar o aplicativo
    run_migrations()
    
    app.run(debug=True, port=os.getenv("PORT", default=5000), use_reloader=True)
    
    
