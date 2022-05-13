# from typing import Dict, Union
from flask import request, url_for
from requests import Response, post
from db import db

# UserJSON = Dict[str, Union[int, str]]
class UserModel(db.Model):
    #El nombre de la tabla para la base de datos
    __tablename__ = 'users'
    
    #Columnas que tendrá la tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)
    ##
    
    # def __init__(self, username: str, password: str) -> None:
    #     self.username = username
    #     self.password = password
    
    ## Este método ya no es requerido si estamos utilizando marshmallow
    # def json(self) -> UserJSON:
    #     return {'id': self.id, 'username': self.username}
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def send_confirmation_email(self) -> Response:
        #http://127.0.0.1:5000/ -> Esta es la url_root
        #Con [0:-1] decimos que queremos desde la primera posición hasta la última, -1 espacio, por lo que no toma el último slash.
        # -> 'userconfirm' es el nombre del resurce anotado como api.add_resource(UserConfirm, '/user_confirm/<int:user_id>'), en app.py
        link = request.url_root[0:-1] + url_for('userconfirm', user_id=self.id)
        
        return post(
            f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
            auth=('api', MAILGUN_API_KEY),
            data={
                'from': f'{FROM_TITLE} {FROM_EMAIL}',
                'to': self.email,
                'subject': 'Confirmación de Registro',
                'text': f'Por favor, haz click en el enlace para confirmar tu registro: {link}'
            }
        )
    
    @classmethod
    def find_by_username(cls, username: str) -> 'UserModel':
        return cls.query.filter_by(username=username).first()   #SELECT * FROM USERS WHERE username = username LIMIT 1
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = 'SELECT * FROM users WHERE username = ?'
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        #     # user = User(row[0], row[1], row[2])
        # else:
        #     user = None
        
        # connection.close()
        
        # return user
    
    @classmethod
    def find_by_email(cls, email: str) -> 'UserModel':
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()  #SELECT * FROM USERS WHERE id = _id LIMIT 1
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = 'SELECT * FROM users WHERE id = ?'
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        #     # user = User(row[0], row[1], row[2])
        # else:
        #     user = None
        
        # connection.close()
        
        # return user