import PySimpleGUI as sg
from PIL import Image
import base64,json,os

def _register ():
    avatar = '././imagenes/avatar.png'
    fondo = background_color=('white')

    columna1 = [
        #Texto de registrarse
        [sg.Text('Registrarse')],
        #Input de nick
        [sg.Text('nick')],[sg.Input(size=(20,5),font=('calibri',10),key="nick")],
        #Input de nombre      
        [sg.Text('Nombre',)],[sg.Input(size=(20,5),font=('calibri',10),key='nombre')],
        #Input de edad
        [sg.Text('Edad',)],[sg.Input(size=(8,5),key='edad')],
        #Genero
        [sg.Text('Género autopercibido',background_color=("white"),text_color=('Black'))],
        [sg.Combo(values=('Hombre','Mujer','-'),readonly=True,key=('lista'),disabled=False,enable_events=True,auto_size_text=True,default_value='-')],
        [sg.Checkbox('Otro',background_color=("white"),text_color=('Black'),enable_events=True,key=('check'))],
        [sg.Text('Complete el género',background_color=("white"),text_color=('Black'))],[sg.Input(size=(8,5),disabled=True,key=('completar'))],
        # Guardar los datos
        [sg.Button('Guardar Datos',key='guardar',pad=(0,30)),sg.Button('Salir',key='salir',pad=(20,0))]

    ]

    columna2 = [
        [sg.Image(source=avatar,key="avatar",pad=((90,10)),subsample=(2),s=(300,300))],
        [sg.Button('Subir Foto',key="foto",pad=(150,0))]
    ]
    layout = [
                [   sg.Column(columna1),
                    sg.VSeparator(pad=(100,0)),
                    sg.Column(columna2)
                ]
            ]
    window = sg.Window('Registro',layout,scaling=3,margins=(100,100),resizable=True)
    visible = True
    errores = False
    dicc = {}
    direc = '././imagenes/perfil.png'
    while True:
        event,value = window.read()
        if event == 'check':
            if visible:
                window['lista'].update(disabled=True)
                window['completar'].update(disabled=False)
                visible = False
            else:
                window['lista'].update(disabled=False)
                window['completar'].update(disabled=True)
                visible = True
        if event == "foto":
            direc = sg.PopupGetFile("Seleccione su foto",background_color=("white"),text_color=("black"),button_color=("white","green"))
            # cambios /////////
            foto_perfil = Image.open(direc)
            #/////////////
            '''if ('.png' in findir[-1]):
                window['avatar'].update(source=direc,subsample=2)
                #print (findir)
            else: 
                sg.popup('Por favor, elija una imagen .png')'''
        if event == "guardar":
            errores = False
            if value['nick'] == '':
                sg.popup_ok("Complete el campo: nick",title='Nick',background_color=("white"),text_color=('Black'),button_color=('green'))
                errores = True
            if value['nombre'] == '':
                sg.popup_ok("Complete el campo: Nombre",title='Nombre',background_color=("white"),text_color=('Black'),button_color=('green'))
                errores = True
            if value['edad'] == '':
                sg.popup_ok("Complete el campo: Edad",title='Edad',background_color=("white"),text_color=('Black'),button_color=('green'))
                errores = True
            else:
                try:
                    print('entro al try')
                    edades = int(value['edad'])
                except:
                    errores = True
                    sg.popup_ok("Ingrese un valor numérico",title='Edad',background_color=("white"),text_color=('Black'),button_color=('green'))
            if visible:
                if value['lista'] == '-':
                    sg.popup_ok("Complete el campo: Genero",title='Error')
                    errores = True
                else:
                    #print('entro aca')
                    genero = value['lista']
            else:
                if value['completar'] == '':
                    sg.popup_ok("Complete el campo: Genero2",title='Error')
                    errores = True
                elif(not visible):
                    genero = value['completar']
            if errores == False:
                # guardar la imagen 
                nombre_avatar = 'avatar'+value['nick']+'.png'
                inicio = os.path.dirname(os.path.realpath('.'))
                carpeta_imagenes = os.path.join(inicio,'UNLPImage','imagenes',nombre_avatar)
                out = foto_perfil.resize((400,400)) 
                out.save(carpeta_imagenes,quality=95)
                # actualizo la imagen 
                window['avatar'].update(source=carpeta_imagenes)
                # armo el diccionario
                dicc = {'Nombre':value['nombre'],
                        'nick':value['nick'],
                        'Edad':value['edad'],
                        'Genero':genero,
                        'foto':carpeta_imagenes}
        if event == sg.WIN_CLOSED or event == 'salir':
            window.close()
            return dicc

dir_json = os.path.join('archivos',"user.json")
registracionExitosa = False

def cargarJson(user):                                  
    aux = []                                            #crea una lista donde va a guardar los elementos
    jsonData = open(dir_json,'r+')                      #abre el archivo json de usuarios en modo lectura
    datos = json.load(jsonData)                   
    for line in datos:                                  #agrega cada linea de el archivo a una variable lista 
        if(line['nick'] == user['nick']):               #compara cada nombre cargado con el ingresado en la registracion. Si el nombre ya existe tira error y deberia elejir otro
            sg.popup('Ya hay un usuario con ese nick. Escoja uno diferente')
            return(False)
        aux.append(line)                                
    jsonData.close()                                    #cierra el archivo json
    jsonData = open(dir_json,'w+')                      #abre el json en modo escritura, para poder pisar la informacion anterior
    aux.append(user)                                    #agrega el usuario leido en el etapa de registracion a la variable tipo lista
    json.dump(aux,jsonData)                             #vuelca la informacion de los usuarios registrados en el json
    sg.popup('Usuario registrado!')
    jsonData.close()  
    return(True)

def registrarse():    
    dic = _register()
    vacio = {}
    if (dic != vacio):
        cargarJson(dic)