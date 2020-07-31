import PySimpleGUI as sg
from Funciones import Funciones as fun
from Funciones import NuevoJuego as n
from Funciones import Jugar as j
from Funciones import Top10 as t


sg.SetOptions(background_color='#E5CEAC', button_color=('white','saddlebrown'), element_background_color='#E5CEAC',  text_element_background_color='#E5CEAC')

des = {'font':("Current",16), 'size':(16, 2)}

layout = [[sg.Image(filename='Imagenes/ScrabbleWord.png', size=(1000,250))],[sg.Button('Nuevo Juego', **des), sg.Button('Cargar Juego', **des), sg.Button('Top 10', **des)]]

window = sg.Window('Bienvenido al ScrabbleAR', layout, size=(900,400), element_justification='center')

while True:
    event, values  = window.read()
    if event is 'Nuevo Juego':
        window.Close()
        n.inicio()
    if event == 'Top 10':
        t.main()
    if event is 'Cargar Juego':
        window.Close()
        carga=True
        valor=fun.set_partida()
        sg.popup('Partida cargada con éxito. ')
        jugador_actual=valor[3][1] if(valor[3][0].get_name()=='PC') else valor[3][0]
        j.jugar(valor[0], valor[1], valor[2], valor[3], jugador_actual, valor[4], valor[5], valor[6], carga, valor[7], valor[8], valor[9])
            
