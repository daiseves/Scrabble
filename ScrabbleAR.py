import PySimpleGUI as sg
from Bag import Bag
from Board import Board
import random
import AI as ai
import Funciones as fun
import Jugar as j
import Configuracion as c

sg.theme_background_color('#E5CEAC')
cant_rondas=1
nivel='Fácil'
jugadores=[]
bag=Bag()

layout = [
            [sg.Image(filename='Imagenes/ScrabbleWord.png', size=(1000,300),background_color='#E5CEAC')],
            [sg.Text('NOMBRE:', font ='centaur 30', size=(13,1), justification='center',background_color='#E5CEAC'), sg.InputText(key='__nombre__',size=(30,1), font='Courier 30')],
            [sg.Text("",background_color='#E5CEAC')],
            [sg.Text("",background_color='#E5CEAC')],
            [sg.Button('INICIAR', button_color=('white','saddlebrown'), font='centaur 30', pad=((100,0)), size=(13,1)), sg.Button('CONFIGURACIÓN', button_color=('white','saddlebrown'), font='centaur 30', size=(20,1))]
            ]
window = sg.Window('Bienvenido', layout, size=(1100,600), location=(200,60))

while True:
    event, values = window.Read()
    if event is None:
        break
    if event is 'INICIAR':
        window.close()
        nom=values['__nombre__']
        jug=fun.instanciar_jugadores(bag, nom, jugadores)
        random.shuffle(jug) 
        jugador_actual=jug[0]
        sg.popup('Es el turno del jugador: ' ,jugador_actual.get_name(), background_color='#FFE0A3', text_color='saddlebrown')
        if nivel=='Medio':
            sg.theme('Purple')
        elif nivel=='Difícil':
            sg.theme('DarkBlue13')
        board=Board(bag, nivel)
        j.jugar(jugador_actual, board, jug, nivel, cant_rondas)
    if event is 'CONFIGURACIÓN':
        nivel=c.configuracion()
            
