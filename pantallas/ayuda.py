import PySimpleGUI as sg

def crear_ventana_ayuda():
    layout = [
        [sg.Text("Este es un texto de ejemplo. Toca la x para cerrar esta ventanta")]
    ]
    return sg.Window("Ayuda", layout, finalize=True, margins=(100,100))

def main():
    crear_ventana_ayuda()
    while True:
         current_window, event, values = sg.read_all_windows()            
         if event == sg.WIN_CLOSED:
            current_window.close()
            break
         