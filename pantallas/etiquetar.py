import PySimpleGUI as sg
import os
from PIL import Image
import io
import csv
from datetime import datetime

#Consultar Popup --------------------------------------------------------------------
# Arreglar lista como texto

def crear_ventana_etiquetar(fnames):
    """Se define el layout de la ventana etiquetar"""
    
    col = [[sg.Text('Ruta: '), sg.Text('', key= '-RUTA-')],
          [sg.Text('Tipo:'), sg.Text('', key= '-TIPO-')], 
          [sg.Text('Resolución:'), sg.Text('', key= '-RESOLUCION-')],
          [sg.Text('Tamaño:'), sg.Text('', key= '-BYTES-'), sg.Text('Bytes')],
          [sg.Image(size=(350,250), key='-IMAGEN-')],
          [sg.Text('Descripción: '), sg.Text('', key='-DESCRIPCION-')]]

    col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(40, 18), key='listbox')],
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



def main(perfil, config):
    # Obtiene la carpeta que contiene las imágenes del usuario
    folder = os.path.join(config[0][0])
    
    # Tipos de imagenes soportados por PIL
    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")
    # Obtengo la lista de archivos en la carpeta
    try:
        flist0 = os.listdir(folder)
    except FileNotFoundError:
        sg.popup("El directorio de imagenes no existe. Cambia la configuración y luego intenta de nuevo")
    else:
        # Crea sub lista de archivos de imagenes
        fnames = [f for f in flist0 if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith(img_types)]
        # Numero de imagenes encontradas
        num_files = len(fnames)                
        if num_files == 0:
            sg.popup('No hay archivos en la carpeta')
        else:
            # No se utiliza mas flist0
            del flist0                             
            try:
                # Se abre el archivo
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'r') as archivo_csv:
                    lector_csv = csv.reader(archivo_csv)
                    contenido_csv = list(lector_csv)
            except FileNotFoundError:
                # Si no esta creado el archivo csv, se crea con un encabezado
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'w') as archivo_csv: 
                    encabezado = ['Ruta',"Descripcion","Resolucion","Tamaño","Tipo",'Tags',"Ultimo Usuario","Hora"]
                    writer = csv.writer(archivo_csv,lineterminator='\n')
                    writer.writerow(encabezado)
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'r') as archivo_csv:
                    lector_csv = csv.reader(archivo_csv)
                    contenido_csv = list(lector_csv)
            except Exception as e:
                print(type(e))
                print(f'La excepción {e} no se pudo resolver')
                sg.Popup('Ocurrió un error inesperado.')

            # Nombre del primer archivo en la lista  
            filename = os.path.join(folder, fnames[0])   
            crear_ventana_etiquetar(fnames)
            fotos = contenido_csv
            logs = []
            # Loop que lee la entrada del usuario y muestra la imagen, el nombre del archivo

            while True:

                current_window, event, values = sg.read_all_windows()
                # Respuesta a distintos eventos
                if event == sg.WIN_CLOSED:
                    current_window.close()
                    break
                # Al clickear algún elemento de la listbox
                elif event == 'listbox': 
                    # Nombre del archivo seleccionado           
                    f = values["listbox"][0]   
                    # Lee este archivo         
                    filename = os.path.join(folder, f)  
                    foto_actual= None
                    for foto in fotos:
                        if(foto[0] == filename):
                            foto_actual = foto
                            try:
                                aux = foto[5]
                                aux = aux.replace("[", "")
                                aux = aux.replace("]", "")
                                aux = aux.replace("'", "")
                                aux = aux.split(',')
                                foto_actual[5] = list(aux)
                            except AttributeError:
                                print('Error de atributo')
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
                    timestamp = datetime.timestamp(datetime.now())
                    fecha_hora = datetime.fromtimestamp(timestamp)
                    tag = values['-TAG-']
                    if tag not in foto_actual[5]:
                        foto_actual[5].append(tag)
                        fecha_mod=fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
                        perfil_mod= perfil['nick']
                        if (foto_actual[7]==""):
                            foto_actual[7]= fecha_hora.strftime("%m/%d/%Y")
                            foto_actual[6]= perfil['nick']
                            fotos.append(foto_actual) 
                            operacion_mod= 'Nueva Imagen Clasificada'
                        else:
                            foto_actual[7]= fecha_hora.strftime("%m/%d/%Y")
                            foto_actual[6]= perfil['nick'] 
                            operacion_mod= 'Imagen Previamente Clasificada'
                        log=[fecha_mod, perfil_mod,operacion_mod]
                        logs.append(log)
                        current_window['-TAGS-LIST-'].update(values=foto_actual[5])                          
                    else:
                        sg.Popup('Este tag ya fue ingresado, intenta con otro.')  
                elif event == '-ELIMINAR-TAG-':
                    timestamp = datetime.timestamp(datetime.now())
                    fecha_hora = datetime.fromtimestamp(timestamp)
                    # Elimina el tag seleccionado de la lista de tags
                    try:
                        selected_tag = values['-TAGS-LIST-'][0]
                        foto_actual[5].remove(selected_tag)
                        fecha_mod=fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
                        perfil_mod= perfil['nick']
                        operacion_mod= 'Imagen Previamente Clasificada'
                        log=[fecha_mod, perfil_mod,operacion_mod]
                        logs.append(log)
                        current_window['-TAGS-LIST-'].update(values=foto_actual[5])
                    except IndexError:
                        sg.Popup('Debes seleccionar un tag para borrarlo.')
                elif event == '-SECUNDARIA-VOLVER-':
                    current_window.close()
                    break
                elif event == '-AGREGAR-DESCRIPCION-':
                    timestamp = datetime.timestamp(datetime.now())
                    fecha_hora = datetime.fromtimestamp(timestamp)
                    descr = values['-IMAGEN-DESCRIPTIVO-']
                    foto_actual[1]= descr
                    fecha_mod=fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
                    perfil_mod= perfil['nick']
                    if (foto_actual[7]==""):
                        foto_actual[7]= fecha_hora.strftime("%m/%d/%Y")
                        foto_actual[6]= perfil['nick']
                        fotos.append(foto_actual) 
                        operacion_mod= 'Nueva Imagen Clasificada'
                    else:
                        foto_actual[7]= fecha_hora.strftime("%m/%d/%Y")  
                        foto_actual[6]= perfil['nick'] 
                        operacion_mod= 'Imagen Previamente Clasificada'
                    log=[fecha_mod, perfil_mod,operacion_mod]
                    logs.append(log)
                    current_window["-DESCRIPCION-"].update(foto_actual[1])
                elif event == '-GUARDAR-':
                    timestamp = datetime.timestamp(datetime.now())
                    fecha_hora = datetime.fromtimestamp(timestamp)
                    with open(os.path.join('archivos','logs.csv'), 'a') as log:
                        writer = csv.writer(log)
                        writer.writerows(logs)
                    # Guarda los cambios en el archivo CSV
                    with open(os.path.join('archivos','archivo_etiquetar.csv'), 'w') as archivo_csv:
                        writer = csv.writer(archivo_csv,lineterminator='\n')
                        writer.writerows(fotos)
                    logs=[]
                    

                    