'''
Aquest codi ha estat creat el juliol de 2023 per en P.G.T.

L'objectiu del codi és prendre les dades del fitxer output de l'aplicació Splitwise i fer un gràfic de les despeses de cada mes.
Les despeses s'agrupen segons les etiquetes de l'aplicació. A les primeres línies del codi l'usuari pot decidir quines despeses vol
dibuixar en línies independents i en quin color. Les despeses que no s'explicitin s'agruparan en una única línia si l'usuari ho desitja.

L'usuari pot decidir si vol un histograma amb la despesa mensual acumulada o no.

Els noms de les categories són els noms de les columnes del fitxer csv (en el meu cas, en castellà). Els noms que surten al gràfic es poden
escirure en català a categories_labels.

Tots els paràmetres que es poden canviar per l'usuari es troben des d'aquest punt fins a la línia de coixinets (#).
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline

# categories_dict = {'Entreteniment': ['Deportes', 'Juegos', 'Música', 'Películas'],
#                    'Menjar i beguda': ['Alimentos', 'Licor', 'Restaurantes'],
#                    'Casa':['Alquiler', 'Electrónica', 'Hipoteca', 'Mantenimiento', 'Mascotas', 'Muebles', 'Servicios', 'Suministros del hogar'],
#                    'Vida': ['Formación', 'Gastos médicos', 'Guardería', 'Impuestos', 'Regalos', 'Ropa', 'Seguro'],
#                    'Transports': ['Autobús/Tren', 'Avión', 'Bicicleta', 'Coche', 'Estacionamiento', 'Gasolina', 'Hotel', 'Taxi'],
#                    'Utilitats': ['Agua', 'Basura', 'Calefacción', 'Electricidad', 'Limpieza', 'TV/teléfono/Internet']}

# Fitxer amb les dades
filename = 'dades/despeses_agost23.csv'
#filename = 'dades/export_mostra.csv'

# Fitxer on es guarda el gràfic
savingfile = 'despeses_agost23.png'
#savingfile = 'despeses_mostra.png'

# Categories que volem respresentar a nivell individual
categories = ['Alimentos', 'Electricidad', 'Agua', 'Calefacción']
#categories = ['Alimentos', 'Restaurantes', 'Suministros del hogar', 'Licor']

# Etiquetes i colors de les categories
categories_labels = ['Aliments', 'Llum', 'Aigua', 'Gas']
categories_colors = ['forestgreen', 'yellow', 'royalblue', 'orangered', 'purple']
#categories_labels = ['Aliments', 'Restaurants', 'Subministraments de la llar', 'Licor']
#categories_colors = ['forestgreen', 'violet', 'darkcyan', 'royalblue', 'purple']

# Escriure True si es volen agrupar les despeses de les categories no explicitades en una única línia. Altrament, escriure False
altres = True

# Escriure True si es vol un histograma al fons amb la despesa total de cada mes. Altrament, escriure False
histogram = True

# Nom de la columna de despeses, cateogria i data al fitxer de dades
despeses_col = 'Coste'
categoria_col = 'Categoría'
data_col = 'Fecha'

# Definir ylabels
ylabel = r'Despesa mensual (€)'
ylabel2 = r'Despesa mensual acumulada (€)'

################################################################
################################################################

# Etiquetes dels mesos
mesos_labels = ['Gen', 'Feb', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Des']

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
        cat_name = 'Altres'
        cat_color = categories_colors[-1]

    # Array on hi guardarem els mesos (eix x) que representarem
    # Ho fem a partir de la columna 'Nombre mes' per tenir totes les entrades amb un mateix mes de referència
    ref_mes = data[mask_cat]['Nombre mes'].drop_duplicates().min()  # Primer mes del qual hi ha entrades
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
