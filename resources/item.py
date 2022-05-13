from flask_restful import Resource
from flask import request
#Un Resource (recurso) es algo que nuestra API puede devolver
#Cada Resource debe ser una clase
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel
from schemas.item import ItemSchema
from marshmallow import ValidationError

NAME_ALREADY_EXISTS = 'Un item con el nombre "{}" ya existe.'
ITEM_NOT_FOUND = 'Item no econtrado'
ERROR_INSERTING = 'Ha ocurrido un error ingresando el item.'
ITEM_DELETED = 'Item eliminado.'

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):
    # parser = reqparse.RequestParser() # -> esto sólo inicializa un nuevo objeto  que podemos usar para analizar la solicitud
    # # parser.add_argument('name', type=str, required=True, help='Este campo no puede estar vacío')
    # parser.add_argument('price', type=float, required=True, help=BLANK_ERROR.format('price'))
    # parser.add_argument('store_id', type=int, required=True, help=BLANK_ERROR.format('store_id'))
    
    #@jwt_required()
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            # return item.json()
            return item_schema.dump(item)
        return {'message': ITEM_NOT_FOUND}, 404
    
    @classmethod
    @jwt_required(refresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            # return {'message': "An item with name '{}' already exists.".format(name)}, 400
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        # data = Item.parser.parse_args()
        item_json = request.get_json()  #price, store_id
        item_json['name'] = name

        # item = ItemModel(name, **data)
        # item = ItemModel(name, data['price'], data['store_id'])
        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': f'Un item con el nombre "{name}" ya existe.'}, 400
        
        # data = Item.parser.parse_args()
        
        # item = {
        #     'name': name,
        #     'price': data['price']
        # }
        # items.append(item)
        # return item, 201
    
    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        # #cambia de 'get_jwt_claims()' a solamente 'get_jwt()' según documentación actual
        # claims = get_jwt()
        # #Si lo que retorna no es 'is_admin', entonces se arroja mensaje de error
        # if not claims['is_admin']:
        #     return {'message': 'Se requieren privilegios de administrador.'}, 401
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}
        return {'message': ITEM_NOT_FOUND}, 404
        
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item eliminado'}
    
    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            # item = ItemModel(name, **item_json)
            item_json['name'] = name
            item = item_schema.load(item_json)

        item.save_to_db()
        # return item.json()
        return item_schema.dump(item), 200
    
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
    @classmethod
    def get(cls):
        # user_id = get_jwt_identity()
        # items = [x.json() for x in ItemModel.find_all()]
        
        # if user_id:
        #     return {
        #         'items': items
        #         # 'items': list(map(lambda x: x.json(), ItemModel.query.all()))
        #     }, 200
        # return {'items': [x['name'] for x in items], 'message': 'Más información disponible si te logueas.'}
        # return {'items': [x.json() for x in ItemModel.find_all()]}, 200
        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200