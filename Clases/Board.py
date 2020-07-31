import PySimpleGUI as sg
import random

#----------------------- CLASE TABLERO -----------------------

class Board:
    '''
      Board representa un tablero de juego de un tamaño específico, de acuerdo a la dificultad ingresada por el usuario. Le agrega las casillas de bonus
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
        if self.nivel=='Facil':
            self.filas=15
            self.columnas=15
        elif self.nivel == 'Medio':
            self.filas=17
            self.columnas=17
        elif self.nivel == 'Dificil':
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
        des={'size':(4,2), 'pad':(0,0), 'border_width':1, 'button_color':('peachpuff','white')}
        for fila in range(self.filas):
            layout_fila = []
            for col in range(self.columnas):
                aux=(fila, col)
                if aux in self.coordenadas()[0]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/x2.png', image_size=(36, 36), size=(4, 2), key=(fila, col), pad=(0,0), button_color=('white', '#79B7BF')))
                elif aux in self.coordenadas()[1]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/x3.png', image_size=(36, 36), size=(4, 2), key=(fila, col), pad=(0,0), button_color=('white', '#D2B3BB')))
                elif aux in self.coordenadas()[2]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/-2.png', image_size=(36, 37), size=(4, 2), key=(fila, col), pad=(0,0)))
                elif aux in self.coordenadas()[3]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/-3.png', image_size=(36, 36), size=(4, 2), key=(fila, col), pad=(0,0)))
                elif aux in self.coordenadas()[4]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/bomba.png', image_size=(36, 36), size=(4, 2), key=(fila, col), pad=(0,0), button_color=('white', 'white')))
                elif aux in self.coordenadas()[5]:
                    layout_fila.append(sg.Button(image_filename='Imagenes/estrella.png', image_size=(36, 36), size=(4, 2), key=(fila, col), pad=(0,0), button_color=('white', 'white')))
                else:
                    layout_fila.append(sg.Button(' ', key=(fila,col), **des))
            tablerogame.append(layout_fila) 
            
        return tablerogame

        
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
        esqueleto[m][s]=sg.Button(fichita,size=(4, 2), key=(m,s), pad=(0,0), button_color=('saddlebrown','#FFE0A3'))
        return esqueleto
        
    def get_board(self, carga, dic):
        '''
        Arma mi tablero final y lo retorna
        '''
        aux=self.esqueleto()
        tablerogame=self.agregar_centro(aux)
        if carga:
            t=self.guardo_board(dic, tablerogame)
            return t
        else:
            return tablerogame

        
    def devolver_fichas(self, dic, cant_rondas, window, diccTablero):
        '''
        Recibe como parámetros el  atril del jugador, la cantidad de rondas y mi window. 
        Si es la primera ronda jugada, elimina del diccionario del jugador la ficha del centro para no tenerla en cuenta.
        Devuelve las fichas jugadas si es que la palabra que se jugó no fue válida
        '''
        a=dic.copy()
        if cant_rondas==1 or len(diccTablero)==1:
            if self.nivel == 'Facil':
                del a[(7,7)]
            elif self.nivel == 'Medio':
                del a[(8,8)]
            elif self.nivel == 'Dificil':
                del a[(9,9)]
        fichas_devolver=list(a.keys())
        for elem in fichas_devolver:
            fila=elem[0]
            columna=elem[1]
            if (fila, columna) in self.lista_coordenadas():
                prob=self.coordenadas()
                if (fila, columna) in prob[0]:
                    window[(fila, columna)]('', image_filename='Imagenes/x2.png', image_size=(36, 35), pad=(0,0), button_color=('white', '#79B7BF'))
                elif (fila, columna) in prob[1]:
                    window[(fila, columna)]('', image_filename='Imagenes/x3.png', image_size=(36, 35), pad=(0,0), button_color=('white', '#D2B3BB'))
                elif (fila, columna) in prob[2]:
                    window[(fila, columna)]('', image_filename='Imagenes/-2.png', image_size=(36, 35), pad=(0,0))
                elif (fila, columna) in prob[3]:
                    window[(fila, columna)]('', image_filename='Imagenes/-2.png', image_size=(36, 35), pad=(0,0))
                elif (fila, columna) in prob[4]:
                    window[(fila, columna)]('', image_filename='Imagenes/bomba.png', image_size=(36, 35), pad=(0,0), button_color=('white', 'white'))
                elif (fila, columna) in prob[5]:
                    window[(fila, columna)]('', image_filename='Imagenes/estrella.png', image_size=(36, 35), pad=(0,0), button_color=('white', 'white'))
            else:
                window.FindElement((fila, columna)).update('', button_color=('peachpuff','white'))


    def coordenadas(self):
        '''
        Inicializa las coordenadas de las imagenes dependiendo el nivel ingresado por el jugador
        '''
        if self.nivel=='Facil':
            imagesX2 = [(0,14), (1,13), (2,12), (3,11),(4,10),(5,9),(6,8),(8,6),(9,5),(10,4),(11,3),(12,2),(13,1),(14,0)]
            imagesx3 = [(0,0), (1,1), (2,2), (3,3),(4,4),(5,5),(6,6),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14)]
            imagesneg2 = [(0,6), (3,5), (3,9), (3,14), (5,2), (11,0), (11,5) ,(14,8), (11,9), (9,12)]
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
        elif self.nivel=='Dificil':
            imagesX2Dificil = [(0,18), (1,17), (2,16), (3,15),(4,14),(5,13),(6,12),(7,11),(8,10),(10,8),(11,7),(12,6),(13,5),(14,4),(15,3),(16,2),(17,1),(18,0)]
            imagesx3Dificil= [(0,7),(0,11),(1,4),(1,14),(4,1),(4,17),(7,0),(7,18),(11,0),(11,18),(14,1),(14,17),(18,7),(18,11),(17,4),(17,14)]  
            imagesneg2Dificil = [(7,4),(2,8),(5,7),(5,11),(5,16),(11,14),(16,10),(13,7),(13,2),(13,11)]
            imagesneg3Dificil = [(6,8),(6,10),(8,5),(10,5),(12,8),(12,10),(8,13),(10,13)]
            imagesbombaDificil = [(0,0), (1,1), (2,2), (3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(3,9),(6,3), (12,3), (15,9), (12,15), (6,15)]
            imagesetrellaDificil = [(5,2), (11,4), (2,10),(7,14),(13,16), (16,8)]
            return imagesX2Dificil, imagesx3Dificil, imagesneg2Dificil, imagesneg3Dificil, imagesbombaDificil, imagesetrellaDificil
    
    
    def guardo_board(self, dic, tablerogame):
        t=tablerogame
        lista_values=[]
        aux=0
        for j in dic.values():
            lista_values.append(j)
        for i in dic.keys():
            t[i[0]][i[1]]=sg.Button(lista_values[aux], button_color=('saddlebrown','#FFE0A3'), size=(4, 2), pad=(0,0))
            aux+=1
        return t


    def lista_coordenadas(self):
        coordenadas=self.coordenadas()
        lista_coord=[]
        for elem in coordenadas:
            for i in elem:
                lista_coord.append(i)
    
        return lista_coord
        
    
