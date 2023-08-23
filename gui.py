import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from despeses_splitwise_en import process_data


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def browse_save_location():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Files', '*.png')])
    save_entry.delete(0, tk.END)
    save_entry.insert(0, save_path)

def execute():
    filename = file_entry.get()
    savingfile = save_entry.get()
    altres = altres_var.get()
    histogram = histogram_var.get()
    process_data(filename=filename,savingfile=savingfile,altres=altres,histogram=histogram)
    messagebox.showinfo("Success", "Graph created successfully!")

# Crear la ventana principal
root = tk.Tk()
root.title("Expense Analyzer")

# Crear y colocar los widgets en la ventana
file_label = tk.Label(root, text="Select Data File:")
file_label.pack()

file_entry = tk.Entry(root, width=40)
file_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

save_label = tk.Label(root, text="Select Save Location:")
save_label.pack()

save_entry = tk.Entry(root, width=40)
save_entry.pack()

browse_save_button = tk.Button(root, text="Browse", command=browse_save_location)
browse_save_button.pack()

altres_var = tk.IntVar()
altres_checkbox = tk.Checkbutton(root, text="Show Other Categories", variable=altres_var)
altres_checkbox.pack()

histogram_var = tk.IntVar()
histogram_checkbox = tk.Checkbutton(root, text="Show Cumulative Expense Histogram", variable=histogram_var)
histogram_checkbox.pack()

execute_button = tk.Button(root, text="Execute", command=execute)
execute_button.pack()

# Iniciar el loop principal de la GUI
root.mainloop()
