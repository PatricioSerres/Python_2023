import os.path

DIR_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def convertir_para_guardar(path, path_proyecto):
    """ Esta función retorna un path relativo para guardar, usando como separador '/'. 
        Recibe como parametros el path del proyecto y el path absoluto del archivo que se va a guardar"""
    path_relativo = os.path.relpath(path, start=path_proyecto)
    path_generico = path_relativo.replace(os.path.sep, "/")
    return path_generico

def convertir_guardado_para_usar(path, path_proyecto):
    """ Esta función retorna un path absoluto empleando como separador el correspondiente al sistema.
        Recibo como parametros el path absoluto del directorio del proyecto y el path relativo del archivo a usar"""
    path_del_sistema = path.replace("/", os.path.sep)
    path_absoluto = os.path.abspath(os.path.join(path_proyecto, path_del_sistema))
    return path_absoluto

DIR_CONFIGURACION = convertir_guardado_para_usar("archivos/archivo_configuracion.csv", DIR_PROYECTO)
DIR_LOGS = convertir_guardado_para_usar("archivos/logs.csv", DIR_PROYECTO)
DIR_ETIQUETAR = convertir_guardado_para_usar("archivos/archivo_etiquetar.csv", DIR_PROYECTO)
DIR_AVATARES = convertir_guardado_para_usar('imagenes/avatares',DIR_PROYECTO)
DIR_IMAGENES = convertir_guardado_para_usar("imagenes", DIR_PROYECTO)
DIR_MINIFOTO = convertir_guardado_para_usar('imagenes/mini_fotos', DIR_PROYECTO)
DIR_USER = convertir_guardado_para_usar("archivos/user.json", DIR_PROYECTO)
DIR_TEMPLATE_MEME = convertir_guardado_para_usar("archivos/template_meme.json", DIR_PROYECTO)
DIR_FUENTES = convertir_guardado_para_usar('fuentes', DIR_PROYECTO)
DIR_TEMPLATE_COLLAGE_1 = convertir_guardado_para_usar('imagenes/opciones/opcion1.png', DIR_PROYECTO)
DIR_TEMPLATE_COLLAGE_2 = convertir_guardado_para_usar('imagenes/opciones/opcion2.png', DIR_PROYECTO)
DIR_TEMPLATE_COLLAGE_3 = convertir_guardado_para_usar('imagenes/opciones/opcion3.png', DIR_PROYECTO)
DIR_TEMPLATE_COLLAGE_4 = convertir_guardado_para_usar('imagenes/opciones/opcion4.png', DIR_PROYECTO)

