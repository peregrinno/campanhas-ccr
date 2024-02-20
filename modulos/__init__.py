from utils.common import *

pessoas_blueprint = Blueprint('pessoas', __name__, template_folder='templates')
campanhas_blueprint = Blueprint('campanhas', __name__, template_folder='templates')
dimensoes_blueprint = Blueprint('dimensoes', __name__, template_folder='templates')

from . import pessoas, campanhas, dimensoes