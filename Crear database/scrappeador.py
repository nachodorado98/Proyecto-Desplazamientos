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

    #Funcion para scrappear los partidos de la tabla de la liga que se hayan disputado
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

    #Funcion para scrappear los partidos de la tabla de la champions que se hayan disputado
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
    
    #Funcion para scrappear los partidos de la tabla de la copa que se hayan disputado
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
            if len(data)==11 and data[4]!="":
                lista.append([data[1],data[2],data[3],data[4],data[5],data[7],data[8]])
        return lista

    #Funcion para obtener los datos historicos de las temporadas de la tabla de la liga
    def obtener_datos_temporadas_liga(self):
        soup=bs4(self.link.text,"html.parser")
        #Cogemos las filas y luego las celdas
        filas=soup.find("table", id="seasons").find("tbody").find_all("tr")
        lista_filas=[]
        #De cada fila, obtenemos la temporada, la competicion, el numero de equipos, el campeon (si hubiera), el pichcihi y los goles
        for i in filas:
            temporada=i.find("th").find("a").text
            competicion=i.find("td").find("a").text
            numero_equipos=i.find_all("td")[1].text
            try:
                campeon=i.find_all("td")[2].find("a").text
            except:
                campeon=""
            pichichi=i.find_all("td")[3].find("a").text
            goles=i.find_all("td")[3].find("span").text

            lista_filas.append([competicion, temporada, numero_equipos, campeon, pichichi, goles])
        return lista_filas

    #Funcion para obtener los datos historicos de las temporadas de la tabla de la copa y la champions (ambas tablas estan igual de estructuradas)
    def obtener_datos_temporadas_champions_copa(self):
        soup=bs4(self.link.text,"html.parser")
        #Cogemos las filas y luego las celdas
        filas=soup.find("table", id="seasons").find("tbody").find_all("tr")
        lista_filas=[]
        #De cada fila, obtenemos la temporada, la competicion, el numero de equipos, el campeon (si hubiera), el pichcihi y los goles
        for i in filas:
            temporada=i.find("th").find("a").text
            competicion=i.find("td").find("a").text
            numero_equipos=i.find_all("td")[1].text
            try:
                campeon=i.find_all("td")[2].find("a").text
            except:
                campeon=""
            pichichi=i.find_all("td")[5].find("a").text
            goles=i.find_all("td")[5].find("span").text


            lista_filas.append([competicion, temporada, numero_equipos, campeon, pichichi, goles])
        return lista_filas
