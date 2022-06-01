import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet('images', IMAGES) #Setea el nombre y las extensiones permitidas


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Tomará el almacenamiento de archivos y los guardará en una carpeta."""
    return IMAGE_SET.save(image, folder, name)

def get_path(filename: str = None, folder: str = None) -> str:
    """Tomará el nombre de la imagen y el directorio, y retornará el path completo."""
    return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Tomará el nombre de archivo y retornará una imagen en cualquiera de los formatos aceptados."""
    for _format in IMAGES:
        image = f'{filename}.{_format}'
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None

def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """
        Tomará un listado de FileStorage y retornará el nombre del archivo.
        Permitirá a nuestras funciones llamar llamar a los filenames y FileStorage y siempre obtener de vuelta un nombre de archivo.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file

def is_filename_safe(file: Union[str, FileStorage]) -> str:
    """Revisará nuestra expresión regular y retornará si la cadena hace match o no."""
    filename =_retrieve_filename(file)
    allowed_format = '|'.join(IMAGES)   #png|svg|jpe|jpg...
    regex = f'^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$'
    return re.match(regex, filename) is not None

def get_basename(file: Union[str, FileStorage]) -> str:
    """Retornará el nombre completo de la imagen en el path"""
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file: Union[str, FileStorage]) -> str:
    """Retornará la extensión de la imagen."""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
    
    