import PySimpleGUI as UI
import os
import json

_dias = (range(1,32))
_meses = ('enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')
_años = range(1930,2024)
_añosString = tuple(map(str,_años))
_diasString = tuple(map(str,_dias))

registrer = UI.Window(title = 'registracion',layout=[[UI.Input('nick ',key = 'nick')],
                                                    [UI.Input('nombre',key = 'nombre')],
                                                    [UI.Text('fecha de nacimiento: ')],
                                                    [UI.DropDown(_añosString,key = 'año'),UI.DropDown(_meses,key='mes'),UI.DropDown(_diasString,key= 'dia')],
                                                    [UI.Combo(values=('Hombre','Mujer','-'),readonly=True,key=('lista'),disabled=False)],
                                                    [UI.Checkbox('Otro',background_color=("white"),text_color=('Black'),enable_events=True,key=('check'))],
                                                    [UI.Button('registrarse')]],margins=(500,300))

dir = os.path.dirname(os.path.realpath("prueba UI"))
dir_json = os.path.join(dir,"user.json")
registracionExitosa = False
jsonData = open(dir_json,'r+')                     #abre el archivo json


def cargarJson(user):                                  
    aux = []                                            #crea una lista donde va a guardar los elementos
    jsonData = open(dir_json,'r+')                      #abre el archivo json de usuarios en modo lectura
    datos = json.load(jsonData)                   
    for line in datos:                                  #agrega cada linea de el archivo a una variable lista 
        if(line['nick'] == user['nick']):               #compara cada nombre cargado con el ingresado en la registracion. Si el nombre ya existe tira error y deberia elejir otro
            UI.popup('Ya hay un usuario con ese nick. Escoja uno diferente')
            return(False)
        aux.append(line)                                
    jsonData.close()                                    #cierra el archivo json
    jsonData = open(dir_json,'w+')                      #abre el json en modo escritura, para poder pisar la informacion anterior
    aux.append(user)                                    #agrega el usuario leido en el etapa de registracion a la variable tipo lista
    json.dump(aux,jsonData)                             #vuelca la informacion de los usuarios registrados en el json
    UI.popup('Usuario registrado!')
    jsonData.close()  
    return(True)
    

def pantallaRegistro():
    registracionExitosa = False
    while(registracionExitosa == False):
            state,values = registrer.read()                     #abre la pantalla de registracion
            user = {'nick': values['nick'],
                    "nombre": values['nombre'],
                    "nacimiento": (values['año'],values['mes'],values['dia'])
                    }
            registracionExitosa = cargarJson(user)
    UI.Window.Minimize


