import PySimpleGUI as sg
import os
from PIL import Image
import io
from datetime import datetime
import funciones.funciones as funciones
import funciones.paths as paths



# ------------------------------------------ FUNCIONES ------------------------------------------

def crear_ventana_etiquetar(nombres_imagenes):
    """"Se define el layout de la ventana etiquetar"""
    
    col = [[sg.Text('Ruta: '), sg.Text('', key= '-RUTA-')],
          [sg.Text('Tipo:'), sg.Text('', key= '-TIPO-')], 
          [sg.Text('Resolución:'), sg.Text('', key= '-RESOLUCION-')],
          [sg.Text('Tamaño:'), sg.Text('', key= '-BYTES-'), sg.Text('Bytes')],
          [sg.Image(size=(350,250), key='-IMAGEN-')],
          [sg.Text('Descripción: '), sg.Text('', key='-DESCRIPCION-')]]

    col_files = [[sg.Listbox(values=nombres_imagenes, change_submits=True, size=(40, 18), key='LISTBOX')],
                [sg.Text('Descripción:'), sg.Input(key= '-IMAGEN-DESCRIPTIVO-', size=(30,20)),sg.Button("Agregar", key="-AGREGAR-DESCRIPCION-")],
                [sg.Text('Tags:'), sg.Input(key='-TAG-'), sg.Button('Agregar Tag', key='-AGREGAR-TAG-')],
                [sg.Text('Tags añadidas:')],
                [sg.Listbox(values=[] ,size=(50, 10), key='-TAGS-LIST-'), sg.Button('Eliminar Tag', key='-ELIMINAR-TAG-')], 
                [sg.Button("Guardar", key="-GUARDAR-"),sg.Button("Volver", key="-SECUNDARIA-VOLVER-")]]

    layout = [[sg.Column(col_files), sg.Column(col)]]

    return sg.Window('Etiquetar Imagen', layout, return_keyboard_events=True, use_default_focus=False, size=(1024,768), finalize=True)




# Usa el PIL para leer la info de una imagen
 
def get_img_data(f):
        """Devuelve los datos de la imagen"""
        img = Image.open(f)
        img_format = img.format
        img_size = img.size
        tamano_bytes = os.path.getsize(os.path.join(f))
        return [f,'',img_size, tamano_bytes, img_format,[],'','']
        
        
# Abre solo una imagen, le ajusta el tamaño y la retorna

def get_image(f, maxsize=(450,350)):
     """Genera una imagen usando Pil"""
     img = Image.open(f)
     img.thumbnail(maxsize)
     bio = io.BytesIO()
     img.save(bio, format="PNG")
     del img
     return bio.getvalue()


def guardar_imagen(operacion_mod, foto_actual, fotos, perfil, pos, clas=""):
    """ Esta función guarda la imagen en el archivo csv y actualiza los logs.
        Recibe como parametros la operacion a guardar, la foto actual, la lista de fotos, el perfil actual,
        la posicion de la foto en la lista de fotos y si la imagen no fue  clasificada anteriormente (clas = "nueva")"""

    # Guardamos el perfil que modifico la imagen y modificamos la lista de tags para guardarla
    timestamp = datetime.timestamp(datetime.now())
    perfil_mod = perfil['nick']
    foto_actual[0] = paths.convertir_para_guardar(foto_actual[0], paths.DIR_PROYECTO)
    foto_actual[6] = perfil_mod
    foto_actual[7] = timestamp
    foto = foto_actual.copy()
    foto[5] = ""
    for tag in foto_actual[5]:
        foto[5] = foto[5] + tag + ";"
    foto[5] = foto[5].removesuffix(";")
    if clas == "nueva":
        fotos.append(foto)
    else:
        fotos[pos] = foto
    log = [timestamp, perfil_mod, operacion_mod, '', '']
    # Guarda los cambios en el archivo de logs
    funciones.escribir_al_final_csv(paths.DIR_LOGS, log)
    # Guarda los cambios en el archivo CSV
    funciones.escribir_csv(paths.DIR_ETIQUETAR, fotos)
    
            
def abrir_archivo_etiquetar():
    """ Esta funcion abre el archivo para el etiquetado de imagenes, en caso de no existir lo crea con un encabezado."""
    try:
        # Se abre el archivo
        contenido_csv = funciones.leer_archivo_csv(paths.DIR_ETIQUETAR)
    except FileNotFoundError:
        # Si no esta creado el archivo csv, se crea con un encabezado
        encabezado = ['Ruta',"Descripcion","Resolucion","Tamanio","Tipo",'Tags',"nick","Hora"]
        funciones.crear_archivo_csv(paths.DIR_ETIQUETAR, encabezado)
        contenido_csv = funciones.leer_archivo_csv(paths.DIR_ETIQUETAR)
    except Exception as e:
        print(type(e))
        print(f'La excepción {e} no se pudo resolver')
        sg.Popup('Ocurrió un error inesperado.')
    return contenido_csv






# ------------------------------------------ MAIN ------------------------------------------

def main(perfil, config):
    """La función main ejecuta la ventana etiquetar imagenes. Muestra las imagenes del repositorio de imagenes,
    permite etiquetarlas y agregar una descripción, y muestra el resultado en pantalla. Además permite guardar 
    toda esta información en un archivo. Recibe un perfil y una configuración como parametros. """

    # Obtiene la carpeta que contiene las imágenes del usuario
    if (config[0][0] != ''):
        directorio = paths.convertir_guardado_para_usar(config[0][0], paths.DIR_PROYECTO)
    # Tipos de imagenes soportados por PIL
    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

    # Obtengo la lista de archivos en la carpeta
    try:
        flist0 = os.listdir(directorio)
    except (FileNotFoundError, UnboundLocalError):
        sg.popup("El directorio de imagenes no existe. Cambia la configuración y luego intenta de nuevo")
    else:
        # Crea sub lista de archivos de imagenes
        nombres_imagenes = [f for f in flist0 if os.path.isfile(
        os.path.join(directorio, f)) and f.lower().endswith(img_types)]
        # Numero de imagenes encontradas
        num_files = len(nombres_imagenes)                
        if num_files == 0:
            sg.popup('No hay archivos en la carpeta')
        else:
            # No se utiliza mas flist0
            del flist0   
            # Nombre del primer archivo en la lista  
            filename = os.path.join(directorio, nombres_imagenes[0])   
           
            crear_ventana_etiquetar(nombres_imagenes)

            # Se abre el archivo csv del etiquetado de imagenes
            contenido_csv = abrir_archivo_etiquetar()
            # En fotos se guarda todo el listado de imagenes etiquetadas
            fotos = contenido_csv

            # Loop que lee la entrada del usuario y muestra la imagen, el nombre del archivo
            while True:
                current_window, event, values = sg.read_all_windows()
                try: 
                    # Al clickear algún elemento de la listbox
                    if event == 'LISTBOX': 
                        # Nombre del archivo seleccionado           
                        f = values["LISTBOX"][0]   
                        # Lee este archivo         
                        filename = os.path.join(directorio, f)
                        foto_actual = None
                        # Verifica si la imagen se encuentra en el archivo csv
                        for i, foto in enumerate(fotos):
                            # En esta variable se guarda la direccion absoluta de cada imagen del archivo csv para compararla con la ruta de la imagen sellecionada de la listbox
                            dir_aux = paths.convertir_guardado_para_usar(foto[0], paths.DIR_PROYECTO)
                            if(dir_aux == filename):
                                pos = i
                                foto_actual = foto.copy()
                                foto_actual[5] = foto_actual[5].split(";")
                                if ('' in foto_actual[5]):
                                    foto_actual[5].remove('')
                        # Si la imagen no fue etiquetada previamente, se recibe su información de la función get_img_data
                        if (foto_actual == None):
                            foto_actual = get_img_data(filename)
                        # Se muestra la imagen en pantalla, junto con sus datos
                        imagen = get_image(filename)
                        current_window['-IMAGEN-'].update(data=imagen)
                        current_window['-RUTA-'].update(foto_actual[0])
                        current_window["-DESCRIPCION-"].update(foto_actual[1])
                        current_window['-RESOLUCION-'].update(foto_actual[2])
                        current_window['-BYTES-'].update(foto_actual[3])
                        current_window['-TIPO-'].update(foto_actual[4])
                        current_window['-TAGS-LIST-'].update(values=foto_actual[5])
                    elif event == '-AGREGAR-TAG-':
                        # Añada tags a la lista de tags
                        tag = values['-TAG-']
                        if tag not in foto_actual[5]:
                            foto_actual[5].append(tag)
                            current_window['-TAGS-LIST-'].update(values = foto_actual[5])                          
                        else:
                            sg.Popup('Este tag ya fue ingresado, intenta con otro.')  
                    elif event == '-ELIMINAR-TAG-':
                        # Elimina el tag seleccionado de la lista de tags
                        try:
                            selected_tag = values['-TAGS-LIST-'][0]
                            foto_actual[5].remove(selected_tag)
                            current_window['-TAGS-LIST-'].update(values = foto_actual[5])
                        except IndexError:
                            sg.Popup('Debes seleccionar un tag para borrarlo.')
                    elif event == '-AGREGAR-DESCRIPCION-':
                        descr = values['-IMAGEN-DESCRIPTIVO-']
                        foto_actual[1] = descr
                        current_window["-DESCRIPCION-"].update(foto_actual[1])
                    elif event == '-GUARDAR-':
                        # Si la foto es nueva
                        if (foto_actual[7] == "" ):
                            if ((foto_actual[1] != "") and(len(foto_actual[5]) != 0)):
                                operacion_mod= 'nueva_imagen_clasificada' 
                                pos = (len(fotos))
                                guardar_imagen(operacion_mod, foto_actual, fotos, perfil, pos, "nueva")
                                sg.popup('La imagen fue guardada correctamente')
                            else: 
                                sg.popup('Faltan campos por completar')
                        else:
                            # Si la imagen ya fue clasificada
                            # Si las tags o la descripción cambiaron, se guarda la imagen
                            lista_auxiliar = fotos[pos][5].split(';')
                            if (len(foto_actual[5]) != 0) and (foto_actual[1] != ""):
                                if (fotos[pos][1] != foto_actual[1]) or (lista_auxiliar != foto_actual[5]):
                                    operacion_mod = 'imagen_previamente_clasificada'
                                    guardar_imagen(operacion_mod, foto_actual, fotos, perfil, pos)
                                    sg.popup('La imagen fue guardada correctamente')
                                else: 
                                    sg.popup('Esta imagen ya fue guardada con la misma información')
                            else:
                                sg.popup('Faltan campos por completar')
                    # Agregar Popup -------------------------------------------------------------------
                    elif (event == '-SECUNDARIA-VOLVER-') or (event == sg.WIN_CLOSED):
                        try:
                            # Si la foto es nueva y se realizo un cambio sin guardar
                            if (foto_actual[7] == "" ):
                                if (len(foto_actual[5]) > 0) or (foto_actual[1] != ""):
                                    respuesta = sg.popup_yes_no("No has guardado los cambios. Desea salir igualmente?")
                                    if (respuesta == "Yes"):
                                        current_window.close()
                                        break
                                else: 
                                    current_window.close()
                                    break
                            else:
                                lista_auxiliar = fotos[pos][5].split(';')
                                # Si la foto ya fue etiquetada y se realizo un cambio sin guardar
                                if (fotos[pos][1] != foto_actual[1]) or (lista_auxiliar != foto_actual[5]):
                                    respuesta = sg.popup_yes_no("No has guardado los cambios. Desea salir igualmente?")
                                    if (respuesta == "Yes"):
                                        current_window.close()
                                        break 
                                else: 
                                    current_window.close()
                                    break 
                        except UnboundLocalError:
                            current_window.close()
                            break   
                except UnboundLocalError:
                    sg.popup("No se ha seleccionado ninguna imagen.")
                    
                    