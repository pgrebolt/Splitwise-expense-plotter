import json
from dependencies.gui_functionalities import *
import tkinter as tk
#import mediator
from dependencies.categories_dictionaries import categories_dict

def create_frames(root):

    # Inicialitzem els frames
    frame_input = tk.Frame(root)
    frame_categories = tk.Frame(root) # button
    frame_plot = tk.Frame(root, borderwidth=5, relief='ridge')#, width=2000, height=2000)

    # Ordenem els frames a la finestra
    frame_input.grid(row = 0, column = 0, padx=5, pady=5, sticky="nsew")
    frame_categories.grid(row = 0, column = 1, padx=5, pady=5, sticky="nsew")
    frame_plot.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5, sticky="nsew")

    return frame_input, frame_plot, frame_categories

def input_language_widget(frame, lang):
    '''
    :param root:
    :param frame:
    :param lang: language to show the label
    :return: user selects the language of the input file (depends on Splitwise version). Stored as tk.StringVar() variable
    '''

    # Carreguem les opcions de llengües
    languages_available = get_languages('json_files/languages_inputfile.json')
    translations_gui = load_translations(lang, 'json_files/languages_gui.json')

    # Variable on hi guardem l'idioma seleccionat
    input_language = tk.StringVar()

    # Finestra desplegable amb els idiomes disponibles
    lang_combobox = ttk.Combobox(frame, textvariable=input_language)
    lang_combobox['values'] = languages_available
    lang_combobox['state'] = 'readonly'
    lang_combobox.set('es') # Valor per defecte
    lang_combobox.grid(row =0, column=1, padx=10, pady=5)

    # Text indicatiu
    language_label = tk.Label(master=frame, text=translations_gui["llengua_input"])
    language_label.grid(row=0, column=0, padx=10, pady=5)

    return input_language

def output_language_widget(frame, lang):

    # Carreguem les opcions de llengües
    languages_available = get_languages('json_files/languages_output.json')
    translations_gui = load_translations(lang, 'json_files/languages_gui.json')

    # Variable on hi guardem l'idioma seleccionat
    output_language = tk.StringVar()

    # Finestra desplegable amb els idiomes disponibles
    lang_combobox = ttk.Combobox(frame, textvariable=output_language)
    lang_combobox['values'] = languages_available
    lang_combobox['state'] = 'readonly'
    lang_combobox.set('ca') # Valor per defecte
    lang_combobox.grid(row=1, column=1, padx=10, pady=5)

    # Text indicatiu
    language_label = tk.Label(master=frame, text=translations_gui["llengua_output"])
    language_label.grid(row=1, column=0, padx=10, pady=5)

    return output_language
def create_inputs(frame, lang):
    # Carreguem el fitxer d'idiomes
    translations_gui = load_translations(lang, 'json_files/languages_gui.json')

    input_language = input_language_widget(frame, lang) #CAL POSAR-LOS A LLOC
    output_language = output_language_widget(frame, lang)

    file_label = tk.Label(master=frame, text=translations_gui.get("cerca_label"))
    file_label.grid(row=2, column=0, padx=10, pady=5)

    file_entry = tk.Entry(master=frame, width=40)
    file_entry.grid(row=2, column=1, padx=10, pady=5)

    browse_button = tk.Button(master=frame, text=translations_gui.get("boto_cerca"), command=lambda: browse_file(file_entry),
                              cursor="hand2")
    browse_button.grid(row=2, column=2, padx=10, pady=5)

    save_label = tk.Label(master=frame, text=translations_gui.get("salva_label"))
    save_label.grid(row=3, column=0, padx=10, pady=5)

    save_entry = tk.Entry(master=frame, width=40)
    save_entry.grid(row=3, column=1, padx=10, pady=5)

    browse_save_button = tk.Button(master=frame, text=translations_gui.get("boto_cerca"), command=lambda:browse_save_location(save_entry),
                                   cursor="hand2")
    browse_save_button.grid(row=3, column=2, padx=10, pady=5)

    return file_entry, save_entry, input_language, output_language

def create_categories(frame, lang):
    # Carreguem el fitxer d'idiomes
    translations_gui = load_translations(lang, 'json_files/languages_gui.json')

    altres_var = tk.IntVar()
    altres_checkbox = tk.Checkbutton(master = frame, text=translations_gui.get("altrescat_label"), variable=altres_var)
    altres_checkbox.grid(row=0, column=0, columnspan=2)

    histogram_var = tk.IntVar()
    histogram_checkbox = tk.Checkbutton(master = frame, text=translations_gui.get("acum_label"), variable=histogram_var)
    histogram_checkbox.grid(row=0, column=3, columnspan=2)

    #checkbox_vars = categories_boxer(frame, categories_dict)
    checkbox_vars, group_vars = create_grouped_checkboxes(frame, categories_dict)

    # SEGUIR DES D'AQUÍ. HE POSAT EL DICCIONARI AMB LES CATEGORIES EN UN PY A PART. S'HAURÀ DE CANVIAR AL LLARG DEL CODI AQUESTA
    # REFERÈNCIA, PERÒ ENS PERMET CREAR ELS CHECKBOXES PER GRUPS I TAMBÉ CANVIAR L'IDIOMA DE L'OUTPUT SI S'HI REFEREIX

    return altres_var, histogram_var, checkbox_vars, group_vars

def create_commander(frame, lang, inlang, outlang, file_entry, save_entry, altres_var, histogram_var, group_vars, checkbox_vars):
    # Carreguem el fitxer d'idiomes
    translations_gui = load_translations(lang, 'json_files/languages_gui.json')

    # Botó d'executar la funció que fa el dibuix
    execute_button = tk.Button(master = frame, text=translations_gui.get("boto_executar"),
                                command=lambda:execute(file_entry, save_entry, inlang, outlang, altres_var,
                                                       histogram_var, group_vars, checkbox_vars, lang),
                               cursor="hand2", padx = 15, pady = 10)
    execute_button.place(relx=0., rely=0.5)
    # execute_button.pack(side=tk.TOP)
    # execute_button.grid(row=0, column=0)

# Per canviar l'idioma de la finestra
#def language_widget(root, frame, lang):
    # Carreguem les opcions de llengües
    # languages_available = get_languages('languages_gui.json')
    # translations_gui = load_translations(lang, 'languages_gui.json')
    #
    # lang_combobox = ttk.Combobox(frame, textvariable=lang)
    # lang_combobox['values'] = languages_available
    # lang_combobox['state'] = 'readonly'
    # lang_combobox.grid(row =0, column=1, padx=10, pady=5)
    # lang_combobox.bind("<<ComboboxSelected>>", lambda event, root = root, lang_combobox=lang_combobox:mediator.change_language(event, root, lang_combobox)) # Canviem l'idioma
    #
    # # Tria de llengua
    # language_label = tk.Label(master=frame, text=translations_gui.get("ca", "Idioma"))
    # language_label.grid(row=0, column=0, padx=10, pady=5)
    #
    # return lang
