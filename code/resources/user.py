import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Este campo no puede estar vacío'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Este campo no puede estar vacío'
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
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