'''
ScrabbleAR
 - Autor: Remorini Maria Lara
 - Mail: remoriniml@gmail.com
 - GitHub: https://github.com/daiseves - 

Todas las imagenes utilizadas en este proyecto son de propia autoría.
'''

import time
import copy
import PySimpleGUI as sg
from Funciones import AI as ai
from Funciones import Funciones as fun

def actualizo_consideraciones(window, tiempo_partida, tiempo_ronda, nivel, bag):
    ''' 
    Función que actualiza las consideraciones del nivel dispuesto por el usuario para mostrarlas por pantalla.
    ''' 
    valores_letras=bag.valores_letras()
    cantidad_letras=bag.diccionario_cantidad()
    n='Nivel de la partida: {}'.format(nivel)
    window.FindElement('__n__').update(n) 
    tp='Tiempo de la partida: {} min'.format(tiempo_partida)
    window.FindElement('__tp__').update(tp) 
    tr='Tiempo de cada ronda: {} sg'.format(tiempo_ronda)
    window.FindElement('__tr__').update(tr) 
    pf='Cantidad de fichas:\n-A | I: {}\n-B | C | F | H | M | P: {}\n-T | U | V | W | Y: {}\n-D | L | S: {}\n-E: {}\n-G: {}\n-J | K | Q | W | X | Z: {}\n-M | R: {}\n-O: {}'.format(cantidad_letras['A'],cantidad_letras['B'],cantidad_letras['B'], cantidad_letras['D'], cantidad_letras['E'], cantidad_letras['G'], cantidad_letras['J'], cantidad_letras['M'], cantidad_letras['O'])
    window.FindElement('__pf__').update(pf) 
    cf='Puntaje de cada ficha:\n-A | E: {}\n-O: {}\n-I | S: {}\n-N | R | U | D: {}\n-L | T | C: {}\n-G | B | M | P | H | K | W: {}\n-F | V | Y | J: {}\n-Q | X | Z: {}'.format(valores_letras['A'], valores_letras['O'], valores_letras['I'], valores_letras['N'] , valores_letras['L'], valores_letras['G'], valores_letras['F'], valores_letras['Q'])
    window.FindElement('__cf__').update(cf) 
    

def turno(window, jugador, tiempo_partida, tiempo_ronda, board, diccTablero, cant_rondas, jugadores, nivel, ultima_palabra, bag, carga, cant_cambios, tp_inicial, tr_inicial):
    
    ''' 
    Función que desarrolla cada turno, tanto los de la Pc como los del usuario.
    ''' 
    
    atril=[]
    fila=True
    columna=True
    cant_cambios=cant_cambios
    fun.completo_atril(window, jugador)
    
    sg.popup('Comienza el jugador: ',jugador.get_name(), title='Primer turno', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
    if carga: 
        temp=fun.cargo(jugadores, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), ultima_palabra, window.FindElement('__n__'), nivel, tiempo_partida, tiempo_ronda, tp_inicial, tr_inicial, window.FindElement('__tp__'), window.FindElement('__tr__'))
        ficha_central=diccTablero[(7,7)] if nivel == 'Facil' else diccTablero[(8,8)] if nivel == 'Medio' else diccTablero[(9,9)]
        tiempo_ronda = temp[0]
        tiempo_partida = temp[1]
        tronda_inicial=(int(tp_inicial) *100)
    else:
        ficha_central=board.ficha_centro
        centro=board.get_medio()
        diccTablero[(centro[0],centro[1])]=ficha_central
        ultima_palabra=['']
        tiempo_partida = (int(tiempo_partida) * 60) *100 #359999 una hora
        tiempo_ronda = (int(tiempo_ronda) *100) #5999 un minuto
        tronda_inicial=tiempo_ronda
    
    
    while True and tiempo_partida!=0:
        window['__tiempoTurno__'].update('{:02d}:{:02d}'.format(((tiempo_ronda // 100) % 60), tiempo_ronda % 100))
        window['__tiempoPartida__'].update('{:02d}:{:02d}'.format((tiempo_partida // 100) // 60, (tiempo_partida // 100) % 60))
        tiempo_partida -= 1
        tiempo_ronda -= 1

        window.FindElement('__nombreAtril__').update(jugador.get_name())
        dicc=jugador.get_dicc()
        lista_coordenadas=board.lista_coordenadas()
        
        #-----TURNO PC-----
        if jugador.get_name()=='PC':
            ai.juega_PC(dicc, diccTablero, ficha_central, jugador, board, window, jugadores, cant_rondas, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), nivel, ultima_palabra, bag, lista_coordenadas)
            jugador=fun.next_player(jugador,jugadores)
            cant_rondas=cant_rondas+1
            fun.completo_atril(window, jugador)
            tiempo_partida -= 1
            columna=True
            fila=True

        else:
            #-----TURNO USER-----
            event, values = window.read(timeout=10)
            if event in (None, 'Salir'):
                break
            elif event in (0,1,2,3,4,5,6):
                if event in atril:
                    sg.popup('Ya usó esta ficha.', title=':(', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                else:
                    atril.append(event)
                    aux = jugador.atril_array()[event]
                    vacio = copy.deepcopy(event)
                    event, values = window.read()
                    if type(event) is tuple:
                         if event not in dicc.keys() and event not in diccTablero.keys():
                            posicion=fun.armar_palabra(dicc, event, aux, window, vacio, fila, columna, cant_rondas, board, diccTablero, lista_coordenadas)
                            columna=posicion[0]
                            fila=posicion[1]
                         else:
                            sg.popup('El casillero ya se encuentra ocupado.', title=':(', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                            atril.pop() 
                    elif event in (None, 'Salir'):
                        break
                    else:
                        sg.popup('Movimiento no válido. Debe poner la ficha en el tablero.', title='No válido', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                        atril.pop() 
            del atril[:]
            
            
            #-----VALIDAR PALABRA-----    
            if event is 'Validar':
                if len(dicc)==1:
                    sg.popup('No se pueden formar palabras de una sóla letra.',title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                else:
                    fun.validar_palabra(window, jugadores, diccTablero, dicc, jugador, window.FindElement('_puntajeUser_'), window.FindElement('_puntajePC_'), window.FindElement('_ultimaPalabra_'), cant_rondas, board, nivel, ultima_palabra, bag)
                    jugador=fun.next_player(jugador,jugadores)
                    fun.completo_atril(window, jugador)
                    cant_rondas=cant_rondas+1
                    tiempo_ronda = tronda_inicial
                    fila=True
                    columna=True
                    #del atril[:]
                    
                    
            #-----PASAR TURNO-----       
            if event == 'Pasar turno':
                fun.reset(window, jugador, cant_rondas, diccTablero, board)
                jugador=fun.next_player(jugador,jugadores)
                cant_rondas=cant_rondas+1
                tiempo_ronda = tronda_inicial
                del atril[:]
                
                
            #-----CAMBIAR FICHAS-----    
            if event == 'Cambiar fichas':
                fun.reset(window, jugador, cant_rondas, diccTablero, board)
                if cant_cambios!=3:
                    fun.cambiar_fichas(window,jugador)
                    jugador=fun.next_player(jugador,jugadores)
                    tiempo_ronda = tronda_inicial
                    cant_cambios+=1
                else:
                    sg.popup('Ya  hizo uso de los tres cambios permitidos.', title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
            
            #-----POSPONER JUEGO-----    
            if event is 'Posponer':
                fun.reset(window, jugador, cant_rondas, diccTablero, board)
                fun.guardar_partida(diccTablero, jugadores, bag, cant_rondas, ultima_palabra, nivel, cant_cambios, tiempo_partida, tiempo_ronda, tr_inicial, tp_inicial)
                sg.popup('¡Partida guardada!', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                break
            
            
            #-----TERMINAR JUEGO-----    
            if event == 'Terminar juego':
                fun.reset(window, jugador, cant_rondas, diccTablero, board)
                fun.termino_juego(jugadores, bag, nivel)
                diccTablero.clear()
                window.close()
                break
                
            if event is 'REGLAS':
                fun.reglas()
            
            #-----SI TERMINA EL TIEMPO DE LA RONDA-----    
            if tiempo_ronda==0:
                fun.reset(window, jugador, cant_rondas, diccTablero, board)        
                cant_rondas=cant_rondas+1
                sg.popup('Se quedó sin tiempo, ha perdido el turno.', title='Se quedó sin tiempo', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                jugador=fun.next_player(jugador,jugadores)
                
                
    #-----SI TERMINA EL TIEMPO DE LA PARTIDA-----    
    if tiempo_partida==0:
        fun.reset(window, jugador, cant_rondas, diccTablero, board)
        fun.termino_juego(jugadores, bag, nivel)
        diccTablero.clear()
    window.close()
    
    
    
def jugar(bag, board, diccTablero, jugadores, jugador_actual, nivel, cant_rondas, ultima_palabra, carga, tiempo_partida, tiempo_ronda, cant_cambios, tp_inicial, tr_inicial):
    
    ''' 
    Función que desarolla la interfaz gráfica principal, donde se muestra el tablero. Inicializa las consideraciones y comienza el turno del primer jugador.
    ''' 
    
    des={'background_color':('#D2B3BB'), 'size':(290,800), 'element_justification':'center'}
    des2={'text_color':('saddlebrown'), 'font':('Verdana', 13, 'bold')}
    col=fun.layout_jugar(diccTablero, board, carga, des2)
    
    layout=[[sg.Column(col[0], element_justification='center'), sg.Column(col[1], **des)]]
    window = sg.Window('TABLERO SCRABBLE', layout, element_justification='center')

    while True:
        event, values = window.Read()
        if event is 'None':
            break
        if event is 'REGLAS':
            fun.reglas()
        if event is 'INICIAR':
            actualizo_consideraciones(window, tiempo_partida, tiempo_ronda, nivel, bag)
            turno(window, jugador_actual, tiempo_partida, tiempo_ronda, board, diccTablero, cant_rondas, jugadores, nivel, ultima_palabra, bag, carga, cant_cambios, tp_inicial, tr_inicial)

