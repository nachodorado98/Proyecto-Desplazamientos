#Importamos re para las regex
import re
#Importamos la libreria que nos permite enviar correos
import smtplib
#Importamos la configuracion de MySQL
from config import Config
import os


#Clase para realizar las consultas del administrador
class Administrador():
	#Creamos la conexion con la BBDD
	conexion=Config().crear_conexion()
	bbdd=conexion[0]
	cursor=conexion[1]

	#Funcion para comprobar el usuario y la contraseña
	def comprobacion(self, usuario, contrasena):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT Usuario, Contrasena, Nombre
                    		FROM usuarios
                    		WHERE Usuario=%s
                    		AND Contrasena=%s""",
                    		(usuario, contrasena))

		return self.cursor.fetchall()

	#Funcion para saber si los datos son validos para poder crear un nuevo usuario
	def registro_valido(self, nombre, usuario, contrasena, correo):

		#Patron nombre (solo letras)
		patron_nombre=r"[a-zA-Z]{3,20}"
		#Patron usuario (letras, numeros o caracteres especiales desde 5 hasta 25)
		patron_usuario=r"[\w]{5,25}"
		#Patron contraseña (debe empezar por un numero o letra y luego letras, numeros o caracteres desde 7 hasta 31)
		patron_contrasena=r"^[a-zA-Z0-9][\w\$\%\&\S]{7,31}"
		#Patron correo (debe empezar por una letra y luego letras, numeros o caracteres pero no espacio desde 2 hasta infinito, luego @, luego letras minusculas o punto de 3 hasta infinito, luego punto y por ultimo letras minusculas de 2 a 3)
		patron_correo=r"^[a-zA-Z][\w\S]{2,}@[a-z\.]{3,}\.[a-z]{2,3}"

		#Si el nombre no es solo letras devuelve False
		if re.search(patron_nombre, nombre, re.IGNORECASE)==None:
			return False
		#Si el usuario no cumple su patron devuelve False
		elif re.search(patron_usuario, usuario, re.IGNORECASE)==None:
			return False
		#Si la contraseña no cumple su patron devuelve False
		elif re.search(patron_contrasena, contrasena, re.IGNORECASE)==None:
			return False
		#Si el correo no cumple su patron devuelve False
		elif re.search(patron_correo, correo, re.IGNORECASE)==None:
			return False
		#Si todos se cumplen devuelve True
		else:
			return True

	#Funcion para saber que no hay ya un usuario o correo igual
	def comprobacion_duplicados(self, usuario, correo):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""SELECT Usuario, Email
                    FROM usuarios
                    WHERE Usuario=%s
                    OR Email=%s""",
                    (usuario, correo))

		if self.cursor.fetchall()==[]:
			return True
		else:
			return False

	#Funcion para insertar un nuevo usuario en la tabla usuarios
	def insertar_usuario(self, usuario, contrasena, nombre, correo):
		self.cursor.execute("""USE futbol""")
		self.cursor.execute("""INSERT INTO usuarios VALUES(%s,%s,%s,%s,%s)""",
                    		(None,usuario, contrasena, nombre, correo))
		self.bbdd.commit()

	#Funcion para enviar el correo de confirmacion
	def enviar_correo(self, nombre, usuario, correo):
		#Obtenemos el valor de las variables de entorno del correo y la contraseña
		correo_atm=os.environ.get("CORREO_ATM")
		contrasena_atm=os.environ.get("CONTRASENA_ATM")
		mensaje=f"""From:{correo_atm}
		To:{correo}
		Subject:SUBSCRIPCION ATM ON TOUR\n
		Bienvenido {nombre}!
		Te has subscrito a la pagina web con el nombre de usuario: {usuario}
		"""
		#Intentamos enviar el correo
		try:
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.starttls()
			server.login(correo_atm, contrasena_atm)
			server.sendmail(correo_atm, correo, mensaje)
			return True
		except:
			return False



    

