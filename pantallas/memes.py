import PySimpleGUI as sg

def crear_ventana_meme(nombre):
    layout = [
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-")],
    ]
    return sg.Window(nombre, layout, finalize=True, margins=(100,100))

def main(nombre):
    crear_ventana_meme(nombre)

    while True:
        current_window, event, values = sg.read_all_windows()            
        if event == sg.WIN_CLOSED:
            current_window.close()
            break
        elif event == "-SECUNDARIA-VOLVER-":
            current_window.close()
            break