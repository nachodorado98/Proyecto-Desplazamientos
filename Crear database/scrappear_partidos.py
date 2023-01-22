from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd


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


#Clase para crear los df
class CrearDataframe():
    
    def __init__(self, codigo):
        self.codigo=codigo

    def crear_dataframe(self, lista_partidos):
        partidos=pd.DataFrame(lista_partidos,columns=["Fecha","Hora", "Local","Resultado","Visitante", "Estadio","Arbitro"])
        df=partidos.loc[(partidos["Local"]=="Atlético Madrid") | (partidos["Visitante"]=="Atlético Madrid")].reset_index().copy()
        df["CodEstadio"]="0"
        df.loc[df["Local"]=="Atlético Madrid","Local"]="Atletico Madrid"
        df.loc[df["Visitante"]=="Atlético Madrid","Visitante"]="Atletico Madrid"
        df["CodCompeticion"]=self.codigo
        df.loc[df["Local"]=="Cádiz","Local"]="Cadiz"
        df.loc[df["Visitante"]=="Cádiz","Visitante"]="Cadiz"
        df=df[["Fecha","Hora", "Local","Resultado","Visitante", "Arbitro","CodEstadio", "CodCompeticion"]]
        return df


codigo_liga=317
lista_liga=Scrapper(requests.get("https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures")).scrappeo_liga()
df_liga=CrearDataframe(codigo_liga).crear_dataframe(lista_liga)
print(df_liga)


codigo_champions=322
lista_champions=Scrapper(requests.get("https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures")).scrappeo_champions()
df_champions=CrearDataframe(codigo_champions).crear_dataframe(lista_champions)
print(df_champions)

codigo_copa=320
lista_copa=Scrapper(requests.get("https://fbref.com/en/comps/569/schedule/Copa-del-Rey-Scores-and-Fixtures")).scrappeo_copa()
df_copa=CrearDataframe(codigo_copa).crear_dataframe(lista_copa)
print(df_copa)