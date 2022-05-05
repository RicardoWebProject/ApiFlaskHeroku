import imp
import sqlite3
from db import db

class ItemModel(db.Model):
    #Nombre de la tabla
    __tablename__ = 'items'
    
    #Columnas
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # store_id = db.Column(db.Integer, db.ForeingKey('stores.id'))    en donde 'stores' es el nombre de la tabla y 'id' es el nombre del campo -> 'stores.id'
    store = db.relationship('StoreModel')   #Con esto encontramos una tienda de acuerdo a la relación con su ID
    ##
    
    def __init__(self, name, price, store_id) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'id': self.id ,'name': self.name, 'price': self.price, 'store_id': self.store_id}
    
    @classmethod
    def find_by_name(cls, name):
        #'query' viene ya en db.Model, y podemos utilizarlo para crear consultas
        return cls.query.filter_by(name = name).first()   #SELECT * FROM items WHERE name = name LIMIT 1
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        #Session es una colección de objetos que escribiremos en la base de datos
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()