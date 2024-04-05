from utils.common import *

from . import rifas_blueprint


@rifas_blueprint.route('/pag_rifas')
@login_required
def pag_rifas():
    username = request.cookies.get('username')
    user_id = request.cookies.get('user_id')
    
    usuario = User.query.get_or_404(user_id)
    
    if {"admin": "sudo"} in usuario.getPermissions():
        nav = navegacao('Rifas', "admin")
    elif {"user": "permissoes padrao"} in usuario.getPermissions():
        nav = navegacao('Rifas', "user")
    

    context = {
        'user': username,
        'navegacao': nav,
        'campanhas': check_campanhas() or None,
        'rifas': check_rifas() or None
    }
    return render_template('templates-privados/rifas.html ', context=context)


@rifas_blueprint.route('/gdr')
@login_required
def gdr():
    username = request.cookies.get('username')

    context = {
        'user': username,
        'navegacao': navegacao('Rifas'),
        'campanhas': check_campanhas() or None
    }
    return render_template('templates-privados/gerador.html ', context=context)


@rifas_blueprint.route('/gerarRifas', methods=['POST'])
@login_required
def gerarRifas():
    user_id = request.cookies.get('user_id')

    data = request.get_json()

    try:
        for rifa in range(0, int(data.get('qtdDeRifas'))):
            rf = Rifa(
                id_campanha=data.get('idCampanha'),
                numero=rifa + 1,
                valor=float(data.get('vlrDaRifa'))
            )

            db.session.add(rf)
            db.session.commit()

        return jsonify({"message": "Rifas geradas com sucesso!"}), 200
    except:
        return jsonify({"message": "Opss... Algo não saiu como planejado.."}), 500


@rifas_blueprint.route('/rifa/<int:id>')
@login_required
def rifa(id):
    username = request.cookies.get('username')
    rifaCotada = True

    rifas = Rifa.query.filter_by(id_campanha=id)
    
    taloes = Talao.query.filter_by(id_campanha=id)

    totalUsuarios = User.query.count()
    
    usuarios = User.query.all()

    if not Talao.query.filter_by(id_campanha=id).first():
        rifaCotada = False

    vlrRifa = rifas[0].valor

    campanha = Campanha.query.get_or_404(id)

    estatisticas = {
        'totalDeRifas': Rifa.query.filter_by(id_campanha=id).count(),
        'totalDeUsuarios': totalUsuarios,
    }

    context = {
        'user': username,
        'navegacao': navegacao('Rifas'),
        'campanha': campanha,
        'taloes': [talao.to_dict() for talao in taloes] if rifaCotada == True else None,
        'vlrRifa': vlrRifa,
        'rifaCotada': rifaCotada,
        'estatisticas': estatisticas,
        'usuarios': [usuario.to_dict() for usuario in usuarios]
    }
    return render_template('templates-privados/rifa.html ', context=context)


@rifas_blueprint.route('/gerarTaloes', methods=['POST'])
@login_required
def gerarTaloes():
    data = request.get_json()

    id_campanha = data.get('id_campanha')
    
    qdt = int(data.get('qtdDeTaloes'))
    qdn = int(data.get('qtdDeNumeros'))
    
    num = 1 #Guarda o ultimo numero usado
    nInicial = 0 #Guarda o primeiro numero do talao
    nFinal = 0 #Guarda o ulimo numero do talo
    qdnpt = qdn // qdt #Computa a quantidade de numeros por talão
    
    try:
        for i in range(qdt):
            nInicial = num
            for j in range(qdnpt):
                nFinal = num
                num += 1

            talao = Talao(
                id_campanha=id_campanha,
                n_inicial=nInicial,
                n_final=nFinal,
            )
            
            db.session.add(talao)
            db.session.commit()
            
        return jsonify({'message': 'Rifa Cotada!'})
    except:    
        return jsonify({'error': 'Algo não saiu como esperavamos...'})

@rifas_blueprint.route('/atualizarCotista', methods=['POST'])
@login_required
def atualizarCotista():
    data = request.get_json()

    # Verifica se 'talaoId' e 'cotista' estão presentes nos dados recebidos
    if 'talaoId' not in data or 'cotista' not in data:
        return jsonify({'error': 'Dados incompletos'}), 400

    talao = Talao.query.get_or_404(data.get('talaoId'))

    talao.uptdCotista(data.get('cotista'))

    db.session.commit()

    return jsonify({'message': 'Responsável atualizado!'})