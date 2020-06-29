import PySimpleGUI as sg
#----------------------- CLASE ATRIL -----------------------

class Atril:
    def __init__(self, Bag):
        self.bag=Bag
        self.atril=[]
        self.agregar_fichas()
        
    def agregar_fichas(self):
        '''
        Inicializa el atril de cada jugador con 7 fichas y lo retorna
        ''' 
        for i in range(7):
            self.atril.append(self.bag.dar_ficha())
        return(self.atril)
    
    def cant_fichas_atril(self):
        '''
        Retorna la cantidad de fichas en el atril
        ''' 
        return len(self.atril)

    def atril_array(self):
        '''
        Devuelve el atril como una lista
        '''
        return self.atril
    
    def eliminar_ficha(self, letra):
        '''
        Elimina una ficha del atril
        ''' 
        self.atril.remove(letra)
        
    def una_ficha(self):
        '''
        Toma una dicha de la bolsa y se la agrega al atril del jugador
        ''' 
        self.atril.append(self.bag.dar_ficha())
    
    def reponer_fichas(self, cant):
        '''
        Repone las fichas faltantes en el atril del jugador, mientras haya en la bolsa
        ''' 
        for i in range(cant):
            if self.bag.cant_fichas_bolsa() > 0:
                self.una_ficha()
        
        
