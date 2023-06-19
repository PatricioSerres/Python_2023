import PySimpleGUI as sg
import os
import pantallas.configuracion as configuracion
import pantallas.registro as registro
import pantallas.memes as memes
import pantallas.collage as collage
import pantallas.ayuda as ayuda
import pantallas.etiquetar as etiquetar
import funciones.paths as paths
import funciones.funciones as funciones

# PEP 8 VER. Idem ayuda, configuración, etiquetar, unlpimage, memes, registro, inicio, modificar y collage.
# SALIR O CERRAR SESIÓN? VER
# Popup en configuración?

# ------- Definicion del layout --------

def crear_ventana_principal(perfil):
    """ Esta función crea el layout de la ventana del menu principal, recibiendo como parametro el perfil elegido
        al iniciar sesión o registrarse. Del mismo se mostrará la imagen seleccionada y su nick."""
    
    image_configuracion = os.path.join(paths.DIR_IMAGENES, "boton_configuracion.png")
    image_perfil = perfil['foto']

    menu_def = [
             ['&Ayuda', 'Acerca de...'],
                ]
    
    left_col = [
        [sg.Menu(menu_def)],
        [sg.Button("Etiquetar imagenes", font=('Helvetica', 15), key="-PRINCIPAL-ETIQUETAR-", size=(15,0))],
        [sg.Button("Generar Meme",font=('Helvetica', 15), key="-PRINCIPAL-MEME-", size=(15,0))],
        [sg.Button("Generar Collage",font=('Helvetica', 15), key="-PRINCIPAL-COLLAGE-", size=(15,0))],
        [sg.Button("Cerrar Sesión", font=('Helvetica', 15), key="-PRINCIPAL-SESION-", size=(15,0))],
        [sg.Button("Salir",font=('Helvetica', 15), key="-PRINCIPAL-SALIR-", size=(15,0))],
    ]
    
    images_col = [sg.Button('', image_filename=image_configuracion, image_size=(50, 50), image_subsample=2, key="-PRINCIPAL-CONFIGURACION-")],

    perfil_col= [sg.Button('', image_filename=image_perfil, image_size=(50, 50), image_subsample=5, key="-PRINCIPAL-EDITAR-")], [sg.Text(perfil['nick'])], 
    
    layout = [[sg.Column(perfil_col, element_justification='l', vertical_alignment='c'),sg.Push(), 
               sg.Column(images_col, element_justification='c', vertical_alignment="t")], 
            [sg.Column(left_col, justification="center", element_justification='c', vertical_alignment="r", pad=((0,100)))]]

    return sg.Window("Menu principal", layout, finalize=True, relative_location=(-250, -100), metadata={"configuracion_csv": None})





# ------- Main -------- 

def main(perfil):
    """ En esta función se ejecuta el menu principal de la aplicación, que durante un loop infinito va leyendo los
        eventos provocados al interactuar con el mismo."""
    
    menu = crear_ventana_principal(perfil)
    menu.set_min_size((800,600))
    # PONER COMO UNA CONSTANTE ------------------------------------------------------------------------------------------------
    # se le asigna a la variable menu el layout, y se le establece el tamaño mínimo.

    # se abre el archivo de configuración en modo lectura, sino existe, se crea vacío y se vuelve a leer.
    try:
        contenido_csv = funciones.leer_archivo_csv(paths.DIR_CONFIGURACION)
    except FileNotFoundError:
        linea_vacia = ["","",""]
        funciones.crear_archivo_csv(paths.DIR_CONFIGURACION, linea_vacia)
        contenido_csv = funciones.leer_archivo_csv(paths.DIR_CONFIGURACION)
    except Exception as e:
        print(type(e))
        print(f'La excepción {e} no se pudo resolver')
        sg.Popup('Ocurrió un error inesperado.')


    menu.metadata["configuracion_csv"] = contenido_csv
    # se le asigna a la metadata del menu la configuración contenida en el archivo csv. 

    # Loop infinito de eventos.

    while True:
        current_window, event, values = sg.read_all_windows()
        
        if (event == "-PRINCIPAL-SALIR-") or event == sg.WIN_CLOSED:
            current_window.close()
            return False
        elif event == "Acerca de...":
            ayuda.main()
        elif event == "-PRINCIPAL-ETIQUETAR-":
            current_window.hide()
            etiquetar.main(perfil, config=menu.metadata["configuracion_csv"])
            # se envía el perfil actual junto con la configuración actual seleccionada por el usuario.
            current_window.un_hide()
        elif event == "-PRINCIPAL-MEME-":
            current_window.hide()
            memes.main(perfil, config=menu.metadata["configuracion_csv"])
            current_window.un_hide()
        elif event == "-PRINCIPAL-COLLAGE-":
            current_window.hide()
            collage.main("generar collage",perfil['nick'], config= menu.metadata["configuracion_csv"])
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
            perfil = registro.modificar(perfil)
            perfil['foto'] = paths.convertir_guardado_para_usar(perfil['foto'], paths.DIR_PROYECTO)
            current_window['-PRINCIPAL-EDITAR-'].update(image_filename = perfil['foto'], image_size=(50, 50), image_subsample=5)                          
            # si se produce algún cambio se cambia el perfil actual.
            current_window.un_hide()
        elif event == "-PRINCIPAL-SESION-":
            current_window.close()
            return True