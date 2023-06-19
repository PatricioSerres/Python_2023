import PySimpleGUI as sg
import pantallas.armar_collage as armar
import funciones.paths as paths

def crear_ventana_collage(nombre):
    op1 = '././imagenes/opciones/opcion1.png'
    op2 = '././imagenes/opciones/opcion2.png'
    op3 = '././imagenes/opciones/opcion3.png'
    op4 = '././imagenes/opciones/opcion4.png'

    layout = [[sg.Button('Volver',key='back',button_color='green',pad=(5,0))],
        #Imagenes
        [sg.Image(source=op1,subsample=2,enable_events=True,key='op1'),
         sg.Image(source=op2,subsample=2,enable_events=True,key='op2'),
         sg.Image(source=op3,subsample=2,enable_events=True,key='op3'),
         sg.Image(source=op4,subsample=2,enable_events=True,key='op4')],
         # Textos
        [sg.Text('Opcion 1',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 2',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 3',pad=(100,0),background_color='white',text_color='black',font=('calibri',20)),
         sg.Text('Opcion 4',pad=(180,0),background_color='white',text_color='black',font=('calibri',20))]
       
    ]
    return sg.Window(nombre, layout, finalize=True, margins=(100,100),background_color='white')

def main(nombre,perfil,config):
    crear_ventana_collage(nombre)
    config_a_usar = paths.convertir_guardado_para_usar(config[0][1], paths.DIR_PROYECTO)

    while True:
        current_window, event, values = sg.read_all_windows()           
        if event == 'op1':
            current_window.close()
            armar.completo(1,perfil, config_a_usar)
            break
        if event == 'op2':
            current_window.close()
            armar.completo(2,perfil, config_a_usar)
            break
        if event == 'op3':
            current_window.close()
            armar.completo(3,perfil, config_a_usar)
            break
        if event == 'op4':
            current_window.close()
            armar.completo(4,perfil, config_a_usar)
            break
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-SECUNDARIA-VOLVER-" or event == 'back':
            current_window.close()
            break 

#