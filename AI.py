import itertools
from Palabra import Palabra
import random
from pattern.es import tag, spelling, lexicon, verbs
import Funciones as fun
import PySimpleGUI as sg


#Función que devuelve una lista de combinaciones posibles con las letras del atril del jugador
def combinaciones_pc(ficha_centro, jugador, cant_rondas):
    letras=jugador.atril_array()
    combinaciones=[]
    if cant_rondas==1:
        letras.append(ficha_centro)
    for p in range(2, 9):
        lista_de_letras= list(itertools.permutations(list(letras), p))
        combinaciones.append(lista_de_letras)
    return combinaciones[1]     #Devuelve sólo las combinaciones de tres letras. (2: cuatro letras. 3: cuatro letras....ó, sin índice, todas)
    

#Función que genera una palabray la verifica
def generador_de_palabra(ficha_centro, jugador, board, cant_rondas, dicTablero):
    found=True
    i=0
    combinaciones=combinaciones_pc(ficha_centro, jugador, cant_rondas)
    while found and i<len(combinaciones):
        if combinaciones!=None :
            word = "".join(combinaciones[i])
            palabra=Palabra(word, jugador, board)
            if cant_rondas==1 or len(dicTablero)==1:
                if ficha_centro in word:
                    if palabra.convert():
                        found=False
                        return word, palabra
                
            else:
                if palabra.convert():
                    found= False
                    return word, palabra
            i=i+1
    if i==(len(combinaciones)):
        word=None
        return word, False
            

#Función que posiciona la palabra genereda en el tablero
def posiciona_palabra(palabra, ficha_centro, dicTablero, board, jugador, window, cant_rondas, dicc):
    f=board.get_medio()[0]
    c=f
    if cant_rondas==1 or len(dicTablero)==1:
        dicc[(f, c)]=ficha_centro
        vp=valor_posicion(palabra, ficha_centro)
        for i in range(len(palabra)):
            if i==vp:
                continue
            mover = (f + i) - vp #ubica en fila, se mueve por columna
            pos_atril=jugador.atril_array().index(palabra[i])
            c=mover
            dicc[(f, c)]=palabra[i]
            dicTablero[(f, c)]=palabra[i]
            fun.actualizo_atril(window, pos_atril, (f,c), palabra[i])
    else:
        f=(random.randint(0, 14))
        c=(random.randint(0, 14))
        key=(f,c)
        aux=key
        cont=0
        while aux not in dicTablero and cont!=len(palabra)-1:
            cont=cont+1
            c=c+1
            aux=(f,c)
        if aux not in dicTablero:
            hayEspacio=True
        else:
            hayEspacio=False
        if hayEspacio:
            fila=key[0]
            columna=key[1]
            for i in range(len(palabra)):
                dicc[(fila, columna)]=palabra[i]
                dicTablero[(fila, columna)]=palabra[i]
                pos_atril=jugador.atril_array().index(palabra[i])
                fun.actualizo_atril(window, pos_atril, (f,columna), palabra[i])
                columna=columna+1
                
                
                
def valor_posicion(lista, ficha_central):
    i=0
    while lista[i]!=ficha_central:
        i=i+1
    return i 
        
            
                
#Función que desarrolla el turno de la PC                
def juega_PC(dicc,dicTablero, ficha_central, jugador, board, window, jugadores, cant_rondas,multiUser, multiPC, ultimaPalabra, nivel):
    palabra=generador_de_palabra(ficha_central, jugador, board, cant_rondas, dicTablero)
    if palabra[0]!=None:
        posiciona_palabra(palabra[0], ficha_central, dicTablero, board, jugador, window, cant_rondas, dicc)
        puntaje=palabra[1].calcular_puntaje(dicc)
        jugador.aumentar_puntaje(puntaje)
        text='La PC encontró la palabra {} con puntaje {}'.format(palabra[0], puntaje)
        sg.popup(text ,background_color='#D2B3BB')
        ultimaPalabra.Update(palabra[1].get_palabra().lower())
        fun.actualizar_multi(jugador,multiUser, multiPC)
        jugador.actualizar_atril(dicc, cant_rondas, nivel)
    else:
        sg.popup('La PC no encontró ninguna palabra y su turno ha pasado',background_color='#D2B3BB')

    jugador.vaciar_dicc()
        

        
