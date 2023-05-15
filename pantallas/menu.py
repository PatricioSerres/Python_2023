import PySimpleGUI as sg
import os
import pantallas.configuracion as configuracion
import pantallas.modificar as modificar
import pantallas.memes as memes
import pantallas.collage as collage
import pantallas.ayuda as ayuda
import pantallas.etiquetar as etiquetar
import csv

def crear_ventana_principal():

    image_configuracion = '././imagenes/boton.png'
    image_perfil = '././imagenes/perfil.png'

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
    
    images_col = [sg.Button('', image_filename=image_configuracion, image_size=(44, 44), image_subsample=2, key="-PRINCIPAL-CONFIGURACION-")],

    perfil_col= [sg.Button('', image_filename=image_perfil, image_size=(44, 44), key="-PRINCIPAL-EDITAR-")],
    

    return [[sg.Column(perfil_col, element_justification='l', vertical_alignment='t'),sg.Push(), sg.Column(images_col, element_justification='c', vertical_alignment="c")], [sg.Column(left_col, justification="center", element_justification='c', vertical_alignment="r", pad=((0,250)))]]

   

def main(perfil):
    menu = sg.Window("Menu principal", crear_ventana_principal(), finalize=True, resizable=True, metadata={"configuracion_csv": None})
    menu.set_min_size((1024,768))

    # abro archivo
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


    # Loop infinito de eventos.

    while True:
        current_window, event, values = sg.read_all_windows()
        # PARA TESTEAR print(f"Ventana actual: {current_window}, Evento: {event}, valores: {values}")    
        
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
            etiquetar.main(config=menu.metadata["configuracion_csv"])
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
            conf = configuracion.main(config=menu.metadata["configuracion_csv"]) 
            if conf is not None:
                menu.metadata["configuracion_csv"] = conf
            current_window.un_hide()  
            # CONSULTAR COMO CERRAR LA VENTANA CONFIGURACIÓN Y NO LA VENTANA MENU
        elif event == "-PRINCIPAL-EDITAR-":
            current_window.hide()
            perfil = modificar.main(perfil)
            current_window.un_hide()