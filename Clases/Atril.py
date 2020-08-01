import PySimpleGUI as sg

#----------------------- CLASE ATRIL -----------------------

class Atril:
    '''
            La clase Atril que representa un atril de fichasc
    
    Atributos
        bag : class
            Representa mi bolsa de fichas
      
    Métodos
        agregar_fichas:
            agrega fichas al atril
        cant_fichas_atril:
            retorna cantidad de fichas del atril
        atril_array:
            retorna el atril
        eliminar_ficha:
            elimina fichas del atril
        una_ficha:
            toma ficha de la bolsa para ponerla en el atril   
        reponer_fichas:
            repone fichas faltantes del atril
    
    '''
    
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
        Toma una ficha de la bolsa y se la agrega al atril del jugador
        ''' 
        self.atril.append(self.bag.dar_ficha())
    
    def reponer_fichas(self, cant):
        '''
        Repone las fichas faltantes en el atril del jugador, mientras haya en la bolsa
        ''' 
        aux=0
        while aux < cant and self.bag.cant_fichas_bolsa() > 0:
            self.una_ficha()
            aux+=1
            
        if self.bag.cant_fichas_bolsa() == 0:
            return False
        else:
            return True
            
        
        
