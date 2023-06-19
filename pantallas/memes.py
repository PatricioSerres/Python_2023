import PySimpleGUI as sg
import funciones.paths as paths
import funciones.funciones as funciones
import pantallas.generar_meme as generar_meme
import os
import io
import PIL
import PIL.Image



def get_image(template_seleccionado, maxsize=(600,800)):
     """Genera una imagen usando Pil"""
     img = PIL.Image.open(template_seleccionado)
     img.thumbnail(maxsize)
     bio = io.BytesIO()
     img.save(bio, format="PNG")
     del img
     return bio.getvalue()

def crear_ventana_meme(nombres_imagenes):    
    """Esta función define el layout de la ventana de memes"""
    col_der = [
        [sg.Push(), sg.Text('Previsualización', font= 'Helvetica'), sg.Push()],
        [sg.Image(size=(600,800), key='-IMAGEN-')],
    ]
    col_izq = [
        [sg.Text('Generar Meme', font= 'Helvetica')],
        [sg.Text('Seleccionar template')],
        [sg.Listbox(values= nombres_imagenes,key=('-MEME-LISTBOX-'),change_submits=True, size=(40, 18))],
        [sg.Button("Volver", key="-SECUNDARIA-VOLVER-"), sg.Button('Generar', key= '-TEMPLATE-GENERAR-')]
    ]
    layout= [[sg.Column(col_izq), sg.Column(col_der)]]
    return sg.Window("Generador de memes", layout, finalize=True, size=((1024,900)),relative_location=(-250, -100))

def main(perfil, config):
    """Esta función genera la ventana de selección de template, que permite seleccionar uno de los templates cargados en el archivo JSON y previsualiza su imagen.
    Recibe como parámetros el perfil y la configuración actual."""
    if (config[0][2] == ''):
        sg.Popup('Debes seleccionar un repositorio para guardar los memes')
    else:    
        templates = funciones.leer_archivo_json(paths.DIR_TEMPLATE_MEME)
        nombres_imagenes = {}
        template_seleccionado = ''
        if (config[0][0] != ""):
            directorio = paths.convertir_guardado_para_usar(config[0][0], paths.DIR_PROYECTO)
        try:
            # Lista que contiene todas las imagenes guardadas en el directorio de imagenes
            flist0 = os.listdir(directorio)
        except (FileNotFoundError, UnboundLocalError):
            sg.popup("El directorio de imagenes no existe. Cambia la configuración y luego intenta de nuevo")
        else:
            # Crea sub lista de archivos de imagenes
            for template in templates:  
                if (template['image'] in flist0):
                    nombres_imagenes[template['name']] = template['image']
            # Numero de imagenes encontradas
            num_files = len(nombres_imagenes)                
            if num_files == 0:
                sg.popup('No hay archivos en la carpeta')
            else:
                # No se utiliza mas flist0
                del flist0   
                crear_ventana_meme(list(nombres_imagenes.keys()))
                while True:
                    current_window, event, values = sg.read_all_windows()            
                    if event == sg.WIN_CLOSED or event == '-SECUNDARIA-VOLVER-':
                        current_window.close()
                        break
                    elif event == "-TEMPLATE-GENERAR-":
                        if (template_seleccionado != ''):
                            current_window.hide()
                            for template in templates:
                                if(template['name'] == template_seleccionado):
                                    template_completo = template
                                    break   
                            imagen = PIL.Image.open(filename)
                            imagen = imagen.convert(mode='RGB')
                            generar_meme.main(perfil, template_completo, imagen, config)
                            current_window.close()
                            break
                        else:
                            sg.Popup('Debes seleccionar una imagen para continuar')
                    elif event == "-MEME-LISTBOX-":
                        # Nombre del template seleccionado
                        template_seleccionado = values["-MEME-LISTBOX-"][0]
                        # Lee este archivo         
                        filename = os.path.join(directorio, nombres_imagenes[template_seleccionado])
                        imagen = get_image(filename)
                        current_window['-IMAGEN-'].update(imagen)