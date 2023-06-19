import PySimpleGUI as sg
from datetime import datetime
import funciones.paths as paths
import funciones.funciones as funciones


# ------------------------------------------ FUNCIONES ------------------------------------------

def crear_ventana_configuracion(config_a_mostrar):
    """Esta función define el layout de la pantalla de configuración. Recibe como parametro la configuración guardada anteriormente. """

    layout = [
        [sg.Text("Repositorio de imagenes"), sg.In(config_a_mostrar[0], disabled=True, enable_events=True, key="-CONFIGURACION-REPOSITORIO-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de collages"), sg.In(config_a_mostrar[1], disabled=True, enable_events=True, key="-CONFIGURACION-COLLAGES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Text("Directorio de memes"), sg.In(config_a_mostrar[2], disabled=True, enable_events=True, key="-CONFIGURACION-MEMES-"), sg.FolderBrowse("Seleccionar")],
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
        [sg.Button("Guardar", key="-CONFIGURACION-GUARDAR-")],
    ]
    return sg.Window("Configuración", layout, finalize=True, margins=(100,100))


def configuracion_en_pantalla(config_a_mostrar):
    for i, con in enumerate(config_a_mostrar):
        if (con != ''):
            config_a_mostrar[i] = paths.convertir_guardado_para_usar(con, paths.DIR_PROYECTO)
    return config_a_mostrar



# ------------------------------------------ MAIN ------------------------------------------

def main(perfil, config = None):
    """Esta función ejecuta la ventana de configuración. Además entra en un loop infinito donde se van registrando los eventos producidos por el usuario.
    Recibe como parametro la configuración guardada anteriormente, aunque este parámetro inicia en None"""
    config_a_mostrar = config[0].copy()
    config_a_mostrar = configuracion_en_pantalla(config_a_mostrar)
    crear_ventana_configuracion(config_a_mostrar)

    # Se guarda en una variable el contenido del archivo de configuración.
    config_aux = config[0].copy()  
    while True:
        current_window, event, values = sg.read_all_windows()
        match event:
            # En caso de que el usuario guarde los cambios, se guardan en una variable auxiliar todos los paths que pueden ser guardados, y luego se escriben
            # en el archivo de configuración. 

            case "-CONFIGURACION-GUARDAR-":                
                dir_aux = values["-CONFIGURACION-REPOSITORIO-"]
                if dir_aux != "":
                    dir_aux = paths.convertir_para_guardar(dir_aux, paths.DIR_PROYECTO)
                    config_aux[0] = dir_aux
                dir_aux = values["-CONFIGURACION-COLLAGES-"]
                if dir_aux != "":
                    dir_aux = paths.convertir_para_guardar(dir_aux, paths.DIR_PROYECTO)
                    config_aux[1] = dir_aux
                dir_aux = values["-CONFIGURACION-MEMES-"]
                if dir_aux != "":
                    dir_aux = paths.convertir_para_guardar(dir_aux, paths.DIR_PROYECTO)
                    config_aux[2] = dir_aux
                if (config[0] != config_aux):
                    config[0] = config_aux.copy()
                    timestamp = datetime.timestamp(datetime.now())
                    perfil_mod= perfil['nick']
                    operacion_mod= 'cambio_configuracion'
                    log = [timestamp, perfil_mod, operacion_mod, '', '']
                    funciones.escribir_csv(paths.DIR_CONFIGURACION, config)
                    funciones.escribir_al_final_csv(paths.DIR_LOGS, log)
                    sg.Popup('Cambios guardados correctamente')
            case sg.WIN_CLOSED:
                current_window.close()
                return config
            case "-SECUNDARIA-VOLVER-":
                current_window.close()
                return config