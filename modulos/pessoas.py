from utils.common import *

from . import pessoas_blueprint

@pessoas_blueprint.route('/pag_pessoas')
@login_required
def pag_pessoas():
    username = request.cookies.get('username')
    
    context = {
       'user': username,
       'navegacao': navegacao('Pessoas')
    }
    
    return render_template('templates-privados/pessoas.html', context=context)

@pessoas_blueprint.route('/', methods=['GET'])
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

@pessoas_blueprint.route('/buscar_pessoas', methods=['GET'])
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

@pessoas_blueprint.route('/add_pessoa', methods=['POST'])
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

@pessoas_blueprint.route('/pessoa/<int:id>', methods=['GET'])
@login_required
def pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    #print(pessoa)
    return jsonify(pessoa.to_dict())

@pessoas_blueprint.route('/updt_pessoa/<int:id>', methods=['POST'])
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
