import AI as ai
import Funciones as fun
import copy
import PySimpleGUI as sg
import time
from time import sleep

def jugar(jugador, board, jugadores, nivel, cant_rondas):
    columna1 =  []
    columna1 += fun.atril_interfaz_vacio()
    columna1 += board.get_board()
    columna1 += fun.atril_interfaz()
    columna2 = fun.columna_layout()
    columna3 = fun.columna3()
    
    layout=[[sg.Column(columna2, background_color='#D2B3BB',size=(300,800)), sg.Column(columna1), sg.Column(columna3, background_color='#D2B3BB', size=(300,800))]]
    window = sg.Window('TABLERO SCRABBLE', layout, location=(130,0))
    window.Finalize()
    

    fila=True
    columna=True
    fun.completo_atril(window, jugador)
    diccTablero={}
    ficha_central=board.ficha_centro()
    centro=board.get_medio()
    diccTablero[(centro[0],centro[1])]=ficha_central

    current_time = 0
    start_time = int(round(time.time() * 100))

    while True:
        event, values = window.read(timeout=10)
        current_time = int(round(time.time() * 100)) - start_time
        window['__time_partida__'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60,current_time % 100))
        
        if jugador.get_name()=="PC":
            dicc=jugador.get_dicc()
            ai.juega_PC(dicc, diccTablero, ficha_central, jugador, board, window, jugadores, cant_rondas, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), nivel)
            jugador=fun.next_player(jugador,jugadores)
            cant_rondas=cant_rondas+1
            fun.completo_atril(window, jugador)
            fila=True
            columna=True
        else:
            event, values = window.read()
            dicc=jugador.get_dicc()
            if event in (None, 'Salir'):
                break
            elif event in (0,1,2,3,4,5,6):
                aux = jugador.atril_array()[event]
                vacio = copy.deepcopy(event)
                event, values = window.read()
                if type(event) is tuple:
                    if event not in dicc.keys() and event not in diccTablero.keys():
                        posicion=fun.armar_palabra(dicc, event, aux, window, vacio, fila, columna, cant_rondas, board, diccTablero)
                        columna=posicion[0]
                        fila=posicion[1]
                    else:
                        sg.popup('El casillero ya se encuentra ocupado.', title=':(', background_color='#D2B3BB')
                    
                else:
                    sg.popup('Movimiento no válido. Debe poner la ficha en el tablero.', background_color='#D2B3BB')
       
            if event is 'Validar':
                fun.validar_palabra(window, diccTablero, dicc, jugador, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), cant_rondas, board, nivel)
                jugador=fun.next_player(jugador,jugadores)
                cant_rondas=cant_rondas+1
                fun.completo_atril(window, jugador)
                fila=True
                columna=True
                
            if event == 'Pasar turno':
                jugador=fun.next_player(jugador,jugadores)
                cant_rondas=cant_rondas+1
                
            if event is 'Cambiar fichas':
                sg.popup('¡No funciona todavía!',background_color='#D2B3BB')
                
            if event == 'Terminar juego':
                fun.ganador(jugadores)
                break
                
            if event == 'Top 10 Jugadores':
                sg.popup_scrolled('Información no disponible por ahora', background_color='#D2B3BB')
                
            if event is 'Salir':
                break
                
            
        
