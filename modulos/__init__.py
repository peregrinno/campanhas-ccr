from utils.common import *

pessoas_blueprint = Blueprint('pessoas', __name__, template_folder='templates')
campanhas_blueprint = Blueprint('campanhas', __name__, template_folder='templates')
dimensoes_blueprint = Blueprint('dimensoes', __name__, template_folder='templates')
rifas_blueprint = Blueprint('rifas', __name__, template_folder='templates')

from . import campanhas, dimensoes, rifas, pessoas