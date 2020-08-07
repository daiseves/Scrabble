import random
import PySimpleGUI as sg



def set_config(values):
    
    '''
    Función que retorna un diccionario con la configuración ingresada por el usuario
    '''

    config=values
    dificultad=(list(config.keys())[list(config.values()).index(True)])
    config['__dificultad__']=dificultad
    del config['Facil']
    del config['Medio']
    del config['Dificil']
    
    return config
    
def configuracion(default):
    
        '''
        Crea la ventana para que el usuario modifique la configuración del juego. Devuelve configuración por defecto si no se configura. 
        '''
        
        if default:
            config={3: 9, 4: 2, 5: 4, 6: 12, 7: 3, 8: 1, 9: 6, 10: 8, 11: 1, 12: 2, 13: 3, 14: 4, 15: 5, 16: 8, 17: 10, 18: 12, '__tiempoTurno__': 30.0, '__tiempoPartida__': 60.0, '__dificultad__': 'Facil'}
            return config, True
        else:
            des={'text_color':('saddlebrown'), 'size':(25,1), 'pad':((20,0),(0,10))}
            
            des2= {'background_color':('#A52A2A'),'range' : (10, 120), 'orientation' : ('h'), 'size' : (22,20), 'default_value' : (60)}
            
            des3 = {'background_color':('#A52A2A'),'range' : (10, 60), 'orientation' : ('h'), 'size' : (22,20), 'default_value' : (30)}
            
            nivel=[[sg.Radio('FÁCIL',1 ,key='Facil', **des ,default=True), sg.Radio('MEDIO',1,key='Medio', **des), sg.Radio('DIFÍCIL',1,key='Dificil',**des)]]

            cantidad=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


            cantidad_fichas=[
                     [sg.Text('A, I: ', **des),sg.InputCombo(cantidad,size=(5,1), default_value=9)],
                     [sg.Text('B, C, F, H, M, P, T, U, V, W, Y : ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=2)],
                     [sg.Text('D, L, S: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=4)],
                     [sg.Text('E: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=12)],
                     [sg.Text('G: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=3)],
                     [sg.Text('J, K, Q, W, X, Z: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=1)],
                     [sg.Text('M, R: ', **des),sg.InputCombo(cantidad,size=(5,1), default_value=6)],
                     [sg.Text('O: ', **des),sg.InputCombo(cantidad,size=(5,1), default_value=8)]]
                  
            puntaje_fichas=[
                     [sg.Text('A, E: ', **des),sg.InputCombo(cantidad,size=(5,1), default_value=1)],
                     [sg.Text('O: ', **des),sg.InputCombo(cantidad,size=(5,1), default_value=2)],
                     [sg.Text('I, S: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=3)],
                     [sg.Text('N, R, U, D: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=4)],
                     [sg.Text('L, T, C: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=5)],
                     [sg.Text('G, B, M, P, H, K, W: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=8)],
                     [sg.Text('F, V, Y, J: ',**des),sg.InputCombo(cantidad,size=(5,1), default_value=10)],
                     [sg.Text('Q, X, Z: ',**des), sg.InputCombo(cantidad,size=(5,1), default_value=12)]]
                     
                     
            layout = [
                     [sg.Image(filename='Imagenes/3.png', pad=(0,20))],
                     [sg.Column(nivel)],
                     [sg.Image(filename='Imagenes/4.png',pad=((10,50),(20,20))), sg.Image(filename='Imagenes/5.png')],
                     [sg.Column(cantidad_fichas), sg.Column(puntaje_fichas)],
                     [sg.Image(filename='Imagenes/7.png',pad=((10,50),(20,20))), sg.Image(filename='Imagenes/8.png')],
                     [sg.Slider(**des3, key = '__tiempoTurno__', pad=((5,40),(5,0))), sg.Slider(**des2, key = '__tiempoPartida__',pad=((15,0),(5,0)))], 
                     [sg.Button('Guardar cambios', font='centaur 15', pad=((0,40)), size=(20,1))]
                     ]        
                     
            window = sg.Window('Configuración', layout, size=(630,700), element_justification='center')
            

            while True:
                event, values = window.Read()
                if event == 'Guardar cambios':
                    sg.popup('Los cambios han sido guardados correctamente.', background_color='#E5CEAC', text_color='#8B4513', button_color= ('white','#8B4513'))
                    config=set_config(values)
                    window.Close()
                    return config, False
                if event is None:
                    return None, True

