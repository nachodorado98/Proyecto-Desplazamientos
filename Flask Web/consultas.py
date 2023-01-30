#Importamos la configuracion de MySQL
from config import Config
#Importamos datetime para tratar las fechas
from datetime import datetime, date


#Clase para realizar las consultas
class Consulta():
	#Creamos la conexion con la BBDD
	conexion=Config().crear_conexion()
	bbdd=conexion[0]
	cursor=conexion[1]

	#Funcion que nos permite obtener los desplazamientos cruzados con otras tablas
	def consulta_desplazamientos(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT d.CodDesplazamiento, d.FechaIda, d.FechaVuelta, p.Equipo, d.Acompañamiento, d.Transporte 
                    		FROM desplazamientos d
                    		JOIN partidos p
                    		ON d.CodPartido=p.CodPartido""")
		consulta=self.cursor.fetchall()
		return [i.strftime("%d/%m/%Y") if isinstance(i, datetime) else i for i in consulta]

	#Funcion que nos permite obtener todos los partidos disputados del Atletico de Madrid
	def consulta_partidos_atm(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT p.ATM, p.Resultado, p.Equipo, p.Fecha, p.Hora, p.Arbitro, e.Nombre, c.Competicion, c.Temporada
                    		FROM estadios e
                    		JOIN partidos p
                    		ON e.CodEstadio=p.CodEstadio
                    		JOIN competiciones c
                    		ON p.CodCompeticion=c.CodCompeticion
                    		ORDER BY Fecha""")
		return self.cursor.fetchall()

	#Funcion que nos permite obtener los puntos del mapa
	def puntos_mapa(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT e.Latitud, e.Longitud, d.CodDesplazamiento, e.Ciudad, d.FechaIda, d.FechaVuelta, e.Pais
                   FROM desplazamientos d
                   JOIN partidos p
                   ON d.CodPartido=p.CodPartido
                   JOIN estadios e
                   ON e.CodEstadio=p.CodEstadio""")

		return self.cursor.fetchall()

	#Funcion que nos permite obtener el desplazamiento seleccionado en detalle
	def detalle_desplazamiento(self, codigo):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT p.Equipo, e.Pais, e.Nombre, e.Ciudad, e.Longitud, e.Latitud, d.FechaIda, d.FechaVuelta, d.Acompañamiento, d.Transporte
                 FROM partidos p
                 JOIN estadios e
                 ON p.CodEstadio=e.CodEstadio
                 JOIN desplazamientos d
                 ON d.CodPartido=p.CodPartido
                 WHERE CodDesplazamiento=%s""",
                 (codigo,))
		
		return self.cursor.fetchall()

	#Funcion para obtener la fecha del ultimo desplazamiento
	def fecha_ultimo_deplazamiento(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT max(Fecha)
                 FROM partidos p
                 JOIN desplazamientos d
                 ON p.CodPartido=d.CodPartido""")
		
		#Intenta devolver la fecha del ultimo desplazamiento
		try:
			return self.cursor.fetchall()[0][0].strftime("%Y-%m-%d")

		#Si aun no hay ningun desplazamiento, para que te devuelva una fecha en vez de None, ponemos una fecha por defecto (anterior a cualquier partido disputado de esta temporada)
		except:
			return "2022-01-01"

	#Funcion que nos permite obtener los partidos visitante
	def partidos_visitante(self, fecha):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT Fecha, Equipo
                 FROM partidos 
                 WHERE CodEstadio != 2830
                 AND Fecha>%s
                 ORDER BY Fecha""",
                 (fecha,))
		
		return self.cursor.fetchall()

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
		

		

#Clase para realizar las consultas de estadistica
class Estadistica(Consulta):

	#Funcion que nos permite obtener los nombres de los estadios de manera unica en donde se han jugado a excepcion del Metropolitano
	def estadios_jugados(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT DISTINCTROW(e.Nombre)
                 FROM partidos p
                 JOIN estadios e
                 ON p.CodEstadio=e.CodEstadio
                 WHERE e.Nombre!='Wanda Metropolitano'
                 ORDER BY e.Nombre""")

		return self.cursor.fetchall()

	#Funcion que nos permite obtener los nombres de los estadios que se han visitado de manera unica
	def estadios_visitados(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT DISTINCTROW(e.Nombre)
                 FROM partidos p
                 JOIN estadios e
                 ON p.CodEstadio=e.CodEstadio
                 JOIN desplazamientos d
                 ON d.CodPartido=p.CodPartido
                 ORDER BY e.Nombre""")

		return self.cursor.fetchall()

	#Funcion que nos permite obtener el estadio mas visitado y el numero de veces
	def mas_visitado(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT e.Nombre, COUNT(e.Nombre) as NumeroVeces
                 FROM partidos p
                 JOIN estadios e
                 ON p.CodEstadio=e.CodEstadio
                 JOIN desplazamientos d
                 ON d.CodPartido=p.CodPartido
                 GROUP BY e.Nombre
                 ORDER BY NumeroVeces""")

		return self.cursor.fetchall()

	#Funcion que nos permite obtener el estadio mas grande y su capacidad (de los visitados)
	def mas_grande(self):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT e.Nombre, MAX(e.Capacidad)
                 FROM partidos p
                 JOIN estadios e
                 ON p.CodEstadio=e.CodEstadio
                 JOIN desplazamientos d
                 ON d.CodPartido=p.CodPartido""")

		return self.cursor.fetchall()


	