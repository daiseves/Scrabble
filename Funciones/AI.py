import random
import itertools
import PySimpleGUI as sg
from Clases.Palabra import Palabra
from Funciones import Funciones as fun
from pattern.es import tag, spelling, lexicon, verbs



def combinaciones_pc(ficha_centro, jugador, cant_rondas):
    
    """
    Función que retorna una lista de combinaciones posibles realizadas con las letras del atril de la PC. 
    Retorna sólo las combinaciones de tres letras.
    
    """
    
    
    letras=jugador.atril_array()
    combinaciones=[]
    if cant_rondas==1:
        letras.append(ficha_centro)
    for p in range(2, 9):
        lista_de_letras= list(itertools.permutations(list(letras), p))
        combinaciones.append(lista_de_letras)
    return combinaciones[1]     #Devuelve sólo las combinaciones de tres letras. (2: cuatro letras. 3: cuatro letras....ó, sin índice, todas)
    


def generador_de_palabra(ficha_centro, jugador, board, cant_rondas, dicTablero, bag):
   
    """
    Función que recibe una lista de combinaciones posibles y toma la primer palabra verificada como válida.
    
    """
    
    found=True
    i=0
    combinaciones=combinaciones_pc(ficha_centro, jugador, cant_rondas)
    while found and i<len(combinaciones):
        if combinaciones!=None :
            word = "".join(combinaciones[i])
            palabra=Palabra(word, jugador, board, bag)
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
            


def posiciona_palabra(palabra, ficha_centro, dicTablero, board, jugador, window, cant_rondas, dicc, lista_coordenadas):
       
    """
    Función que posiciona en el tablero una palabra ya generada y tomada como válida.
    
    """
    
    f=board.get_medio()[0]
    c=f
    if cant_rondas==1 or len(dicTablero)==1:
        dicc[(f, c)]=ficha_centro
        #Recibo la posición de la letra que coincide con la ficha central para hacer el continue y poder posicionar la palabra de forma correcta sin superponer las fichas.
        vp=valor_posicion(palabra, ficha_centro)
        for i in range(len(palabra)):
            if i==vp:
                continue
            mover = (f + i) - vp #ubica en fila, se mueve por columna
            pos_atril=jugador.atril_array().index(palabra[i])
            c=mover
            dicc[(f, c)]=palabra[i]
            dicTablero[(f, c)]=palabra[i]
            fun.actualizo_atril_tablero(window, pos_atril, (f,c), palabra[i], lista_coordenadas)
    else:
        exito=False
        while not exito:
            pos=random.choice([0,1])
            f=(random.randint(0, 14))
            c=(random.randint(0, 14))

            modo=random.choice([0,1])   #0: vertical , 1:horizontal

            #Verifico si la palabra entra en el tablero
            if modo==0:  
                if (f+len(palabra)>=15):    
                    a = f+len(palabra)-15
                    f = f-a
            elif modo==1:
                if (c+len(palabra)>=15):
                    a = c+len(palabra)-15
                    c = c-a

            #Verifico que la palabra se pueda poner en el tablero
            key=(f,c)
            aux=key
            cont=0
            while aux not in dicTablero and cont!=len(palabra)-1:
                cont=cont+1
                if modo==0:  
                    f=f+1
                elif modo==1:
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
                    fun.actualizo_atril_tablero(window, pos_atril, (fila,columna), palabra[i], lista_coordenadas)
                    if modo==0:
                        fila=fila+1
                    else:
                        columna=columna+1
                exito=True
                
                
def valor_posicion(lista, ficha_central):
       
    """
    De acuerdo a la palabra generada, devuelve la posición en la que se encuentra la letra que coincide con la ficha en el centro del tablero.
    
    """
    
    i=0
    while lista[i]!=ficha_central:
        i=i+1
    return i 
        
            
                              
def juega_PC(dicc,dicTablero, ficha_central, jugador, board, window, jugadores, cant_rondas, multiUser, multiPC, ultimaPalabra, nivel, ultima_palabra, bag, lista_coordenadas):
       
    """
    Función que desarrolla el turno de la PC.
    
    """
    
    palabra=generador_de_palabra(ficha_central, jugador, board, cant_rondas, dicTablero, bag)
    if palabra[0]!=None:
        posiciona_palabra(palabra[0], ficha_central, dicTablero, board, jugador, window, cant_rondas, dicc, lista_coordenadas)
        puntaje=palabra[1].calcular_puntaje(dicc)
        jugador.aumentar_puntaje(puntaje)
        text='La PC encontró la palabra {} con puntaje {}'.format(palabra[0], puntaje)
        sg.popup(text ,background_color='#D2B3BB')
        ultimaPalabra.Update(palabra[1].get_palabra().lower())
        ultima_palabra[0]=palabra[1].get_palabra().lower()
        fun.actualizar_multi(jugador,multiUser, multiPC)
        jugador.actualizar_atril(dicc, cant_rondas, nivel)
    else:
        sg.popup('La PC no encontró ninguna palabra y su turno ha pasado', background_color='#D2B3BB')

    jugador.vaciar_dicc()
        

        

