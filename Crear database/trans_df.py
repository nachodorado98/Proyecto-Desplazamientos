from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import re
import json
from config import Config

#Clase para crear los df y modificarlos
class CrearDataframe():
    
    def __init__(self, codigo=None):
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

    #Funcion para crear el dataframe de las competiciones
    def crear_dataframe_competiciones(self, datos):
        return pd.DataFrame(datos, columns=["Competicion","Temporada","Numero Equipos", "Campeon", "Pichichi", "Goles"])


#Creamos la clase para terminar de crear el dataframe de los partidos
class Definitivo():

    #Para concatenar dfs pasados en una lista
    def concatenar(self, lista_dfs):

        return pd.concat(lista_dfs).reset_index()

    #Funcion para transformar el atleti de posicion de visitante a local
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

    #Funcion para terminar el dataframe de los partidos
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
        print(f"Excel {nombre} generado con exito")


