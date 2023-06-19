import PySimpleGUI as sg

def crear_ventana_collage():
    """Esta función define el layout de la ventana de collages """
    layout = [
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
    ]
    return sg.Window("Generador de Collages", layout, finalize=True, margins=(100,100))

def main():
    """Esta función ejecuta la ventana de collages"""
    crear_ventana_collage()

    while True:
        current_window, event, values = sg.read_all_windows()            
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-SECUNDARIA-VOLVER-":
            current_window.close()
            break 