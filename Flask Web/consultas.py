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


	