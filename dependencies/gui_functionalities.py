import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dependencies.functions import *
from dependencies.plotter import process_data
#import mediator

def categories_boxer(frame, dictionary):
    # Aquesta funció dibuixa les caixes de cada categoria que es vol dibuixar. Cada tipus de categoria anirà en una línia diferent
    checkbox_vars = {} # Diccionari on hi guardem la selecció de l'usuari
    ncol = 0 # Cada família en una columna
    for key in dictionary.keys():
        nrow = 1 # Cada categoria en una fila
        checkbox_vars[key] = {}
        for cat in dictionary[key]:
            cat_var = tk.BooleanVar() # Es guarda un bool
            cat_checkbox = tk.Checkbutton(master=frame, text=cat, variable=cat_var) # Caixeta i etiqueta
            cat_checkbox.grid(row = nrow, column = ncol, padx=5, pady=5, sticky='w') # Col·loquem la caixeta
            checkbox_vars[key][cat] = cat_var # Guardem la selecció al diccionari
            nrow +=1
        ncol +=1
    return checkbox_vars # Recuperem el diccionari

def create_grouped_checkboxes(frame, cat_dict):
    checkbox_vars = {}  # Dictionary to store checkbox variables
    group_vars = {}     # Dictionary to store group variables

    ncol = 0  # Each group in a column
    for group, categories in cat_dict.items():
        nrow = 1  # Each category in a row

        # Create a BooleanVar for the group
        group_var = tk.BooleanVar()
        group_var.set(False)  # Initialize as unchecked
        group_checkbox = tk.Checkbutton(
            master=frame, text=group, variable=group_var,
            command=lambda g=group: toggle_group(g, checkbox_vars, group_vars))
        group_checkbox.grid(row=nrow, column=ncol, padx=5, pady=5, sticky='w')

        # Initialize the group dictionary
        group_vars[group] = group_var # Guardem True/False al diccionari si el grup sencer és seleccionat
        checkbox_vars[group] = {} # Per cada grup fem un diccionari de True/False per apuntar-hi les categories seleccionades

        nrow += 1 # Perquè la caixa surti a la línia següent

        # Create checkboxes for categories within the group
        for cat in categories:
            cat_var = tk.BooleanVar()  # Create a BooleanVar for each category
            cat_checkbox = tk.Checkbutton(master=frame, text=cat, variable=cat_var) # Creem la caixeta
            cat_checkbox.grid(row=nrow, column=ncol, padx=35, pady=5, sticky='w') # Col·loquem la caixeta on toca

            # Store the checkbox variable in the dictionary
            checkbox_vars[group][cat] = cat_var # Guardem True/False al diccionari si la categoria és seleccioanda

            nrow += 1

        #ncol += 1
        # Línia vertical que separa categories
        #canvas = tk.Canvas(frame)
        #canvas.create_line(15, 15, 10, 200, width=5)
        #canvas.grid(row=1, column=ncol, rowspan=len(categories))

        ncol += 1

    return checkbox_vars, group_vars

def toggle_group(group, checkbox_vars, group_vars):
    # Toggle all checkboxes within the specified group
    group_checkbox_state = group_vars[group].get()
    for cat_var in checkbox_vars[group].values():
        cat_var.set(group_checkbox_state)


def browse_file(file_entry):
    # Funció per buscar un fitxer a través d'una finestra
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def browse_save_location(save_entry):
    # Funció per guardar un fitxer a través d'una finestra
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Files', '*.png')])
    save_entry.delete(0, tk.END)
    save_entry.insert(0, save_path)

def execute(file_entry, save_entry, input_language, output_language, altres_var, histogram_var, groups_bool, categories_bool, language):
    # Llegim les variables introduïdes
    filename = file_entry.get()
    savingfile = save_entry.get()
    altres = altres_var.get()
    histogram = histogram_var.get()
    categories_bool = get_python_bool_values(categories_bool) # Aquest comandament dins a execute fa que es prenguin els booleans de les caselles en el moment de l'execució del codi principal
    groups_bool = get_python_bool_values_groups(groups_bool) # Aquest comandament és igual que el de la línia anterior però adaptat al diccionari de grups
    lang = language

    # Executem el codi dibuixant
    success = process_data(filename=filename,savingfile=savingfile, input_language=input_language, output_language=output_language, groups_bool = groups_bool, categories_bool = categories_bool, altres=altres,histogram=histogram, language = lang)
    if success == 0:
        messagebox.showinfo("Final", "El gràfic ha estat dibuixat! :)") # Missatge que surt quan acaba el programa principal
    elif success == 1:
        messagebox.showinfo("Final", "Hi ha hagut un error al codi :(") # Missatge que surt quan acaba el programa principal

def change_language(event, root, lang):
    mediator.change_language(event, root, lang)