from .model import db
from .serealizer import ma
from marshmallow import fields
from datetime import date


class Usuario(db.Model):
    __tabelname__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    nome = db.Column(db.String(255), nullable=False)
    nome_social = db.Column(db.String(255), nullable=True)
    senha = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=True, unique=True)
    token = db.Column(db.String(255), nullable=False)
    foto = db.Column(db.String(255), nullable=True)
    tipo_cadastro = db.Column(db.Integer, default=1)
    sexo = db.Column(db.Integer, default=0)
    papel = db.Column(db.Integer, default=1)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.id = data.get("id")
        self.nome = data.get('nome')
        self.email = data.get('email')
        self.nome_social = data.get('nome_social')
        self.senha = data.get('senha')
        self.cpf = data.get('cpf')
        self.foto = data.get('foto')
        self.tipo_cadastro = int(data.get('tipo_cadastro'))
        self.sexo = int(data.get('sexo')) if data.get('sexo') else 0
        self.papel = int(data.get('papel'))
        self.ativo = data.get('ativo')
        self.created_at = self.created_at if self.id else date.today()
        self.updated_at = date.today()


class UsuarioSchema(ma.Schema):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'nome_social', 'senha', 'cpf',
                  'foto', 'tipo_cadastro', 'sexo', 'papel', 'token')
