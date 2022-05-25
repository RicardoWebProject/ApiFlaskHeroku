import traceback
from flask import request
from flask_restful import Resource
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from models.user import UserModel
from flask_jwt_extended import (
        create_access_token, 
        create_refresh_token, 
        jwt_required, 
        get_jwt_identity, 
        get_jwt
    )
from schemas.user import UserSchema
from models.confirmation import ConfirmationModel
from libs.strings import gettext

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
            return {'message': gettext("user_name_exists")}, 409
        
        #Validar si existe un email en base de datos
        if UserModel.find_by_email(user.email):
            return {'message': gettext("user_email_exists")}, 409
        
        try:
            #Instanciar objeto de UserModel, y se guarda en base de datos con el método llamado 'save_to_db'
            #Al final, sigue siendo POO
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {'message': gettext("user_created")}, 201
        except MailGunException as e:
            user.delete_from_db() #rollback
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {'message': gettext("user_error_creating")}, 500
        

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': gettext("user_not_found")}, 404
        # return user.json()
        return user_schema.dump(user)
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': gettext("user_not_found")}, 404
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
            confirmation = user.most_recent_confirmation
            # if user.activated:
            if confirmation and confirmation.confirmed:
                #Crear el token de acceso
                access_token = create_access_token(identity = user.id, fresh=True)
                #Refrescar el token
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': gettext("user_not_confirmed").format(user.email)}, 400
        #Retornar el token
        return {'message': gettext("user_invalid_credentials")}, 401

class UserLogout(Resource):
    @jwt_required()
    @classmethod
    def post(cls):
        jti = get_jwt()['jti']  #El jti es el identificador único para un JWT
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': gettext("user_logged_out").format(user_id)}, 200

class TokenRefresh(Resource):
    # @jwt_refresh_token_required se cambia a jwt_required(refresh=True)
    @jwt_required(refresh=True)
    @classmethod
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        return {'access_token': new_token}, 200

# class UserConfirm(Resource):
#     @classmethod
#     def get(cls, user_id: int):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': gettext("user_not_found")}, 404
        
#         if user.activated == False:
#             user.activated = True
#             user.save_to_db()
#             headers = {'Content-Type': 'text/html'}
#             # return {'message': gettext("user_USER_CONFIRMED")}, 200
#             return make_response(render_template('confirmation_page.html', email=user.email), 200, headers)
#         else:
#             return {'message': gettext("user_USER_ALREADY_CONFIRMED")}, 200