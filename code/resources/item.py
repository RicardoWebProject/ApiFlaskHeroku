import sqlite3
from flask_restful import Resource, reqparse
#Un Resource (recurso) es algo que nuestra API puede devolver
#Cada Resource debe ser una clase
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # -> esto sólo inicializa un nuevo objeto  que podemos usar para analizar la solicitud
    # parser.add_argument('name', type=str, required=True, help='Este campo no puede estar vacío')
    parser.add_argument('price', type=float, required=True, help='Este campo no puede estar en blanco.')
    parser.add_argument('store_id', type=int, required=True, help='Todos los items necesitan un id de tienda')
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            # return {'message': "An item with name '{}' already exists.".format(name)}, 400
            return {'message': f'un item con el nombre {name} ya existe.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        # item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "Ha ocurrido un error ingresando el item."}, 500

        return item.json(), 201
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': f'Un item con el nombre "{name}" ya existe.'}, 400
        
        # data = Item.parser.parse_args()
        
        # item = {
        #     'name': name,
        #     'price': data['price']
        # }
        # items.append(item)
        # return item, 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item eliminado.'}
        return {'message': 'Item no encontrado.'}, 404
        
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item eliminado'}
    
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()
    
        # data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {
        #         'name': name,
        #         'price': data['price']
        #     }
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item

class ItemList (Resource):
    def get(self):
        return {
            'items': list(map(lambda x: x.json(), ItemModel.query.all()))
        }
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = 'SELECT * FROM items'
        # result = cursor.execute(query)
        
        # row = result.fetchall()
        # connection.close()
        
        # if row:
        #     return {'items': row}
        
        # return {'message': 'El item no existe.'}, 404
        # return {'items': items}