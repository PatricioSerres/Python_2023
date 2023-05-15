import PySimpleGUI as sg
import os
import csv

def crear_ventana_configuracion(config):

    layout = [
        [sg.Text("Repositorio de imagenes"), sg.In(config[0][0], disabled=True, enable_events=True, key="-CONFIGURACION-REPOSITORIO-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de collages"), sg.In(config[0][1], disabled=True, enable_events=True, key="-CONFIGURACION-COLLAGES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de memes"), sg.In(config[0][2], disabled=True, enable_events=True, key="-CONFIGURACION-MEMES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
        [sg.Button("Guardar", key="-CONFIGURACION-GUARDAR-")],
    ]
    return sg.Window("Configuración", layout, finalize=True, margins=(100,100))

def main(config = None):
    crear_ventana_configuracion(config)
    config_aux = config[0].copy()
    

    while True:
        current_window, event, values = sg.read_all_windows()
           

        

        match event:
            case "-CONFIGURACION-REPOSITORIO-":
                config_aux[0] = values["-CONFIGURACION-REPOSITORIO-"]
            case "-CONFIGURACION-COLLAGES-":
                config_aux[1] = values["-CONFIGURACION-COLLAGES-"]
            case "-CONFIGURACION-MEMES-":
                config_aux[2] = values["-CONFIGURACION-MEMES-"]
            case "-CONFIGURACION-GUARDAR-":
                config[0] = config_aux.copy()
                with open(os.path.join('archivos','archivo_configuracion.csv'), 'w') as archivo_csv:
                    writer = csv.writer(archivo_csv)
                    writer.writerow([config[0][0], config[0][1], config[0][2]])
            case sg.WIN_CLOSED:
                current_window.close()
                return None
            case "-SECUNDARIA-VOLVER-":
                current_window.close()
                return config




