from utils.common import *

from . import rifas_blueprint

@rifas_blueprint.route('/pag_rifas')
@login_required
def pag_rifas():
    username = request.cookies.get('username')
    
    context = {
        'user': username,
        'navegacao': navegacao('Rifas'),
        'campanhas': check_campanhas() or None
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
            rf = Rifa (
                id_campanha = data.get('idCampanha'),
                numero = rifa + 1,
                valor= float(data.get('vlrDaRifa'))
            )
            
            
            db.session.add(rf)
            db.session.commit()
            
        return jsonify({"message":"Rifas geradas com sucesso!"})
    except:
        return jsonify({"message":"Opss... Algo não saiu como planejado.."})
       