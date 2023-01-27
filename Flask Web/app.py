from flask import Flask, render_template, url_for
from consultas import Consulta

objeto_consulta=Consulta()

app=Flask(__name__, template_folder="templates")

app.secret_key="clave_super_secreta"

@app.route('/')
def inicio():
 
	return render_template("base.html")

@app.route('/desplazamientos')
def desplazamientos():

    datos_desplazamientos=objeto_consulta.consulta_desplazamientos()
    return render_template("desplazamientos.html",datos_desplazamientos=datos_desplazamientos)

@app.route('/partidos')
def partidos():

    datos_partidos=objeto_consulta.consulta_partidos_atm()
    return render_template("partidos.html", datos_partidos=datos_partidos)


if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1')