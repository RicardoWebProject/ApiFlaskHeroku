from ma import ma
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only= ('store',)
        dump_only = ('id', )
        #Para incluir llaves foráneas
        include_fk = True
        load_instance = True