from pattern.es import tag, spelling, lexicon, verbs


#----------------------- CLASE PALABRA -------------------------------------------

valores_letras = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1, "K": 5,
                 "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4,
                 "W": 4, "X": 8, "Y": 4, "Z": 10, "#": 0}

                 
class Palabra:
    def __init__(self, word, jugador, board):
        self.jugador=jugador
        self.word=word
        self.board=board


    def convert(self):
        '''
        Verifica si una palabra es válida y retorna el resultado de la verificación
        ''' 
        if not self.word.lower() in verbs:
            #print('La palabra NO está en verbs.')
            if (self.word.lower() in lexicon) and (self.word.lower() in spelling):
                #print('La palabra si existe.')
                #self.clasificar_palabra(pal):
                ok = True
            else:
                #print('La palabra ingresada no existe.')
                ok = False
        else:
            #print('La palabra si existe.')
            ok = True
            #self.clasificar_palabra(pal)
        return ok

            

    # def clasificar_palabra(pal):
        # aux=(tag(pal))
        # p=aux[0][1]
        # if p in (tipo['verb']):
            # print('La palabra ingresada es un verbo.')
        # elif p in (tipo['sus']):
            # print('La palabra ingresada es un sustantivo.')
        # elif p in (tipo['adj']): 
            # print('La palabra ingresada es un ajetivo.')
    


    def calcular_puntaje(self, dic):
        '''
        Calcula el puntaje de la palabra jugada una vez que es tomada como válida. 
        Retorna el puntaje como entero
        ''' 
        puntaje_parcial=0
        bomba=0
        estrella=0
        aux=self.board.coordenadas()
        
        for key, value in dic.items():
            if key in aux[0]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]*2
            elif key in aux[1]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]*3
            elif key in aux[2]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]-2
            elif key in aux[3]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]-3
            elif key in aux[4]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]
                bomba=bomba+1
            elif key in aux[5]:
                puntaje_parcial=puntaje_parcial+valores_letras[value]
                estrella=estrella+1
            else: 
                puntaje_parcial=puntaje_parcial+valores_letras[value]

        puntaje_total=(puntaje_parcial+(estrella*5)-(bomba*4))      
        return puntaje_total
        

    # def get_palabra(self):
        # return self.word

        
