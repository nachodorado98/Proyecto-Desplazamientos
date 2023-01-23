#Importamos la configuracion de MySQL
from config import Config



#Clase para realizar las consultas
class Consulta():
	#Creamos la conexion con la BBDD
	conexion=Config().crear_conexion()
	bbdd=conexion[0]
	cursor=conexion[1]

	#Funcion que nos permite obtener los desplazamientos cruzados con otras tablas
	def consulta_desplazamientos(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT d.CodDesplazamiento, p.Equipo, p.Fecha, e.Ciudad
                 				FROM desplazamientos d
                 				JOIN partidos p
                 				ON d.CodPartido=p.CodPartido
                 				JOIN estadios e
                 				ON p.CodEstadio=e.CodEstadio""")
		return self.cursor.fetchall()


	#Funcion que nos permite, insertando la fecha del ultimo partido ido, obtener los partidos que se han disputado despues FUERA DE CASA (codigo del metropolitano 2830)
	def consulta_partidos(self, fecha_ultimo_partido):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT Fecha, Equipo
                 				FROM partidos 
                 				WHERE CodEstadio != 2830
                 				AND Fecha>%s
                 				ORDER BY Fecha""",
                 				(fecha_ultimo_partido,))
		
		return self.cursor.fetchall()


	#Funcion que nos devuelve la fecha del ultimo partido ido cruzando la tabla de desplazamientos con la de los partidos
	def fecha_ultimo_partido_ido(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT max(Fecha)
			FROM partidos p
            JOIN desplazamientos d
            ON p.CodPartido=d.CodPartido""")
		fecha=self.cursor.fetchall()
		#Le damos formato de fecha
		try:
			return fecha[0][0].strftime("%Y-%m-%d")
		#Si aun no hay ningun desplazamiento, para que te devuelva una fecha en vez de None, ponemos una fecha por defecto (anterior a cualquier partido disputado de esta temporada)
		except:
			return "2022-01-01"


	#Funcion que nos permite obtener el codigo del partido a traves de la fecha y el equipo
	def obtener_codigo_partido(self, fecha, equipo):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT CodPartido
                				FROM partidos 
                 				WHERE Fecha=%s and Equipo=%s""",
             				(fecha, equipo))

		codigopartido=self.cursor.fetchone()
		return codigopartido[0]


	#Funcion que nos permite insertar los desplazamientos en la tabla
	def insertar_desplazamiento(self, codigo, ida, vuelta, acompanante, transporte):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""INSERT INTO desplazamientos 
								VALUES(%s,%s,%s,%s,%s,%s)""",
								(None,codigo,ida,vuelta,acompanante,transporte))

		self.bbdd.commit()
		#print(str(codigo)+" "+ida+" "+vuelta+" "+acompanante+" "+transporte)

		