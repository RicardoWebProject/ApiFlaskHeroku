"""
libs.strings

Por default, utiliza el archivo 'es-gt.json', dentro de la carpeta superior llamada 'strings'.

Si el lenguaje cambia, coloca 'libs.strings.default_locale' y corre 'libs.strings.refresh()'
"""

import json

default_locale = 'es-gt'
cached_strings = {}

def refresh():
    global cached_strings
    with open(f'strings/{default_locale}.json') as f:
        cached_strings = json.load(f)

def gettext(name):
    return cached_strings[name]

# def set_default_locale(locale):
#     global default_locale
#     default_locale = locale

refresh()