import PySimpleGUI as sg
import json
from operator import itemgetter

def abro_archivo(ruta, nivel):
    with open(ruta) as f:
        data = json.load(f)
        f.close()
    return(data[nivel])


def muestro_valores(datos, lista):
    #Ordeno mi lista de elementos por puntaje (mayor a menor)
    l = sorted(datos, key=itemgetter('Puntaje'), reverse=True)
    for i in range(10):
        aux=l[i]
        lista.append(aux)


def main():
    sg.theme_background_color('#E5CEAC')
    des= {'button_color':('white','saddlebrown'), 'font':('centaur',15), 'pad':((0,40)), 'size':(10,1)}
    layout = [
                [sg.Image(filename='Imagenes/top10.png' , background_color='#E5CEAC', pad=((0,0),(40,0)))],   #arriba: primero del segundo   #abajo:segundo del segundo
                [sg.Button('Fácil', **des), sg.Button('Medio', **des), sg.Button('Difícil', **des)],
                [sg.Listbox('',size =(60,10),key='listbox',background_color='#E5CEAC', text_color='saddlebrown')],
                [sg.Button('Volver', **des)]
             ]
    
    window = sg.Window('Configuración', layout, size=(500,600),element_justification='center')
    
    lista=[]
    ruta='Archivos/Top10.json'
    while True:
        event, value = window.read()
        try:
            if event is None or event is 'Volver':
                break
            if event is 'Fácil':
                nivel='Facil'
                muestro_valores(abro_archivo(ruta, nivel), lista)
                print(lista)
                window.FindElement('listbox').Update(lista);
                del lista[:]
            if event is 'Medio':
                nivel='Medio'
                muestro_valores(abro_archivo(ruta, nivel), lista)
                window.FindElement('listbox').Update(lista);
                del lista[:]
            if event is 'Difícil':
                nivel='Dificil'
                muestro_valores(abro_archivo(ruta, nivel), lista)
                window.FindElement('listbox').Update(lista);
                del lista[:]
            
        except FileNotFoundError:
            sg.popup('Error. Archivo no encontrado.',background_color='#E5CEAC', text_color='saddlebrown')

    window.close()

