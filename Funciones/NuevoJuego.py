'''
ScrabbleAR
 - Autor: Remorini Maria Lara
 - Mail: remoriniml@gmail.com
 - GitHub: https://github.com/daiseves - 

Todas las imagenes utilizadas en este proyecto son de propia autoría.
'''

import random
import os.path as path
import PySimpleGUI as sg
from Clases.Bag import Bag
from Clases.Board import Board
from Funciones import Jugar as j
from Funciones import Funciones as f
from Funciones import Configuracion as c


def inicio():
    if path.exists('Archivos/partidaGuardada.pckl'):
        preguntar()
    else:
        main()
        
        
def preguntar():
    des={'font':('Verdana', 10), 'size':(10, 2)}
    layout=[[sg.Text("Hay una partida guardada ¿Desea continuarla?", font=("Current",13),  text_color= 'saddlebrown', pad=(0,10))], [sg.Button('Si', **des), sg.Button('No', **des)]]
    
    window = sg.Window('Partida guardada.', layout, size=(500,120), element_justification='center')
    event, values = window.Read()
    if event is 'Si':
        window.Close()
        carga=True
        valor=f.set_partida()
        jugador_actual=valor[3][1] if(valor[3][0].get_name()=='PC') else valor[3][0]
        j.jugar(valor[0], valor[1], valor[2], valor[3], jugador_actual, valor[4], valor[5], valor[6], carga, valor[7], valor[8], valor[9], valor[10], valor[11])
    elif event is 'No':
        window.Close()
        main()
        

def main():
    
    des={'font':("Current",16), 'size':(16, 2)}
        
    layout = [
             [sg.Text('NOMBRE:', font=("Current",20), text_color= 'saddlebrown',), sg.InputText(key='__nombre__', size=(30,5), pad=(0,30), font=("Current",20))],
             [sg.Button('Jugar',  **des), sg.Button('Configuración', **des)],
             [sg.Image(filename='Imagenes/1.png', pad=(0,30))]
             ]
    window = sg.Window('¡Bienvenido!', layout, size=(630,350), element_justification='center')

    cant_rondas=1
    cant_cambios=0
    diccTablero={}
    jugadores=[]
    ultima_palabra=[]
    default=True
    while True:
        event, values = window.Read()
        if event is None:
            break
        if event is 'Configuración':
            default=False
            config=c.configuracion(default)
            default=config[1]
        if event is 'Jugar':
            nom=values['__nombre__']
            print (len(nom))
            if len(nom)<3 or len(nom)>10:
                 sg.popup('El nombre debe tener entre 3 y 10 letras.',title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
            else:
                window.Close()
                if default:
                    config=c.configuracion(default)
                bag=Bag((dict(list(config[0].items())[0:8])), dict(list(config[0].items())[8:16]))
                board=Board(bag, config[0]['__dificultad__'])
                jugadores=f.instanciar_jugadores(bag, nom, jugadores)
                random.shuffle(jugadores)
                jugador_actual=jugadores[0]
                carga=False
                tp_inicial=config[0]['__tiempoPartida__']
                tr_inicial=config[0]['__tiempoTurno__']
                j.jugar(bag, board, diccTablero, jugadores, jugador_actual, config[0]['__dificultad__'], cant_rondas, ultima_palabra, carga, config[0]['__tiempoPartida__'], config[0]['__tiempoTurno__'], cant_cambios, int(tp_inicial), int(tr_inicial))


