import os
from flask import Flask, jsonify
#Un Resource (recurso) es algo que nuestra API puede devolver
#Cada Resource debe ser una clase
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.store import Store, StoreList
from marshmallow import ValidationError

from ma import ma
from db import db
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList

###########################################################
app = Flask(__name__)

###########################################################
app.config['DEBUG'] = True

uri = os.getenv('DATABASE_URL')

if uri is not None:
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(uri, 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_BLOCKLIST_ENABLED'] = True
# app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

##########################################################
app.secret_key = 'ricardo'  #app.config['JWT_SECRET_KEY']
api = Api(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

##########################################################
jwt = JWTManager(app)  #/auth
# jwt = JWT(app, authenticate, identity)  # ya no crea /auth

#Cambia a additional_claims_loader según la documentación actual, en lugar de user_claims_loader
# @jwt.additional_claims_loader
# def add_claims_to_jwt(identity):
#     if identity == 1:   #En lugar de codificarlo, con esto debería de poder leerse un archivo desde configuración o una bd
#         return {'is_admin': True}
#     return {'is_admin': False}

# @jwt.token_in_blacklist_loader
#Ahora se reciben dos argumentos al usar este decorador: jwt_header y jwt_payload, que es un diccionario con el contenido del token
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload: dict):
    #Uso 'sub' porque es el número de ID que referencia a un usuario dentro de mi aplicación, en lugar del 'jti' que es el identificador de JWT para el usuario.
    #Para obtener más índices, hay que decodificar el token y revisar cuál se necesita: https://jwt.io/
    identity = jwt_payload['jti']
    return identity in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        'description': 'El token ha caducado',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader   #Se disparará cuando se detecte un token que no sea un JWT real
def invalid_token_callback():
    return jsonify({
        'message': 'Que estas haciendo?',
        'error': 'invalid_token'
    }), 401

# @jwt.unauthorized_loader    #Se llamará cuando no nos envién un JWT en absoluto

# @jwt.needs_fresh_token_loader   #Cuando nos envían un token no reciente pero necesitamos un token nuevo en el endpoint

# @jwt.revoked_token_loader   #Puede decir que determinado token ya no es válido


##########################################################
#URLs | Recursos
api.add_resource(Item, '/item/<string:name>') #-> http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

##########################################################
if __name__ == '__main__':
    #iniciación de objeto db para la aplicación Flask
    db.init_app(app)
    ma.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)