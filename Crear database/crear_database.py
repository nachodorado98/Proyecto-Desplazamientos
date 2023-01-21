#Importamos la libreria os y la libreria pandas
import os
import pandas as pd

#Importamos el modulo creado para las clases de la Base de datos y las tablas
from bbdd_tablas import BaseDatos, Tabla

#Importamos el modulo creado para la configuracion de MySQL
from config import Config

#Ruta donde se encuentran los JSON para las tablas
ruta=os.path.join(os.getcwd(),"JSON_TABLAS")

#Lista con los nombres de los JSON
lista_jsons=os.listdir(ruta)

#Creamos una lista con la ruta completa de cada archivo
lista_rutas=[ruta+"\\"+i for i in lista_jsons]

#Creamos los dataFrames de los JSON
for i in lista_rutas:
    if i.endswith("tabla_competiciones.json"):
        dfcompeticiones=pd.read_json(i)
    elif i.endswith("tabla_equipos.json"):
        dfequipos=pd.read_json(i)
    elif i.endswith("tabla_estadios.json"):
        dfestadios=pd.read_json(i)
    elif i.endswith("tabla_ligas.json"):
        dfligas=pd.read_json(i)
    elif i.endswith("tabla_partidos.json"):
        dfpartidos=pd.read_json(i)
    else:
        pass

configuracion=Config()
conexion=configuracion.crear_conexion()
bbdd=conexion[0]
c=conexion[1]


#--------------------------------------------BASE DE DATOS---------------------------------------
#creacion_bbdd=BaseDatos("pruebas", bbdd, c)
#creacion_bbdd.crear_bbdd()




#--------------------------------------------TABLA LIGAS---------------------------------------
#Creamos un objeto tabla para las ligas
tabla_ligas=Tabla(dfligas,"ligas", "pruebas", bbdd, c)

#Obtenemos los registros en forma de lista
lista_ligas=tabla_ligas.convertir_df_lista()

#Creamos la tabla ligas
consulta_creacion_ligas="""CREATE TABLE ligas 
                            (NombreLiga VARCHAR(50), 
                            MasParticipaciones VARCHAR(70), 
                            Participaciones INT, 
                            MasVictorias VARCHAR(50), 
                            Victorias INT, 
                            MasDerrotas VARCHAR(50), 
                            Derrotas INT,
                            MasGolesPartido INT,
                            MasExpulsado VARCHAR(50),
                            Expulsiones INT,
                            PorteroMasInvicto VARCHAR(50),
                            Minutos INT,
                            MasEntrenados VARCHAR(50),
                            Entrenados INT,
                            PRIMARY KEY (NombreLiga))
                            """
#creacion_tabla_ligas=tabla_ligas.crear_tabla(consulta_creacion_ligas)

#Insertamos los registros en la tabla ligas
consulta_insercion_ligas="""INSERT INTO ligas 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_tabla_ligas=tabla_ligas.insertar_registros(consulta_insercion_ligas, lista_ligas)
