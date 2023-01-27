#Importamos mysql para poder trabajar con la base de datos
import mysql.connector

class Config():
	def crear_conexion(self):
		#Creamos la conexion con msql
		bbdd=mysql.connector.connect(host="localhost", user="root", passwd="root")
		#Creamos un cursor
		c=bbdd.cursor()
		return bbdd, c 