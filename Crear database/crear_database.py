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
    else:
        pass

#Creamos la conexion con MySQL
configuracion=Config()
conexion=configuracion.crear_conexion()
bbdd=conexion[0]
c=conexion[1]


#--------------------------------------------BASE DE DATOS---------------------------------------
nombre_bbdd="futbol"
#creacion_bbdd=BaseDatos(nombre_bbdd, bbdd, c)
#creacion_bbdd.crear_bbdd()


#--------------------------------------------TABLA LIGAS---------------------------------------
#Creamos un objeto tabla para las ligas
tabla_ligas=Tabla("ligas", nombre_bbdd, bbdd, c, dfligas)

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


#--------------------------------------------TABLA COMPETICIONES---------------------------------------
#Creamos un objeto tabla para las competiciones
tabla_competiciones=Tabla("competiciones", nombre_bbdd, bbdd, c, dfcompeticiones)

#Obtenemos los registros en forma de lista
lista_competiciones=tabla_competiciones.convertir_df_lista()

#Creamos la tabla competiciones
consulta_creacion_competiciones="""CREATE TABLE competiciones 
(CodCompeticion INT, 
Competicion VARCHAR(70), 
Temporada VARCHAR(50), 
NumeroEquipos INT, 
Campeon VARCHAR(50), 
Pichichi VARCHAR(50), 
Goles INT, 
PRIMARY KEY (CodCompeticion),
FOREIGN KEY (Competicion) REFERENCES ligas (NombreLiga) ON DELETE CASCADE)
"""

#creacion_tabla_competiciones=tabla_competiciones.crear_tabla(consulta_creacion_competiciones)

#Insertamos los registros en la tabla competiciones
consulta_insercion_competiciones="""INSERT INTO competiciones 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_tabla_competiciones=tabla_competiciones.insertar_registros(consulta_insercion_competiciones, lista_competiciones)


#--------------------------------------------TABLA ESTADIOS---------------------------------------
#Creamos un objeto tabla para los estadios
tabla_estadios=Tabla("estadios", nombre_bbdd, bbdd, c, dfestadios)

#Obtenemos los registros en forma de lista
lista_estadios=tabla_estadios.convertir_df_lista()

#Ponemos la posicion donde iria el codigo como None
for i in lista_estadios:
    i[0]=None

#Creamos la tabla ligas
consulta_creacion_estadios="""CREATE TABLE estadios 
                                (CodEstadio INT AUTO_INCREMENT, 
                                Nombre VARCHAR(70), 
                                Pais VARCHAR(50), 
                                Ciudad VARCHAR(50), 
                                Latitud FLOAT, 
                                Longitud FLOAT, 
                                Capacidad VARCHAR(50), 
                                PRIMARY KEY (CodEstadio))
                                """

#creacion_tabla_estadios=tabla_estadios.crear_tabla(consulta_creacion_estadios)

#Insertamos los registros en la tabla estadios
consulta_insercion_estadios="""INSERT INTO estadios 
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
#insertar_tabla_estadios=tabla_estadios.insertar_registros(consulta_insercion_estadios, lista_estadios)


#--------------------------------------------TABLA EQUIPOS---------------------------------------
#Creamos un objeto tabla para las equipos
tabla_equipos=Tabla("equipos", nombre_bbdd, bbdd, c, dfequipos)

#Obtenemos los registros en forma de lista
lista_equipos=tabla_equipos.convertir_df_lista()

#Creamos la tabla equipos
consulta_creacion_equipos="""CREATE TABLE equipos 
(NombreEquipo VARCHAR(50), 
Codigo VARCHAR(6), 
Pais VARCHAR(50), 
CodEstadio INT, 
Fundacion DATE, 
LigasNacionales INT, 
Champions INT, 
MaximoGoleador VARCHAR(50), 
Goles INT, 
MaximoApariciones VARCHAR(50), 
Partidos INT, 
PRIMARY KEY (NombreEquipo), 
FOREIGN KEY (CodEstadio) REFERENCES estadios (CodEstadio) ON DELETE CASCADE)"""

#creacion_tabla_equipos=tabla_equipos.crear_tabla(consulta_creacion_equipos)

#Insertamos los registros en la tabla equipos
consulta_insercion_equipos="""INSERT INTO equipos 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#insertar_tabla_equipos=tabla_equipos.insertar_registros(consulta_insercion_equipos, lista_equipos)


#--------------------------------------------TABLA PARTIDOS---------------------------------------
#Creamos un objeto tabla para los partidos
tabla_partidos=Tabla("partidos", nombre_bbdd, bbdd, c)

#Creamos la tabla partidos
consulta_creacion_partidos="""CREATE TABLE partidos 
(CodPartido INT AUTO_INCREMENT, 
Fecha DATE, 
Hora VARCHAR(50), 
ATM VARCHAR(50),
Resultado VARCHAR(50),
Equipo VARCHAR(50),
Arbitro VARCHAR(50),
CodEstadio INT,
CodCompeticion INT,
PRIMARY KEY (CodPartido),
FOREIGN KEY (Equipo) REFERENCES equipos (NombreEquipo) ON DELETE CASCADE,
FOREIGN KEY (CodEstadio) REFERENCES estadios (CodEstadio) ON DELETE CASCADE,
FOREIGN KEY (CodCompeticion) REFERENCES competiciones (CodCompeticion))"""

creacion_tabla_partidos=tabla_partidos.crear_tabla(consulta_creacion_partidos)


#--------------------------------------------TABLA DESPLAZAMIENTOS---------------------------------------
#Creamos un objeto tabla para los desplazamientos
tabla_desplazamientos=Tabla("desplazamientos", nombre_bbdd, bbdd, c)

#Creamos la tabla desplazamientos
consulta_creacion_desplazamientos="""CREATE TABLE desplazamientos 
(CodDesplazamiento INT AUTO_INCREMENT,
CodPartido INT,
FechaIda DATE,
FechaVuelta DATE,
Acompañamiento VARCHAR(50), 
Transporte VARCHAR(50),
PRIMARY KEY (CodDesplazamiento),
FOREIGN KEY (CodPartido) REFERENCES partidos (CodPartido) ON DELETE CASCADE)"""

creacion_tabla_desplazamientos=tabla_desplazamientos.crear_tabla(consulta_creacion_desplazamientos)