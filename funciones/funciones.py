import csv
import json
from datetime import datetime
import os
import funciones.paths as path
import PIL.Image as Image
import PIL.ImageTk
import PIL.ImageOps
import PIL.ImageDraw
import PySimpleGUI as sg

def leer_archivo_csv(path):
    """ Esta función guarda y retorna en una variable el contenido del archivo csv a partir de un path absoluto. 
    En caso de que el archivo no exista eleva la excepción 'FileNotFoundError'."""
    try: 
        with open(path, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            contenido_csv = list(lector_csv)
            return contenido_csv
    except FileNotFoundError:
        raise

def crear_archivo_csv(path, linea):
    """ Esta función crea un archivo csv. Recibe como parámetros un path absoluto y la linea a escribir."""
    with open(path, 'w') as archivo_csv:
        writer = csv.writer(archivo_csv, lineterminator= "\n")
        writer.writerow(linea)

def escribir_csv(path, lineas):
    """ Esta función escribe un archivo csv. Recibe como parámetros un path absoluto y las lineas a escribir."""
    with open(path, 'w') as archivo_csv:
        writer = csv.writer(archivo_csv, lineterminator= "\n")
        writer.writerows(lineas)

def escribir_al_final_csv(path, linea):
    """ Esta función escribe al final de un archivo csv. Recibe como parámetros un path absoluto y la linea a escribir."""
    with open(path, 'a', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(linea)

def leer_archivo_json(path):
    """ Esta función guarda y retorna en una variable el contenido del archivo json a partir de un path absoluto. 
    En caso de que el archivo no exista eleva la excepción 'FileNotFoundError'."""
    try: 
        with open(path, 'r') as archivo_json:
            datos = json.load(archivo_json)
            return datos
    except FileNotFoundError:
        raise

def crear_archivo_json(path):
    """ Esta función crea un archivo json. Recibe como parámetro un path absoluto."""
    with open(path,'w') as archivo_json:                      
        json.dump([], archivo_json)

def escribir_json(path, aux):
    """ Esta función escribe un archivo json. Recibe como parámetros un path absoluto y las lineas a escribir."""
    with open(path, 'w')as archivo_json:
        json.dump(aux, archivo_json)

def agregarLog(perfil,lista,titulo):
    """ Esta función escribe en el archivo de logs cada vez que se realiza un cambio en el generador de collage."""
    logs = []
    timestamp = datetime.timestamp(datetime.now())
    lista_aux = lista.copy()
    lista_aux = ""
    for imagen in lista:
        lista_aux = lista_aux + imagen + ";" 
    lista_aux = lista_aux.removesuffix(";")
    logs= [timestamp,perfil,'nuevo collage',lista_aux,titulo]
    escribir_al_final_csv(path.DIR_LOGS, logs)

def guardar_collage(collage,perfil,imagenes,texto, config):
    """ Esta funcion guarda el progreso del collage y llama a la funcion para agregar el log"""
    try: 
        # El usuario elige el nombre de la imagen a guardar.
        destino = sg.PopupGetText('Ingrese el nombre de la imagen')
        destino += '.jpg' 
    except TypeError:
        raise
    else:
        destino = os.path.join(config, destino)
        collage.save(destino)
        sg.Popup('Collage guardado correctamente!')
        # Crea una nueva linea en el archivo de logs con los datos necesarios.
        agregarLog(perfil, imagenes, texto)

def colocar_imagenes (imagenes,collage,rutas,tags,nombre_imagen,common,lugar_imagen,posicion):
    """ Esta funcion toma la imagen seleccionada, le cambia el tamaño y la encaja en
     la posicion que va y finalmente retorna la imagen """
    # Guarda la direccion en una variable
    direccion = (rutas[tags.index(nombre_imagen)])
    # Toma el nombre de la imagen
    aux = direccion.split("/")
    imagenes[posicion] = aux[-1]
    # Guarda la imagen original cambiada de tamaño
    original = (Image.open(direccion)).resize((common))
    # Copia la imagen y la encaja
    copia = original.copy()
    aux = PIL.ImageOps.fit(copia, (common))
    # Lo pega en el collage y lo guarda
    collage.paste(aux,lugar_imagen)
    return collage

def actualizar_imagen(collage,x,y,imagen_a_mostrar,titulo):
    """Esta función crea un Tk de imagen para mostrar en pantalla y verifica si tiene titulo"""
    if (titulo != ''):
        imagen_con_texto = collage.copy()
        draw = PIL.ImageDraw.Draw(imagen_con_texto)
        draw.text((x,y),titulo)  
        imagen_a_mostrar = imagen_con_texto.copy()
    else:
        imagen_a_mostrar = collage.copy()
    imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
    return imagen_a_mostrar