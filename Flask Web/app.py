#Impotamos lo necesario de Flask
from flask import Flask, render_template, url_for
#Impotamos la clase consulta y estadistica
from consultas import Consulta, Estadistica
#Importamos el traductor
from translate import Translator
#Importamos os
import os 
#Importamos lo necesario para el mapa
import folium
import geopandas as gpd

#Creamos los objetos para las consultas
objeto_consulta=Consulta()
objeto_estadistica=Estadistica()

#Creamos la app
app=Flask(__name__, template_folder="templates")

#Clave Secreta
app.secret_key="clave_super_secreta"

#Creamos la funcion de la direccion de inicio
@app.route('/')
def inicio():
    
    #Devolvemos el html de la pagina inicio
	return render_template("base.html")

#Creamos la funcion de la direccion de desplazamientos
@app.route('/desplazamientos')
def desplazamientos():

    #Obtenemos los datos de los desplazamientos llamando a consulta_desplazamientos
    datos_desplazamientos=objeto_consulta.consulta_desplazamientos()
    #Devolvemos el html de la pagina desplazamientos
    return render_template("desplazamientos.html",datos_desplazamientos=datos_desplazamientos)

#Creamos la funcion de la direccion de partidos
@app.route('/partidos')
def partidos():

    #Obtenemos los datos de los partidos del atleti llamando a consulta_partidos_atm
    datos_partidos=objeto_consulta.consulta_partidos_atm()
    #Devolvemos el html de la pagina partidos
    return render_template("partidos.html", datos_partidos=datos_partidos)


#Creamos la funcion de la direccion de estadisticas
@app.route('/estadisticas', methods=["POST", "GET"])
def estadisticas():

    #ESTADISTICA 1
    #Obtenemos los nombres de los estadios en los que se ha jugado (sin contar el del atleti)
    estadios_jugados=objeto_estadistica.estadios_jugados()
    #Obtenemos el numero de estadios jugados
    cantidad_estadios_jugados=len(estadios_jugados)
    #Obtenemos los nombres de los estadios a los que se ha ido
    estadios_visitados=objeto_estadistica.estadios_visitados()
    #Obtenemos el numero de estadios visitados
    cantidad_estadios_visitados=len(estadios_visitados)
    #Calculamos el porcentaje
    porcentaje=int((cantidad_estadios_visitados/cantidad_estadios_jugados)*100)
    #Lista con los datos necesarios para la estadistica1
    estadistica1=[estadios_jugados,cantidad_estadios_jugados,estadios_visitados,cantidad_estadios_visitados,porcentaje]
    
    #ESTADISTICA 2
    #Obtenemos el nombre del estadio que mas se ha visitado y el numero de veces
    estadistica2=objeto_estadistica.mas_visitado()[0]

    #ESTADISTICA 3
    #Obtenemos el nombre del estadio que se ha visitado con mas capacidad y su capacidad
    estadistica3=objeto_estadistica.mas_grande()[0]


    #Devolvemos el html de la pagina estadisticas
    return render_template("estadisticas.html", 
                            estadistica1=estadistica1, 
                            estadistica2=estadistica2, 
                            estadistica3=estadistica3)

#Creamos la funcion de la direccion de mapa
@app.route('/mapa')
def mapa():

    #Obtenemos los datos para poner en el mapa llamando a puntos_mapa
    datos_para_mapa=objeto_consulta.puntos_mapa()
    #Pasamos los datos necesario a numero (latitud y longitud)
    datos_numero=[(float(i[0]), float(i[1]), i[2], i[3], i[4], i[5]) for i in datos_para_mapa]
    #Obtenemos los paises que tendra el mapa (de manera unica)
    paises_unicos=set([i[6] for i in datos_para_mapa])
    #Traducimos el nombre del pais de castellano al ingles
    traductor=Translator(from_lang="spanish", to_lang="english")
    paises_unicos_ing=[traductor.translate(i) for i in paises_unicos]
    #Leemos el archivo geojson de los paises del mundo con geopandas
    paths=os.getcwd() 
    path_mapa=os.path.join(paths,"JSON\world-countries.json")
    gdf=gpd.read_file(path_mapa)
    #Obtenemos el geodataframe que tenga los paises que tenemos nosotros en ingles
    data_buena=gdf[gdf["name"].isin(paises_unicos_ing)]
    #Creamos un mapa con una localizacion inicial cualquiera y un zoom
    mapa=folium.Map(location=[40.5, -3.25], zoom_start=3)
    #Agregamos al mapa los paises del geodataframe
    folium.GeoJson(data_buena, name="desplazamientos").add_to(mapa)
    #Generamos tantos marcadores como desplazamientos hayamos realizado
    for i in datos_numero:
        #Le damos formato a la fecha de ida y de vuelta
        ida=i[4].strftime("%d/%m/%Y")
        vuelta=i[5].strftime("%d/%m/%Y")
        #Creamos el marcador de la ubicacion del desplazamiento (estadio) y un mensaje emergente con la fecha utilizando etiquetas HTML
        folium.Marker([i[0], i[1]], tooltip=f"{i[3]}", popup=folium.Popup(f"<h1>{i[3]}</h1><h3>{ida} - {vuelta}</h3>", max_width=500)).add_to(mapa)
    #Guardamos el mapa como un template mas
    mapa.save(os.path.join(paths,"templates\mapa_desplazamientos.html"))

    #Devolvemos el html de la pagina mapa_desplazamientos
    return render_template("mapa_desplazamientos.html")

#Iniciamos la apliacion
if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1')