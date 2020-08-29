import jwt
import os
import datetime
from flask import json, request, Response, g
from functools import wraps
from .UsuarioService import UsuarioService


class Auth():
    @staticmethod
    def gerar_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                "os.getenv('JWT_SECRET_KEY')",
                'HS256'
            ).decode("utf-8")
        except Exception:
            return Response(
                mimetype="application/json",
                response=json.dumps(
                    {'error': 'Erro ao gerar jwt_token'}),
                status=400
            )

    @staticmethod
    def decodificar_token(token):
        re = {'data': {}, 'error': {}}

        try:
            payload = jwt.decode(token, "os.getenv('JWT_SECRET_KEY')")
            re['data'] = {'id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError:
            re['error'] = {'message': 'Token expirada, logue novamente'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {
                'message': 'Token inválida, por favor, tente novamento com uma nova token'}
            return re

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {'error': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )
            g.id = data['data']['id']
            return func(*args, **kwargs)
        return decorated_auth
