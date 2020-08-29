from .Usuario import Usuario
from .Usuario import UsuarioSchema
from passlib.hash import bcrypt_sha256, sha256_crypt
from flask import current_app, jsonify
from .model import db
from datetime import date
from .Auth import Auth


class UsuarioService():
    usuario_schema = UsuarioSchema()

    @Auth.
    def listar(self):
        return self.usuario_schema.jsonify(Usuario.query.all(), many=True)

    def cadastrar(self, request):
        usuario = self.usuario_schema.load(request.json)

        emailEncontrado = self.buscar_email(usuario['email'])
        if emailEncontrado:
            raise Exception("Email já está sendo utilizado")

        if "cpf" in usuario:
            cpfEncontrado = self.buscar_cpf(usuario["cpf"])
            if cpfEncontrado:
                raise Exception("Cpf já está sendo utilizado")

        usuario['papel'] = 2
        usuario['token'] = self.gerar_token(
            usuario['tipo_cadastro'], usuario['email'])
        usuario['ativo'] = usuario['token'] == ""

        usuario['senha'] = self.gerar_hash(usuario['senha'])

        novoUsuario = Usuario(usuario)
        self.salvar(novoUsuario)
        return self.usuario_schema.jsonify(usuario), 201

    def gerar_token(self, tipo_cadastro, email):
        if tipo_cadastro == 2 or tipo_cadastro == 3:
            return ""
        else:
            return sha256_crypt.hash(email)

    def salvar(self, usuario):
        current_app.db.session.add(usuario)
        current_app.db.session.commit()

    def atualizar(self, data, usuario):
        for key, value in data.items():
            if key == 'senha':
                usuario.senha = self.gerar_hash(value)
            else:
                setattr(usuario, key, value)

            usuario.modified_at = date.today()
        current_app.db.session.commit()

    def buscar_email(self, email):
        return Usuario.query.filter(Usuario.email == email).first()

    def buscar_cpf(self, cpf):
        return Usuario.query.filter(Usuario.cpf == cpf).first()

    def gerar_hash(self, senha):
        return bcrypt_sha256.hash(senha)

    def verificar_senha(self, senha_requisicao, senha):
        return bcrypt_sha256.verify(senha_requisicao, senha)

    def login(self, request):
        usuario = self.usuario_schema.load(request.json)
        usuarioEncontrado = self.buscar_email(usuario['email'])

        if not usuarioEncontrado and not self.verificar_senha(usuario['senha'], usuarioEncontrado.senha):
            raise Exception("Credênciais inválidas")

        token = Auth.gerar_token(usuarioEncontrado.id)

        return token

    def buscar_id(self, id):
        return Usuario.query.filter(Usuario.id == id).first()
