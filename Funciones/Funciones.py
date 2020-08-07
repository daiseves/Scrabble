'''
ScrabbleAR
 - Autor: Remorini Maria Lara
 - Mail: remoriniml@gmail.com
 - GitHub: https://github.com/daiseves - 

Todas las imagenes utilizadas en este proyecto son de propia autoría.
'''

import sys
import copy
import socket
import pickle
import os.path
import PySimpleGUI as sg
from Clases.Atril import Atril
from Clases.Board import Board
from Funciones import Top10 as top
from Clases.Palabra import Palabra
from Clases.Jugador import Jugador



'''
FUNCIONES SOBRE:
1. Turno del usuario.
2. Armado de palabra sobre el tablero.
3. Cambiar fichas.
4. Fin del turno.
5. Guardado y carga de una partida.
6. Fin del juego.
7. Interfaz gráfica principal.
'''



def verificar():
    ''' 
    Función que verifica si el usuario se encuentra conectado a una red. Es necesario para el uso del pattern.
    ''' 
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        soc.connect(('www.google.com', 80))
    except:
        sg.popup('Para jugar debes estar conectado a internet.', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        sys.exit()
    #soc.close()


def instanciar_jugadores(bag, nom, jugadores):
    ''' 
    Función que instancia los dos jugadores que van a jugar una partida.
    ''' 
    jugador1 = Jugador(bag, nom)
    jugador2 = Jugador(bag, 'PC')
    jugadores.append(jugador1)
    jugadores.append(jugador2)
    return jugadores
    
    
def reset(window, jugador, cant_rondas, diccTablero, board):
    ''' 
    Función que vacía el diccionario de cada jugador y devuelve esos valores al atril
    ''' 
    if jugador.get_dicc():
        board.devolver_fichas(jugador.get_dicc(), cant_rondas, window, diccTablero)
        jugador.vaciar_dicc()


#---------------------------------- TURNO DEL USUARIO ----------------------------------    


def validar_palabra(window, jugadores, diccTablero, dicc, jugador, multiUser, multiPC, ultimaPalabra, cant_rondas, board, nivel, ultima_palabra, bag):
    '''
    Función que desarrolla el turno del usuario.
    '''
    diccOrd=dict(sorted(dicc.items()))
    listaLetras=a_lista(diccOrd)
    word = "".join(listaLetras)
    palabra=Palabra(word, jugador, board, bag)
    if palabra.convert():
        puntaje=palabra.calcular_puntaje(diccOrd)
        jugador.aumentar_puntaje(puntaje)
        actualizar_multi(jugador,multiUser, multiPC)
        sg.popup('Palabra válida.\nPuntaje: ',puntaje, background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        ultimaPalabra.Update(palabra.get_palabra().lower())
        ultima_palabra[0]=palabra.get_palabra().lower()
        diccTablero.update(dicc)
        exito=jugador.actualizar_atril(diccOrd, cant_rondas, nivel)
        if exito==None:
            window.Finalize()
            termino_juego(jugadores, bag, nivel)
    else:
        sg.popup('Palabra Inválida. Perdió el turno.\nSe devuelven las fichas jugadas', title='Palabra inválida', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        board.devolver_fichas(diccOrd, cant_rondas, window, diccTablero)
    jugador.vaciar_dicc()
    


def a_lista(dic):
    ''' 
    Función que convierte los valores de mi diccionario en una lista de letras (con la que verifico si existe mi palabra).
    ''' 
    listaLetras=[]
    for elem in dic.values():
        listaLetras.append(elem)
    return listaLetras



#---------------------------------- ARMADO DE PALABRA SOBRE EL TABLERO ----------------------------------

def armar_palabra(dicc, event, aux, window, vacio, fila, columna, cant_rondas, board, diccTablero, lista_coordenadas):
    '''
    Función principal del armado de la palabra del usuario sobre el tablero
    '''
    if cant_rondas==1 or len(diccTablero)==1:
        medio=board.get_medio()
        dicc[(medio[0],medio[1])]=board.ficha_centro
    if not dicc:
        dicc[event] = aux 
        actualizo_atril_tablero(window, vacio, event, aux, lista_coordenadas)
    else:
        pos=list(dicc.keys())[0]
        if len(dicc)==1:
            var_de_pos=verificar_segunda(event, pos, dicc, aux, window, vacio, lista_coordenadas)
            if  var_de_pos==1:
                columna=False
            else:
                fila=False
        else:
            pos_palabra(pos, event, window, vacio, aux, dicc, fila, columna, lista_coordenadas)
    return columna, fila


def pos_palabra(vieja_coord, nueva_coord, window, vacio, aux, dicc, fila, columna, lista_coordenadas):
    '''
    Función que verifica que la palabra se posicione en la dirección correcta
    '''
    if nueva_coord[0] == vieja_coord[0] and fila:
        juego(vieja_coord, nueva_coord, window, vacio, aux, dicc, lista_coordenadas)
    elif nueva_coord[1] == vieja_coord[1] and columna:
        juego(vieja_coord, nueva_coord, window, vacio, aux, dicc, lista_coordenadas)
    else:
        sg.popup('Error. Movimiento no permitido.', title='No permitido', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        
            
def juego (vieja_coord, nueva_coord,  window, vacio, aux, dicc, lista_coordenadas):
    '''
    Función que agrega mi letra al tablero una vez verifica la pos
    '''
    dicc[nueva_coord] = aux
    actualizo_atril_tablero(window, vacio, nueva_coord, aux, lista_coordenadas)
            
            
def verificar_segunda(event, pos, dicc, aux, window, vacio, lista_coordenadas):
    '''
    Función que verifica si la segunda letra se ingresa de forma verical u horizontal, para luego bloquear la otra posición
    '''
    if (event[0]==pos[0]) and ((event[1]==(pos[1]-1)) or (event[1]==(pos[1]+1))):
        dicc[event] = aux 
        actualizo_atril_tablero(window, vacio, event, aux, lista_coordenadas)
        #print('entra fila')
        return 1
    elif (event[1]==pos[1]) and ((event[0]==(pos[0]-1)) or (event[0]==(pos[0]+1))):
        dicc[event] = aux 
        actualizo_atril_tablero(window, vacio, event, aux, lista_coordenadas)
        #print('entra columna')
        return 2
    else:
        sg.popup('Error. Movimiento no permitido.', title='No permitido', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
            

def actualizo_atril_tablero(window, vacio, event, aux, lista_coordenadas):
    '''
    Función que me actualiza el atril cuando se juega la ficha (vacía el espacio) y actualiza el tablero con la letra del atril.
    '''
    des={'button_color':('saddlebrown','#FFE0A3')}
    if event in lista_coordenadas:
        window[event](image_filename='Imagenes/casillero.png')
    window.FindElement(vacio).update("", **des) 
    window.FindElement(event).update(aux, **des) 


    
#---------------------------------- CAMBIAR FICHAS ----------------------------------
    
def cambiar_fichas(window, jugador):
    '''
    Función que desarrolla la interfaz gráfica del cambio de fichas del atril.
    '''
    atril = [[sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=(elem,0)) for elem in range(7)]]
    lista_letras=copy.deepcopy(jugador.atril_array())

    layout = [
              [sg.Text('Seleccione las fichas a cambiar.',background_color='#E5CEAC')],
              [sg.Column(atril)],
              [sg.Button('Cambiar',font=("Current",16), button_color=('white','saddlebrown')), sg.Button('Cancelar',font=("Current",16),  button_color=('white','saddlebrown'))]
              ]

    window2 = sg.Window('', layout, font=("Current",16), element_justification='center').finalize()

    for i in range(7):
        window2.FindElement((i,0)).update(jugador.atril_array()[i]) 

    cant=0
    evento=[]
    letras_a_cambiar=[]
    
    sigue=True
    while sigue:
        event, values = window2.Read()
        if event in ((0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)):
            aux=jugador.atril_array()[event[0]]
            if cant!=3 and event not in evento:
                evento.append(event)
                window2.FindElement(event,0).update(aux,button_color=('white','saddlebrown'))
                letras_a_cambiar.append(jugador.atril_array()[event[0]])
                cant=cant+1
            elif event in evento:
                window2.FindElement(event,0).update(aux,button_color=('saddlebrown','#FFE0A3'))
                evento.remove(event)
                letras_a_cambiar.remove(aux)
                cant=cant-1
            else:
                sg.popup('Sólo se pueden cambiar tres letras por turno.',title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        if event is 'Cambiar':
            if jugador.cambiar_fichas(letras_a_cambiar):
                completo_atril(window, jugador)
                sigue=False
                window2.Close()
            else:
                sg.popup('No hay suficientes fichas en la bolsa.',title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        if event is 'Cancelar':
            window2.Close()
            sigue=False
        if event is None:
            sigue=False
            window2.Close()   
            


#---------------------------------- FIN DE TURNO ----------------------------------

def next_player(jugador,jugadores):
    ''' 
    Función que me retorna el jugador siguiente para cambiar el turno
    ''' 
    if jugadores.index(jugador) != (len(jugadores)-1):
        jugador=jugadores[jugadores.index(jugador)+1]
    else:
        jugador = jugadores[0]
    return jugador
    
    
def actualizar_multi(jugador, frameUser, framePC):
    '''
    Función que actualiza los puntajes de los jugadores en pantalla luedo de cada turno.
    '''
    var=jugador.get_puntaje()
    if jugador.get_name()=='PC':
        framePC.Update(var)
    else:
        frameUser.Update(var)
            
    

#---------------------------------- GUARDADO Y CARGA DE UNA PARTIDA ----------------------------------

def set_partida():
    ''' 
    Función que setea los valores mis valores iniciales y los retorna en una lista para iniciar la partida con la configuración previamente guardada.
    ''' 
    lista=[]
    valores=cargar_partida()
    bag=valores[0]
    jugadores=valores[1]
    cant_rondas=valores[2]
    diccTablero=valores[3]
    ultima_palabra=valores[4]
    nivel=valores[5]
    tiempo_ronda=valores[6]
    tiempo_partida=valores[7]
    cant_cambios=valores[8]
    tp_inicial=valores[9]
    tr_inicial=valores[10]
    board=Board(bag, nivel)
    
    lista=[bag, board, diccTablero, jugadores, nivel, cant_rondas, ultima_palabra, tiempo_ronda, tiempo_partida, cant_cambios, tp_inicial, tr_inicial]
    
    return lista
    


def guardar_partida(dic, jugadores, bag, cant_rondas, ultima_palabra, nivel, cant_cambios, tiempo_partida, tiempo_ronda, tp_inicial, tr_inicial):
    ''' 
    Función que guarda una partida en proceso. Recibe el tablero, el usuario, la PC y la bolsa de fichas y los almacena.
    ''' 
    ruta = os.path.join('Archivos', '')
    datos_guardar=[bag, jugadores, cant_rondas, dic, ultima_palabra, nivel, tiempo_ronda, tiempo_partida, cant_cambios, tp_inicial, tr_inicial]
    with open(f'{ruta}''partidaGuardada.pckl', 'wb') as f:
        pickle.dump(datos_guardar, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    


def cargar_partida():
    ''' 
    Función que carga una partida guardada. 
    ''' 
    try:
        ruta = os.path.join('Archivos', '')
        with open(f'{ruta}''partidaGuardada.pckl', 'rb') as f:
            juego = pickle.load(f)
            f.close()
            bolsa=juego[0]
            jugadores=juego[1]
            cant_rondas=juego[2]
            dic=juego[3]
            ultima_palabra=juego[4]
            nivel=juego[5]
            tiempo_ronda=juego[6]
            tiempo_partida=juego[7]
            cant_cambios=juego[8]
            tp_inicial=juego[9]
            tr_inicial=juego[10]

    except FileNotFoundError:
        sg.popup('No existen partidas guardadas.',title='Error', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        sys.exit()
    else:
        return bolsa, jugadores, cant_rondas, dic, ultima_palabra, nivel, tiempo_ronda, tiempo_partida, cant_cambios, tp_inicial, tr_inicial


def cargo(jugadores, multiUser, multiPC, ultimaPalabra, ultima_palabra, nivelConsideraciones, nivel, tiempo_partida, tiempo_ronda, tp_inicial, tr_inicial, tpConsideraciones, trConsideraciones):
    ''' 
    Función que actualiza los valores que se mostrarán por pantalla, según la configuración previamente guardada
    ''' 

    n='Nivel de la partida: {}'.format(nivel)
    tr='Tiempo de cada ronda: {} sg'.format(tp_inicial)
    tp='Tiempo de la partida: {} min'.format(tr_inicial)
    tpConsideraciones.Update(tp)
    trConsideraciones.Update(tr)
    nivelConsideraciones.Update(n)
    actualizar_multi(jugadores[0], multiUser, multiPC)
    actualizar_multi(jugadores[1], multiUser, multiPC)
    ultimaPalabra.Update(ultima_palabra[0].lower())

    return tiempo_partida, tiempo_ronda
    
    
    
#---------------------------------- FIN DEL JUEGO ----------------------------------

def atril(window, jugadores):
    aux=7
    for i in range(len(jugadores[0].atril_array())):
        window.FindElement(i).update(jugadores[0].atril_array()[i])

    for j in range(len(jugadores[1].atril_array())):
        window.FindElement(aux).update(jugadores[1].atril_array()[j]) 
        aux+=1

def ganador(jugadores, nivel):
    '''
    Función que recibe como parámetro mi lista de jugadores y me calcula el ganador del juego de acuerdo a sus puntajes.
    '''
    max=-999
    ganador=""
    for jugador in jugadores:
        if jugador.get_name()!='PC':
            top.guardo_puntajes(jugador, nivel)
        if jugador.get_puntajeFinal()>max:
            max=jugador.get_puntajeFinal()
            ganador=jugador.get_name()
        elif jugador.get_puntajeFinal()==max:
            ganador='Empate'


    if ganador=='PC':
        imagen='Imagenes/Derrota.png'
    elif ganador=='Empate': 
        imagen='Imagenes/Empate.png'
    else:
        imagen='Imagenes/Victoria.png'
        
    return imagen


def calcular(window, bag, jugadores):
    '''
    Función que resta al puntaje de cada jugador, el valor de las fichas que quedaron en su atril al final el juego. Retorna dos cadenas con cada letra y su valor para mostrarlo por pantalla y los dos puntajes finales.
    '''
    valores=bag.valores_letras()
    valores=bag.valores_letras()
    lista1=[]
    lista2=[]
    
    resta=0
    text1=''
    text2=''
    for i in range(len(jugadores[0].atril_array())):
        text1 = text1 + '- Letra: {} | Puntaje: {}\n'.format(jugadores[0].atril_array()[i], valores.get(jugadores[0].atril_array()[i]))
        resta = resta + valores.get(jugadores[0].atril_array()[i])

    total = jugadores[0].get_puntaje() - resta
    jugadores[0].set_puntajeFinal(total)
    final1 = '-Puntaje del jugador: {}\n-Suma de las fichas que quedaron en el atril: {}\n{} - {} = {} '.format(jugadores[0].get_puntaje(), resta, jugadores[0].get_puntaje(), resta, total)

    resta=0
    for j in range(len(jugadores[1].atril_array())):
        text2 = text2 + '- Letra {} | Puntaje {}\n'.format(jugadores[1].atril_array()[j], valores.get(jugadores[1].atril_array()[j]))
        resta = resta + valores.get(jugadores[1].atril_array()[j])
        
    total = jugadores[1].get_puntaje() - resta
    jugadores[1].set_puntajeFinal(total)

    final2 ='-Puntaje del jugador: {}\n-Suma de las fichas que quedaron en el atril: {}\n{} - {} = {} '.format(jugadores[1].get_puntaje(), resta, jugadores[1].get_puntaje(), resta, total)
    
    return text1, text2, final1, final2
  

def termino_juego(jugadores, bag, nivel):
    '''
    Función que desarrolla la interfaz gráfica que se muestra una vez finalizado el juego
    '''
    sg.SetOptions(background_color=('#D2B3BB'), text_element_background_color='#D2B3BB', element_background_color='#D2B3BB', text_color='saddlebrown')
    des={'font':('Verdana', 10), 'size':(12, 2), 'pad':((2,2),(30,30))}
    des1={'font':('Verdana', 15, 'bold'), 'text_color':('white')}
    des2={'button_color': ('saddlebrown','#FFE0A3'),'size':(4,2), 'font':('Verdana', 14)}
    des3={'font':('Verdana', 13)}
     
    text1= [[sg.Text('Fichas de:', **des3)] + [sg.Text(jugadores[0].get_name(), **des3)]]
    text2= [[sg.Text('Fichas de:', **des3)] + [sg.Text(jugadores[1].get_name(), **des3)]]
    
    

    layout = [  
                [sg.Text('LA PARTIDA HA FINALIZADO', **des1)],
                [sg.Column(text1)],
                [sg.Column(atril_interfaz(des2))],
                [sg.Multiline(size=(50, 5), key='__ml1__')],
                [sg.Column(text2)],
                [sg.Column(atril_interfaz_vacio(des2))],
                [sg.Multiline(size=(50, 5), key='__ml2__')],
                [sg.Button('Ver valores', **des), sg.Button('Calcular', **des), sg.Button('Salir', **des)],
                [sg.Image(filename='', pad=(0,10), key='__final__')]
             ]

    window = sg.Window('¡Gracias por jugar al ScrabbleAR!', layout, (500, 600), element_justification='center')
    window.Finalize()
            
    atril(window, jugadores)
    valores=calcular(window, bag, jugadores)
    imagen=ganador(jugadores, nivel)
    window.FindElement('__final__').update(imagen)
    while True:
        event, values = window.read()
        if event == 'Ver valores':
            lista1=valores[0]
            lista2=valores[1]
            window.FindElement('__ml1__').update(lista1)
            window.FindElement('__ml2__').update(lista2)
        if event is 'Calcular':
            total1=valores[2]
            total2=valores[3]
            window.FindElement('__ml1__').update(total1)
            window.FindElement('__ml2__').update(total2)
        if event is 'Salir':
            window.Close()
            sys.exit()
            
            


#---------------------------------- INTERFAZ GRÁFICA ----------------------------------

def columna_3():
    '''
    Función que desarrolla la interfaz gráfica de la columna derecha, donde se muestran el tiempo de la partida, las consideraciones, el puntaje de los usuarios, la última palabra escrita en el tablero 
    y los botones que dan fin al juego.
    '''
    sg.SetOptions(text_element_background_color='#D2B3BB', element_background_color='#D2B3BB')
    des={'font':('Verdana', 10, 'bold')}
    des2={'font':('Verdana', 15, 'bold')}
    des3={'font':('Verdana', 10), 'button_color': ('saddlebrown','#E5CEAC'), 'size':(16, 2), 'pad':((2,2),(45,2))}
    des4={'font':('Verdana', 10), 'title_color':'white', 'pad':(10,10)}
    frame_layout_user = [[sg.Text('0',key='_puntajeUser_', size=(10,2))]]
    frame_layout_pc = [[sg.Text('0', key='_puntajePC_', size=(10,2))]]
    
    columna_3 = [
                [sg.Text('TIEMPO (ronda / partida)', **des, background_color='#E5CEAC', text_color='saddlebrown')],
                [sg.Text("00:00",key=('__tiempoTurno__'), **des2), sg.Text('/', **des2), sg.Text("00:00", key=('__tiempoPartida__'), **des2)],
                [sg.Button('INICIAR', **des, size=(14, 2)), sg.Button('REGLAS', **des,  size=(14, 2))],
                [sg.Text(**des, key='__n__', size=(30, 1))],
                [sg.Text(**des, key='__tp__',size=(30, 1))],
                [sg.Text(**des, key='__tr__',size=(30, 1))],
                [sg.Text(**des, key='__pf__',size=(30, 9))],
                [sg.Text(**des, key='__cf__',size=(30, 9))],
                [sg.Frame('Puntaje Usuario', frame_layout_user, **des4),sg.Frame('  Puntaje PC  ', frame_layout_pc, **des4)],
                [sg.Text('Última palabra agregada:', **des)],
                [sg.Multiline(default_text='Aún no se ha ingresado ninguna palabra.',size=(30,3),key='_ultimaPalabra_', autoscroll=False)],
                [sg.Button('Salir', **des3),sg.Button('Posponer', **des3)],
                [sg.Button('Terminar juego', size=(30, 2), **des)],
              ]
    return columna_3


def atril_interfaz(des):
    '''
    Función que retorna una lista que representa el interfaz del jugador actual. Sus fichas se mostrarán siempre
    '''
    atrilInterfaz = [
                     [sg.Button(**des, key=0), 
                      sg.Button(**des, key=1),
                      sg.Button(**des, key=2),
                      sg.Button(**des, key=3),
                      sg.Button(**des, key=4),
                      sg.Button(**des, key=5),
                      sg.Button(**des, key=6)]
                    ]
    return atrilInterfaz
    
    
def atril_interfaz_vacio(des):
    '''
    Función que retorna una lista que representa un atril vacío (del jugador que está en espera). Nunca se mostrarán sus fichas
    '''
    atrilInterfaz = [
                     [sg.Button(**des, key=7), 
                      sg.Button(**des, key=8),
                      sg.Button(**des, key=9),
                      sg.Button(**des, key=10),
                      sg.Button(**des, key=11),
                      sg.Button(**des, key=12),
                      sg.Button(**des, key=13)]
                    ]
    return atrilInterfaz

    
def completo_atril(window, jugador):
    '''
    Función que completa el atril del jugador actual para la visualización de sus fichas.
    '''
    if jugador.get_name()=='PC':
        window.FindElement(0).update(jugador.atril_array()[0])
        window.FindElement(1).update(jugador.atril_array()[1])
        window.FindElement(2).update(jugador.atril_array()[2])
        window.FindElement(3).update(jugador.atril_array()[3])
        window.FindElement(4).update(jugador.atril_array()[4])
        window.FindElement(5).update(jugador.atril_array()[5])
        window.FindElement(6).update(jugador.atril_array()[6])
    else: 
        window.FindElement(0).update(jugador.atril_array()[0])
        window.FindElement(1).update(jugador.atril_array()[1])
        window.FindElement(2).update(jugador.atril_array()[2])
        window.FindElement(3).update(jugador.atril_array()[3])
        window.FindElement(4).update(jugador.atril_array()[4])
        window.FindElement(5).update(jugador.atril_array()[5])
        window.FindElement(6).update(jugador.atril_array()[6])  
        
        
        
def layout_jugar(diccTablero, board, carga, des2):
    '''
    Función que desarrolla la interfaz gráfica donde se muestra el tablero, los atriles de ambos jugadores y los botones que influyen en el turno del usuario.
    '''
    des={'button_color': ('saddlebrown','#FFE0A3'),  'size':(4,2), 'font':('Verdana', 14)}
    des3={'font':('Verdana', 10), 'size':(16, 2)}
    botones=[[sg.Button('Validar', **des3, pad=(7,5)), sg.Button('Pasar turno', **des3, pad=(7,5)), sg.Button('Cambiar fichas', **des3, pad=(7,0))]]
    text= [[sg.Text('ATRIL DE: ', **des2)] + [sg.Text('', key='__nombreAtril__', **des2, size=(15,1))]]
    columna1 =  []
    columna1 += atril_interfaz_vacio(des)
    columna1 += board.get_board(carga, diccTablero) 
    columna1 += atril_interfaz(des) +  text
    columna1 += botones
    columna3 =  columna_3()
    return columna1, columna3


def reglas():
    '''
    Función que desarrolla la interfaz gráfica donde se muestran las reglas del juego.
    '''
    sg.SetOptions(background_color='#D2B3BB')
    des={'font':('Verdana', 10), 'size':(10, 2)}
    layout=[
           [sg.Image(filename='Imagenes/Reglas.png', size=(630,700))], 
           [sg.Button('Volver', **des)]]
    
    window = sg.Window('Reglas del juego.', layout, size=(630,800), element_justification='center')
    
    event, values = window.Read()
    if event is 'Volver':
        window.Close()
    
