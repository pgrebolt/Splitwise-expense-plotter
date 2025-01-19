'''
This codefile has been created on July 2023 by P.G.T.

The goal of this code is to take the data from the output file of the Splitwise mobile app and plot the monthly expenses.
Expenses are grouped based on the app labels. In the first lines of the code the user can define which expenses to plot and their color
The non-defined expenses can be grouped in a single line of the plot

The user can decide if they want a background histogram with the monthly cumulative expense.

The name of the categories are the .csv file column labels (in my case, in Spanish). However, the user can define the new labels as desired.

All the lines that may be changed by the user are found up to the hashtags (#) line.
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline

# Data file
filename = 'export_mostra.csv'

# Saving file
savingfile = 'expenses.png'

# Individual categories to plot
categories = ['Alimentos', 'Restaurantes', 'Suministros del hogar']

# Categories colors and labels
categories_labels = ['Groceries', 'Restaurants', 'Household supplies']
categories_colors = ['forestgreen', 'red', 'blue', 'purple']

# Write True if you want to show all the other categories in a single plot. Otherwise, write False
altres = True

# Write True if you want to show a histogram plot with the cummulative monthly expense. Otherwise, write False
histogram = True

# Expenses, categories and date column label in the datafile
despeses_col = 'Coste'
categoria_col = 'Categoría'
data_col = 'Fecha'

# Define the ylabels
ylabel = r'Monthly expense (€)'
ylabel2 = r'Cummulative monthly expense (€)'

# Months labels
mesos_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

################################################################
################################################################


# Llegim i tractem les dades
data = pd.read_csv(filename, sep=',')
data = data.drop(index= (data.shape[0]-1)) # Treiem l'última fila, que té el saldo total

# Columna amb el mes i any de cada entrada
data['Mes'] = pd.to_datetime(data[data_col]).dt.month #Número del mes
data['Any'] = pd.to_datetime(data[data_col]).dt.year # Número de l'any
data['Mes_nom'] = pd.to_datetime(data[data_col]).dt.strftime('%b') #Nom del mes
data['Nombre mes'] = (data['Any'] - data['Any'].min()) * 12 + \
                     (data['Mes'] - data[data['Any'] == data['Any'].min()]['Mes'].min()) # Columna amb el nombre de mes assignat a cada entrada (nombre d'entrada)

# Comptador de nombre de mesos entre la primera i última entrada de cada categoria
nmesos = data['Nombre mes'].max() + 1 # Nombre de mesos que abarca el plot

#Creem la figura
fig, ax = plt.subplots(figsize = (10, 5))

if altres:
    ncategories = len(categories) + 1
else:
    ncategories = len(categories)

# Pintarem una línia per cada categoria (3 categories i una d'agrupació entre les que sobren)
for categoria in range(ncategories):
    # Creem les màscares i els labels de la categoria
    if categoria != (len(categories)):
        mask_cat = data[categoria_col] == categories[categoria]
        cat_name = categories_labels[categoria]
        cat_color = categories_colors[categoria]
    else:
        mask_cat = ~data[categoria_col].isin(categories)
        cat_name = 'Other'
        cat_color = categories_colors[-1]

    # Array on hi guardarem els mesos (eix x) que representarem
    # Ho fem a partir de la columna 'Nombre mes' per tenir totes les entrades amb un mateix mes de referència
    ref_mes = data[mask_cat]['Nombre mes'].drop_duplicates().min()  # Primer mes del qual hi ha entrades
    if np.isnan(ref_mes):  # Si no es pot determinar ref_mes és perquè no hi ha entrades d'aquesta categoria
        continue
    entrades = np.full(nmesos+ref_mes, np.nan)
    despeses = np.full(nmesos+ref_mes, np.nan)
    for mes in (data[mask_cat]['Nombre mes'].drop_duplicates()):
        mask_mes = (data[mask_cat]['Nombre mes']) == mes

        entrades[mes] = mes #+ ref_mes # Mes del qual hi tenim entrada

        # Sumem les despeses d'aquest mes
        despesa = data[mask_cat][mask_mes][despeses_col].astype(float).sum()

        # Si no hi ha entrades, la suma és 0 i ho passem a nan
        if despesa == 0.:
            despesa = np.nan

        # Guardem la despesa d'aquest mes a l'array de despeses de la categoria
        despeses[mes] = despesa

    remove_nan = ~np.isnan(entrades)
    entrades, despeses = entrades[remove_nan], despeses[remove_nan]

    # Fem spline
    try:
        X_Y_Spline = make_interp_spline(entrades, despeses) # Creem instància de spline
        x_ = np.linspace(0., data['Nombre mes'][mask_cat].max(), 1000) # Fem 500 punts entre els punts de les entrades
        y_ = X_Y_Spline(x_) # Retorna els punts y corresponents als punts x que hem creat
        ax.plot(x_, y_, '--', c=cat_color, zorder = 1) # Dibuix spline
    except:
        ax.plot(entrades, despeses, '--', c=cat_color)  # Dibuix plot recte

    # Dibuixem les línies d'aquesta categoria
    ax.scatter(entrades, despeses, label=cat_name, c= cat_color, zorder = 1)

## Histograma
if histogram:
    ref_mes = data['Nombre mes'].drop_duplicates().min() # Primer mes del qual hi ha entrades
    despeses_tot = np.full(nmesos+ref_mes, np.nan) #Array on hi guardarem les despeses totals de cada mes
    entrades = np.full(nmesos+ref_mes, np.nan) # Array on hi guardem el nombre de mes que es representa

    for mes in (data['Nombre mes'].drop_duplicates()): # Per cada mes del qual hi ha entrada
        mask_mes = data['Nombre mes'] == mes # Per triar el mes corresponent
        entrades[mes] = mes #+ ref_mes # Mes del qual hi tenim entrada
        despeses_tot[mes] = data[mask_mes][despeses_col].astype(float).sum() # Guardem la despesa total del mes

    # Figura
    ax2 = ax.twinx()
    ax2.set_zorder(0)
    ax.patch.set_visible(False)  # Hide the 'background' subplot
    ax.set_zorder(1)  # zorder general. Això és per si després hi posem un secondary axis

    ax2.bar(entrades, despeses_tot, edgecolor='sandybrown', linewidth=3, facecolor='white', zorder = 0, alpha = 0.6)
    ax2.set_ylabel(ylabel2)

mes_idx = data['Mes'][data['Any'] == data['Any'].min()].min() -1 # Li treiem 1 perquè Gen = 0, Feb = 1, Jul = 6 a mesos_labels
ticklabels = np.full(nmesos, 'MES\nANY_') # Cal que l'string contingui els mateixos caràcters que tindrà el label
for nmes in range(nmesos):
    label = str(str(mesos_labels[mes_idx]) +'\n'+ str(data['Any'].min() + (nmes + (mes_idx)) // 12))
    ticklabels[nmes] = label
    mes_idx += 1
    if mes_idx > 11:
        mes_idx = 0

# Paràmetres del plot
ax.legend()
ax.set_xticks(np.arange(nmesos))
ax.set_xticklabels(ticklabels)
ax.set_ylabel(ylabel)

# Guardem la figura
plt.savefig(savingfile, dpi = 300, bbox_inches ='tight')
