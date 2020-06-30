
import PySimpleGUI as sg
import random

#----------------------- CLASE TABLERO -----------------------

class Board:
    '''
      Board represent un tablero de juego de un tamaño específico, de acuerdo a la dificultad ingresada por el usuario. Le agrega las casillas de bonus
    '''
    def __init__(self, Bag, nivel):
        self.filas=0
        self.columnas=0
        self.nivel=nivel
        self.ini_dim()
        self.bag=Bag
        self.ficha_central=self.bag.dar_ficha()
        self.cant_rondas=1

    def ini_dim(self):
        '''
        inicializa las filas y columnas de mi tablero según la dificultad ingresada por el usuario
        '''
        if self.nivel=='Fácil':
            self.filas=15
            self.columnas=15
        elif self.nivel == 'Medio':
            self.filas=17
            self.columnas=17
        elif self.nivel == 'Difícil':
            self.filas=19
            self.columnas=19

    def get_medio(self):
        '''
        calcula cuál es el casillero central del tablero y retorna el valor como un entero
        '''
        filaMedio=int(self.filas-1)//2
        columnaMedio=int(self.columnas-1)//2
        return filaMedio, columnaMedio
    

    def esqueleto(self):
        '''
        crea una matriz con las dimensiones según la dificultad elegida y le agrega un botón vacío a cada casillero. Retorna el tablero de botones vacío
        '''
        tablerogame = []
        for fila in range(self.filas):
            layout_fila = []
            for col in range(self.columnas):
                layout_fila.append(sg.Button(' ', size=(4, 2), key=(fila,col), pad=(2,2), button_color=('peachpuff','white')))
            tablerogame.append(layout_fila) 
        return tablerogame

    def agregar_bonus(self, esqueleto):
        '''
        Recibe como parámetro mi tablero de botones vacíos, les agrega las casillas de bonus y retorna el tablero modificado
        '''
        aux=self.coordenadas()
        for j in aux[0]:
            esqueleto[j[0]][j[1]]=sg.Button(filename='Imagenes/x2.png', image_size=(37, 37), size=(4, 2), key=(j[0],j[1]), pad=(2,2), button_color=('white', '#79B7BF'))
        for k in aux[1]:
            esqueleto[k[0]][k[1]]=sg.Button(filename='Imagenes/x3.png', image_size=(37, 37), size=(4, 2), key=(k[0],k[1]), pad=(2,2), button_color=('white', '#D2B3BB'))
        for l in aux[2]:
            esqueleto[l[0]][l[1]]=sg.Button(filename='Imagenes/-2.png', image_size=(37, 37), size=(4, 2), key=(l[0],l[1]), pad=(2,2))
        for m in aux[3]:
            esqueleto[m[0]][m[1]]=sg.Button(filename='Imagenes/-3.png', image_size=(37, 37), size=(4, 2), key=(m[0],m[1]), pad=(2,2))
        for n in aux[4]:
            esqueleto[n[0]][n[1]]=sg.Button(filename='Imagenes/bomba.png', image_size=(37, 37), size=(4, 2), key=(n[0],n[1]), pad=(2,2), button_color=('white', 'white'))
        for o in aux[5]:
            esqueleto[o[0]][o[1]]=sg.Button(filename='Imagenes/estrella.png', image_size=(37, 37), size=(4, 2), key=(o[0],o[1]), pad=(2,2), button_color=('white', 'white'))
        return esqueleto
        
        
    def ficha_centro(self):
        '''
        Retorna al valor de la ficha que inicia en el centro del tablero al comienzo del juego
        '''
        return self.ficha_central
    
    def agregar_centro(self, esqueleto):
        '''
        Recibe como parámetro mi tablero con los bonus ya agregados y le añade la ficha que inicia en el centro al comienzo del juego
        '''
        m=self.get_medio()[0]
        s=self.get_medio()[1]
        fichita=self.ficha_centro()
        esqueleto[m][s]=sg.Button(fichita,size=(4, 2), key=(m,s), pad=(2,2), button_color=('saddlebrown','#FFE0A3'))
        return esqueleto
        
    def get_board(self):
        '''
        Arma mi tablero final y lo retorna
        '''
        aux=self.esqueleto()
        aux2=self.agregar_bonus(aux)
        tablerogame=self.agregar_centro(aux2)
        return tablerogame
        
    def devolver_fichas(self, dic, cant_rondas, window):
        '''
        Recibe como parámetros el  atril del jugador, la cantidad de rondas y mi window. 
        Si es la primera ronda jugada, elimina del diccionario del jugador la ficha del centro para no tenerla en cuenta.
        Devuelve las fichas jugadas si es que la palabra que se jugó no fue válida
        '''
        a=dic.copy()
        if cant_rondas==1:
            if self.nivel == 'Fácil':
                del a[(7,7)]
            elif self.nivel == 'Medio':
                del a[(8,8)]
            elif self.nivel == 'Difícil':
                del a[(9,9)]
        fichas_devolver=list(a.keys())
        for elem in fichas_devolver:
            fila=elem[0]
            columna=elem[1]
            window.FindElement((fila, columna)).update('', button_color=('peachpuff','white'))


    def coordenadas(self):
        '''
        Inicializa las coordenadas de las imagenes dependiendo el nivel ingresado por el jugador
        '''
        if self.nivel=='Fácil':
            imagesX2 = [(0,14), (1,13), (2,12), (3,11),(4,10),(5,9),(6,8),(8,6),(9,5),(10,4),(11,3),(12,2),(13,1),(14,0)]
            imagesx3 = [(0,0), (1,1), (2,2), (3,3),(4,4),(5,5),(6,6),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14)]
            imagesneg2 = [(0,6), (3,5), (3,9), (3,14), (5,2), (11,0), (14,8), (11,9), (9,12)]
            imagesneg3 = [(4,6), (4,8), (6,3), (8,3), (6,11), (8,11), (10,6), (10,8)]
            imagesbomba = [(4,1),(1,7),(4,13),(10,1),(13,7),(10,13)]
            imagesestrella = [(0,8),(9,2),(14,6),(3,0),(5,12),(11,14)]
            return imagesX2, imagesx3, imagesneg2, imagesneg3, imagesbomba,  imagesestrella
        elif self.nivel=='Medio':
            imagesX2Medio = [(0,16), (1,15), (2,14), (3,13),(4,12),(5,11),(6,10),(7,9),(9,7),(10,6),(11,5),(12,4),(13,3),(14,2),(15,1),(16,0)]
            imagesx3Medio = [(0,0), (2,2),(4,4),(6,6),(10,10),(12,12),(14,14),(16,16)]
            imagesneg2Medio = [(1,7),(4,6),(4,10),(4,15),(6,3),(10,13),(12,1),(12,6),(12,10),(15,9)]
            imagesneg3Medio = [(5,7),(5,9),(7,4),(7,12),(9,4),(9,12),(11,7),(11,9)]
            imagesbombaMedio = [(1,1),(3,3),(2,8),(3,0),(3,16),(5,2),(5,5),(5,14),(7,7),(9,9),(11,2),(11,11),(11,14),(13,0),(13,13),(13,16),(14,8),(15,15)]
            imagesetrellaMedio = [(1,9),(4,1),(6,13),(10,3),(12,15),(15,7)]
            return imagesX2Medio, imagesx3Medio, imagesneg2Medio, imagesneg3Medio, imagesbombaMedio, imagesetrellaMedio 
        elif self.nivel=='Difícil':
            imagesX2Dificil = [(0,18), (1,17), (2,16), (3,15),(4,14),(5,13),(6,12),(7,11),(8,10),(10,8),(11,7),(12,6),(13,5),(14,4),(15,3),(16,2),(17,1),(18,0)]
            imagesx3Dificil= [(0,7),(0,11),(1,4),(1,14),(4,1),(4,17),(7,0),(7,18),(11,0),(11,18),(14,1),(14,17),(18,7),(18,11),(17,4),(17,14)]  
            imagesneg2Dificil = [(7,4),(2,8),(5,7),(5,11),(5,16),(11,14),(16,10),(13,7),(13,2),(13,11)]
            imagesneg3Dificil = [(6,8),(6,10),(8,5),(10,5),(12,8),(12,10),(8,13),(10,13)]
            imagesbombaDificil = [(0,0), (1,1), (2,2), (3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(3,9),(6,3), (12,3), (15,9), (12,15), (6,15)]
            imagesetrellaDificil = [(5,2), (11,4), (2,10),(7,14),(13,16), (16,8)]
            return imagesX2Dificil, imagesx3Dificil, imagesneg2Dificil, imagesneg3Dificil, imagesbombaDificil, imagesetrellaDificil


