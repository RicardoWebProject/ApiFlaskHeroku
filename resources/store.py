from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Tienda no encontrada'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Una tienda con el nombre: {name} , ya existe.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "Ocurrio un error creando la tienda"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Tienda eliminada.'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}