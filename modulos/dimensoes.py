from utils.common import *

from . import dimensoes_blueprint

@dimensoes_blueprint.route('/tipos', methods=['GET'])
@login_required
def tipos():
    tipos = DimTipoCampanha.query.all()
    
    return jsonify({'tipos': [tipo.to_dict() for tipo in tipos]})