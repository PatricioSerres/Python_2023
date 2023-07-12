import PySimpleGUI as sg
import pandas as pd
import funciones.paths as paths
import funciones.funciones as funciones
import PIL.Image as Image
import PIL.ImageTk
import PIL.ImageOps
import PIL.ImageDraw

def crear_ventana_collage(tags, coordenadasx, coordenadasy, cant):
    """ Esta función crea el layout de la ventana de la ventana collage"""    

    input_rows =[[sg.Text(('Elija la imagen ' + str(i+1))), 
                  sg.Combo(values=tags, font=('calibri',20), pad=(50,5), key= 'im'+ str(i+1), enable_events=True, readonly=True)] for i in range(cant)]

    columna1 = [             
              [sg.Text('Titulo del collage',font=('calibri',30),background_color='#C0C0C0',
                       text_color='black')],
              [sg.Input(size=(20,0),font=('calibri',20),key='completar',
                        do_not_clear=False)],
              
              [sg.Text('Coordenadas',font=('calibri',30),background_color='#C0C0C0',
                       text_color='black')],
              [sg.Text('X',font=('calibri',10),background_color='#C0C0C0',
                       text_color='black'),sg.Spin(coordenadasx,size=(5,15),key='x'),
               sg.Text('Y',font=('calibri',10),background_color='#C0C0C0',
                       text_color='black'),sg.Spin(coordenadasy,size=(5,15),key='y')],

              [sg.Button('Actualizar texto',font=('calibri',20),button_color='green',
                         pad=(5,5),key='agregar_texto')]
            ]
    
    columna2 = [[sg.Image(key='muestra')],
                [sg.Button('Guardar y salir',font=('calibri',20),button_color='green',pad=(200,40),key='Guardar')]]
    
    layout = [[sg.Text('Generador de Collages',font=('calibri',50),
                       background_color='white',text_color='black',pad=(0,50)),
               sg.Button('Volver',font=('calibri',20),button_color='green',pad=(5,5),key='volver')],
              [sg.Column(input_rows + columna1,background_color='white'),
              sg.VSeparator(color='white'),
              sg.Column(columna2,background_color='white')]]
    
    # Asigno la ventana
    return sg.Window('Generar Collage',layout,margins=(50,50),background_color='white',resizable=True, finalize=True)

def iniciar_collage (perfil, directorio_collage, template, commons, lugares):
    """ Esta funcion recibe la opcion elegida para el collage, lee el csv con las imagenes etiquetadas 
     y llama a una funcion dependiendo si se usaran dos o tres fotos """

    direc_archivos = paths.DIR_ETIQUETAR
    data_set = pd.read_csv(direc_archivos)

    # Listo las direcciones y las tags
    rutas = list(data_set['Ruta'])
    tags = list(data_set['Tags'])
    # Coordenadas para la ubicacion del texto
    max_y = 501
    max_x = 501
    coordenadasy = [i for i in range(0,max_y)]
    coordenadasx = coordenadasy
    
    # Tamaño del collage
    # Se ve cuantas fotos son segun el template y que tamaño tendrá la imagen
    match template:
        case 1 | 3: 
            cant = 2
            size = (500,500)
        case 2:
            cant = 3
            size = (500,500)
        case 4:
            cant = 3
            size = (900,500)
            max_x = 901
            coordenadasx = [i for i in range(0,max_x)]
            
    window = crear_ventana_collage(tags, coordenadasx, coordenadasy, cant)

    # Se crea el collage como una imagen en negro y se actualiza en el layout
    collage = Image.new('RGB',size)
    imagen_a_mostrar = collage.copy()
    imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
    window['muestra'].update(data = imagen_a_mostrar)

    # Establezco en donde se dibujara el texto
    draw = PIL.ImageDraw.Draw(collage)
    
    # Nombre de las imagenes
    imagenes = ["ej" for i in range(cant)]
    titulo = ''
    while True:        
        window, event, values = sg.read_all_windows()   
        # Listas para almacenar las direcciones, las copias y las originales
        if event == 'im1':
            # Si se quiere elegir la primera imagen, se envían los parametros necesarios a la función colocar imagenes
            collage = funciones.colocar_imagenes(imagenes,collage,rutas,tags,values['im1'],commons[0],lugares[0],posicion=0)
            imagen_a_mostrar = funciones.actualizar_imagen(collage,x,y,max_x,max_y,imagen_a_mostrar,titulo)
            window['muestra'].update(data = imagen_a_mostrar)     
        elif event == 'im2':
            # Se repite la misma logica que para el anterior if
            collage = funciones.colocar_imagenes(imagenes,collage,rutas,tags,values['im2'],commons[1],lugares[1],posicion=1)
            imagen_a_mostrar = funciones.actualizar_imagen(collage,x,y,max_x,max_y,imagen_a_mostrar,titulo)
            window['muestra'].update(data = imagen_a_mostrar)
        elif event == 'im3':
            # Se repite la misma logica que para el anterior if
            collage = funciones.colocar_imagenes(imagenes,collage,rutas,tags,values['im3'],commons[2],lugares[2],posicion=2)
            imagen_a_mostrar = funciones.actualizar_imagen(collage,x,y,max_x,max_y,imagen_a_mostrar,titulo)
            window['muestra'].update(data = imagen_a_mostrar)
        elif event == 'agregar_texto':
            # Crea una copia de la imagen sin texto para agregarle uno y luego mostrarlo en pantalla
            imagen_con_texto = collage.copy()
            draw = PIL.ImageDraw.Draw(imagen_con_texto)
            try:
                # Me fijo si los valores ingresados son numéricos, sino mostrara una ventana de error
                x = int(values['x'])
                y = int(values['y'])
            except:
                sg.popup_ok("Por favor, ingrese un valor numérico",title='Error',background_color=("white"),text_color=('Black'),button_color=('green'))
            else:
                titulo = values['completar']
                titulo = funciones.actualizar(draw, titulo, x, y, max_x,max_y)      
                imagen_a_mostrar = imagen_con_texto.copy()
                imagen_a_mostrar = PIL.ImageTk.PhotoImage(imagen_a_mostrar)
                window['muestra'].update(data = imagen_a_mostrar)              
        elif event == 'Guardar':
            # Si se guarda se hara un ultimo guardado de los cambios y 
            # se llamara a la funcion para hacer los logs
            if ('ej' in imagenes):
                sg.Popup('Hay fotos sin seleccionar')
            elif (titulo == ''): 
                sg.Popup('Debes agregar un titulo')
            else:
                try:
                    funciones.guardar_collage(imagen_con_texto,perfil,imagenes,titulo, directorio_collage)
                except TypeError:
                    None
                else: 
                    window.close()
                    break
        elif event == sg.WIN_CLOSED or event == 'volver':
            # Si se cierra la ventana o se presiona volver
            window.close()
            break