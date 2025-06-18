# Splitwise expense plotter
*(English below)*

Tots els drets corresponents reservats a l'entitat Splitwise. // *All corresponding rights reserved to Splitwise company.*

## Índex / Table of contents 
1. [Objectiu](#objectiu) / [Goal](#goal)
2. [Instal·lació](#installacio) / [Installation](#installation)
3. [Com funciona el programa?](#com-funciona-el-programa) / [How does the program work?](#how-does-the-program-work)

## Objectiu
Aquest simple programa interactiu permet representar les despeses que hagis anotat a l'aplicació Splitwise (disponible a Android i a iOS).
Es pot dibuixar en un gràfic punts per veure com varien les despeses mensuals per cada categoria. També està preparat per dibuixar un gràfic de barres amb totes les despeses acumulades.

## Instal·lació
Si no tens Python instal·lat a l'ordinador, has de descarregar el fitxer executble. Entra dins de la carpeta `/dist` d'aquest repositori. Clica sobre el fitxer `gui.exe`. A la nova finestra, prem el botó amb tres puntets i descarrega el fitxer. Ubica'l dins el teu ordinador a la carpeta que vulguis. Ja ho tens tot a punt per obrir el programa.

Si tens Python descarregat a l'ordinador, pots seguir els passos anteriors o bé clonar aquest repositori. El programa principal és `gui.py`.

## Com funciona el programa?
A l'aplicació del teu mòbil, exporta el fitxer `.csv` amb les despeses i desa'l al teu ordinador.

Per obrir el programa, executa el fitxer `.exe`. Quan s'obri la finestra, podràs cercar el nom del fitxer que vols pintar (el que has exportat de Splitwise). També podràs escollir a quina carpeta el vols desar i amb quin nom.
Pots escollir en quin idioma es troba el fitxer que has extret de l'Splitwise i en quin idioma vols dibuixar el teu gràfic (EN PROVES).

Després, tria les categories que vols representar. Pots escollir si vols pintar una categoria o bé una temàtica, d'acord amb les classificacions de l'Splitwise.

També es pot pintar un histograma acumulatiu que inclou les despeses de cada mes.

Un cop s'han escollit totes les opcions, prem el botó "Dibuixa!" per poder veure el gràfic amb les opcions que has escollit. Quan tanquis la finestra es desarà el gràfic a la carpeta que has escollit.

Pots trobar un fitxer `.csv` i un gràfic resultant de mostra a la carpeta `/example`.

Actualment, el codi només es troba disponible en català, però es preveu una traducció a l'anglès en un futur.

---

## Goal
This simple interactive program allows you to represent the expenses you have annotated in the Splitwise application (available on Android and iOS).
You can draw points in a graph to see how monthly expenses vary for each category. It is also prepared to draw a bar graph with all the accumulated expenses.

## Installation
If you don't have Python installed on your computer, you must download the runable file. Enter the `/dist` carpeta folder of this repository. Click on the .gui.exe fitxer file. In the new window, press the button with three dots and download the file. Place it inside your computer in the folder you want. You have everything ready to open the program.

If you have Python downloaded to your computer, you can follow the above steps or clone this repository. The main program is `.gui.py`.
## How does the program work?
In your phone app, export the `.csv` file with the expenses and save it to your computer.

To open the program, run the .exe fitxer file. When the window opens, you can search for the name of the file you want to paint (the one you exported from Splitwise). You can also choose which folder you want to save it in and by what name.
You can choose in which language the file you extracted from Splitwise is located and in which language you want to draw your graph (IN TESTS).

Then choose the categories you want to represent. You can choose whether you want to paint a category or a theme, according to the Splitwise classifications.

You can also paint a cumulative histogram that includes the expenses of each month.

Once all the options have been chosen, press the "Draw!" button to be able to see the graph with the options you have chosen. When you close the window, the graph will be saved to the folder you have chosen.

You can find a mock '.csv' file and plot at the `/example` folder.

Currently, the code is only available in Catalan, but a translation into English is expected in the future.
