import traceback
from flask import make_response, render_template, request
from flask_restful import Resource
from blacklist import BLACKLIST
from models.user import UserModel
from flask_jwt_extended import (
        create_access_token, 
        create_refresh_token, 
        jwt_required, 
        get_jwt_identity, 
        get_jwt
    )
from schemas.user import UserSchema
from marshmallow import ValidationError

BLANK_ERROR = '{} no puede estar en blanco.'
NAME_ALREADY_EXISTS = 'El username ya existe. Pruebe con otro.'
EMAIL_ALREADY_EXISTS = 'El correo electrónico ya existe. Pruebe con otro.'
USER_NOT_FOUND = 'Usuario no econtrado'
ERROR_INSERTING = 'Ha ocurrido un error ingresando el Usuario.'
USER_DELETED = 'Usuario eliminado.'
USER_CREATED = 'Usuario creado correctamente'
INVALID_CREDENTIALS = 'Credenciales inválidas'
USER_LOGOUT = 'Usuario <id={}> deslogueado correctamente.'
NOT_CONFIRMED_ERROR = 'No has completado el registro. Por favor, revisa tu correo electronico: <{}> '
USER_CONFIRMED = 'Usuario confirmado.'
USER_ALREADY_CONFIRMED = 'Usuario ya confirmado.'
FAILED_TO_CREATE = 'Error interno del servidor. Fallo al crear el usuario.'

user_schema = UserSchema()

class UserRegister(Resource):
    
    @classmethod
    def post(cls):
        # data = _user_parser.parse_args()
        #Al migrar a Flask_Marshmallow, ahora 'user' es un objeto de UserModel
        user = user_schema.load(request.get_json())
        
        # if UserModel.find_by_username(user['username']):
        #Validar si existe un usuario en bse de datos
        if UserModel.find_by_username(user.username):
            return {'message': NAME_ALREADY_EXISTS}, 409
        
        #Validar si existe un email en base de datos
        if UserModel.find_by_email(user.email):
            return {'message': EMAIL_ALREADY_EXISTS}, 409
        
        try:
            #Instanciar objeto de UserModel, y se guarda en base de datos con el método llamado 'save_to_db'
            #Al final, sigue siendo POO
            user.save_to_db()
            user.send_confirmation_email()
            return {'message': USER_CREATED}, 201
        except:
            traceback.print_exc()
            return {'message': FAILED_TO_CREATE}, 500
        

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        # return user.json()
        return user_schema.dump(user)
    
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
        user_data = user_schema.load(request.get_json(), partial=('email',))
        
        #Encontrar un usuario en la bd
        user = UserModel.find_by_username(user_data.username)
        
        #Checkear la contraseña
        if user and user.password == user_data.password:
            if user.activated:
                #Crear el token de acceso
                access_token = create_access_token(identity = user.id, fresh=True)
                #Refrescar el token
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': NOT_CONFIRMED_ERROR.format(user.email)}, 400
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

class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        
        if user.activated == False:
            user.activated = True
            user.save_to_db()
            headers = {'Content-Type': 'text/html'}
            # return {'message': USER_CONFIRMED}, 200
            return make_response(render_template('confirmation_page.html', email=user.email), 200, headers)
        else:
            return {'message': USER_ALREADY_CONFIRMED}, 200