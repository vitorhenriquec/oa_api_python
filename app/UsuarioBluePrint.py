from .Usuario import Usuario
from .Usuario import UsuarioSchema
from .UsuarioService import UsuarioService
from flask import Blueprint, request, json, g
from .Auth import Auth

bp_usuarios = Blueprint('usuarios', __name__)

usuario_service = UsuarioService()


@bp_usuarios.route('/usuario/listar', methods=['GET'])
@Auth.auth_required
def listar():
    return usuario_service.listar(), 200


@bp_usuarios.route('/usuario/cadastrar', methods=['POST'])
def cadastrar():
    try:
        return usuario_service.cadastrar(request), 201
    except Exception as e:
        return {"error": str(e)}, 500


@bp_usuarios.route('/usuario/logar', methods=['POST'])
def logar():
    try:
        return {'jwt_token': usuario_service.login(request)}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@bp_usuarios.route('/usuario/minha_info', methods=['POST'])
@Auth.auth_required
def info():
    return {'error': 'Informação não achada'}, 200
