'''
ScrabbleAR
 - Autor: Remorini Maria Lara
 - Mail: remoriniml@gmail.com
 - GitHub: https://github.com/daiseves - 

Todas las imagenes utilizadas en este proyecto son de propia autoría.
'''

import random
import itertools
import PySimpleGUI as sg
from Clases.Palabra import Palabra
from Funciones import Funciones as fun
from pattern.es import tag, spelling, lexicon, verbs

#Función que devuelve una lista de combinaciones posibles con las letras del atril del jugador
def combinaciones_pc(ficha_centro, jugador, cant_rondas):
    letras=jugador.atril_array().copy()
    combinaciones=[]
    if cant_rondas==1:
        letras.append(ficha_centro)
    for p in range(2, 5):       #rango de 2 a 4 letras, si quiero las combinaciones completas, cambio a range(2,9)
        lista_de_letras= list(itertools.permutations(list(letras), p))
        combinaciones.append(lista_de_letras)
    return combinaciones     
    

#Función que genera una palabray la verifica
def generador_de_palabra(ficha_centro, jugador, board, cant_rondas, dicTablero, bag):
    found=True
    j=1    #Combinaciones de tantas letras. 2=combinaciones de cuatro letras
    combinaciones=combinaciones_pc(ficha_centro, jugador, cant_rondas)
    while found and j>=0:
        i=0
        while found and i<len(combinaciones[j]):
            if combinaciones!=None :
                word = "".join(combinaciones[j][i])
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
        j=j-1     
    
    #Si llega al valor de len(combinaciones), significa que no encontró la palabra
    if found:
        word=None
        return word, False
        
            
    # if i==(len(combinaciones[j])):
        # word=None
        # return word, False
            

#Función que posiciona la palabra generada en el tablero
def posiciona_palabra(palabra, ficha_centro, dicTablero, board, jugador, window, cant_rondas, dicc, lista_coordenadas, nivel):
    if nivel=='Facil':
        limite=15
    elif nivel=='Medio':
        limite=17
    elif nivel=='Dificil':
        limite=19
        
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
            fun.actualizo_atril_tablero(window, pos_atril, (f,c), palabra[i], lista_coordenadas)
    else:
        exito=False
        while not exito:
            pos=random.choice([0,1])
            f=(random.randint(0, limite-1))
            c=(random.randint(0, limite-1))

            modo=random.choice([0,1])   #0: vertical , 1:horizontal

            #Verifico si la palabra entra en el tablero
            if modo==0:  
                if (f+len(palabra)>=limite):    
                    a = f+len(palabra)-limite
                    f = f-a
            elif modo==1:
                if (c+len(palabra)>=limite):
                    a = c+len(palabra)-limite
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
                
                
            # HAY PROBLEMA SI NO HAY ESPACIO HAY QUEPONERLE UN TRY EXCEPT
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
    i=0
    while lista[i]!=ficha_central:
        i=i+1
    return i 
 
 
def cambia_fichasAI(window, jugador):
    azar=[0,1,2,3,4,5,6]
    print(jugador.atril_array())
    letras_a_cambiar=[]
    for i in range(3):
        num=random.choice(azar)
        azar.remove(num)
        print(num)
        letras_a_cambiar.append(jugador.atril_array()[num])
    jugador.cambiar_fichas(letras_a_cambiar)
    fun.completo_atril(window, jugador)

                
#Función que desarrolla el turno de la PC                
def juega_PC(dicc,dicTablero, ficha_central, jugador, board, window, jugadores, cant_rondas, multiUser, multiPC, ultimaPalabra, nivel, ultima_palabra, bag, lista_coordenadas):
    palabra=generador_de_palabra(ficha_central, jugador, board, cant_rondas, dicTablero, bag)
    if palabra[0]!=None:
        posiciona_palabra(palabra[0], ficha_central, dicTablero, board, jugador, window, cant_rondas, dicc, lista_coordenadas, nivel)
        puntaje=palabra[1].calcular_puntaje(dicc)
        jugador.aumentar_puntaje(puntaje)
        text='La PC encontró la palabra {} con puntaje {}'.format(palabra[0], puntaje)
        sg.popup(text ,title='Válida', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        ultimaPalabra.Update(palabra[1].get_palabra().lower())
        ultima_palabra[0]=palabra[1].get_palabra().lower()
        fun.actualizar_multi(jugador,multiUser, multiPC)
        exito=jugador.actualizar_atril(dicc, cant_rondas, nivel)
        if exito==None:
            window.Finalize()
            fun.termino_juego(jugadores, bag)
    else:
        sg.popup('La PC no encontró ninguna palabra y su turno ha pasado', title=':(', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
        cambia_fichasAI(window, jugador)

    jugador.vaciar_dicc()

