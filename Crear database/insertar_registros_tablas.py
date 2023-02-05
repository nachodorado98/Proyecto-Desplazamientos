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


#Funcion que nos devuelve el codigo maximo
def maximo_codigo(bbdd, c):
    c.execute("""USE futbol""")
    c.execute("""SELECT max(CodCompeticion) FROM competiciones""")
    return c.fetchone()

#-------------------------------------------------------Insertar en tabla ligas
ligas=Tabla("ligas", nombre_bbdd, bbdd, c)
#NombreLiga, MasParticipaciones, Participaciones, MasVictorias, Victorias, MasDerrotas, Derrotas, MasGolesPartido, MasExpulsado, Expulsiones, PorteroMasInvicto, Minutos, MasEntrenados, Entrenados
registro_ligas=[]
consulta_insertar_ligas="""INSERT INTO ligas 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_ligas=ligas.insertar_registros(consulta_insertar_ligas, [registro_ligas])



#--------------------------------------------------------Insertar en tabla competiciones
#Leemos el excel con las competiciones y los obtenemos ne forma de lista
df_competiciones=pd.read_excel("competiciones.xlsx").fillna("NULL")
lista_competiciones=df_competiciones.values.tolist()
#Comprobamos que el campeon ya esta definido (que ese campo no es NULL) en TODAS las competiciones
if lista_competiciones[0][4]!="NULL" and lista_competiciones[1][4]!="NULL" and lista_competiciones[2][4]!="NULL":
	print(lista_competiciones)
	competiciones=Tabla("competiciones", nombre_bbdd, bbdd, c)
	#Preguntamos por pantalla si estamos seguros de insertarlos
	respuesta=input("¿Quieres actualizar las competiciones? Si o No\n")
	if respuesta.lower()=="si":
		consulta_actualizar_competiciones="""UPDATE competiciones SET Campeon=%s, Pichichi=%s, Goles=%s
		WHERE CodCompeticion=%s"""
		consulta_insertar_competiciones="""INSERT INTO competiciones 
		VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		#Actualizamos e insertamos una nueva temporada en cada competicion
		for i in range(len(lista_competiciones)):
			#Actualizamos el campeon, pichichi y los goles de las competiciones
			competiciones.actualizar_registro(consulta_actualizar_competiciones, [lista_competiciones[i][4],lista_competiciones[i][5],lista_competiciones[i][6],lista_competiciones[i][7]])
			#Obtenemos el codigo maximo que se haya insertado
			codigo_maximo=maximo_codigo(bbdd, c)
			#Aumentamos en uno la temporada siguiente
			temporada_nueva=[str(int(i)+1) for i in lista_competiciones[i][2].split("-")]
			#Insertamos un nuevo registro poniendo el codigo de la competicion uno mas que el maximo que ya teniamos (ya que no es AUTO_INCREMENT)
			lista_insertar=[codigo_maximo[0]+1, lista_competiciones[i][1], "-".join(temporada_nueva), lista_competiciones[i][3], "Nada", "Nada", 0]
			competiciones.insertar_registros(consulta_insertar_competiciones,[lista_insertar])
			print(lista_insertar)

		print("Se han acttualizado las competiciones")
	else:
		print("No se han actualizado las competiciones")
else:
	print("No hay competiciones para insertar")


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
	#Agregamos a cada partido un campo inicial de None para luego insertar en la tabla ya que es AUTO_INCREMENT
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


#--------------------------------------------------------Insertar en tabla usuarios
#Los registros de esta tabla se insertan a partir de la interfaz grafica

