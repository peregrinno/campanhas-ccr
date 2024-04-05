from utils.common import *

from . import admin_blueprint

@admin_blueprint.route('/administracao')
@login_required
def pag_admin():
    username = request.cookies.get('username')
    user_id = request.cookies.get('user_id')
    
    usuario = User.query.get_or_404(user_id)
    
    if {"admin": "sudo"} in usuario.getPermissions():
        nav = navegacao('Admin', "admin")
    elif {"user": "permissoes padrao"} in usuario.getPermissions():
        nav = navegacao('Adimin', "user")
    

    context = {
       'user': username,
       'navegacao': nav,
    }
    
    return render_template('templates-privados/administracao/administracao.html', context=context)