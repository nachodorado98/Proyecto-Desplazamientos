#Impotamos lo necesario de Flask
from flask import Flask, render_template, url_for, request, redirect, flash
#Impotamos la clase consulta y estadistica
from consultas import Consulta, Estadistica
#Importamos el traductor
from translate import Translator
#Importamos os
import os 
#Importamos lo necesario para el mapa
import folium
import geopandas as gpd
#Importamos la clase administrador
from admin import Administrador


#Creamos los objetos para las consultas
objeto_consulta=Consulta()
objeto_estadistica=Estadistica()

#Creamos un objeto para el administrador de usuarios
objeto_admin=Administrador()

#Inicializamos el acceso de manera global
acceso=False

#Creamos la app
app=Flask(__name__, template_folder="templates")

#Clave Secreta
app.secret_key="clave_super_secreta"

#Creamos la funcion de la direccion de inicio
@app.route('/')
def inicio():

    global acceso

    #Si has tenido acceso, puedes cerrar sesion llamando a la funcion cerrar_sesion
    if acceso:
        cerrar_sesion()

    return render_template("base.html")

#Creamos la funcion para cerrar sesion
@app.route('/cerrar_sesion', methods=["POST", "GET"])
def cerrar_sesion():

    global acceso

    #Si has tenido acceso puedes cerrar sesion
    if acceso:
        acceso=False
        #Mostramos un mensaje de sesion cerrada correctamente
        flash("Has cerrado sesion!","info")
        #Nos devuelve a la pagina de inicio ya con la sesion cerrada
        return redirect(url_for('inicio'))
    #Si no has tenido acceso, sigues sin tener  y te devuelve a la pagina de inicio
    else:
        #Mostramos un mensaje de acceso denegado sin iniciar sesion
        flash("No puedes cerrar sesion sin antes haberla iniciado!!","error")
        return redirect(url_for('inicio'))

#Creamos la funcion de la direccion de desplazamientos
@app.route('/desplazamientos')
def desplazamientos():

    global acceso
    
    #Si tienes acceso puedes ver los desplazamientos
    if acceso:
        #Obtenemos los datos de los desplazamientos llamando a consulta_desplazamientos
        datos_desplazamientos=objeto_consulta.consulta_desplazamientos()
        #Devolvemos el html de la pagina desplazamientos
        return render_template("desplazamientos.html",datos_desplazamientos=datos_desplazamientos)
    #Si no has tenido acceso, sigues sin tener y te devuelve a la pagina de inicio
    else:
        #Mostramos un mensaje de acceso denegado sin iniciar sesion
        flash("Para poder acceder debes iniciar sesion primero!!","error")
        return redirect(url_for('inicio'))

#Creamos la funcion de la direccion de partidos
@app.route('/partidos')
def partidos():

    global acceso

    #Si tienes acceso puedes ver los partidos
    if acceso:
        #Obtenemos los datos de los partidos del atleti llamando a consulta_partidos_atm
        datos_partidos=objeto_consulta.consulta_partidos_atm()
        #Devolvemos el html de la pagina partidos
        return render_template("partidos.html", datos_partidos=datos_partidos)
    #Si no has tenido acceso, sigues sin tener y te devuelve a la pagina de inicio
    else:
        #Mostramos un mensaje de acceso denegado sin iniciar sesion
        flash("Para poder acceder debes iniciar sesion primero!!","error")
        return redirect(url_for('inicio'))


#Creamos la funcion de la direccion de estadisticas
@app.route('/estadisticas', methods=["POST", "GET"])
def estadisticas():

    global acceso

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

    #Si tienes acceso puedes ver las estadisticas
    if acceso:
        #Devolvemos el html de la pagina estadisticas
        return render_template("estadisticas.html", 
                                estadistica1=estadistica1, 
                                estadistica2=estadistica2, 
                                estadistica3=estadistica3)
    #Si no has tenido acceso, sigues sin tener y te devuelve a la pagina de inicio
    else:
        #Mostramos un mensaje de acceso denegado sin iniciar sesion
        flash("Para poder acceder debes iniciar sesion primero!!","error")
        return redirect(url_for('inicio'))
    
#Creamos la funcion de la direccion de mapa
@app.route('/mapa')
def mapa():

    global acceso

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

    #Si tienes acceso puedes ver el mapa
    if acceso:
        #Devolvemos el html de la pagina mapa_desplazamientos
        return render_template("mapa_desplazamientos.html")
    #Si no has tenido acceso, sigues sin tener y te devuelve a la pagina de inicio
    else:
        #Mostramos un mensaje de acceso denegado sin iniciar sesion
        flash("Para poder acceder debes iniciar sesion primero!!","error")
        return redirect(url_for('inicio'))

#Creamos la funcion del detalle del desplazamiento
@app.route('/detalle/Desplazamiento<boton>')
def detalle(boton):

    #Obtenemos los datos del desplazamiento
    detalle_desplazamiento=list(objeto_consulta.detalle_desplazamiento(boton)[0])
    #Obtenemos el path de la imagen del nombre del equipo
    equipo=os.path.join("\\static", f"{detalle_desplazamiento[0]}.png")
    #Obtenemos la longitud del nombre del estadio
    longitud_nombre_estadio=len(detalle_desplazamiento[2])
    #Obtenemos el path de la imagen del pais
    pais=os.path.join("\\static", f"{detalle_desplazamiento[1].lower()}.png")

    return render_template("detalle_desplazamiento.html", detalle_desplazamiento=detalle_desplazamiento[2:], equipo=equipo, longitud_nombre_estadio=longitud_nombre_estadio, pais=pais)

#Creamos la funcion que nos permite logearnos
@app.route('/login', methods=["POST", "GET"])
def login():

    global acceso

    #Obtenemos el usuario y contraseña introducidos
    usuario=request.form.get("usuario")
    contrasena=request.form.get("contrasena")

    #Realizamos una consulta a la tabla de usuarios para saber si esta registrado
    consulta=objeto_admin.comprobacion(usuario, contrasena)

    #Si la consulta devuelve datos, se accede a la pagina de login y el acceso se activa
    if consulta!=[]:
        acceso=True
        return render_template("login.html", usuario=consulta[0][2])
    #Si no devuelve nada la conuslta es que no son validas las credenciales
    else:
        #Mostramos un mensaje de acceso denegado debido a las credenciales
        flash("El usuario o la contraseña no es valido!!","error")
        return redirect(url_for('inicio'))

#Creamos la funcion de la direccion registro
@app.route('/registro', methods=["POST", "GET"])
def registro():

    return render_template("registro.html")

#Creamos la funcion que nos permite registrarnos
@app.route('/registro_correcto', methods=["POST", "GET"])
def registro_correcto():

    global acceso

    #Obtenemos el nombre, usuario, contraseña y correo electronico introducidos
    nombre_nuevo=request.form.get("nombre_nuevo").title()
    usuario_nuevo=request.form.get("usuario_nuevo")
    contrasena_nueva=request.form.get("contrasena_nueva")
    correo_nuevo=request.form.get("correo_nuevo")

    #Comprobamos que estan todos los campos introducidos
    if nombre_nuevo and usuario_nuevo and contrasena_nueva and correo_nuevo:

        #Comprobamos que cumple los requisitos de registro valido
        if objeto_admin.registro_valido(nombre_nuevo, usuario_nuevo, contrasena_nueva, correo_nuevo):

            #Comprobamos que no hay usuarios o correos duplicados
            if objeto_admin.comprobacion_duplicados(usuario_nuevo, correo_nuevo):

                #Insertamos el nuevo usuario en la tabla usuarios y activamos el acceso
                objeto_admin.insertar_usuario(usuario_nuevo, contrasena_nueva, nombre_nuevo, correo_nuevo)
                acceso=True

                ##Comprobamos que se ha enviado el correo
                if objeto_admin.enviar_correo(nombre_nuevo, usuario_nuevo, correo_nuevo):
                    correo_confirmacion=f"Se ha enviado un correo de confirmacion a la direccion {correo_nuevo}!!"
                else:
                    correo_confirmacion=f"No se ha enviado un correo de confirmacion a la direccion {correo_nuevo}!!"
                
                return render_template("login.html", usuario=nombre_nuevo, correo_confirmacion=correo_confirmacion)
            
            else:
                #Mostramos un mensaje de que el usuario o el correo ya han sido utilizados
                flash("Usuario o correo electronico ya utilizados!!","error")
                return redirect(url_for('registro'))
        else:
            #Mostramos un mensaje de que no cumple los requisitos validos
            flash("No cumple los requisitos validos!!","error")
            return redirect(url_for('registro'))
    else:
        #Mostramos un mensaje de que se deben introducir todos los datos
        flash("Debes rellenar todos los campos!!","error")
        return redirect(url_for('registro'))

#Iniciamos la apliacion
if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1')