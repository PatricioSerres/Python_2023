import csv
import json
from datetime import datetime
import os
import funciones.paths as path

def leer_archivo_csv(path):
    try: 
        with open(path, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            contenido_csv = list(lector_csv)
            return contenido_csv
    except FileNotFoundError:
        raise

def crear_archivo_csv(path, linea):
    with open(path, 'w') as archivo_csv:
        writer = csv.writer(archivo_csv, lineterminator= "\n")
        writer.writerow(linea)

def escribir_csv(path, lineas):
    with open(path, 'w') as archivo_csv:
        writer = csv.writer(archivo_csv, lineterminator= "\n")
        writer.writerows(lineas)

def escribir_al_final_csv(path, linea):
    with open(path, 'a', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(linea)

def leer_archivo_json(path):
    try: 
        with open(path, 'r') as archivo_json:
            datos = json.load(archivo_json)
            return datos
    except FileNotFoundError:
        raise

def crear_archivo_json(path):
    with open(path,'w') as archivo_json:                      
        json.dump([], archivo_json)

def escribir_json(path, aux):
    with open(path, 'w')as archivo_json:
        json.dump(aux, archivo_json)

def agregarLog(perfil,lista,titulo):
    logs = []
    timestamp = datetime.timestamp(datetime.now())
    lista_aux = lista.copy()
    lista_aux = ""
    for imagen in lista:
        lista_aux = lista_aux + imagen + ";" 
    lista_aux = lista_aux.removesuffix(";")
    logs= [timestamp,perfil,'nuevo collage',lista_aux,titulo]
    escribir_al_final_csv(path.DIR_LOGS, logs)