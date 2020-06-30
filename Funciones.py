from Jugador import Jugador
from Board import Board
from Palabra import Palabra
from Atril import Atril
import PySimpleGUI as sg


primer_ronda= [(4,5),(5,4),(5,6),(6,5)]       

def instanciar_jugadores(bag, nom, jugadores):
    jugador1 = Jugador(bag, nom)
    jugador2 = Jugador(bag, 'PC')
    jugadores.append(jugador1)
    jugadores.append(jugador2)
    return jugadores
    
#-------------------------------------------------------------------------------        
#Funciones de la interfaz gráfica

def columna_layout():
    columna =   [
                [sg.Text('-'*70,background_color='#D2B3BB')],
                [sg.Button('Validar', button_color=('white','saddlebrown'), size=(16, 2), font=("Verdana", 10)), 
                 sg.Button('Pasar turno',  button_color=('white','saddlebrown'), size=(16, 2), font=("Verdana", 10))], 
                [sg.Button('Cambiar fichas', button_color=('white','saddlebrown'),  size=(16, 2), font=("Verdana", 10)),
                 sg.Button('Salir', button_color=('white','saddlebrown'),  size=(16, 2), font=("Verdana", 10))],
                [sg.Text('  ',background_color='#D2B3BB')],
                [sg.Text('Puntaje Total del Usuario', font='Default 10', justification='center', background_color='#D2B3BB')],
                [sg.Multiline(default_text='Puntaje del usuario: 0',size=(37,5),key='_puntajeUser_', autoscroll=False)],
                [sg.Text('Puntaje Total de la PC', font='Default 10', justification='center', background_color='#D2B3BB')],
                [sg.Multiline(default_text='Puntaje de la PC: 0', size=(37,5),key='_puntajePC_', autoscroll=False)],
                [sg.Text('Última palabra agregada:', font='Default 10', justification='center', background_color='#D2B3BB')],
                [sg.Multiline(size=(37,5),key='_ultimaPalabra_', autoscroll=False)],
                [sg.Text(size=(8, 2), font=('Helvetica', 20), justification='center', key='__time_partida__', background_color='#D2B3BB', pad=(80,10))],
                [sg.Button('Terminar juego', button_color=('saddlebrown','#E5CEAC'), size=(16, 2), font=("Verdana", 10), pad=(80,10))]
                ]
    return columna
                
def columna3():
    columna_3 = [
                [sg.Text('-'*70,background_color='#D2B3BB')],
                [sg.Button('Top 10 Jugadores', button_color=('white','saddlebrown'), size=(16, 2), font=("Verdana", 10)),
                 sg.Button('Guardar partida', button_color=('white','saddlebrown'), size=(16, 2), font=("Verdana", 10))],
                [sg.Text("", size=(35, 3), key='__topten__', background_color='#D2B3BB')]
              ]
    return columna_3


def atril_interfaz():
    atrilInterfaz = [
                     [sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=0), 
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=1),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=2),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=3),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=4),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=5),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=6)]
                    ]
    return atrilInterfaz
    
    
def atril_interfaz_vacio():
    atrilInterfaz = [
                     [sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=7), 
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=8),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=9),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=10),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=11),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=12),
                      sg.Button(size=(4,2),font='verdana 14', button_color=('saddlebrown','#FFE0A3'), key=13)]
                    ]
    return atrilInterfaz

    
def completo_atril(window, jugador):
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
                      

#-------------------------------------------------------------------------------    

#Función que me calcula el ganador del juego cuando aprieto el botón "Terminar Juego"

def ganador(jugadores):
    max=0
    ganador=""
    for jugador in jugadores:
        if jugador.get_puntaje()>max:
            max=jugador.get_puntaje()
            ganador=jugador.get_name()
            
    sg.popup('El ganador es: ',ganador,'. ¡Felicitaciones! ',background_color='#D2B3BB')
    
    
#-------------------------------------------------------------------------------       

#Función que me actualiza los puntajes de los jugadores en pantalla

def actualizar_multi(jugador,multiUser, multiPC):
    if jugador.get_name()=='PC':
        text='Puntaje de la PC: {}'.format(jugador.get_puntaje())
        multiPC.Update(text)
    else:
        text='Puntaje de {} : {}'.format(jugador.get_name(),jugador.get_puntaje())
        multiUser.Update(text)
        
            
#-------------------------------------------------------------------------------       

#Función que desarrolla el turno del usuario

def validar_palabra(window, diccTablero, dicc, jugador, multiUser, multiPC, ultimaPalabra, cant_rondas, board, nivel):
    diccOrd=dict(sorted(dicc.items()))
    listaLetras=a_lista(diccOrd)
    word = "".join(listaLetras)
    palabra=Palabra(word, jugador, board)
    if palabra.convert():
        puntaje=palabra.calcular_puntaje(diccOrd)
        jugador.aumentar_puntaje(puntaje)
        actualizar_multi(jugador,multiUser, multiPC)
        jugador.actualizar_atril(diccOrd, cant_rondas, nivel)
        sg.popup('Palabra válida. Puntaje: ',puntaje, background_color='#D2B3BB')
        ultimaPalabra.Update(palabra.get_palabra().lower())
        diccTablero.update(dicc)
    else:
        sg.popup('Palabra Inválida. Perdió el turno. Se devuelven las fichas jugadas', background_color='#D2B3BB')
        #devolver fichas al atril
        board.devolver_fichas(diccOrd, cant_rondas, window)

    
    jugador.vaciar_dicc()
    

#-------------------------------------------------------------------------------        

#Funciones que influyen en el armado de palabra en el tablero. Determinan que sea por fila o columna

def armar_palabra(dicc, event, aux, window, vacio, fila, columna, cant_rondas, board, diccTablero):
    if cant_rondas==1 or len(diccTablero)==1:
        medio=board.get_medio()
        dicc[(medio[0],medio[1])]=board.ficha_centro()
    if not dicc:
        dicc[event] = aux 
        actualizo_atril(window, vacio, event, aux)
    else:
        pos=list(dicc.keys())[0]
        if len(dicc)==1:
            var_de_pos=verificar_segunda(event, pos, dicc, aux, window, vacio)
            if  var_de_pos==1:
                columna=False
            else:
                fila=False
        else:
            pos_palabra(pos, event, window, vacio, aux, dicc, fila, columna)
    return columna, fila


def pos_palabra(vieja_coord, nueva_coord, window, vacio, aux, dicc, fila, columna):
    if nueva_coord[0] == vieja_coord[0] and fila:
        juego(vieja_coord, nueva_coord, window, vacio, aux, dicc)
    elif nueva_coord[1] == vieja_coord[1] and columna:
        juego(vieja_coord, nueva_coord, window, vacio, aux, dicc)
    else:
        sg.popup('Error. Movimiento no permitido.', background_color='#D2B3BB')
        
            
def juego (vieja_coord, nueva_coord,  window, vacio, aux, dicc):
    dicc[nueva_coord] = aux
    actualizo_atril(window, vacio, nueva_coord, aux)
            
def verificar_segunda(event, pos, dicc, aux, window, vacio):
    if (event[0]==pos[0]) and ((event[1]==(pos[1]-1)) or (event[1]==(pos[1]+1))):
        dicc[event] = aux 
        actualizo_atril(window, vacio, event, aux)
        #print('entra fila')
        return 1
    elif (event[1]==pos[1]) and ((event[0]==(pos[0]-1)) or (event[0]==(pos[0]+1))):
        dicc[event] = aux 
        actualizo_atril(window, vacio, event, aux)
        #print('entra columna')
        return 2
    else:
        sg.popup('Error. Movimiento no permitido.', background_color='#D2B3BB')
            
    

#------------------------------------------------------------------------------- 

#Función que me actualiza el atril cuando se juega la ficha (vacía el espacio) y actualiza el tablero con la letra del atril

def actualizo_atril(window, vacio, event, aux):
    window.FindElement(vacio).update("",button_color=('saddlebrown','#FFE0A3')) 
    window.FindElement(event).update(aux, button_color=('saddlebrown','#FFE0A3')) 

#-------------------------------------------------------------------------------    

#Función que me devuelve el jugador siguiente

def next_player(jugador,jugadores):
    if jugadores.index(jugador) != (len(jugadores)-1):
        jugador=jugadores[jugadores.index(jugador)+1]
    else:
        jugador = jugadores[0]
    sg.popup('Es el turno del jugador: ' ,jugador.get_name(), background_color='#FFE0A3', text_color='saddlebrown')
    return jugador
    
    
#------------------------------------------------------------------------------- 

#Función que convierte los valores de mi diccionario en una lista de letras (con la que verifico si existe mi palabra)
    
def a_lista(dic):
    listaLetras=[]
    for elem in dic.values():
        listaLetras.append(elem)
    return listaLetras


                 
