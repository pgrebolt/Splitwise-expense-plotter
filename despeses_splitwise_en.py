'''
This codefile has been created on July 2023 by P.G.T.

The goal of this code is to take the data from the output file of the Splitwise mobile app and plot the monthly expenses.
Expenses are grouped based on the app labels. In the first lines of the code the user can define which expenses to plot and their color
The non-defined expenses can be grouped in a single line of the plot

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

# Expenses, categories and date column label in the datafile
despeses_col = 'Coste'
categoria_col = 'Categoría'
data_col = 'Fecha'

# Define the ylabel
ylabel = r'Despesa total (€)'

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

# Comptador de nombre de mesos entre la primera i última entrada de cada categoria
nmesos0 = 0 # Nombre de mesos que abarca el plot (ho reescriurem més endavant)
nmes0 = 6 # Número de mes del primer mes del qual hi ha registre (ho reescriurem més endavant)

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

    # Nombre de mesos entre el primer i últim dia d'entrades
    nmesos = (pd.to_datetime(data[data_col][mask_cat]).max().year - pd.to_datetime(data[data_col][mask_cat]).min().year) * 12 + \
             (pd.to_datetime(data[data_col][mask_cat]).max().month - pd.to_datetime(data[data_col][mask_cat]).min().month) + 1

    # Array on hi guardarem els mesos (eix x) que representarem
    entrades = np.arange(nmesos)

    # Anys en els quals hi ha entrades d'aquesta categoria
    anys = data['Any'][mask_cat].drop_duplicates()

    # Array on hi guardarem les despeses a cada mes
    despeses = np.full(nmesos, np.nan)

    # Destriem el primer mes del qual hi ha entrada d'aquesta categoria
    min_any = data[mask_cat]['Any'].min() # Seleccionem el primer any del qual hi ha entrada
    mask_minany = np.where(data[mask_cat]['Any'] == data[mask_cat]['Any'].min()) # Màscara per triar aquelles entrades del primer any
    mes_min = data[mask_cat].iloc[mask_minany]['Mes'].min() # Primer mes de registre d'aquesta categoria. És el mes de referència

    # Columna amb el nombre de mes assignat a cada entrada (nombre d'entrada)
    nombre_mes = (data[mask_cat]['Any'] - min_any) * 12 + (data[mask_cat]['Mes'] - data[mask_cat][data[mask_cat]['Any'] == min_any]['Mes'].min())

    # Índex del mes (per connectar-ho amb l'array de nom de cada mes)
    mes_idx = mes_min - 1

    # Per cada mes del qual hi ha entrada (indep. de l'any), farem la suma de despeses d'aquesta categoria
    for nmes in range(nmesos):

        # Mask per triar totes les entrades d'aquest mes
        mask_nmes = nombre_mes == nmes

        # Creem un dataframe amb només aquelles entrades del mes que tractem ara
        df = data[mask_cat & mask_nmes]

        # Sumem les despeses d'aquest mes
        despesa = df[despeses_col].astype(float).sum()

        # Si no hi ha entrades, la suma és 0 i ho passem a nan
        if despesa == 0.:
            despesa = np.nan

        # Guardem la despesa d'aquest mes a l'array de despeses de la categoria
        despeses[nmes] = despesa

        # Si cal, guardem els noms dels mesos totals que abarca aquesta categoria
        if nmesos > nmesos0:
            nmesos0 = nmesos
            nmes0 = min(df['Mes'][df['Any'] == min(df['Any'])]) # Primer mes de la categoria

    # Fem spline
    X_Y_Spline = make_interp_spline(entrades, despeses) # Creem instància de spline
    x_ = np.linspace(entrades.min(), entrades.max(), 500) # Fem 500 punts entre els punts de les entrades
    y_ = X_Y_Spline(x_) # Retorna els punts y corresponents als punts x que hem creat

    ax.plot(x_, y_, '--', c=cat_color) # Dibuix spline

    # Dibuixem les línies d'aquesta categoria
    ax.scatter(entrades, despeses, label=cat_name, c= cat_color)
    #ax.plot(entrades, despeses, '--', c=cat_color) # Dibuix plot recte

mes_idx = nmes0 - 1 # Cal tenir en compte que mes_idx = 0 equival a 'Gen'
ticklabels = np.full(nmesos0, 'MES\nANY_') # Cal que l'string contingui els mateixos caràcters que tindrà el label
for nmes in range(nmesos0):
    label = str(str(mesos_labels[mes_idx]) +'\n'+ str(2023 + (nmes + (nmes0-1)) // 12))
    #label = str(2023 + (nmes + 6) // 12)
    ticklabels[nmes] = label
    mes_idx += 1
    if mes_idx > 11:
        mes_idx = 0


# Paràmetres del plot
ax.legend()
ax.set_xticks(np.arange(nmesos0))
ax.set_xticklabels(ticklabels)
ax.set_ylabel(ylabel)

# Guardem la figura
plt.savefig(savingfile, dpi = 300, bbox_inches ='tight')
