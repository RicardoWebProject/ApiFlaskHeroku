# from marshmallow import Schema, fields

from ma import ma
from models.user import UserModel
from marshmallow import pre_dump

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        # load_instance = True
    
    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user

# class UserSchema(Schema):
#     class Meta:
#         load_only = ('password',)   #Deberá de ser una tupla
#         dump_only = ('id',)
    
#     id = fields.Int()
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)