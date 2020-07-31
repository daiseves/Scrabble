import time
import copy
import PySimpleGUI as sg
from Funciones import AI as ai
from Funciones import Top10 as top
from Funciones import Funciones as fun

def actualizo_consideraciones(window, tiempo_partida, tiempo_ronda, nivel, bag):
    valores_letras=bag.valores_letras()
    cantidad_letras=bag.diccionario_cantidad()
    n='Nivel de la partida: {}'.format(nivel)
    window.FindElement('__n__').update(n) 
    tp='Tiempo de la partida: {} min'.format(tiempo_partida)
    window.FindElement('__tp__').update(tp) 
    tr='Tiempo de cada ronda: {} sg'.format(tiempo_ronda)
    window.FindElement('__tr__').update(tr) 
    pf='Cantidad de fichas:\n-A | I: {}\n-B | C | F | H | M | P | T | U | V | W | Y : {}\n-D | L | S: {}\n-E : {}\n-G: {}\n-J | K | Q | W | X | Z: {}\n-M | R: {}\n-O: {}'.format(cantidad_letras['A'],cantidad_letras['B'], cantidad_letras['D'], cantidad_letras['E'], cantidad_letras['G'], cantidad_letras['J'], cantidad_letras['M'], cantidad_letras['O'])
    window.FindElement('__pf__').update(pf) 
    cf='Puntaje de cada ficha:\n-A | E: {}\n-O : {}\n-I | S: {}\n-N | R | U | D: {}\n-L | T | C: {}\n-G | B | M | P | H | K | W: {}\n-F | V | Y | J: {}\n-Q | X | Z: {}'.format(valores_letras['A'], valores_letras['O'], valores_letras['I'], valores_letras['N'] , valores_letras['L'], valores_letras['G'], valores_letras['F'], valores_letras['Q'])
    window.FindElement('__cf__').update(cf) 
    

def turno(window, jugador, tiempo_partida, tiempo_ronda, board, diccTablero, cant_rondas, jugadores, nivel, ultima_palabra, bag, carga, cant_cambios):
    
    atril=[]
    fila=True
    columna=True
    cant_cambios=cant_cambios
    ficha_central=board.ficha_centro()
    fun.completo_atril(window, jugador)

    if carga: 
        temp=fun.cargo(jugadores, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), ultima_palabra, window.FindElement('__n__'), nivel, tiempo_partida, tiempo_ronda)
        tiempo_partida = temp[0]
        tiempo_ronda = temp[1]
    else:
        centro=board.get_medio()
        diccTablero[(centro[0],centro[1])]=ficha_central
        ultima_palabra=['']
        tiempo_partida = (int(tiempo_partida) * 60) *100 #359999 una hora
        tiempo_ronda = (int(tiempo_ronda) *100) #5999 un minuto
        
    tiempo_ronda_inicial=tiempo_ronda

    while True and tiempo_partida!=0:
        window['__tiempoTurno__'].update('{:02d}:{:02d}'.format(((tiempo_ronda // 100) % 60), tiempo_ronda % 100))
        window['__tiempoPartida__'].update('{:02d}:{:02d}'.format((tiempo_partida // 100) // 60, (tiempo_partida // 100) % 60))
        tiempo_partida -= 1
        tiempo_ronda -= 1

        window.FindElement('__nombreAtril__').update(jugador.get_name())
        dicc=jugador.get_dicc()
        lista_coordenadas=board.lista_coordenadas()
        
        if jugador.get_name()=='PC':
            ai.juega_PC(dicc, diccTablero, ficha_central, jugador, board, window, jugadores, cant_rondas, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), nivel, ultima_palabra, bag, lista_coordenadas)
            jugador=fun.next_player(jugador,jugadores)
            cant_rondas=cant_rondas+1
            fun.completo_atril(window, jugador)
            fila=True
            columna=True
        else:
            event, values = window.read(timeout=10)
            
            if event in (None, 'Salir'):
                break
            elif event in (0,1,2,3,4,5,6):
                if event not in atril:
                    atril.append(event)
                else:
                    sg.popup('Ya usó esta ficha.', title=':(')
                    event, values = window.read()
                aux = jugador.atril_array()[event]
                vacio = copy.deepcopy(event)
                event, values = window.read()
                print(event)
                if type(event) is tuple:
                     if event not in dicc.keys() and event not in diccTablero.keys():
                        posicion=fun.armar_palabra(dicc, event, aux, window, vacio, fila, columna, cant_rondas, board, diccTablero, lista_coordenadas)
                        atril.pop() 
                        columna=posicion[0]
                        fila=posicion[1]
                     else:
                        sg.popup('El casillero ya se encuentra ocupado.', title=':(')
                        atril.pop() 
                        
                else:
                    sg.popup('Movimiento no válido. Debe poner la ficha en el tablero.')
        
                
            if event is 'Validar':
                if len(dicc)<=1:
                    sg.popup('No se pueden formar palabras de una sóla letra.')
                else:
                    fun.validar_palabra(window, jugadores, diccTablero, dicc, jugador, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), cant_rondas, board, nivel, ultima_palabra, bag)
                    jugador=fun.next_player(jugador,jugadores)
                    fun.completo_atril(window, jugador)
                    cant_rondas=cant_rondas+1
                    tiempo_ronda = tiempo_ronda_inicial
                    fila=True
                    columna=True
                    del atril[:]
                
            if event == 'Pasar turno':
                if jugador.get_dicc():
                    board.devolver_fichas(jugador.get_dicc(), cant_rondas, window, diccTablero)
                jugador=fun.next_player(jugador,jugadores)
                cant_rondas=cant_rondas+1
                tiempo_ronda = tiempo_ronda_inicial
                del atril[:]
                
            if event == 'Cambiar fichas':
                if cant_cambios!=3:
                    fun.cambiar_fichas(window,jugador)
                    jugador=fun.next_player(jugador,jugadores)
                    tiempo_ronda = tiempo_ronda_inicial
                    cant_cambios+=1
                else:
                    sg.popup('Ya  hizo uso de los tres cambios permitidos.')
                
            if event is 'Posponer':
                fun.guardar_partida(diccTablero, jugadores, bag, cant_rondas, ultima_palabra, nivel, cant_cambios, tiempo_partida, tiempo_ronda)
                sg.popup('¡Partida guardada!')

                break
                
            if event == 'Terminar juego':
                #fun.ganador(jugadores, tiempo=False)
                termino_juego(jugadores, bag, tiempo=False)
                top.guardo_puntajes(jugador, nivel)
                diccTablero.clear()
                window.close()
                break
            
            if tiempo_ronda==0:               
                cant_rondas=cant_rondas+1
                sg.popup('Se quedó sin tiempo, ha perdido el turno.')
                jugador=fun.next_player(jugador,jugadores)
                
                
    if tiempo_partida==0:
        #fun.ganador(jugadores, tiempo=True)
        termino_juego(jugadores, bag, tiempo=False)
        top.guardo_puntajes(jugador, nivel)
        diccTablero.clear()
    else:
        sg.popup('¡Adiós!.')
    window.close()
    
    
    
def jugar(bag, board, diccTablero, jugadores, jugador_actual, nivel, cant_rondas, ultima_palabra, carga, tiempo_partida, tiempo_ronda, cant_cambios):

    des={'background_color':('#D2B3BB'), 'size':(290,800), 'element_justification':'center'}
    des2={'text_color':('saddlebrown'), 'font':('Verdana', 13, 'bold')}
    col=fun.layout_jugar(diccTablero, board, carga, des2)
    
    
    layout=[[sg.Column(col[0], element_justification='center'), sg.Column(col[1], **des)]]
    window = sg.Window('TABLERO SCRABBLE', layout, element_justification='center')

    
    while True:
        event, values = window.Read()
        if event is 'None':
            break
        if event is 'INICIAR':
            sg.popup('Comienza el jugador: ',jugador_actual.get_name())
            actualizo_consideraciones(window, tiempo_partida, tiempo_ronda, nivel, bag)
            turno(window, jugador_actual, tiempo_partida, tiempo_ronda, board, diccTablero, cant_rondas, jugadores, nivel, ultima_palabra, bag, carga, cant_cambios)
