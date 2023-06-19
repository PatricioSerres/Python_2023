import PySimpleGUI as sg
import PIL 
from PIL import Image
import PIL.ImageTk
import os
import funciones.paths as paths
import funciones.funciones as funciones
from datetime import datetime

def crear_ventana_registro():
    """ Esta función define el layout para la ventana registro"""


    columna1 = [
        [sg.Text('Registrarse')],
        [sg.Text('nick')], [sg.Input(size=(20,5),font=('calibri',10),key="nick")],
        [sg.Text('Nombre')],[sg.Input(size=(20,5),font=('calibri',10),key='nombre')],
        [sg.Text('Edad')],[sg.Input(size=(8,5),key='edad')],
        [sg.Text('Género autopercibido')],
        [sg.Combo(values=('Hombre','Mujer','-'),readonly=True,key=('lista'),disabled=False,enable_events=True,auto_size_text=True,default_value='-')],
        [sg.Checkbox('Otro',enable_events=True,key=('check'))],
        [sg.Text('Complete el género')],[sg.Input(size=(8,5),disabled=True,key=('completar'))],
        # Guardar los datos
        [sg.Button('Guardar y Salir',button_color=("green"),key='guardar',pad=(0,30)),sg.Button('Salir',key='salir',button_color=('#F53A3A'),pad=(20,0))]
    ]

    columna2 = [
        [sg.Image(key="avatar",pad=((90,10)))],
        [sg.Button('Subir Foto',button_color=("#63ABE7"),key="foto",pad=(150,0))]
    ]

    layout = [
                [   sg.Column(columna1),
                    sg.VSeparator(pad=(100,0)),
                    sg.Column(columna2)
                ]
            ]
    
    return sg.Window('Registro',layout,margins=(100,100),resizable=True, finalize=True)         
       
def cargar_json_nuevo(user):        
    """ Esta funcion carga el perfil del usuario dentro del json. Genera los logs correspondientes."""                          
    # Se leen los elementos del json
    datos = funciones.leer_archivo_json(paths.DIR_USER)
    for line in datos:                                  
        if(line['nick'] == user['nick']):  
        #compara cada nombre cargado con el ingresado en la registracion. Si el nombre ya existe tira error y 
        # deberia elejir otro        
            sg.popup('Ya hay un usuario con ese nick. Escoja uno diferente')
            return False
    # Agrega el nuevo usuario al final de la lista y lo guarda en el json
    datos.append(user)  
    funciones.escribir_json(paths.DIR_USER, datos)
    # Carga de los logs
    timestamp = datetime.timestamp(datetime.now())
    perfil_mod= user['nick']
    operacion_mod= 'nuevo_perfil'
    log = [timestamp, perfil_mod, operacion_mod, '', '']
    funciones.escribir_al_final_csv(paths.DIR_LOGS, log)
    sg.popup('Usuario registrado!') 
    return True
                
def cargar_json(user):
    ''' Esta funcion modificar el perfil del usuario dentro del json. Genera los logs correspondientes. '''
    datos = funciones.leer_archivo_json(paths.DIR_USER)        
    for i, line in enumerate(datos):                                  
        if(line['nick'] == user['nick']):
            datos[i] = user
    funciones.escribir_json(paths.DIR_USER, datos)
    sg.popup('Cambios realizados con éxito!') 
    # Carga de los logs
    timestamp = datetime.timestamp(datetime.now())
    perfil_mod= user['nick']
    operacion_mod= 'modificar_perfil'
    log = [timestamp, perfil_mod, operacion_mod, '', '']
    funciones.escribir_al_final_csv(paths.DIR_LOGS, log)

def register (ya_registrado, perfil = None):
    """ Esta función itera la ventana de registro en un loop infinito y va leyendo los distintos eventos que se producen en la misma.
    Recibe como parametro un booleano que indica si el perfil es nuevo o no y un perfil, en caso de ser un perfil viejo """
    window = crear_ventana_registro()   

    marcado = True

    if (ya_registrado == True):
        # En caso de modificar perfil, se actualiza el layout con los valores de dicho perfil
        # Se desactiva el nick para que no se produzcan cambios
        dic = perfil
        window['nick'].update(perfil['nick'], disabled=True)
        window['nombre'].update(perfil['Nombre'])      
        window['edad'].update(perfil['Edad'])   
        # Se almacena en una variable auxiliar la direccion absoluta de la imagen y se actualiza el layout
        direccion_imagen = paths.convertir_guardado_para_usar(perfil['foto'], paths.DIR_PROYECTO)
        # Se actualiza el genero
        if(perfil['Genero'] == 'Hombre' or perfil['Genero'] == 'Mujer'):
            window['lista'].update(perfil['Genero'], disabled=False)
        else:
            window['lista'].update(disabled=True)
            window['check'].update(True)
            window['completar'].update(perfil['Genero'], disabled=False) 
            marcado = False
    else:
        dic = {}
        # Almacena como direccion de la foto una por defecto
        direccion_imagen = os.path.join(paths.DIR_IMAGENES, 'avatar_inicio.png')
    foto_perfil = Image.open(direccion_imagen).convert(mode= 'RGB')
    imagen_a_mostrar = foto_perfil.copy()
    imagen_a_mostrar.thumbnail((350, 300))
    imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
    window['avatar'].update(data = imagen_a_mostrar)
    while True:
        event,value = window.read()
        if event == 'check':
            # Si marcado es verdadero, se desactiva la lista de seleccion de genero y se habilita el campo para
            # completar el genero autopercibido
            if marcado:
                window['lista'].update(disabled=True)
                window['completar'].update(disabled=False)
                marcado = False
            # Si marcado es falso, se habilita la lista de seleccion de genero y se desactiva el campo a completar
            else:
                window['lista'].update(disabled=False)
                window['completar'].update(disabled=True)
                marcado = True
        elif event == "foto":
            try:
                direccion_aux = sg.PopupGetFile("Seleccione su foto",text_color=("black"),button_color=("white","green"))
                foto_perfil = Image.open(direccion_aux).convert(mode='RGB')
                direccion_imagen = direccion_aux
                imagen_a_mostrar = foto_perfil.copy()
                imagen_a_mostrar.thumbnail((350, 300))
                imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
                window['avatar'].update(data = imagen_a_mostrar)
            except PIL.UnidentifiedImageError:
                sg.popup('Por favor, elija una imagen .png')
            except AttributeError:
                # No se selecciona ninguna imagen
                None       
        elif event == sg.WIN_CLOSED or event == 'salir':
            window.close()
            return dic
        elif event == "guardar":
            try:
                if (value['nick'] == '') or (value['nombre'] == '') or (value['edad'] == ''):
                    raise Exception
                else:
                    # Comprobación de que el genero no es vacío
                    if marcado:
                        if value['lista'] == '-':
                            raise Exception
                        else:
                            genero = value['lista']
                    else:
                        if value['completar'] == '':
                            raise Exception
                        else:
                            genero = value['completar']
                    # Comprobación de que la edad sea un entero
                    try:
                        edades = int(value['edad'])
                    except ValueError:
                        raise ValueError
            except ValueError:
                sg.popup_ok("Ingrese un valor numérico para la edad",title='Edad',button_color=('green'))
            except Exception:
                sg.popup_ok("Hay campos sin completar",title='Advertencia',button_color=('green'))
            else: 
                # guardar la imagen en la carpeta "imagenes" del proyecto   
                if (edades < 0) or (edades > 150):  
                    sg.popup_ok("Ingrese un número válido para la edad",title='Edad',button_color=('green'))
                else:
                    nombre_avatar = 'avatar_'+ value['nick'] + '.png'
                    carpeta_imagenes = os.path.join(paths.DIR_AVATARES,nombre_avatar)
                    # armo el diccionario y lo almaceno en el archivo json
                    carpeta_imagenes = paths.convertir_para_guardar(carpeta_imagenes, paths.DIR_PROYECTO)
                    dic_aux = {'Nombre':value['nombre'],
                            'nick':value['nick'],
                            'Edad':edades,
                            'Genero':genero,
                            'foto':carpeta_imagenes}
                    if (ya_registrado == True):
                        direccion_a_comparar = paths.convertir_guardado_para_usar(carpeta_imagenes, paths.DIR_PROYECTO)
                        # Si se realizaron cambios en los campos o si se seleccionó una nueva imagen, se carga el json
                        if ((dic_aux != perfil) or (direccion_imagen != direccion_a_comparar)):
                            cargar_json(dic_aux)
                            aux = True
                        else:
                            sg.Popup("No se realizó ningun cambio que necesite ser guardado")
                            aux = False
                    else:
                        aux = cargar_json_nuevo(dic_aux)
                    if (aux == True):
                        dic = dic_aux
                        out = foto_perfil.copy()
                        out.thumbnail((350, 300))
                        out.save(carpeta_imagenes,quality=95)
                        window.close()
                        return dic


def registrarse():
    ''' Esta funcion permite registrar un nuevo usuario en la aplicacion'''
    dic = register(False)
    return dic

def modificar(perfil):
    ''' Esta funcion permite modificar un usuario en la aplicacion. Recibe el perfil a modificar'''
    dic = register(True, perfil)
    return dic


