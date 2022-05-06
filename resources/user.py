from hashlib import new
import sqlite3
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
from flask_jwt_extended import (
        create_access_token, 
        create_refresh_token, 
        jwt_required, 
        get_jwt_identity, 
        get_jwt
    )

_user_parser = reqparse.RequestParser()

_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='Este campo no puede estar vacío'
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='Este campo no puede estar vacío'
)
class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'El username ya existe. Pruebe con otro.'}, 409
        
        #Instanciar objeto de UserModel, y se guarda en base de datos con el método llamado 'save_to_db'
        #Al final, sigue siendo POO
        
        user = UserModel(**data)
        # user = UserModel(data['username'], data['password'])
        user.save_to_db()
        
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        # cursor.execute(query, (data['username'], data['password']))
        
        # connection.commit()
        # connection.close()
        
        return {'message': 'Usuario creado correctamente'}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        user.delete_from_db()

class UserLogin(Resource):
    @classmethod
    def post(cls):
        #Obtener data del parser
        data = _user_parser.parse_args()
        
        #Encontrar un usuario en la bd
        user = UserModel.find_by_username(data['username'])
        
        #Checkear la contraseña
        if user and user.password == data['password']:
            #Crear el token de acceso
            access_token = create_access_token(identity = user.id, fresh=True)
            #Refrescar el token
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        #Retornar el token
        return {'message': 'Credenciales inválidas'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  #El jti es el identificador único para un JWT
        BLACKLIST.add(jti)
        return {'message': 'Deslogueado correctamente.'}, 200

class TokenRefresh(Resource):
    # @jwt_refresh_token_required se cambia a jwt_required(refresh=True)
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        return {'access_token': new_token}, 200