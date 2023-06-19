import PySimpleGUI as UI
import os
import json
import pantallas.registro as registro
from PIL import Image, ImageTk
 

def main():
    nums = ('0','1','2','3')                                               #variable que contiene los posibles valores que retorne la funcion login, uno para cada pestaña
    dir = os.path.dirname(os.path.realpath("imagenes"))
    dir_json = os.path.join('archivos',"user.json")
    try:
        jsonData = open(dir_json,'r+')
    except FileNotFoundError:                                               #si no esta creado lo inicializa
        with open(dir_json,'w') as jsonData:                      
            json.dump([],jsonData)
        jsonData = open(dir_json,'r+')

    lista = []
    for i in range(0,20,1):                                          #inicia la lista de perfiles a cargar. En la funcion "recorrerJson" se reemplazaran las imagenes por default por las  
        lista.append(os.path.join(dir, 'imagenes', 'perfil.png'))    #correspondientes a los perfiles. El limite es de 20 perfiles (5 pestañas)
    def recorrerJson():
        datos = json.load(jsonData)
        i=0
        if (datos != []):
            for line in datos:
                lista[i] = line["foto"]
                i += 1
        jsonData.close()

    recorrerJson()

    def _login(act,state):                                       #defino una funcion que vaya abriendo la ventana con valores actualizados por fuera
        login = UI.Window(title = 'A - Inicio', layout =[[UI.Button(key ='0',image_filename=lista[act],image_size=(175,175)),UI.Button(key ='1',image_size=(175,175),image_filename=lista[act+1]),UI.Button(key ='2',image_size=(175,175),image_filename=lista[act+2]),UI.Button(key ='3',image_size=(175,175),image_filename=lista[act+3]),UI.Button('ver mas >',key='mas')],
                                                        [UI.Text(' '*79),UI.Button('registrarse',key = 'register')]],margins =(500,300))
        state,values= login.read()
        if state == 'mas':
            act = act+4
        if state == UI.WIN_CLOSED:
            login.close()
        else:
            login.hide()
        return act,state,login  
    perfil_actual= []
    act = 0
    state = 0
    while True:
        act,state,login = _login(act,state)                    #act para manejar la pantalla y state para verificar si se elije un perfil
        if state == UI.WIN_CLOSED:
            break
        if(act == 20):                                         #si llega a el limite (la ultima pantalla) vuelve a la principal
            act = 0
        if state == 'register':
            login.hide()
            registro.registrarse()
            login.un_hide()
        try:
            if state in nums:
                jsonData = open(dir_json,'r+')
                perfil_actual = json.load(jsonData)                
                perfil_actual= perfil_actual[int(state)+act]    #guarda el perfil elegido
                break
        except IndexError:                                  #si se clickea una posicion sin ningun perfil registrado aparece la opcion de registrarse         
            aux = UI.PopupYesNo('no hay ningun perfil registrado en esta posicion, desea registrar un nuevo perfil?')   
            if aux == 'Yes':
                login.hide()
                registro.registrarse()
                login.un_hide()
    login.close()
    return perfil_actual
                           
#llamar a la siguiente funcion con la variable perfil_actual