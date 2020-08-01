import json
import PySimpleGUI as sg
from operator import itemgetter
from datetime import datetime, date, time, timedelta


def abro_archivo(ruta, nivel):
    ''' 
    Función que abre mi archivo json
    ''' 
    with open(ruta) as f:
        data = json.load(f)
        f.close()
    return(data[nivel])


def muestro_valores(datos, lista):
    ''' 
    Función que retorna una cadena con la información del archivo abierto para luego mostrarla en pantalla.
    ''' 
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
    ''' 
    Función que recibe como parámetros al jugador y el nivel en el cual se encontraba jugando y guarda su puntaje una vez terminada la partida.
    ''' 
    with open('Archivos/Top10.json','r+') as f:
        json_data = json.load(f)
        puntaje=jugador.get_puntaje()
        fecha = datetime.now()
        fecha = "{} de {} del {}".format(fecha.day, fecha.month, fecha.year)
        valores={"Fecha": fecha, "Puntaje":puntaje, "Nivel": nivel}
        json_data[nivel].append(valores)
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()
        print('Puntaje guardado.')
        

def main():
    ''' 
    Función que desarrolla mi interfaz gráfica donde muestro los puntajes guardados en todos los niveles del juego.
    ''' 
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

