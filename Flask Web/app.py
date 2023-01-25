from flask import Flask, render_template, url_for

app=Flask(__name__, template_folder="templates")

app.secret_key="clave_super_secreta"

@app.route('/')
def inicio():
 
	return render_template("base.html")


if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1')