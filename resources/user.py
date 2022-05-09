from hashlib import new
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


BLANK_ERROR = '{} no puede estar en blanco.'
NAME_ALREADY_EXISTS = 'El username ya existe. Pruebe con otro.'
USER_NOT_FOUND = 'Usuario no econtrado'
ERROR_INSERTING = 'Ha ocurrido un error ingresando el Usuario.'
USER_DELETED = 'Usuario eliminado.'
USER_CREATED = 'Usuario creado correctamente'
INVALID_CREDENTIALS = 'Credenciales inválidas'
USER_LOGOUT = 'Usuario <id={}> deslogueado correctamente.'

_user_parser = reqparse.RequestParser()

_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help=BLANK_ERROR.format('username')
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help=BLANK_ERROR.format('password')
)
class UserRegister(Resource):
    
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': NAME_ALREADY_EXISTS}, 409
        
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
        
        return {'message': USER_CREATED}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
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
        return {'message': INVALID_CREDENTIALS}, 401

class UserLogout(Resource):
    @jwt_required()
    @classmethod
    def post(cls):
        jti = get_jwt()['jti']  #El jti es el identificador único para un JWT
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': USER_LOGOUT.format(user_id)}, 200

class TokenRefresh(Resource):
    # @jwt_refresh_token_required se cambia a jwt_required(refresh=True)
    @jwt_required(refresh=True)
    @classmethod
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        return {'access_token': new_token}, 200