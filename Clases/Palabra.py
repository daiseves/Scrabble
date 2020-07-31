import pattern.es
from pattern.es import tag, spelling, lexicon, verbs


#----------------------- CLASE PALABRA -------------------------------------------
                 
class Palabra:
    def __init__(self, word, jugador, board, bag):
        self.jugador=jugador
        self.word=word
        self.board=board
        self.valores_letras=bag.valores_letras()


    def convert(self):
        '''
        Verifica si una palabra es válida y retorna el resultado de la verificación
        ''' 
        if not self.word.lower() in pattern.es.verbs:
            #print('La palabra NO está en verbs.')
            if (self.word.lower() in pattern.es.lexicon) and (self.word.lower() in pattern.es.spelling):
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
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]*2
            elif key in aux[1]:
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]*3
            elif key in aux[2]:
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]-2
            elif key in aux[3]:
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]-3
            elif key in aux[4]:
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]
                bomba=bomba+1
            elif key in aux[5]:
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]
                estrella=estrella+1
            else: 
                puntaje_parcial=puntaje_parcial+self.valores_letras[value]

        puntaje_total=(puntaje_parcial+(estrella*5)-(bomba*4))      
        return puntaje_total
        

    def get_palabra(self):
        return self.word
