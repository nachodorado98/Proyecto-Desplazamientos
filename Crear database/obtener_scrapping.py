#Importamos la libreria requests
import requests
#Importamos la libreria pandas
import pandas as pd
#Importamos la clase Config
from config import Config
#Importamos la clase Scrapper
from scrappeador import Scrapper
#Importamos las clases CrearDataframe y Definitivo
from trans_df import CrearDataframe, Definitivo


#-----------------------------------------------------------------------------CONSULTAS
#Consulta que nos devuelve los equipos con su codigo de estadio
def consulta_equipos(bbdd, c):
    c.execute("""USE futbol""")
    c.execute("""SELECT NombreEquipo, CodEstadio FROM equipos""")
    return c.fetchall()

#Consulta para obterner el codigo maximo de una competicion especifica
def maximo_codigo(bbdd, c, competicion):
    c.execute("""USE futbol""")
    c.execute("""SELECT MAX(CodCompeticion)
                FROM competiciones
                WHERE Competicion=%s""",
                (competicion,))
    return c.fetchone()

#Consulta que devuelve los datos de la competicion segun codigo especifico
def datos_con_codigo_maximo(bbdd, c, codigo):
    c.execute("""USE futbol""")
    c.execute("""SELECT Competicion, Temporada
                FROM competiciones
                WHERE CodCompeticion=%s""",
                (codigo,))
    return c.fetchone()
    

#-------------------------------------------------------------------------------------------BBDD
#Creamos la conexiona a MySQL
configuracion=Config().crear_conexion()
bbdd=configuracion[0]
c=configuracion[1]


#------------------------------------------------------------------------------------------COMPETICIONES
#Scrappeamos el campeon de la liga si ya estuviera
datos_laliga=Scrapper(requests.get("https://fbref.com/en/comps/12/history/La-Liga-Seasons")).obtener_datos_temporadas_liga()
#Creamos un dataframe con los datos scrappeados
liga_scrapp_df=CrearDataframe().crear_dataframe_competiciones(datos_laliga)
#Obtenemos el codigo maximo de la competicion La Liga
maximo_codigo_laliga=maximo_codigo(bbdd, c, "La Liga")
#Obtenemos la competicion y la temporada con el codigo maximo (la ultima que esta registrada)
competicion_temporada_maximas_liga=datos_con_codigo_maximo(bbdd, c, maximo_codigo_laliga[0])
#Identificamos la ultima temporada registrada de La Liga con los datos del scrappeo y le agregamos el codigo maximo
registro_posible_insercion_liga=liga_scrapp_df[(liga_scrapp_df["Competicion"]==competicion_temporada_maximas_liga[0])&(liga_scrapp_df["Temporada"]==competicion_temporada_maximas_liga[1])]
registro_posible_insercion_liga_copia=registro_posible_insercion_liga.copy()
registro_posible_insercion_liga_copia["CodCompeticion"]=maximo_codigo_laliga[0]

#Scrappeamos el campeon de la champions si ya estuviera
datos_champions=Scrapper(requests.get("https://fbref.com/en/comps/8/history/Champions-League-Seasons")).obtener_datos_temporadas_champions_copa()
#Creamos un dataframe con los datos scrappeados
champions_scrapp_df=CrearDataframe().crear_dataframe_competiciones(datos_champions)
#Obtenemos el codigo maximo de la competicion UEFA Champions League
maximo_codigo_champions=maximo_codigo(bbdd, c, "UEFA Champions League")
#Obtenemos la competicion y la temporada con el codigo maximo (la ultima que esta registrada)
competicion_temporada_maxima_champions=datos_con_codigo_maximo(bbdd, c, maximo_codigo_champions[0])
#Identificamos la ultima temporada registrada de UEFA Champions League con los datos del scrappeo y le agregamos el codigo maximo
registro_posible_insercion_champions=champions_scrapp_df[(champions_scrapp_df["Competicion"]==competicion_temporada_maxima_champions[0])&(champions_scrapp_df["Temporada"]==competicion_temporada_maxima_champions[1])]
registro_posible_insercion_champions_copia=registro_posible_insercion_champions.copy()
registro_posible_insercion_champions_copia["CodCompeticion"]=maximo_codigo_champions[0]

#Scrappeamos el campeon de la copa del rey si ya estuviera
datos_copa=Scrapper(requests.get("https://fbref.com/en/comps/569/history/Copa-del-Rey-Seasons")).obtener_datos_temporadas_champions_copa()
#Creamos un dataframe con los datos scrappeados
copa_scrapp_df=CrearDataframe().crear_dataframe_competiciones(datos_copa)
#Obtenemos el codigo maximo de la competicion Copa del Rey
maximo_codigo_copa=maximo_codigo(bbdd, c, "Copa del Rey")
#Obtenemos la competicion y la temporada con el codigo maximo (la ultima que esta registrada)
competicion_temporada_maxima_copa=datos_con_codigo_maximo(bbdd, c, maximo_codigo_copa[0])
#Identificamos la ultima temporada registrada de Copa del Rey con los datos del scrappeo y le agregamos el codigo maximo
registro_posible_insercion_copa=copa_scrapp_df[(copa_scrapp_df["Competicion"]==competicion_temporada_maxima_copa[0])&(copa_scrapp_df["Temporada"]==competicion_temporada_maxima_copa[1])]
registro_posible_insercion_copa_copia=registro_posible_insercion_copa.copy()
registro_posible_insercion_copa_copia["CodCompeticion"]=maximo_codigo_copa[0]


#Concatenamos los dfs de las 3 competiciones y devolvemos un excel
concatenar_competiciones=Definitivo()
concatenar_competiciones.excel(concatenar_competiciones.concatenar([registro_posible_insercion_liga_copia, registro_posible_insercion_champions_copia, registro_posible_insercion_copa_copia]), "competiciones")



#--------------------------------------------------------------------------------------------PARTIDOS
#Llamamos a la funcion para obtener los equipos y su codigo de estadio
equipos=consulta_equipos(bbdd, c)

#Scrappeamos los partidos de liga
lista_liga=Scrapper(requests.get("https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures")).scrappeo_liga()
#Creamos el dataframe de la liga con los partidos
codigo_liga=maximo_codigo_laliga[0]
liga=CrearDataframe(codigo_liga)
df_liga=liga.crear_dataframe(lista_liga)
#Añadimos el codigo del estadio a los partidos
df_liga_codestadio=liga.anadir_codestadio(df_liga, equipos)


#Scrappeamos los partidos de champions
lista_champions=Scrapper(requests.get("https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures")).scrappeo_champions()
#Creamos el dataframe de la champions con los partidos
codigo_champions=maximo_codigo_champions[0]
champions=CrearDataframe(codigo_champions)
df_champions=champions.crear_dataframe(lista_champions)
#Añadimos el codigo del estadio a los partidos
df_champions_codestadio=champions.anadir_codestadio(df_champions, equipos)


#Scrappeamos los partidos de copa
lista_copa=Scrapper(requests.get("https://fbref.com/en/comps/569/schedule/Copa-del-Rey-Scores-and-Fixtures")).scrappeo_copa()
#Creamos el dataframe de la copa con los partidos
codigo_copa=maximo_codigo_copa[0]
copa=CrearDataframe(codigo_copa)
df_copa=copa.crear_dataframe(lista_copa)
#Añadimos el codigo del estadio a los partidos
df_copa_codestadio=copa.anadir_codestadio(df_copa, equipos)


#Concatenamos los dfs de las 3 competiciones
concatenacion=Definitivo()
df_concatenado=concatenacion.concatenar([df_liga_codestadio, df_copa_codestadio, df_champions_codestadio])
#Transformamos el df para que el atleti este de local siempre
df_atm_visitante=concatenacion.transformar_atm_visitante(df_concatenado)
#Concatenamos ambos dfs
df_concatenado_final=concatenacion.concatenar(df_atm_visitante)
#Obtenemos el df final y definitivo
df_final=concatenacion.terminar(df_concatenado_final)
#Generamos un excel del df para futuras acciones
concatenacion.excel(df_final, "partidos")

