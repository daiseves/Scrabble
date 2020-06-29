from random import shuffle

#----------------------- CLASE BOLSA -----------------------
class Bag:
    def __init__(self):
        self.bag=[]
        self.letras = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.repeticiones = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,2,2,2,2,1,2,1]
        self.anexo()
        #valores = [1,3,3,2,1,4,2,4,1,1,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10,0]
        
    def anexo(self):
        '''
        Genera una bolsa llena de fichas
        ''' 
        global valores_letras
        for letra, cantrep in zip(self.letras, self.repeticiones):
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
