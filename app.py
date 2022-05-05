from dataclasses import replace
import os
import re

from flask import Flask
#Un Resource (recurso) es algo que nuestra API puede devolver
#Cada Resource debe ser una clase
from flask_restful import Api
from flask_jwt import JWT
from resources.store import Store, StoreList

from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)

app.config['DEBUG'] = False

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

app.secret_key = 'ricardo'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth

#URLs | Recursos
api.add_resource(Item, '/item/<string:name>') #-> http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    #iniciación de objeto db para la aplicación Flask
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)