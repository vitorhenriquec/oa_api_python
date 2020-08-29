from .Usuario import Usuario
from .Usuario import UsuarioSchema
from .UsuarioService import UsuarioService
from flask import Blueprint, request, jsonify

bp_usuarios = Blueprint('usuarios', __name__)

usuario_service = UsuarioService()


@bp_usuarios.route('/usuario/listar', methods=['GET'])
def listar():
    return usuario_service.listar(), 200


@bp_usuarios.route('/usuario/cadastrar', methods=['POST'])
def cadastrar():
    try:
        return usuario_service.cadastrar(request)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_usuarios.route('/usuario/logar', methods=['POST'])
def logar():
    try:
        return {'jwt_token': usuario_service.login(request)}
    except Exception as e:
        return jsonify({"error": str(e)}), 500
