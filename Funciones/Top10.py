'''
ScrabbleAR
 - Autor: Remorini Maria Lara
 - Mail: remoriniml@gmail.com
 - GitHub: https://github.com/daiseves - 

Todas las imagenes utilizadas en este proyecto son de propia autoría.
'''

import json
import PySimpleGUI as sg
from operator import itemgetter
from datetime import datetime, date, time, timedelta


def abro_archivo(ruta, nivel):
    with open(ruta) as f:
        data = json.load(f)
        f.close()
    return(data[nivel])


def muestro_valores(datos, lista):
    #Ordeno mi lista de elementos por puntaje (mayor a menor)
    l = sorted(datos, key=itemgetter('Puntaje'), reverse=True)
    aux = 0
    text=''
    for i in l:
        if(aux < 10):
            lista.append(i)
        aux = aux+1

    for i in range(len(lista)):
        text = text + '{}.    Fecha: {}     |   Puntaje: {}       |   Nivel: {}\n'.format(i+1, lista[i]['Fecha'], lista[i]['Puntaje'], lista[i]['Nivel'])

    return text

def guardo_puntajes(jugador, nivel):
    with open('Archivos/Top10.json','r+') as f:
        json_data = json.load(f)
        puntaje=jugador.get_puntajeFinal()
        fecha = datetime.now()
        fecha = "{} de {} del {}".format(fecha.day, fecha.month, fecha.year)
        valores={"Fecha": fecha, "Puntaje":puntaje, "Nivel": nivel}
        json_data[nivel].append(valores)
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()
        print('Puntaje guardado.')
        

def main():
    sg.theme_background_color('#E5CEAC')
    des= {'button_color':('white','saddlebrown'), 'font':('centaur',15), 'pad':((0,40)), 'size':(10,1)}
    layout = [
                [sg.Image(filename='Imagenes/top10.png' , pad=((0,0),(40,0)))],   #arriba: primero del segundo   #abajo:segundo del segundo
                [sg.Button('Fácil', **des), sg.Button('Medio', **des), sg.Button('Difícil', **des)],
                [sg.Multiline('',size =(60,10),key='__multiline__',background_color='#E5CEAC', text_color='saddlebrown')],
                [sg.Button('Volver', **des)]
             ]
    
    window = sg.Window('Configuración', layout, size=(500,600),element_justification='center')
    
    lista=[]
    ruta='Archivos/Top10.json'
    while True:
        event, value = window.read()
        try:
            if event in (None, 'Volver'):
                break
            if event is 'Fácil':
                nivel='Facil'
                text=muestro_valores(abro_archivo(ruta, nivel), lista)
                window.FindElement('__multiline__').Update(text);
                del lista[:]
            if event is 'Medio':
                nivel='Medio'
                text=muestro_valores(abro_archivo(ruta, nivel), lista)
                window.FindElement('__multiline__').Update(text);
                del lista[:]
            if event is 'Difícil':
                nivel='Dificil'
                text=muestro_valores(abro_archivo(ruta, nivel), lista)
                window.FindElement('__multiline__').Update(text);
                del lista[:]
            
        except FileNotFoundError:
            sg.popup('Error. No se ha encontrado el archivo.',background_color='#E5CEAC', text_color='saddlebrown')

    window.close()
