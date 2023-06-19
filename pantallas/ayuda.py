import PySimpleGUI as sg

def crear_ventana_ayuda():
    """ Esta función genera el layout de la ventana de ayuda. """

    texto = """
    Esta aplicación permite generar memes y collages a partir de imágenes etiquetadas (en el caso de los collages).
    Las imágenes se extraen por un directorio elegido por el usuario desde la ventana de configuración, 
    donde también se pueden elegir los repositorios para guardar los memes y los collages.
    Las imágenes son etiquetadas desde la pantalla "Etiquetar Imágenes".
    Se puede editar el perfil presionando el boton ubicado en la esquina superior izquierda.
    Toca la x para cerrar esta ventanta
    """
    
    layout = [
    [sg.Text(text = texto)]
    ]
    return sg.Window("Ayuda", layout, finalize=True, margins=(100,100))

def main():
    """ Esta función ejecuta la ventana de ayuda, que entrará en loop hasta que se cierre """
    crear_ventana_ayuda()
    while True:
         current_window, event,values = sg.read_all_windows()            
         if event == sg.WIN_CLOSED:
            current_window.close()
            break
         