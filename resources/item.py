import sqlite3
from flask_restful import Resource, reqparse
#Un Resource (recurso) es algo que nuestra API puede devolver
#Cada Resource debe ser una clase
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # -> esto sólo inicializa un nuevo objeto  que podemos usar para analizar la solicitud
    # parser.add_argument('name', type=str, required=True, help='Este campo no puede estar vacío')
    parser.add_argument('price', type=float, required=True, help='Este campo no puede estar en blanco.')
    parser.add_argument('store_id', type=int, required=True, help='Todos los items necesitan un id de tienda')
    
    #@jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    @jwt_required(refresh=True)
    def post(self, name: str):
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
    
    @jwt_required()
    def delete(self, name: str):
        # #cambia de 'get_jwt_claims()' a solamente 'get_jwt()' según documentación actual
        # claims = get_jwt()
        # #Si lo que retorna no es 'is_admin', entonces se arroja mensaje de error
        # if not claims['is_admin']:
        #     return {'message': 'Se requieren privilegios de administrador.'}, 401
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item eliminado.'}
        return {'message': 'Item no encontrado.'}, 404
        
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item eliminado'}
    
    def put(self, name: str):
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
    #@jwt_required(optional=True)
    def get(self):
        # user_id = get_jwt_identity()
        # items = [x.json() for x in ItemModel.find_all()]
        
        # if user_id:
        #     return {
        #         'items': items
        #         # 'items': list(map(lambda x: x.json(), ItemModel.query.all()))
        #     }, 200
        # return {'items': [x['name'] for x in items], 'message': 'Más información disponible si te logueas.'}
        return {'items': [x.json() for x in ItemModel.find_all()]}, 200
        
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