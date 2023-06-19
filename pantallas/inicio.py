import PySimpleGUI as sg
import os
import pantallas.registro as registro
import funciones.paths as paths
import funciones.funciones as funciones
import PIL.Image as Image
import PIL.ImageOps
 
# ------------------------------------------ FUNCIONES ------------------------------------------
def crear_ventana_inicio(lista):
    """ Esta función genera el layout de la ventana de inicio""" 
    
    espacio_en_blanco = [sg.Text('')],

    botones = [
            [sg.Push(), sg.Text("INICIO DE SESION", justification = "center"), sg.Push()], 
            [sg.Push(), sg.Button(key = '0', image_filename = lista[0]["foto"]),
            sg.Button(key = '1', image_filename = lista[1]["foto"]),
            sg.Button(key = '2', image_filename = lista[2]["foto"]),
            sg.Button(key = '3', image_filename = lista[3]["foto"]), sg.Push()],
            [sg.Text("USUARIOS: ", justification = 'left'), sg.Push(), sg.Text(lista[0]["nick"], pad=(50,30), key='Usuario 0'),
             sg.Text(lista[1]["nick"], pad=(55,30), key='Usuario 1'),
             sg.Text(lista[2]["nick"], pad=(55,30), key='Usuario 2'),
             sg.Text(lista[3]["nick"], pad=(55,30), key='Usuario 3'), sg.Push()],
            [sg.Button('< Atrás', key = '-INICIO-ATRAS-'), sg.Push(),
            sg.Button('Ver más >',key = '-INICIO-MAS-')],
            [sg.Push(), sg.Text("Pagina 1/5", key = '-PAGINAS-')]
            ]
    
    layout = [[sg.Column(espacio_en_blanco, element_justification = 'center', vertical_alignment = 'bottom')],
            [sg.Column(botones, justification = 'center', element_justification = 'center', vertical_alignment = 'bottom', pad=((0,150)))]]


    return sg.Window('Inicio', layout = layout, finalize = True, relative_location=(-250, -100))

def agregar_a_la_lista(lista, i, perfil):
    #lista[i]["foto"] = paths.convertir_guardado_para_usar(perfil["foto"], paths.DIR_PROYECTO)
    lista[i]["nick"] = perfil["nick"]
    nombre = 'foto' + perfil['nick'] + '.png'
    guardar_foto = os.path.join(paths.DIR_MINIFOTO, nombre)
    foto = Image.open(perfil['foto'])
    aux = PIL.ImageOps.fit(foto,(175,175))
    aux.save(guardar_foto,'PNG')
    lista[i]['foto'] = guardar_foto 
    
 

def recorrer_json(datos_json, lista):
    """ Esta función recorre una lista de diccionarios y guarda parte de su información en una nueva lista"""    
    if (datos_json != []):
        for i, perfil in enumerate(datos_json):
            agregar_a_la_lista(lista, i, perfil)

def actualizar_perfiles(login, lista, act):
    """ Esta función actualiza el layout de la pantalla de inicio, mostrando otras imagenes y nombres 
        de usuario
      """
    pagina = "Pagina: " + str(int((act/4)+1)) + " /5"
    login['0'].update(image_filename = lista[act]["foto"])
    login['1'].update(image_filename = lista[act+1]["foto"])
    login['2'].update(image_filename = lista[act+2]["foto"])
    login['3'].update(image_filename = lista[act+3]["foto"])
    login['Usuario 0'].update(lista[act]['nick'])
    login['Usuario 1'].update(lista[act+1]['nick'])
    login['Usuario 2'].update(lista[act+2]['nick'])
    login['Usuario 3'].update(lista[act+3]['nick'])
    login['-PAGINAS-'].update(pagina)


# ------------------------------------------ MAIN ------------------------------------------

def main():
    """ En esta función se ejecuta el inicio de la aplicación, que durante un loop infinito va leyendo los
        eventos provocados al interactuar con el mismo. Se crea el encabezado de los logs del sistema en caso de no existir"""
    try:
        archivo = open(paths.DIR_LOGS)
        archivo.close()
    except FileNotFoundError:
        # Crea archivo de logs en caso no existir.
        linea = ['timestamp', 'nick', 'operacion', 'valores', 'textos']
        funciones.crear_archivo_csv(paths.DIR_LOGS, linea)
    

    # Variable que contiene los posibles valores que retorna la funcion login, uno para cada pestaña
    nums = ('0','1','2','3')
    # Apertura del archivo json de usuarios  
    try:
        datos_json = funciones.leer_archivo_json(paths.DIR_USER)
    except FileNotFoundError:      
        #si no esta creado lo inicializa
        funciones.crear_archivo_json(paths.DIR_USER)           
        datos_json = funciones.leer_archivo_json(paths.DIR_USER)                                       
    # Inicia la lista de perfiles a cargar. En la funcion "recorrer_json" se reemplazaran las imagenes por 
    # default por las correspondientes a los perfiles. El limite es de 20 perfiles (5 pestañas)
    imagen_por_defecto = os.path.join(paths.DIR_IMAGENES, 'avatar_inicio.png')
    lista = [{'foto': imagen_por_defecto, 'nick': 'Sin Registrar'} for i in range(0, 20)]
    recorrer_json(datos_json, lista)

    perfil_actual= {}
    act = 0
    login = crear_ventana_inicio(lista)
    login.set_min_size((1024,768))


    while True:
        login, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:
            login.close()
            return perfil_actual
        elif event == '-INICIO-MAS-':
            act = act + 4
            #si llega a el limite (la ultima pantalla) vuelve a la principal
            if(act == 20):                                       
                act = 0
            actualizar_perfiles(login, lista, act)
        elif event == '-INICIO-ATRAS-':
            act = act - 4
            if(act < 0):                                       
                act = 16
            actualizar_perfiles(login, lista, act)
        elif event in nums:
            # En caso de que el perfil seleccionado exista, se cierra la ventana actual y retorna el perfil
            try:
                perfil_actual = datos_json[int(event)+act]
                login.close()
                return perfil_actual
            except IndexError:                                  
                # Si se clickea una posicion sin ningun perfil registrado aparece la opcion de registrarse         
                aux = sg.PopupYesNo('No hay ningun perfil registrado en esta posicion, ¿desea registrar un nuevo perfil?')   
                if aux == 'Yes':
                    login.hide()
                    perfil = registro.registrarse()
                    # Luego de registrar el nuevo usuario, lo agrega al final de la lista y abre la pantalla de 
                    # inicio nuevamente en la primer pagina
                    if (perfil != {}):
                        datos_json = funciones.leer_archivo_json(paths.DIR_USER)
                        tam = len(datos_json) - 1
                        agregar_a_la_lista(lista, tam, perfil)
                    login.un_hide()
                    act = 0
                    actualizar_perfiles(login, lista, act)