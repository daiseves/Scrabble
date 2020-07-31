from random import shuffle

#----------------------- CLASE BOLSA -----------------------
class Bag:
    def __init__(self, cant, valores):
        self.bag=[]
        self.letras=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.cant=list(cant.values())
        self.values=list(valores.values())
        self.anexo()

        
    def set_cantidad(self):
        '''
        Setea la cantidad de fichas que tendrá cada letra. Retorna una lista con las cantidades
        ''' 
        letras=[self.cant[0], self.cant[1], self.cant[1], self.cant[2], self.cant[3], self.cant[1], self.cant[4], 
                self.cant[1], self.cant[0], self.cant[5], self.cant[5], self.cant[2], self.cant[1], self.cant[6], 
                self.cant[7], self.cant[1], self.cant[5], self.cant[6], self.cant[2], self.cant[1], self.cant[1], 
                self.cant[1], self.cant[1], self.cant[5], self.cant[1], self.cant[5]]
        return letras
    
    
    def diccionario_cantidad(self):
        '''
        Retorna un diccionario con la cantidad de fichas de cada letra.(key: letra, valor: cantidad). Para mostrar en 'consideraciones de la partida'
        ''' 
        aux=self.valores_letras()
        letras=self.set_cantidad()
        indice=0
        for elem in aux:
            aux[elem]=letras[indice]
            indice+=1
        return aux

    def set_valores(self):
        '''
        Setea el valor de cada letra. Retorna un diccionario. (key: letra, valor: puntaje)
        ''' 
        valores_letras={'A': self.values[0], 'B': self.values[5], 'C': self.values[4], 'D': self.values[3], 'E': self.values[0],
                        'F': self.values[6], 'G': self.values[5], 'H': self.values[5], 'I': self.values[2], 'J': self.values[6], 
                        'K': self.values[5], 'L': self.values[4], 'M': self.values[5], 'N': self.values[3], 'O': self.values[1], 
                        'P': self.values[5], 'Q': self.values[7], 'R': self.values[3], 'S': self.values[2], 'T': self.values[4], 
                        'U': self.values[3], 'V': self.values[6], 'W': self.values[5], 'X': self.values[7], 'Y': self.values[6], 
                        'Z': self.values[7]}
        return valores_letras
        
        
    def valores_letras(self):
        '''
        Retorna un diccionario de valores. (key: letra, valor: puntaje)
        ''' 
        return self.set_valores()
        
    def anexo(self):
        '''
        Genera una bolsa llena de fichas
        ''' 
        rep=self.set_cantidad()
        for letra, cantrep in zip(self.letras, rep):
            for i in range (cantrep):
                self.bag.append(letra)


        #Desordena las letras de la bolsa
        shuffle(self.bag)
        return self.bag
     
    def dar_ficha(self):   
        '''
        Elimina una ficha de la bolsa y la retorna
        ''' 
        return self.bag.pop()

    def cant_fichas_bolsa(self):
        '''
        Retorna la cantidad de fichas que quedan en la bolsa
        ''' 
        aux=len(self.bag)
        return aux
        
    def devolver_a_bolsa(self,lista):
        '''
        Devuelve a la bolsa las fichas que el usuario quiso cambiar
        ''' 
        for elem in lista:
            self.bag.append(elem)
            
            

