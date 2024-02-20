from utils.common import *

from modulos import dimensoes_blueprint, pessoas_blueprint, campanhas_blueprint

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_APP_KEY', 'not-secret-flask123')

app.config.from_object(Config)

db.init_app(app)

CORS(app) 

migrate = Migrate(app, db)

def run_migrations():
    # Cria as tabelas se não existirem
    with app.app_context():
        db.create_all()

    # Aplica as migrações ao banco de dados
    with app.app_context():
        upgrade()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    username = request.cookies.get('username')
    
    total_pessoas = Pessoa.query.count() or 0
    total_campanhas = Campanha.query.count() or 0
    total_metas = db.session.query(func.sum(Campanha.meta)).scalar() or 0
    
    context = {
        'user': username,
        'navegacao': navegacao('Inicio'),
        'total_pessoas' : total_pessoas,
        'total_campanhas' : total_campanhas,
        'total_metas' : total_metas,
    }
    
    #print(context['user'])
    return render_template("templates-privados/index.html", context=context)

@app.route('/autenticacao', methods=['POST'])
def authenticate():
    # Cria o usuário padrão
    create_default_user()
    
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(email=username).first()

    if user and user.check_password(password):
        # Salva os dados do usuário em um cookie
        response = make_response(jsonify({'success': True, 'user': f'{user.id}'}))
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

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('erros/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    # Manipulador de erro para o código de erro 404
    return render_template('erros/404.html'), 404

# Registrar os blueprints para cada modulo
app.register_blueprint(pessoas_blueprint, url_prefix='/pessoas')
app.register_blueprint(campanhas_blueprint, url_prefix='/campanhas')
app.register_blueprint(dimensoes_blueprint, url_prefix='/dimensoes')

if __name__ == '__main__':
    # Executa as migrações antes de iniciar o aplicativo
    run_migrations()
    
    app.run(debug=True, port=os.getenv("PORT", default=5000), use_reloader=True)
    
    
