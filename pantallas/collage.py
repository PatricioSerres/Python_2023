import PySimpleGUI as sg
import pantallas.armar_collage as armar
import funciones.paths as paths

def crear_ventana_collage(nombre):
    """ Esta función devuelve el layout de la ventana a usar """


    layout = [[sg.Button('Volver',key='back',button_color='green',pad=(5,0))],
        #Imagenes
        [sg.Image(source=paths.DIR_TEMPLATE_COLLAGE_1,subsample=2,enable_events=True,key=1),
         sg.Image(source=paths.DIR_TEMPLATE_COLLAGE_2,subsample=2,enable_events=True,key=2),
         sg.Image(source=paths.DIR_TEMPLATE_COLLAGE_3,subsample=2,enable_events=True,key=3),
         sg.Image(source=paths.DIR_TEMPLATE_COLLAGE_4,subsample=2,enable_events=True,key=4)],
         # Textos
        [sg.Text('Opcion 1',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 2',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 3',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 4',pad=(100,0),background_color='white',text_color='black',font=('calibri',20))]
       
    ]
    return sg.Window(nombre, layout, finalize=True, background_color='white')

def main(nombre,perfil,config):
    """ Esta función ejecuta la ventana de seleccion de template para el collage. Una vez seleccionado, lleva a la ventana de armado del
    collage. Recibe como parametros el perfil actual, el nombre de la ventana y la configuración"""

    # Se crea la ventana y se elije la configuración
    crear_ventana_collage(nombre)
    directorio_collage = paths.convertir_guardado_para_usar(config[0][1], paths.DIR_PROYECTO)

    # Lugares de comienzo y tamaño de cada una de las imagenes de cada template
    commons = [[(250,500), (250,500)], 
               [(200,500), (300,250), (300,250)], 
               [(500,250), (500,250)], 
               [(300,500), (300,500), (300,500)]]

    lugares = [[(0,0),(250,0)], 
               [(0,0), (200,0), (200,250)],
               [(0,0),(0,250)],
               [(0,0),(300,0),(600,0)]]

    nums = (1, 2, 3, 4)
    while True:
        # Leo la ventana creada
        current_window, event, values = sg.read_all_windows()   

        # Dependiendo de que template se elija se envia un numero a la función armar, el perfil y la config        
        if event in nums:
            current_window.hide()
            armar.iniciar_collage(perfil, directorio_collage, event, commons[event-1], lugares[event-1])
            current_window.close()
            break
        # Casos en que se cierre la ventana o se vuelva
        elif event == "-SECUNDARIA-VOLVER-" or event == 'back' or event == sg.WIN_CLOSED:
            current_window.close()
            break 
        

     