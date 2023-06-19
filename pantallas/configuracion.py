import PySimpleGUI as sg
import os
import csv
from datetime import datetime

def crear_ventana_configuracion(config):
    """Esta función define el layout de la pantalla de configuración. Recibe como parametro la configuración guardada anteriormente. """

    layout = [
        [sg.Text("Repositorio de imagenes"), sg.In(config[0][0], disabled=True, enable_events=True, key="-CONFIGURACION-REPOSITORIO-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de collages"), sg.In(config[0][1], disabled=True, enable_events=True, key="-CONFIGURACION-COLLAGES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de memes"), sg.In(config[0][2], disabled=True, enable_events=True, key="-CONFIGURACION-MEMES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
        [sg.Button("Guardar", key="-CONFIGURACION-GUARDAR-")],
    ]
    return sg.Window("Configuración", layout, finalize=True, margins=(100,100))

def main(perfil, config = None):
    """Esta función ejecuta la ventana de configuración. Además entra en un loop infinito donde se van registrando los eventos producidos por el usuario.
    Recibe como parametro la configuración guardada anteriormente, aunque este parámetro inicia en None"""
    crear_ventana_configuracion(config)

    # Se guarda en una variable el contenido del archivo de configuración.
    config_aux = config[0].copy()  
    while True:
        current_window, event, values = sg.read_all_windows()
        match event:
            # Cada vez que se modifica uno de los directorios, se cambia el valor de una variable auxiliar. En caso de que el usuario guarde los cambios,
            # estos se reflejarán en el archivo de configuración. 

            case "-CONFIGURACION-REPOSITORIO-":
                config_aux[0] = values["-CONFIGURACION-REPOSITORIO-"]
            case "-CONFIGURACION-COLLAGES-":
                config_aux[1] = values["-CONFIGURACION-COLLAGES-"]
            case "-CONFIGURACION-MEMES-":
                config_aux[2] = values["-CONFIGURACION-MEMES-"]
            case "-CONFIGURACION-GUARDAR-":
                config[0] = config_aux.copy()
                timestamp = datetime.timestamp(datetime.now())
                fecha_hora = datetime.fromtimestamp(timestamp)
                with open(os.path.join('archivos','archivo_configuracion.csv'), 'w') as archivo_csv:
                    writer = csv.writer(archivo_csv)
                    writer.writerow([config[0][0], config[0][1], config[0][2]])
                with open(os.path.join('archivos','logs.csv'), 'a') as log:
                    writer = csv.writer(log)
                    fecha_mod=fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
                    perfil_mod= perfil['nick']
                    operacion_mod= 'Cambio en configuracion'
                    writer.writerow([fecha_mod, perfil_mod,operacion_mod])
            case sg.WIN_CLOSED:
                current_window.close()
                return config
            case "-SECUNDARIA-VOLVER-":
                current_window.close()
                return config




