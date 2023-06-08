import PySimpleGUI as sg

def crear_ventana_meme():    
    """Esta función define el layout de la ventana de memes"""
    layout = [
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
    ]
    return sg.Window("Generador de memes", layout, finalize=True, margins=(100,100))

# vaya momazos papu :v

def main():
    """Esta función ejecuta la ventana de memes"""
    crear_ventana_meme()

    while True:
        current_window, event, values = sg.read_all_windows()            
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-SECUNDARIA-VOLVER-":
            current_window.close()
            break