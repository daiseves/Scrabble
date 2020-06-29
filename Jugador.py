from Atril import Atril

#----------------------- CLASE JUGADOR -----------------------
class Jugador:
    def __init__(self, bag, name):
        '''
        Recibe como parámetros mi bolsa de fichas para crear el atril de cada jugador y el nombre del jugador actual para crear sus manos en cada ronda
        '''
        self.atril = Atril(bag)
        self.name=name
        self.dicUser={}
        self.dicPC={}
        self.puntaje=0

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
        self.puntaje=self.puntaje+aumento
        
    def get_puntaje(self):
        '''
        Retorna un entero que representa el puntaje del jugador
        ''' 
        return self.puntaje
        
    def actualizar_atril(self, aux, cant_rondas, nivel):
        '''
        Recibe como parámetros el nivel, la cantidad de rondas jugadas, y un aux(diccionario con los valores que se jugaron)
        Si la palabra fue válida, elimina las fichas jugadas del atril del jugador y le repone nuevas fichas
        ''' 
        cant=0
        if cant_rondas==1:
            if nivel == 'Fácil':
                del aux[(7,7)]
            elif nivel == 'Medio':
                del aux[(8,8)]
            elif nivel == 'Difícil':
                del aux[(9,9)]
        valores=aux.values()
        for valor in valores:
            if valor in self.atril_array():
                self.atril.eliminar_ficha(valor)
                cant=cant+1
        self.atril.reponer_fichas(cant)
        return self.atril
        
    def get_dicc(self):
        '''
        Retorna un diccionario que representa la jugada de cada turno
        ''' 
        if self.name=='PC':
            return self.dicPC
        else:
            return self.dicUser

    def vaciar_dicc(self):
        '''
        Vacía el diccionario de cada jugador una vez que finaliza el turno 
        ''' 
        if self.name=='PC':
            self.dicPC.clear()
            return self.dicPC
        else:
            self.dicUser.clear()
            return self.dicUser


