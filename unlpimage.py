import pantallas.inicio
import pantallas.menu
# Recibe un perfil de la pantalla de inicio. En caso de que exista, lo envia al menu principal.
# Si el usuario elige Cerrar Sesión se vuelve a iniciar el proceso
continuar = True
while (continuar == True):
    perfil = pantallas.inicio.main()
    if (perfil != {}):
        continuar = pantallas.menu.main(perfil)
    else:
        continuar = False
