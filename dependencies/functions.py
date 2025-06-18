import json
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def load_translations(lang, langfile):
    with open(resource_path(langfile), "r", encoding="utf-8") as file:
        translations = json.load(file)
    try:
        dict = translations.get(lang.get(), {})
    except:
        # Per si lang és una string
        dict = translations.get(lang, {})
    return dict

def get_python_bool_values(checkbox_vars):
    python_bool_values = {}
    for key in checkbox_vars.keys():
        python_bool_values[key] = {}
        for cat, var in checkbox_vars[key].items():
            python_bool_values[key][cat] = var.get() == 1
    return python_bool_values

def get_python_bool_values_groups(groups_vars):
    # Aquesta funció crea un diccionari on cada key es un dels grups i el seu valor és un True/False.
    # Ho crea a partir dels True/False de TKinter
    python_bool_values = {}
    for key in groups_vars.keys():
        python_bool_values[key] = groups_vars[key].get()
    return python_bool_values

def get_languages(langfile):
    with open(resource_path(langfile), "r", encoding="utf-8") as file:
        translations = json.load(file)
    return list(translations.keys())

categories_colors = {
    "Deportes": "#ff7f50",  # Coral
    "Juegos": "#ff1493",    # Deep Pink
    "Música": "#ff69b4",    # Hot Pink
    "Películas": "#dc143c",  # Crimson
    "Alimentos": "#32cd32",  # Lime Green
    "Licor": "#adff2f",      # Green Yellow
    "Restaurantes": "#008000",  # Green
    "Alquiler": "#ff0000",   # Red
    "Electrónica": "#ff6347",  # Tomato
    "Hipoteca": "#dc143c",    # Crimson
    "Mantenimiento": "#b22222",  # Fire Brick
    "Mascotas": "#ff4500",   # Orange Red
    "Muebles": "#8b0000",    # Dark Red
    "Servicios": "#e74c3c",  # Indian Red
    "Suministros del hogar": "#cd5c5c",  # Indian Red
    "Formación": "#4169e1",  # Royal Blue
    "Gastos médicos": "#0000cd",  # Medium Blue
    "Guardería": "#000080",  # Navy
    "Impuestos": "#1e90ff",  # Dodger Blue
    "Regalos": "#87cefa",    # Light Sky Blue
    "Ropa": "#6495ed",       # Cornflower Blue
    "Seguro": "#4682b4",      # Steel Blue
    "Agua": "#0000ff",        # Blue
    "Basura": "#00bfff",      # Deep Sky Blue
    "Calefacción": "#87ceeb",  # Sky Blue
    "Electricidad": "#add8e6",  # Light Blue
    "Limpieza": "#1e90ff",    # Dodger Blue
    "TV/teléfono/internet": "#4682b4",  # Steel Blue
    "Autobús/Tren": "#ff1493",   # Deep Pink
    "Avión": "#ff69b4",          # Hot Pink
    "Bicicleta": "#dc143c",      # Crimson
    "Coche": "#9b59b6",          # Amethyst
    "Estacionamiento": "#32cd32",  # Lime Green
    "Gasolina": "#adff2f",       # Green Yellow
    "Hotel": "#008000",          # Green
    "Taxi": "#008080",            # Teal
    "Altres": "#ffffff"
}

groups_colors = {'Entreteniment': "#ff7f50",  # Coral
                'Menjar i beguda': "#008000",  # Green
                   'Casa':"#ff6347",  # Tomato
                   'Vida':  "#4169e1",  # Royal Blue
                   'Despeses de la llar': "#00bfff",      # Deep Sky Blue
                   'Transports':  "#ff1493" # Deep Pink
                 }
