from Clases.Atril import Atril

#----------------------- CLASE JUGADOR -----------------------
class Jugador:
    def __init__(self, bag, name):
        '''
        Recibe como parámetros mi bolsa de fichas para crear el atril de cada jugador y el nombre del jugador actual para crear sus manos en cada ronda
        '''
        self.bag=bag
        self.atril = Atril(self.bag)
        self.name=name
        self.dicJugador={}
        #self.dicPC={}
        self.puntaje=0
        self.puntaje_final=0

    def set_name(self, name):
        '''
        Setea el nombre del jugador
        '''
        self.name = name

    def get_name(self):
        '''
        Retorna el nombre del jugador
        '''
        return self.name

    def atril_array(self):
        '''
        Retorna una lista que representa el atril del jugador
        ''' 
        return self.atril.atril_array()

    def aumentar_puntaje(self, aumento):
        '''
        Recibe un entero como argumento y se lo suma al puntaje del jugador
        ''' 
        self.puntaje = self.puntaje+aumento
        
    def get_puntaje(self):
        '''
        Retorna un entero que representa el puntaje del jugador
        ''' 
        return self.puntaje
        
        
    def set_puntajeFinal(self, total):
        
        self.puntaje_final = total

        
    def get_puntajeFinal(self):
        
        return self.puntaje_final
        
        
       
    def actualizar_atril(self, aux, cant_rondas, nivel):
        '''
        Recibe como parámetros el nivel, la cantidad de rondas jugadas, y un aux(diccionario con los valores que se jugaron)
        Si la palabra fue válida, elimina las fichas jugadas del atril del jugador y le repone nuevas fichas
        ''' 
        cant=0
        try:
            if nivel == 'Facil':
                del aux[(7,7)]
            elif nivel == 'Medio':
                del aux[(8,8)]
            elif nivel == 'Difícil':
                del aux[(9,9)]
        except:
            pass
        valores=aux.values()
        for valor in valores:
            if valor in self.atril_array():
                self.atril.eliminar_ficha(valor)
                cant=cant+1
        exito=self.atril.reponer_fichas(cant)
        if exito:
            return self.atril
        else:
            return None 
        
    def get_dicc(self):
        '''
        Retorna un diccionario que representa la jugada de cada turno
        ''' 
        return self.dicJugador

    def vaciar_dicc(self):
        '''
        Vacía el diccionario de cada jugador una vez que finaliza el turno 
        ''' 
        self.dicJugador.clear()
        return self.dicJugador


    def cambiar_fichas(self, lista):
        '''
        Cambia las fichas del atril del jugador
        ''' 
        if self.bag.cant_fichas_bolsa()>=len(lista):
            for elem in lista:
                self.atril_array().pop(self.atril_array().index(elem))
            self.atril.reponer_fichas(len(lista))
            self.bag.devolver_a_bolsa(lista)
            return True
        else:
            return False        
   
