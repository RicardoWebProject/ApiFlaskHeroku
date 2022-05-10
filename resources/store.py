from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

NAME_ALREADY_EXISTS = 'Una tienda con el nombre "{}" ya existe.'
STORE_NOT_FOUND = 'Tienda no econtrada'
ERROR_INSERTING = 'Ha ocurrido un error ingresando la tienda.'
STORE_DELETED = 'Tienda eliminada.'

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            # return store.json()
            return store_schema.dump(store), 200
        return {'message': STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        # store = StoreModel(name)
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': STORE_DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores': store_list_schema.dump(StoreModel.find_all())}
        # return {'stores': [x.json() for x in StoreModel.find_all()]}
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}