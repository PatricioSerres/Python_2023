import pantallas.INICIO
import pantallas.menu

perfil = pantallas.INICIO.main()
if perfil != []:
    pantallas.menu.main(perfil)