from config import Config
from bbdd_tablas import Tabla

nombre_bbdd="futbol"
configuracion=Config().crear_conexion()
bbdd=configuracion[0]
c=configuracion[1]

#Insertar en tabla ligas
ligas=Tabla("ligas", nombre_bbdd, bbdd, c)
#NombreLiga, MasParticipaciones, Participaciones, MasVictorias, Victorias, MasDerrotas, Derrotas, MasGolesPartido, MasExpulsado, Expulsiones, PorteroMasInvicto, Minutos, MasEntrenados, Entrenados
registro_ligas=[]
consulta_insertar_ligas="""INSERT INTO ligas 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_ligas=ligas.insertar_registros(consulta_insertar_ligas, [registro_ligas])


#Insertar en tabla competiciones
competiciones=Tabla("competiciones", nombre_bbdd, bbdd, c)
#CodCompeticion, Competicion, Temporada, NumeroEquipos, Campeon, Pichichi, Goles
registro_competiciones=[]
consulta_insertar_competiciones="""INSERT INTO competiciones 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_competiciones=competiciones.insertar_registros(consulta_insertar_competiciones, [registro_competiciones])


#Insertar en tabla estadios
estadios=Tabla("estadios", nombre_bbdd, bbdd, c)
#CodEstadio (None), Nombre, Pais, Ciudad, Latitud, Longitud, Capacidad
registro_estadios=[]
consulta_insertar_estadios="""INSERT INTO estadios 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_estadios=estadios.insertar_registros(consulta_insertar_estadios, [registro_estadios])


#Insertar en tabla equipos
equipos=Tabla("equipos", nombre_bbdd, bbdd, c)
#NombreEquipo, Codigo, Pais, CodEstadio, Fundacion, Ligasnacionales, Champions, MaximoGoleador, Goles, MaximoApariciones, Partidos
registro_equipos=[]
consulta_insertar_equipos="""INSERT INTO equipos 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_equipos=equipos.insertar_registros(consulta_insertar_equipos, [registro_equipos])


#Insertar en tabla partidos



