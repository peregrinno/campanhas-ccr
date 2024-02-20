from utils.common import *

from . import campanhas_blueprint

@campanhas_blueprint.route('/pag_campanhas')
@login_required
def pag_campanhas():
    username = request.cookies.get('username')
    tipos = DimTipoCampanha.query.all()
    context = {
       'user': username,
       'navegacao': navegacao('Campanhas'),
       'tipos': tipos
    }
    
    return render_template('templates-privados/campanhas.html', context=context)

@campanhas_blueprint.route('/', methods=['GET'])
@login_required
def campanhas():
    # Obtem os parâmetros da consulta da URL
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    campanhas = paginate(Campanha.query.order_by(desc(Campanha.id)), page, per_page)

    # Converte as instâncias da classe campanha para dicionários usando o método to_dict
    campanhas_serializadas = [campanha.to_dict() for campanha in campanhas]

    # Informações sobre a paginação
    total_items = Campanha.query.count()
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
    return jsonify({'campanhas': campanhas_serializadas, 'paginacao': paginacao})

@campanhas_blueprint.route('/buscar_campanhas', methods=['GET'])
@login_required
def buscar_campanhas():
    # Obtenha o termo de busca da URL
    search_term = request.args.get('search', default='', type=str)

    # Use o filtro para pesquisar campanhas com base no termo de busca
    query = Campanha.query.filter(Campanha.nome.ilike(f'%{search_term}%'))

    # Converte as instâncias da classe campanha para dicionários usando o método to_dict
    campanhas_serializadas = [campanha.to_dict() for campanha in query]

    # Retorna os dados encontrados em formato JSON
    return jsonify({'campanhas': campanhas_serializadas})

@campanhas_blueprint.route('/add_campanha', methods=['POST'])
@login_required
def add_campanha():
    data = request.get_json()  # Obtém os dados do JSON na solicitação

    user_id = request.cookies.get('user_id')
    
    #print(data)
    
    #print(f"Dados: {data} \n Data de Inicio: {data.get('dt_inicio')}")
    
    # Cria uma nova instância da classe campanha
    nova_campanha = Campanha(
        nome=data.get('nome'),
        criador_id = user_id,
        dt_inicio=data.get('dt_inicio'),
        dt_fim=data.get('dt_fim'),
        meta= float(data.get('meta').replace(',', '')),
        tipo_id=data.get('tipo') 
    )
    
    # Adiciona a nova campanha ao banco de dados
    db.session.add(nova_campanha)
    db.session.commit()

    return jsonify({'message': 'campanha adicionada com sucesso!'}), 201

@campanhas_blueprint.route('/campanha/<int:id>', methods=['GET'])
@login_required
def campanha(id):
    campanha = Campanha.query.get_or_404(id)
    #print(campanha)
    return jsonify(campanha.to_dict())

@campanhas_blueprint.route('/updt_campanha/<int:id>', methods=['POST'])
@login_required
def updt_campanha(id):
    campanha = Campanha.query.get_or_404(id)

    #Dados atualizados
    att = request.get_json()
       
    #print(att)
     
    #Atribuindo dados novos
    campanha.nome = att['nome']
    campanha.dt_inicio = att['dt_inicio']
    campanha.dt_fim = att['dt_fim']
    campanha.meta = float(att['meta'].replace(',',''))
    campanha.tipo_id = att['tipo']
    
    #Confirmando transação
    db.session.commit()
    
    #print(campanha)
    return jsonify({'message': 'campanha atualizada com sucesso!'}), 201
