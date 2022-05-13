# from marshmallow import Schema, fields

from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "activated")
        load_instance = True

# class UserSchema(Schema):
#     class Meta:
#         load_only = ('password',)   #Deberá de ser una tupla
#         dump_only = ('id',)
    
#     id = fields.Int()
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)