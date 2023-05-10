import PySimpleGUI as UI
import os
import json
import REGISTRACION



login = UI.Window(title = 'iniciar sesion', layout=[[UI.Input('nick',key = 'nombre')],
                                                    [UI.Button('iniciar sesion',button_color='blue')],
                                                    [UI.Button('no tienes cuenta?')]])







dir = os.path.dirname(os.path.realpath("prueba UI"))
dir_json = os.path.join(dir,"user.json")
registracionExitosa = False
jsonData = open(dir_json,'r+')                     #abre el archivo json
state,values = login.read()                        #abre la pantalla de login

if state == 'no tienes cuenta?':
    REGISTRACION.pantallaRegistro()


elif(state == 'iniciar sesion'):
    reader = json.load(jsonData)                    
    for linea in reader:                            #recorre el archivo para buscar si el usuario ya esta registrado
        if linea["nombre"] == values["nombre"]:     #si lo encuentra deberia avanzar a la siguiente ventana
            usuarioActual = values["nombre"]        #se guarda la informacion de el usuario que inicio la sesion
            #lector a la siguiente pantalla    
            UI.popup('sesion iniciada!')
            break

jsonData.close()