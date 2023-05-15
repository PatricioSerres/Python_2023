import PySimpleGUI as sg
import os
from PIL import Image
import io
import csv
from datetime import datetime

def crear_ventana_etiquetar(fnames):
    # define layout, show and read the form
    col = [[sg.Text('Ruta: '), sg.Text('', key= '-RUTA-')],
          [sg.Text('Tipo:'), sg.Text('', key= '-TIPO-')], 
          [sg.Text('Resolución:'), sg.Text('', key= '-RESOLUCION-')],
          [sg.Text('Tamaño:'), sg.Text('', key= '-BYTES-'), sg.Text('Bytes')],
          [sg.Image(size=(350,250), key='-IMAGEN-')],
          [sg.Text('Descripción: '), sg.Text('', key='-DESCRIPCION-')]]

    col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(40, 18), key='listbox')],
                [sg.Text('Descripción:'), sg.Input(key= '-IMAGEN-DESCRIPTIVO-', size=(30,20)),sg.Button("Agregar", key="-AGREGAR-DESCRIPCION-")],
                [sg.Text('Tags:'), sg.InputText(key='-TAG-'), sg.Button('Agregar Tag', key='-AGREGAR-TAG-')],
                [sg.Text('Tags añadidas:')],
                [sg.Listbox(values=[] ,size=(50, 10), key='-TAGS-LIST-'), sg.Button('Eliminar Tag', key='-ELIMINAR-TAG-')], 
                [sg.Button("Guardar", key="-GUARDAR-"),sg.Button("Volver", key="-SECUNDARIA-VOLVER-")]]

    layout = [[sg.Column(col_files), sg.Column(col)]]

    return sg.Window('Etiquetar Imagen', layout, return_keyboard_events=True, use_default_focus=False, size=(1024,768), finalize=True)

    # ------------------------------------------------------------------------------
    # use PIL to read data of one image
    # ------------------------------------------------------------------------------
def get_img_data(f, maxsize=(450,350)):
        """Generate image data using PIL
        """
        img = Image.open(f)
        img_format = img.format
        img_size = img.size
        tamano_bytes = os.path.getsize(os.path.join(f))
        return [f,'',img_size, tamano_bytes, img_format,[],"",""]
        
        
    # ------------------------------------------------------------------------------

def get_image(f, maxsize=(450,350)):
     img = Image.open(f)
     img.thumbnail(maxsize)
     bio = io.BytesIO()
     img.save(bio, format="PNG")
     del img
     return bio.getvalue()



def main(config):
    # Get the folder containin:g the images from the user
    folder = os.path.join(config[0][0])
    
    # PIL supported image types
    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")
    # get list of files in folder
    try:
        flist0 = os.listdir(folder)
    except FileNotFoundError:
        sg.popup("El directorio de imagenes no existe. Cambia la configuración y luego intenta de nuevo")
    else:
        # create sub list of image files (no sub folders, no wrong file types)
        fnames = [f for f in flist0 if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith(img_types)]

        num_files = len(fnames)                # number of iamges found
        if num_files == 0:
            sg.popup('No hay archivos en la carpeta')
        else:
            del flist0                             # no longer needed
            try:
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'r') as archivo_csv:
                    lector_csv = csv.reader(archivo_csv)
                    contenido_csv = list(lector_csv)
            except FileNotFoundError:
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'w') as archivo_csv:
                    linea_vacia = ['Ruta',"Descripcion","Resolucion","Tamaño","Tipo",'Tags',"Ultimo Usuario","Hora"]
                    writer = csv.writer(archivo_csv,lineterminator='\n')
                    writer.writerow(linea_vacia)
                with open(os.path.join('archivos','archivo_etiquetar.csv'), 'r') as archivo_csv:
                    lector_csv = csv.reader(archivo_csv)
                    contenido_csv = list(lector_csv)
            except Exception as e:
                print(type(e))
                print(f'La excepción {e} no se pudo resolver')
                sg.Popup('Ocurrió un error inesperado.')

            
            filename = os.path.join(folder, fnames[0])  # name of first file in list   
            crear_ventana_etiquetar(fnames)
            fotos = contenido_csv
            
            # loop reading the user input and displaying image, filename
            
            while True:
                # read the form
                current_window, event, values = sg.read_all_windows()
                # perform button and keyboard operations
                if event == sg.WIN_CLOSED:
                    current_window.close()
                    break
                elif event == 'listbox':            # something from the listbox
                    f = values["listbox"][0]            # selected filename
                    filename = os.path.join(folder, f)  # read this file
                    foto_actual= None
                    for foto in fotos:
                        if(foto[0] == filename):
                            foto_actual = foto
                            aux = foto_actual[5].split(',')
                            print(aux)
                    if (foto_actual== None):
                        foto_actual=get_img_data(filename)
                    imagen = get_image(filename)
                    current_window['-IMAGEN-'].update(data=imagen)
                    current_window['-RUTA-'].update(foto_actual[0])
                    current_window["-DESCRIPCION-"].update(foto_actual[1])
                    current_window['-RESOLUCION-'].update(foto_actual[2])
                    current_window['-BYTES-'].update(foto_actual[3])
                    current_window['-TIPO-'].update(foto_actual[4])
                    current_window['-TAGS-LIST-'].update(values=foto_actual[5])
                    print(foto_actual)
                elif event == '-AGREGAR-TAG-':
                    # Add the new tag to the list of tags
                    tag = values['-TAG-']
                    if tag not in foto_actual[5]:
                        foto_actual[5].append(tag)
                        if (foto_actual[7]==""):
                            foto_actual[7]= datetime.timestamp(datetime.now())
                            foto_actual[6]= 'Usuario'
                            fotos.append(foto_actual) 
                        else:
                            foto_actual[7]= datetime.timestamp(datetime.now())
                            foto_actual[6]= 'Usuario' 
                        current_window['-TAGS-LIST-'].update(values=foto_actual[5])                          
                    else:
                        sg.Popup('Este tag ya fue ingresado, intenta con otro.')  
                elif event == '-ELIMINAR-TAG-':
                    # Remove the selected tag from the list of tags
                    try:
                        selected_tag = values['-TAGS-LIST-'][0]
                        foto_actual[5].remove(selected_tag)
                        current_window['-TAGS-LIST-'].update(values=foto_actual[5])
                    except IndexError:
                        sg.Popup('Debes seleccionar un tag para borrarlo.')
                elif event == '-SECUNDARIA-VOLVER-':
                    current_window.close()
                    break
                elif event == '-AGREGAR-DESCRIPCION-':
                    descr = values['-IMAGEN-DESCRIPTIVO-']
                    foto_actual[1]= descr
                    if (foto_actual[7]==""):
                        foto_actual[7]= datetime.timestamp(datetime.now())
                        foto_actual[6]= 'Usuario'
                        fotos.append(foto_actual) 
                    else:
                        foto_actual[7]= datetime.timestamp(datetime.now())  
                        foto_actual[6]= 'Usuario'  
                    current_window["-DESCRIPCION-"].update(foto_actual[1])
                elif event == '-GUARDAR-':
                    with open(os.path.join('archivos','archivo_etiquetar.csv'), 'w') as archivo_csv:
                        writer = csv.writer(archivo_csv,lineterminator='\n')
                        writer.writerows(fotos)



    

