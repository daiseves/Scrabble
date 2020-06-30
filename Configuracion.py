import PySimpleGUI as sg

'''Crea la ventana para que el usuario modifique la configuración del juego. SOLO TIENE FUNCIONALIDAD EL NIVEL (CAMBIA EL TAMAÑO DEL TABLERO)'''

def configuracion():
        sg.theme_background_color('#E5CEAC')
        tiempoRonda=['30sg', '40sg', '50sg', '60sg']
        nivelJuego=['Fácil', 'Medio', 'Difícil']
        puntajeFicha=[]
        cantidadFichas=[]

        layout=[
                [sg.Image(filename='Imagenes/ScrabbleWord.png', size=(1000,300),background_color='#E5CEAC')],
                [sg.Text('Tiempo por ronda: ', font ='centaur 15', background_color='saddlebrown',pad=(60,5)), sg.Combo(values=tiempoRonda, size=(20, 100), key='__tiempoRonda__', pad=(90,30))] , 
                [sg.Text('Nivel del juego: ',font ='centaur 15', background_color='saddlebrown',pad=(60,5)) , sg.Combo(values=nivelJuego, size=(20, 30), key='__nivelJuego__', pad=(120,30))],
                [sg.Text('Puntaje de cada ficha: ', font ='centaur 15', background_color='saddlebrown',pad=(60,5)), sg.Combo(values=puntajeFicha, size=(20, 30), key='__puntajeFicha__', pad=(60,30))],
                [sg.Text('Cantidad de fichas por letra: ', font ='centaur 15', background_color='saddlebrown',pad=(60,5)), sg.Combo(values=cantidadFichas, size=(20, 30), key='__cantidadFichas__', pad=(8,30))],
                [sg.Button('Guardar cambios',button_color=('white','#D2B3BB'), font='centaur 15', pad=(150,5)), sg.Button('Volver',button_color=('white','#D2B3BB'), font='centaur 15', pad=(90,5))],
                [sg.Image(filename='Imagenes/ScrabbleWord.png',background_color='#E5CEAC')]
               ]
    
    
        window = sg.Window('Configuración', layout, size=(850,600), location=(200,60))
        
        event, values = window.Read()
        if event is 'Guardar cambios':
            nivel = values['__nivelJuego__']
            sg.popup('¡Cambios guardados! ', background_color='#FFE0A3', text_color='saddlebrown')
            window.Close()
        if event is 'Volver':
            window.Close()

        #Cambiar
        return nivel
