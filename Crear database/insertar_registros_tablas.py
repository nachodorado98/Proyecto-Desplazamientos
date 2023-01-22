from config import Config
from bbdd_tablas import Tabla
import pandas as pd

nombre_bbdd="futbol"
configuracion=Config().crear_conexion()
bbdd=configuracion[0]
c=configuracion[1]


#Funcion que nos devuelve la fecha del ultimo partido insertado
def fecha_maxima(bbdd, c):
    c.execute("""USE futbol""")
    c.execute("""SELECT max(Fecha)FROM partidos""")
    fechas_dt=c.fetchall()
    fecha=fechas_dt[0][0].strftime("%Y-%m-%d")
    return fecha


#Funcion que nos devuelve los partidos que se pueden insertar en funcion de la fecha del ultimo insertado
def partidos_a_insertar(df_partidos, fecha):
	df=df_partidos.copy()
	df_insertar=df[df["Fecha"]>fecha]
	lista=df_insertar.values.tolist()
	return lista


#-------------------------------------------------------Insertar en tabla ligas
ligas=Tabla("ligas", nombre_bbdd, bbdd, c)
#NombreLiga, MasParticipaciones, Participaciones, MasVictorias, Victorias, MasDerrotas, Derrotas, MasGolesPartido, MasExpulsado, Expulsiones, PorteroMasInvicto, Minutos, MasEntrenados, Entrenados
registro_ligas=[]
consulta_insertar_ligas="""INSERT INTO ligas 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_ligas=ligas.insertar_registros(consulta_insertar_ligas, [registro_ligas])



#--------------------------------------------------------Insertar en tabla competiciones
competiciones=Tabla("competiciones", nombre_bbdd, bbdd, c)
#CodCompeticion, Competicion, Temporada, NumeroEquipos, Campeon, Pichichi, Goles
registro_competiciones=[]
consulta_insertar_competiciones="""INSERT INTO competiciones 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_competiciones=competiciones.insertar_registros(consulta_insertar_competiciones, [registro_competiciones])



#--------------------------------------------------------Insertar en tabla estadios
estadios=Tabla("estadios", nombre_bbdd, bbdd, c)
#CodEstadio (None), Nombre, Pais, Ciudad, Latitud, Longitud, Capacidad
registro_estadios=[]
consulta_insertar_estadios="""INSERT INTO estadios 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_estadios=estadios.insertar_registros(consulta_insertar_estadios, [registro_estadios])



#--------------------------------------------------------Insertar en tabla equipos
equipos=Tabla("equipos", nombre_bbdd, bbdd, c)
#NombreEquipo, Codigo, Pais, CodEstadio, Fundacion, Ligasnacionales, Champions, MaximoGoleador, Goles, MaximoApariciones, Partidos
registro_equipos=[]
consulta_insertar_equipos="""INSERT INTO equipos 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_equipos=equipos.insertar_registros(consulta_insertar_equipos, [registro_equipos])



#--------------------------------------------------------Insertar en tabla partidos
#Obtenemos la fecha del ultimo partido insertado
fecha_ultimo_partido=fecha_maxima(bbdd, c)
#Leemos el excel con los partidos
df_partidos=pd.read_excel("partidos.xlsx")
#Obtenemos los partidos que se pueden insertar teniendo en cuenta la fecha del ultimo insertado
partidos_insertar=partidos_a_insertar(df_partidos, fecha_ultimo_partido)

#Si hay partidos jugados que superen la fecha del ultimo insertado
if partidos_insertar!=[]:
	for i in partidos_insertar:
		i.insert(0, None)
	print(partidos_insertar)
	partidos=Tabla("partidos", nombre_bbdd, bbdd, c)
	consulta_insertar_partidos="""INSERT INTO partidos 
	VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	#Preguntamos por pantalla si estamos seguros de insertarlos
	respuesta=input("¿Quieres insertar los partidos? Si o No\n")
	if respuesta.lower()=="si":
		#Insertamos los partidos en la tabla partidos
		insertar_partidos=partidos.insertar_registros(consulta_insertar_partidos, partidos_insertar)
		print("Se han insertado los partidos")
	else:
		print("No se han insertado los partidos")
else:
	print("No hay partidos para insertar")



#--------------------------------------------------------Insertar en tabla deslazamientos
#Los registros de esta tabla se insertan a partir de la interfaz grafica


