import PySimpleGUI as sg
import PIL.Image as Image
import PIL.ImageTk
import PIL.ImageOps
import PIL.ImageDraw
import os
import funciones.funciones as funciones


def armar3(carpeta_collage,data_set,perfil):
    size = (500,500)
    coordenadas = [i for i in range(0,501)]
    collage = Image.new('RGB',size)
    collage.save(carpeta_collage,'PNG')
    #
    rutas = list(data_set['Ruta'])
    tags = list(data_set['Tags'])
    #
    columna1 = [#[sg.Text('Generador de Collages',font=('calibri',50),background_color='white',text_color='black')],
              #  
              [sg.Text('Elija la imagen 1',font=('calibri',30),background_color='#C0C0C0',text_color='black')],
              [sg.Combo(values=tags,font=('calibri',20),pad=(50,5),key='im1',enable_events=True)],
              #
              [sg.Text('Elija la imagen 2',font=('calibri',30),background_color='#C0C0C0',text_color='black')],
              [sg.Combo(values=tags,font=('calibri',20),pad=(50,5),key='im2',enable_events=True)],
              #
              [sg.Text('Titulo del collage',font=('calibri',30),background_color='#C0C0C0',text_color='black')],
              [sg.Input(size=(20,0),font=('calibri',20),key='completar')],
              #
              [sg.Text('Coordenadas',font=('calibri',30),background_color='#C0C0C0',text_color='black')],
              [sg.Text('X',font=('calibri',10),background_color='#C0C0C0',text_color='black'),sg.Spin(coordenadas,size=(5,15),key='x'),
               sg.Text('Y',font=('calibri',10),background_color='#C0C0C0',text_color='black'),sg.Spin(coordenadas,size=(5,15),key='y')],
               #
              [sg.Button('Actualizar texto',font=('calibri',20),button_color='green',pad=(5,5),key='actualizar'),
               sg.Button('Deshacer',font=('calibri',20),button_color='green',pad=(5,5),key='deshacer')]
              ]
    
    columna2 = [[sg.Image(source=carpeta_collage,key='muestra')],
                [sg.Button('Guardar',font=('calibri',20),button_color='green',pad=(200,40))]]
    layout = [[sg.Text('Generador de Collages',font=('calibri',50),background_color='white',text_color='black',pad=(0,50)),
               sg.Button('Volver',font=('calibri',20),button_color='green',pad=(5,5),key='volver')],
              [sg.Column(columna1,background_color='white'),
              sg.VSeparator(color='white'),
              sg.Column(columna2,background_color='white')]]
    window = sg.Window('ventana',layout,margins=(50,50),background_color='white',resizable=True)
    draw = PIL.ImageDraw.Draw(collage)
    common = (500,250)

    imagenes= ['ej','ej']
    while True:
        event,value = window.read()
        direcciones = ['ej','ej']
        copias = ['ej','ej']
        originales = ['ej','ej']
        if event == 'im1':
            direcciones[0] = (rutas[tags.index(value['im1'])])
            aux = direcciones[0].split("/")
            imagenes[0] = aux[-1]
            originales[0] = (Image.open(direcciones[0])).resize((common))
            copias[0] = originales[0].copy()
            aux = PIL.ImageOps.fit(copias[0],(common))
            collage.paste(aux,(0,0))
            collage.save(carpeta_collage,'PNG')
            window['muestra'].update(source=carpeta_collage)

        if event == 'im2':
            direcciones[1] = (rutas[tags.index(value['im2'])])
            aux = direcciones[1].split("/")
            imagenes[1] = aux[-1]
            originales[1] = (Image.open(direcciones[1])).resize((common))
            copias[1] = originales[1].copy()
            aux = PIL.ImageOps.fit(copias[1],(common))
            collage.paste(aux,(0,250))
            collage.save(carpeta_collage,'PNG')
            window['muestra'].update(source=carpeta_collage)
        #
        if event == 'actualizar':
            try:
                x = int(value['x'])
                y = int(value['y'])
            except:
                sg.popup_ok("Por favor, ingrese un valor numérico",title='Error',background_color=("white"),text_color=('Black'),button_color=('green'))
            if (-1< x < 500) and (-1 < y < 500):
                anterior = collage.copy()
                draw.text((x,y),value['completar'])
                collage.save(carpeta_collage,'PNG')
                window['muestra'].update(source=carpeta_collage)
            elif(not(-1< x < 500)):
                sg.popup_ok("Por favor, ingrese un valor del 0 y 900",title='Error X',background_color=("white"),text_color=('Black'),button_color=('green'))
            else:
                sg.popup_ok("Por favor, ingrese un valor del 0 y 500",title='Error Y',background_color=("white"),text_color=('Black'),button_color=('green'))

        #
        if event == 'deshacer':
            try:
                collage = anterior
                collage.save(carpeta_collage,'PNG')
                draw = PIL.ImageDraw.Draw(collage)
                window['muestra'].update(source=carpeta_collage)
            except:
                None
        #
        if event == 'Guardar':
            collage.save(carpeta_collage,'PNG')
            funciones.agregarLog(perfil,imagenes,value['completar'])
        if event == sg.WIN_CLOSED or event == 'volver':
            window.close()
            break