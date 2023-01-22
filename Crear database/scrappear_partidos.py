from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import re
import json
from config import Config

#Clase para scrappear los partidos de liga, copa y champions
class Scrapper():

    def __init__(self, link):
        self.link=link

    def scrappeo_liga(self):
        #Hacemos scrappeo a la tabla
        soup=bs4(self.link.text,"html.parser")
        #Cogemos las filas y luego las celdas
        filas=soup.find("tbody").find_all("tr")
        celdas=[i.find_all("td") for i in filas]
        lista=[]
        #Detectamos el ultimo partido que tiene publico (ultimo registrado) y creamos una lista con lo que nos interesa de ellos
        for i in celdas:
            data=[j.text for j in i]
            if data[8]!="":
                lista.append([data[1], data[2], data[3], data[5], data[7], data[9], data[10]])
        return lista

    def scrappeo_champions(self):
        #Hacemos scrappeo a la tabla
        soup=bs4(self.link.text,"html.parser")
        #Cogemos las filas y luego las celdas
        filas=soup.find("tbody").find_all("tr")
        celdas=[i.find_all("td") for i in filas]
        lista=[]
        #Detectamos el ultimo partido que tiene publico (ultimo registrado) y creamos una lista con lo que nos interesa de ellos
        for i in celdas:
            data=[j.text for j in i]
            #Quitamos los digitos de la bandera de los paises
            data[4]=data[4][:-3].strip()
            data[8]=data[8][3:].strip()
            if data[9]!="":
                lista.append([data[2], data[3], data[4], data[6], data[8], data[10], data[11]])
        return lista
            
    def scrappeo_copa(self):
        #Hacemos scrappeo a la tabla
        soup=bs4(self.link.text,"html.parser")
        #Cogemos las filas y luego las celdas
        filas=soup.find("tbody").find_all("tr")
        celdas=[i.find_all("td") for i in filas]
        lista=[]
        #Detectamos el ultimo partido que tiene publico (ultimo registrado) y creamos una lista con lo que nos interesa de ellos
        for i in celdas:
            data=[j.text for j in i]
            if len(data)==11:
                lista.append([data[1],data[2],data[3],data[4],data[5],data[7],data[8]])
        return lista


#Clase para crear los df y modificarlos
class CrearDataframe():
    
    def __init__(self, codigo):
        self.codigo=codigo

    #Funcion para crear el df con los partidos del atleti
    def crear_dataframe(self, lista_partidos):
        #Creamos el df con todos los partidos
        partidos=pd.DataFrame(lista_partidos,columns=["Fecha","Hora", "Local","Resultado","Visitante", "Estadio","Arbitro"])
        #Creamos uno a partir de la extraccion unicamente de los que juega el atleti
        df=partidos.loc[(partidos["Local"]=="Atlético Madrid") | (partidos["Visitante"]=="Atlético Madrid")].reset_index().copy()
        #Añadimos la columna del cod estadio, quitamos las tildes de los equipos y añadimos el codigo de la competicion
        df["CodEstadio"]="0"
        df.loc[df["Local"]=="Atlético Madrid","Local"]="Atletico Madrid"
        df.loc[df["Visitante"]=="Atlético Madrid","Visitante"]="Atletico Madrid"
        df["CodCompeticion"]=self.codigo
        df.loc[df["Local"]=="Cádiz","Local"]="Cadiz"
        df.loc[df["Visitante"]=="Cádiz","Visitante"]="Cadiz"
        #Devolvemos el df estructurado
        df=df[["Fecha","Hora", "Local","Resultado","Visitante", "Arbitro","CodEstadio", "CodCompeticion"]]
        return df

    #Añadimos el codigo del estadio segun el equipo
    def anadir_codestadio(self, df_creado, lista_equipos):
        df=df_creado.copy()

        for i in lista_equipos:
            #Dividimos el nombre de los equipos para que lo detecte
            spliteao=i[0].split()

            for j in spliteao:
                #Discriminamos por ciertas palabras ya que se repiten o hay conflicto (Aston Villa y Villareal)
                if len(j)>2 and j!="Real" and j!="Club" and j!="RCD" and j!="Villa":
                    df.loc[df["Local"].str.match(j)==True, ["Local","CodEstadio"]]=[i[0],i[1]]
                    df.loc[df["Visitante"].str.match(j)==True, "Visitante"]=i[0]

            df.loc[df["Local"].str.match(i[0])==True, ["Local","CodEstadio"]]=[i[0],i[1]]
            df.loc[df["Visitante"].str.match(i[0])==True, "Visitante"]=i[0]

        return df


#Creamos la clase para terminar de crear el dataframe de los partidos
class Definitivo():

    #Para concatenar dfs pasados en una lista
    def concatenar(self, lista_dfs):

        return pd.concat(lista_dfs).reset_index()

    def transformar_atm_visitante(self, df):

        #Estructuramos el df
        df_codpartido=df.copy()
        df_codpartido=df_codpartido[["Fecha","Hora", "Local","Resultado","Visitante", "Arbitro","CodEstadio", "CodCompeticion"]]
        
        #Creamos un df con los partidos del atleti de local
        local_atm=df_codpartido.loc[df_codpartido["Local"]=="Atletico de Madrid"].copy()

        #Creamos un df con los partidos del atleti de visitante
        visitante_atm=df_codpartido.loc[df_codpartido["Visitante"]=="Atletico de Madrid"].copy()
        #Cogemos las columnas del atleti y el equipo local del df del atleti de visitante para intercambiarlas
        atleti=visitante_atm["Visitante"]
        visitante=visitante_atm["Local"]
        visitante_atm["Local"]=atleti
        visitante_atm["Visitante"]=visitante
        #Damos la vuelta al resultado ya que el local ahora seria visitante
        resultado_dado_vuelta=[i[::-1] for i in visitante_atm["Resultado"]]
        visitante_atm["Resultado"]=resultado_dado_vuelta

        #Devolvemos el df del atleti de local y el df del atleti de visitante pero puesto ya en la columna de local
        return local_atm, visitante_atm

    def terminar(self, df):
        df_final=df.copy()
        #Renombramos las columnas de local y visitante y estructuramos el df
        df_final=df_final.rename(columns={"Local":"ATM","Visitante":"NombreEquipo"})
        df_final=df_final[["Fecha","Hora", "ATM","Resultado","NombreEquipo", "Arbitro","CodEstadio", "CodCompeticion"]]
        #Devolvemos el df ordenado por la fecha
        return df_final.sort_values(by=["Fecha"])

    #Pasamos a excel un df dandole un nombre
    def excel(self, df, nombre):
        df.to_excel(nombre+".xlsx", index=False)
        print("Excel generado con exito")


#Consulta que nos devuelve los equipos con su codigo de estadio
def consulta_equipos(bbdd, c):
    c.execute("""USE futbol""")
    c.execute("""SELECT NombreEquipo, CodEstadio FROM equipos""")
    lista=c.fetchall()
    return lista

#Creamos la conexiona a MySQL
configuracion=Config().crear_conexion()
bbdd=configuracion[0]
c=configuracion[1]

#Llamamos a la funcion para obtener los equipos y su codigo de estadio
equipos=consulta_equipos(bbdd, c)

#Scrappeamos los partidos de liga
lista_liga=Scrapper(requests.get("https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures")).scrappeo_liga()
#Creamos el dataframe de la liga con los partidos
codigo_liga=317
liga=CrearDataframe(codigo_liga)
df_liga=liga.crear_dataframe(lista_liga)
#Añadimos el codigo del estadio a los partidos
df_liga_codestadio=liga.anadir_codestadio(df_liga, equipos)


#Scrappeamos los partidos de champions
lista_champions=Scrapper(requests.get("https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures")).scrappeo_champions()
#Creamos el dataframe de la champions con los partidos
codigo_champions=322
champions=CrearDataframe(codigo_champions)
df_champions=champions.crear_dataframe(lista_champions)
#Añadimos el codigo del estadio a los partidos
df_champions_codestadio=champions.anadir_codestadio(df_champions, equipos)


#Scrappeamos los partidos de copa
lista_copa=Scrapper(requests.get("https://fbref.com/en/comps/569/schedule/Copa-del-Rey-Scores-and-Fixtures")).scrappeo_copa()
#Creamos el dataframe de la copa con los partidos
codigo_copa=320
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
