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
import matplotlib
import pandas as pd
from scipy.interpolate import make_interp_spline
from functions import load_translations, categories_colors, groups_colors
from categories_dictionaries import categories_dict, languages_months

def process_data(filename,savingfile, input_language, output_language, groups_bool, categories_bool, altres = True,histogram = True, language = 'ca')->int:
    try:

        # Carreguem el diccionari de traduccions en català. És per poder relacionar categories_dict amb translations
        # ES PODRIA PRESCINDIR D'AQUESTA LÍNIA SI UNIFIQUÉSSIM LES keys DELS DICCIONARIS, CREC
        translations_cat = load_translations(output_language, 'languages_categories.json')

        # Data file
        groups = [] #Grups sencers per pintar. Hi guardem els noms del grups
        categories = [] # Categories individuals per pintar. Hi guardem els noms de les categories
        for group in groups_bool.keys():
            if groups_bool[group] == True:
                groups.append(str(group)) #Nom del grup sencer que volem pintar
            else:
                 # Si no pintem el grup sencer, apuntem les categories individuals que pintem
                 # selected és una llista dels noms de les categories si el seu corresponent bool és True
                 selected = [a for a, b in zip(categories_dict[group], categories_bool[group].values()) if b]
                 if selected:
                     for categoria in selected:
                         categories.append([i for i in translations_cat.keys() if translations_cat[i] == categoria][0]) #Guardem a la llista categories

        ## Individual categories to plot
        # categories conté el nom de les keys dels diccionaris

        # Categories labels
        translations_gui = load_translations(output_language, 'languages_categories.json') #output_language must be tk.StrVar()
        categories_labels = [translations_gui[categoria] for categoria in categories]

        # Categories colors
        cmap = matplotlib.cm.get_cmap('Accent')
        #categories_colors = cmap(np.linspace(0, 1, len(categories)))
        #groups_colors = cmap(np.linspace(0, 1, len(groups)))

        # Expenses, categories and date column label in the datafile
        translations_datafile = load_translations(input_language, 'languages_inputfile.json')
        despeses_col = translations_datafile['Coste']
        categoria_col = translations_datafile['Categoria']
        data_col = translations_datafile['Fecha']

        # Define the ylabels
        translations_axis = load_translations(output_language, 'languages_output.json')
        ylabel = translations_axis['y1axis']
        ylabel2 = translations_axis['y2axis']

        # Months labels
        #mesos_labels = load_translations(language, 'languages_months.json')
        mesos_labels = languages_months[output_language.get()]

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
        if histogram:
            fig, axs = plt.subplots(figsize = (10, 12), ncols = 1, nrows = 2, sharex = True)
            plt.subplots_adjust(hspace=0)
            axs = axs.flatten()
            ax = axs[0]

        else:
            fig, ax = plt.subplots(figsize = (10, 5))

        if altres:
            ncategories = len(categories) + 1
        else:
            ncategories = len(categories)

        ### PINTEM GRUPS
        if groups:
            for group in groups:
                group_categories = categories_dict[group]
                categories_g = []
                for categoria in group_categories:
                    # Guardem els noms de les categories del grup. Els noms són tal i com surten al fitxer Splitwise
                    categories_g.append([i for i in translations_cat.keys() if translations_cat[i] == categoria][0])

                # Màscara que tria totes les entrades d'aquest grup
                mask_group = data[categoria_col].isin(categories_g)
                group_name = group # Potser s'ha de canviar això
                group_color = groups_colors[group]

                # Array on hi guardarem els mesos (eix x) que representarem
                ref_mes = data[mask_group]['Nombre mes'].drop_duplicates().min()  # Primer mes del qual hi ha entrades
                if np.isnan(ref_mes):  # Si no es pot determinar ref_mes és perquè no hi ha entrades d'aquest group
                    continue

                entrades = np.full(nmesos + ref_mes, np.nan)
                despeses = np.full(nmesos + ref_mes, np.nan)
                for mes in (data[mask_group]['Nombre mes'].drop_duplicates()):
                    mask_mes = (data[mask_group]['Nombre mes']) == mes

                    entrades[mes] = mes  # + ref_mes # Mes del qual hi tenim entrada

                    # Sumem les despeses d'aquest mes
                    despesa = data[mask_group][mask_mes][despeses_col].astype(float).sum()

                    # Si no hi ha entrades, la suma és 0 i ho passem a nan
                    if despesa == 0.:
                        despesa = np.nan

                    # Guardem la despesa d'aquest mes a l'array de despeses de la categoria
                    despeses[mes] = despesa

                remove_nan = ~np.isnan(entrades)
                entrades, despeses = entrades[remove_nan], despeses[remove_nan]

                # Fem spline
                try:
                    X_Y_Spline = make_interp_spline(entrades, despeses)  # Creem instància de spline
                    x_ = np.linspace(0., data[mask_group]['Nombre mes'].max(),
                                     1000)  # Fem 500 punts entre els punts de les entrades
                    y_ = X_Y_Spline(x_)  # Retorna els punts y corresponents als punts x que hem creat
                    ax.plot(x_, y_, '--', color=group_color, zorder=1)  # Dibuix spline
                except:
                    ax.plot(entrades, despeses, '--', color=group_color)  # Dibuix plot recte

                # Dibuixem les línies d'aquest grup
                ax.scatter(entrades, despeses, label=group_name, facecolor=group_color, marker='s', edgecolor='k', zorder=1)


        # Pintarem una línia per cada categoria (3 categories i una d'agrupació entre les que sobren)
        for categoria in range(ncategories):
            # Creem les màscares i els labels de la categoria
            if categoria != (len(categories)):
                mask_cat = data[categoria_col] == categories[categoria]
                cat_name = categories_labels[categoria]
                cat_color = categories_colors[categories[categoria]]

            else:
                mask_cat = ~data[categoria_col].isin(categories)
                cat_name = translations_gui['Altres']
                cat_color = '#ffa07a'


            # Array on hi guardarem els mesos (eix x) que representarem
            # Ho fem a partir de la columna 'Nombre mes' per tenir totes les entrades amb un mateix mes de referència
            ref_mes = data[mask_cat]['Nombre mes'].drop_duplicates().min()  # Primer mes del qual hi ha entrades
            if np.isnan(ref_mes): #Si no es pot determinar ref_mes és perquè no hi ha entrades d'aquesta categoria
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
                ax.plot(x_, y_, '--', color=cat_color, zorder = 1) # Dibuix spline
            except:
                ax.plot(entrades, despeses, '--', color=cat_color)  # Dibuix plot recte

            # Dibuixem les línies d'aquesta categoria
            ax.scatter(entrades, despeses, label=cat_name, facecolor= cat_color, edgecolor='k', zorder = 1)

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
            ax2 = axs[1]
            #ax2 = ax.twinx()
            ax2.set_zorder(0)
            ax2.patch.set_visible(False)  # Hide the 'background' subplot
            ax2.set_zorder(1)  # zorder general. Això és per si després hi posem un secondary axis

            ax2.bar(entrades, despeses_tot, edgecolor='sandybrown', linewidth=3, facecolor='white', zorder = 0, alpha = 0.6)
            for entrada in range(len(entrades)):
                despesa_mensual = "{:.2f}".format(despeses_tot[entrada])
                ax2.text(entrades[entrada], despeses_tot[entrada]/2, despesa_mensual, rotation='vertical',
                         verticalalignment = 'center', horizontalalignment = 'center')
            ax2.set_ylabel(ylabel2)

        mes_idx = data['Mes'][data['Any'] == data['Any'].min()].min() - 1
        ticklabels = np.full(nmesos, 'MES\nANY_')

        mes_compt = mes_idx
        any_compt = 0
        for nmes in range(nmesos):
            if nmes == 0: # primer element del qual hi ha dades
                label = f"{mesos_labels[mes_compt]}\n{data['Any'].min() + any_compt}"
            elif mes_compt == 0:  # mes de gener (posem l'any)
                label = f"{mesos_labels[mes_compt]}\n{data['Any'].min() + any_compt}"
            else: # qualsevol altre mes
                label = f"{mesos_labels[mes_compt]}"
            ticklabels[nmes] = label
            mes_compt += 1
            if mes_compt > 11:
                mes_compt = 0
                any_compt += 1

        # Paràmetres del plot
        ax.legend()
        ax.set_xticks(np.arange(nmesos))
        ax.hlines(0, 0, nmesos, colors = 'black', linestyles='solid', alpha=0.7, zorder = 0)
        if histogram:
            ax.set_xticklabels([])
            ax2.set_xticks(np.arange(nmesos))
            ax2.set_xticklabels(ticklabels)
        else:
            ax.set_xticklabels(ticklabels)

        ax.set_ylabel(ylabel)

        # Mostrem la figura
        #plt.show()

        # Guardem la figura
        plt.savefig(savingfile, dpi = 300, bbox_inches ='tight')
        plt.clf()

        return 0

    except Exception:
        print("Hi ha hagut algun error al codi :(")
        return 1
