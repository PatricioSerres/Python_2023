import PySimpleGUI as sg
import os
import PIL
import PIL.ImageDraw
import PIL.ImageFont
import PIL.ImageTk
import funciones.paths as paths
import funciones.funciones as funciones
from datetime import datetime


def tam_box(x1, y1, x2, y2):
    """ Esta funcion retorna una tupla con la resta entre el ancho y el alto de la text box"""
    return(x2 - x1, y2 - y1)

def entra(contenedor, contenido):
    """ Esta funcion retorna verdadero si la fuente cabe en la text box y falso en caso contrario. """
    return contenido [0] <= contenedor[0] and contenido [1] <= contenedor[1]

def calcular_tam_fuente(draw, texto, path_fuente, box):
    """ Esta función calcula el tamaño que debe de tener el texto para caber en las text boxes. 
    Recibe como parámetros el texto, la fuente, la text box y un objeto draw correspondiente a la imagen."""
    tam_contenedor = tam_box(box['top_left_x'], box['top_left_y'], box['bottom_right_x'], box['bottom_right_y'])
    for tam in range (200, 5, -5):
        fuente = PIL.ImageFont.truetype(path_fuente, tam)
        box_texto = draw.textbbox((box['top_left_x'], box['top_left_y']), texto, font= fuente)
        tam_box_texto = tam_box(*box_texto)
        if entra(tam_contenedor, tam_box_texto):
            return fuente

    return fuente

def generar_meme(text_boxes, imagen, path_fuente, textos, color):
    """Esta función le agrega textos a una imagen para generar un meme y la retorna. 
    Recibe como parametros la imagen, la posición de los distintos text_boxes, el path de la fuente, los textos a escribir en la imagen y el color seleccionado. """
    meme = imagen.copy()
    draw = PIL.ImageDraw.Draw(meme)
    for i, text_box in enumerate(text_boxes):
        fuente_ajustada = calcular_tam_fuente(draw, textos[i], path_fuente, text_box)
        draw.text((text_box['top_left_x'], text_box['top_left_y']), textos[i], font=fuente_ajustada, fill=color)
    return meme

def crear_ventana_generar_meme(cant, fuentes_guardadas):
    """Esta función define el layout de la ventana de memes """
    input_rows =[[sg.Text(('Texto ' + str(i+1))), sg.Input(size=(15,1), pad=(0,0), key= str(i))] for i in range(cant)]
    col_izq = [
        [sg.Text('Seleccionar Fuente', font= "Helvetica")],
        [sg.Combo(values = fuentes_guardadas, readonly= True, key= '-MEME-FUENTE-', enable_events= True)],
        [sg.Input('#000000', key='-MEME-COLOR-', enable_events= True, disabled=True, size= ((0,0))),sg.ColorChooserButton('Seleccionar Color')]
    ]
    boton_volver = [[sg.Button("Volver", key="-SECUNDARIA-VOLVER-")]]
    col_der = [
        [sg.Image(size= (600,800), key='-MEME-IMAGEN-')],
        [sg.Button('Actualizar', key='-MEME-ACTUALIZAR-'), sg.Button('Guardar y salir', key='-MEME-GUARDAR-')]    
    ]
    layout = [[sg.Column(col_izq + input_rows + boton_volver), sg.Column(col_der)]]
    return sg.Window("Generador de Collages", layout, finalize=True, size=((1024,900)))

def main(perfil, template, imagen, config):
    """Esta función ejecuta la ventana de memes"""
    text_boxes = template['text_boxes']
    fuentes_guardadas = os.listdir(paths.DIR_FUENTES)
    # Cantidad de inputs que hay que incluir en el layout.
    cant = len(text_boxes)
    imagen_a_mostrar = imagen.copy()
    imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
    directorio_memes= paths.convertir_guardado_para_usar(config[0][2], paths.DIR_PROYECTO)
    window = crear_ventana_generar_meme(cant, fuentes_guardadas)
    window['-MEME-IMAGEN-'].update(data = imagen_a_mostrar)
    color = 'black'
    path_fuente = ''
    while True:
        # Loop infinito de eventos.
        current_window, event, values = sg.read_all_windows()           
        if (event == sg.WIN_CLOSED) or (event == '-SECUNDARIA-VOLVER-'):
            current_window.close()
            break
        elif event == '-MEME-FUENTE-':
            # Obtiene la fuente y la guarda en una variable.
            path_fuente = os.path.join(paths.DIR_FUENTES, values["-MEME-FUENTE-"])
        elif event == '-MEME-COLOR-':
            # Toma el color elegido por el usuario y lo guarda en una variable. 
            # En caso de no elegir ninguno se toma al color negro por defecto.
            color = values['-MEME-COLOR-']
            if (color == 'None'):
                color = 'black'
                current_window['-MEME-COLOR-'].update('#000000')
        elif event == '-MEME-ACTUALIZAR-':
            if(path_fuente == ''):
                sg.Popup('Debes seleccionar una fuente')
            else:
                # Genera la imagen con los textos y lo muestra en pantalla.
                textos = []
                for i in range(cant):
                    textos.append(values[str(i)])
                meme_a_mostrar = generar_meme(text_boxes, imagen, path_fuente, textos, color)
                meme_a_mostrar = PIL.ImageTk.PhotoImage(meme_a_mostrar)
                current_window['-MEME-IMAGEN-'].update(data = meme_a_mostrar)
        elif event == '-MEME-GUARDAR-':
            if(path_fuente == ''):
                sg.Popup('Debes seleccionar una fuente')
            else:
                try: 
                    # El usuario elige el nombre de la imagen a guardar.
                    destino = sg.PopupGetText('Ingrese el nombre de la imagen')
                    destino += '.jpg' 
                except TypeError:
                    None
                else:
                     # Genera la imagen con los textos y lo guarda en el directorio seleccionado.
                    textos = []
                    for i in range(cant):
                        textos.append(values[str(i)])
                    meme_a_guardar = generar_meme(text_boxes, imagen, path_fuente, textos, color)
                    destino = os.path.join(directorio_memes, destino)
                    meme_a_guardar.save(destino)
                    sg.Popup('Meme guardado correctamente!')
                    # Crea una nueva linea en el archivo de logs con los datos necesarios.
                    operacion = 'nuevo_meme'
                    timestamp = datetime.timestamp(datetime.now())
                    perfil_mod = perfil['nick']
                    valores = template['image']
                    texto_aux = ""
                    for texto in textos:
                        if (texto != ''):
                           texto_aux = texto_aux + texto + ";"
                    texto_aux = texto_aux.removesuffix(";")
                    linea = [timestamp, perfil_mod, operacion, valores, texto_aux]
                    funciones.escribir_al_final_csv(paths.DIR_LOGS, linea)
                    current_window.close()
                    break
                
        