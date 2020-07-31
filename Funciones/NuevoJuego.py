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
        print('ok')
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
    window = sg.Window('¡Bienvenido!', layout, size=(630,370), element_justification='center')

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
            window.Close()
            if default:
                config=c.configuracion(default)
            bag=Bag((dict(list(config[0].items())[0:8])), dict(list(config[0].items())[8:16]))
            board=Board(bag, config[0]['__dificultad__'])
            nom=values['__nombre__']
            jugadores=f.instanciar_jugadores(bag, nom, jugadores)
            random.shuffle(jugadores)
            jugador_actual=jugadores[0]
            carga=False
            j.jugar(bag, board, diccTablero, jugadores, jugador_actual, config[0]['__dificultad__'], cant_rondas, ultima_palabra, carga, config[0]['__tiempoPartida__'], config[0]['__tiempoTurno__'], cant_cambios)
            #f.termino_juego(jugadores, bag)

