import PySimpleGUI as sg
import os
import pantallas.configuracion as configuracion
import pantallas.modificar as modificar
import pantallas.memes as memes
import pantallas.collage as collage
import pantallas.ayuda as ayuda
import pantallas.etiquetar as etiquetar
import csv

def crear_ventana_principal(perfil):
    """ Esta función crea el layout de la ventana del menu principal, recibiendo como parametro el perfil elegido
        al iniciar sesión o registrarse. Del mismo se mostrará la imagen seleccionada y su nick."""
    
    image_configuracion = '././imagenes/boton.png'  # CONSULTAR 
    image_perfil = perfil['foto']

    menu_def = [
             ['&Ayuda', 'Acerca de...'],
                ]
    
    left_col = [
        [sg.Menu(menu_def)],
        [sg.Button("Etiquetar imagenes", font=('Helvetica', 15), key="-PRINCIPAL-ETIQUETAR-", size=(15,0))],
        [sg.Button("Generar Meme",font=('Helvetica', 15), key="-PRINCIPAL-MEME-", size=(15,0))],
        [sg.Button("Generar Collage",font=('Helvetica', 15), key="-PRINCIPAL-COLLAGE-", size=(15,0))],
        [sg.Button("Salir",font=('Helvetica', 15), key="-PRINCIPAL-SALIR-", size=(15,0))],
    ]
    
    images_col = [sg.Button('', image_filename=image_configuracion, image_size=(50, 50), image_subsample=2, key="-PRINCIPAL-CONFIGURACION-")],

    perfil_col= [sg.Button('', image_filename=image_perfil, image_size=(50, 50), image_subsample=5, key="-PRINCIPAL-EDITAR-")], [sg.Text(perfil['nick'])], 
    

    return [[sg.Column(perfil_col, element_justification='l', vertical_alignment='c'),sg.Push(), sg.Column(images_col, element_justification='c', vertical_alignment="t")], [sg.Column(left_col, justification="center", element_justification='c', vertical_alignment="r", pad=((0,250)))]]

   

def main(perfil):
    """ En esta función se ejecuta el menu principal de la aplicación, que durante un loop infinito va leyendo los
        eventos provocados al interactuar con el mismo."""
    
    menu = sg.Window("Menu principal", crear_ventana_principal(perfil), finalize=True, resizable=True, metadata={"configuracion_csv": None})
    menu.set_min_size((1024,768))
    # se le asigna a la variable menu el layout, y se le establece el tamaño mínimo.

    # se abre el archivo de configuración en modo lectura, sino existe, se crea vacío y se vuelve a leer.
    try:
        with open(os.path.join('archivos','archivo_configuracion.csv'), 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            contenido_csv = list(lector_csv)
    except FileNotFoundError:
        with open(os.path.join('archivos','archivo_configuracion.csv'), 'w') as archivo_csv:
            linea_vacia = ["","",""]
            writer = csv.writer(archivo_csv)
            writer.writerow(linea_vacia)
        with open(os.path.join('archivos','archivo_configuracion.csv'), 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            contenido_csv = list(lector_csv)
    except Exception as e:
        print(type(e))
        print(f'La excepción {e} no se pudo resolver')
        sg.Popup('Ocurrió un error inesperado.')


    

    menu.metadata["configuracion_csv"] = contenido_csv
    # se le asigna a la metadata del menu la configuración contenida en el archivo csv. 

    # Loop infinito de eventos.

    while True:
        current_window, event, values = sg.read_all_windows()
        
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-PRINCIPAL-SALIR-":
            current_window.close()
            break
        elif event == "Acerca de...":
            ayuda.main()
        elif event == "-PRINCIPAL-ETIQUETAR-":
            current_window.hide()
            etiquetar.main(perfil, config=menu.metadata["configuracion_csv"])
            # se envía el perfil actual junto con la configuración actual seleccionada por el usuario.
            current_window.un_hide()
        elif event == "-PRINCIPAL-MEME-":
            current_window.hide()
            memes.main("Generar Meme")
            current_window.un_hide()
        elif event == "-PRINCIPAL-COLLAGE-":
            current_window.hide()
            collage.main("Generar Collage")
            current_window.un_hide()
        elif event == "-PRINCIPAL-CONFIGURACION-":   
            current_window.hide() 
            conf = configuracion.main(perfil, config=menu.metadata["configuracion_csv"])
            if conf is not None:
                menu.metadata["configuracion_csv"] = conf
            current_window.un_hide()  
            # Se pasa como parametro la configuración actual, y si se produce algún cambio se modifica la metadata
            # de la ventana menu.
        elif event == "-PRINCIPAL-EDITAR-":
            current_window.hide()
            perfil = modificar.main(perfil)
            current_window['-PRINCIPAL-EDITAR-'].update(image_filename = perfil['foto'], image_size=(50, 50), image_subsample=5)                          
            # si se produce algún cambio se cambia el perfil actual.
            current_window.un_hide()