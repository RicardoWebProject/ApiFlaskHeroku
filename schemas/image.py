from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        'invalid': 'No es una imagen valida.'
    }
    
    def _deseralize(self, value, attr, data) -> FileStorage:
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            self.fail('invalid')    #Arroja un ValidationError
        
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)