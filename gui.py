# from despeses_splitwise_en import process_data
from dependencies.gui_assembler import *
from dependencies.gui_functionalities import *

#categories_dict = {'Entreteniment': ['Deportes', 'Juegos', 'Música', 'Películas'],
#                   'Menjar i beguda': ['Alimentos', 'Licor', 'Restaurantes'],
#                   'Casa':['Alquiler', 'Electrónica', 'Hipoteca', 'Mantenimiento', 'Mascotas', 'Muebles', 'Servicios', 'Suministros del hogar'],
#                   'Vida': ['Formación', 'Gastos médicos', 'Guardería', 'Impuestos', 'Regalos', 'Ropa', 'Seguro'],
#                   'Utilitats': ['Agua', 'Basura', 'Calefacción', 'Electricidad', 'Limpieza', 'TV/teléfono/internet'],
#                   'Transports': ['Autobús/Tren', 'Avión', 'Bicicleta', 'Coche', 'Estacionamiento', 'Gasolina', 'Hotel', 'Taxi']}

if __name__ == "__main__":

    #translations_datafile = load_translations(lang, 'languages_datafile.json')
    root = tk.Tk()

    frame_input, frame_categories, frame_plot = create_frames(root)

    # create a combobox
    lang = tk.StringVar()
    lang.set('ca') # Llengua per defecte
    # AQUÍ HI INTRODUIRÍEM UN WIDGET PER TRIAR L'IDIOMA DE LA FINESTRETA

    #output_language = output_language_widget(root, frame_input, lang)
    #input_language = input_language_widget(root, frame_input, lang)

    # Creem i col·loquem els widgets a la finestra
    file_entry, save_entry, input_language, output_language = create_inputs(frame_input, lang)
    altres_var, histogram_var, checkbox_vars, group_vars = create_categories(frame_categories, lang)
    create_commander(frame_plot, lang, input_language, output_language, file_entry, save_entry, altres_var, histogram_var, group_vars, checkbox_vars)

    translations_gui = load_translations(lang, 'languages_gui.json')
    root.title(translations_gui.get("títol"))

    # Iniciar el loop principal de la GUI
    root.mainloop()
