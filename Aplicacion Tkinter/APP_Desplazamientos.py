from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
import os
import re
#Importamos la clase Consulta para realizar todas las consultas a la BBDD
from consultas import Consulta

#Objeto que nos permite realizar las consultas a la BBDD futbol
objeto_consulta=Consulta()

#Creamos la interfaz utilizando Tkinter. Le damos un titulo y unas dimensiones a la ventana
root=Tk()
root.title("APP Desplazamientos")
root.geometry("1550x830")
root.resizable(0,0)

def ver_mapa():
    pass

def detalle_desplazamiento():
    pass


#Funcion que pasado un tiempo, nos destruye la ventana
def destruccion(emergente):
    emergente.destroy()

#Funcion que crea una ventana emergente segun los datos que quieras ver en detalle
def poner_datos_emergentes(datos, titulo, lista_texto, e=None):

    #Creamos la ventana emergente
    emergente=Toplevel()
    emergente.geometry("500x300")
    emergente.title("Datos en detalle")
    emergente.resizable(0,0)
    
    #Creamos un frame general para poner los widgets
    frame=Frame(emergente, bg="skyblue")
    frame.pack(fill="both", expand=True)
    
    #Creamos un frame para el titulo
    frame_title=Frame(frame, bg="skyblue")
    frame_title.pack()
    label_titulo=Label(frame_title, text=titulo, bg="skyblue", font=("Helvetica", 18, "bold"))
    label_titulo.pack(pady=5)
    
    #Creamos un frame para los datos
    frame_labels=Frame(frame, bg="skyblue")
    frame_labels.pack()
    
    #Iteramos por los datos y su texto para ubicarlos conjuntamente
    for i in range(len(datos)):

        label_texto=Label(frame_labels, text=lista_texto[i]+": ", bg="skyblue", font=("Helvetica", 12, "bold"))
        label_texto.grid(row=i, column=0, pady=5)

        label=Label(frame_labels, text=datos[i], bg="skyblue", font=("Helvetica", 12, "bold"))
        label.grid(row=i, column=1,pady=5)
    
    #Llamamos a la funcion destruccion para cerrar la ventana pasados 9 segundos
    emergente.after(9000, lambda : destruccion(emergente))
    
    emergente.mainloop()


#Funcion que nos permite ver en detalle el partido seleccionado en el treeview
def detalle_partido():
    try:
        
        #Obtenemos el indice del registro del treeview seleccionado
        indice=int(tree.selection()[0])
        #Obtenemos asi el codigo del desplazamiento de ese registro
        cod_desplazamiento=tree.item(indice,"values")[0]

        #Obtenemos los datos del equipo llamando a datos_sobre_equipo y pasandole el codigo del desplazamiento
        datos_equipo=objeto_consulta.datos_sobre_equipo(cod_desplazamiento)
        #Obtenemos los datos de la temporada llamando a datos_temporada y pasandole el codigo del desplazamiento
        datos_competicion_temporada=objeto_consulta.datos_temporada(cod_desplazamiento)
        #Obtenemos los datos historicos de la competicion llamando a datos_historico y pasandole el codigo del desplazamiento
        datos_competicion_historico=objeto_consulta.datos_historico(cod_desplazamiento)

        #Obtenemos los datos totales que nos interesan del partido del cual se ha realizado el desplazamiento llamando a datos_totales_partido
        datos_partido_completo=objeto_consulta.datos_totales_partido(cod_desplazamiento)

        #Creamos una ventana para mostrar todos estos datos consultados
        detalle_partido=Toplevel()
        detalle_partido.geometry("500x630")
        detalle_partido.title("Detalle del Partido")
        detalle_partido.resizable(0,0)

        #Creamos un frame general para poner los widgets
        frame=Frame(detalle_partido, bg="#c78be7")
        frame.pack(fill="both", expand=True)

        #Cogemos el equipo obtenido para poner su escudo
        equipo=datos_partido_completo[3]
        path=os.getcwd() 
        path_imagenes=os.path.join(path,"Archivos Extra\Equipos")
        imagen=[path_imagenes+"\\"+i for i in os.listdir(path_imagenes) if re.search(equipo,i)]
        escudo=PhotoImage(file=imagen[0])
        label_escudo=Label(frame, image=escudo, bg="#c78be7")
        label_escudo.pack(pady=(10,7))
        #Hacemos que el escudo pueda ejecutar una funcion (la de poner los datos de ese equipo) al pulsarlo
        titulo_equipo="Datos del Club"
        lista_texto_equipos=["Equipo", "Pais", "Fundacion", "Ligas", "Champions", "Goleador", "Apariciones"]
        label_escudo.bind("<Button-1>", lambda e: poner_datos_emergentes(datos_equipo, titulo_equipo, lista_texto_equipos,e))
        label_escudo.config(cursor="hand2")

        #Cogemos el nombre de la competicion
        competicion=datos_partido_completo[4]
        #Si no es La Liga, ampliamos la ventana
        if competicion!="La Liga":
            detalle_partido.geometry("660x650")
        label_competi=Label(frame, text=competicion, bg="#c78be7", font=("Helvetica",40, "bold"))
        label_competi.pack(pady=(10,5))
        #Hacemos que el texto de la competicion pueda ejecutar una funcion (la de poner los datos de esa competicion) al pulsarlo
        titulo_historico="Historico de la Competicion"
        lista_texto_historico=["Liga","Equipo","Participaciones", "Victorias", "Derrotas"]
        label_competi.bind("<Button-1>", lambda e: poner_datos_emergentes(datos_competicion_historico, titulo_historico, lista_texto_historico, e))
        label_competi.config(cursor="hand2")

        #Cogemos la temporada
        temporada=datos_partido_completo[5]
        label_temporada=Label(frame, text="Temporada "+temporada, bg="#c78be7", font=("Times",20, "italic"))
        label_temporada.pack(pady=(2,10))
        #Hacemos que el texto de la temporada pueda ejecutar una funcion (la de poner los datos de esa temporada) al pulsarlo
        titulo_temporada="Datos de la Competicion Actual"
        lista_texto_temporada=["Competicion", "Temporada", "Equipos", "Campeon", "Pichichi", "Goles"]
        label_temporada.bind("<Button-1>", lambda e: poner_datos_emergentes(datos_competicion_temporada, titulo_temporada, lista_texto_temporada,e))
        label_temporada.config(cursor="hand2")

        #Creamos un frame para poner las fechas
        frame_fecha=Frame(frame,bg="#c78be7")
        frame_fecha.pack()

        #Cogemos la fecha del partido y le damos la forma que queremos
        fecha=datos_partido_completo[0].strftime("%d/%m/%Y")
        label_fecha=Label(frame_fecha, text="Fecha: "+fecha, bg="#c78be7", font=("Times",20))
        label_fecha.grid(row=0, column=0,pady=5, padx=15)

        #Cogemos la hora del partido
        hora=datos_partido_completo[1] 
        label_hora=Label(frame_fecha, text="Hora: "+hora, bg="#c78be7", font=("Times",20))
        label_hora.grid(row=0, column=1,pady=5, padx=15)

        #Cogemos el resultado del partido
        resultado=datos_partido_completo[2]
        label_result=Label(frame, text="Resultado", bg="#c78be7", font=("Arial Baltic",30))
        label_result.pack(pady=(10,2))
        label_resultado=Label(frame, text=resultado, bg="#c78be7", font=("Helvetica",30,"italic"))
        label_resultado.pack()

        detalle_partido.mainloop()

    #Si no seleccionas ningun partido te lanza un mensaje de warning
    except:
        
        messagebox.showwarning("ATENCIÓN!!!", "Debes seleccionar uno de las ciudades para poder verla en detalle.")



#Funcion para confirmar la insercion del registro del desplazamiento
def confirmacion_insertar(entryp, c1, c2, entry3, entry4, nueva_ventana):
    
    #Obtenemos el valor introducido de los input
    partido=str(entryp.get())
    fechaida=c1.get_date()
    fechavuelta=c2.get_date()
    acompanante=str(entry3.get())
    transporte=str(entry4.get())
    
    #Verificamos que estan todos seleccionados
    if partido and fechaida and fechavuelta and acompanante and transporte:
        #Preguntamos para la confirmacion
        opcion=messagebox.askquestion("Confirmacion!", "¿Estas seguro de añadir este desplazamiento?")
        if opcion=="yes":
            try:
                #Dividimos el partido seleccionaod en la fecha y el equipo
                partido_dividido=partido.split(" VS ")
                fecha=partido_dividido[0]
                equipo=partido_dividido[1]
                #Obtenemos el codigo del partido con la funcion obtener_codigo_partido
                codigo_partido=objeto_consulta.obtener_codigo_partido(fecha, equipo)
                #Insertamos el registro del desplazamiento en la BBDD con la funcion insertar_desplazamiento
                objeto_consulta.insertar_desplazamiento(codigo_partido, fechaida, fechavuelta, acompanante, transporte)
                #Mostramos un mensaje de que se ha insertado con exito
                messagebox.showinfo("FELICIDADES!!!", "Has agregado una nueva experiencia de viaje de manera correcta.")
                #Eliminamos la ventana para insertar los registros
                nueva_ventana.destroy()
                #Llamamos a la funcion que nos inserta en el treeview los desplazamientos para actualizarlo con el nuevo
                inicio()

            except:
                messagebox.showwarning("ATENCIÓN!!!", "Algo falló. Que raro.")

    #Si no introduces todos los parametros te lanza un mensaje de warning
    else:
        messagebox.showwarning("ATENCIÓN!!!", "Debes introducir todos los parametros.")


#Funcion para crear la interfaz que nos permitirá elegir los datos para insertar nuevos registros
def insertar():
    
    #Creamos la ventana
    nueva_ventana=Toplevel()
    nueva_ventana.title("¡¡Desplazamiento nuevo!!")
    nueva_ventana.geometry("750x670")
    
    #Creamos el frame donde van a ir los widgets
    frame1=Frame(nueva_ventana, bg="lightgreen")
    frame1.pack(fill="both", expand=True)
    
    #Ponemos un titulo a la ventana
    lb=Label(frame1, text=f"AGREGA LOS DATOS DEL DESPLAZAMIENTO",bg="lightgreen", font=("Helvetica", 20, "bold"))
    lb.pack(pady=10)
    
    #Creamos el frame para el input del partido
    frame28=Frame(frame1, bg="lightgreen")
    frame28.pack(pady=10)
    
    #Input para el partido
    lbp=Label(frame28, text="Partido",bg="lightgreen", font=("Helvetica", 14))
    lbp.grid(row=0, column=0,pady=10)
    #Obtenemos la fecha del ultimo partido al que se ha ido con la funcion fecha_ultimo_partido_ido
    fecha=objeto_consulta.fecha_ultimo_partido_ido()
    #Utilizamos la fecha anterior para obtener los partidos posteriores a los que has podido ir llamando a consulta_partidos
    partidos_cons=objeto_consulta.consulta_partidos(fecha)
    #Damos forma a como queremos que se muestren los partidos
    partidos_str=[str(i[0].strftime("%Y-%m-%d"))+" VS "+i[1] for i in partidos_cons]
    #Creamos una lista desplegable que nos permite seleccionar el partido
    entryp=ttk.Combobox(frame28, value=partidos_str, width=40)
    entryp.grid(row=1, column=0, padx=45)
    entryp.current()
    
    #Creamos el frame para el input de las fechas de ida y vuelta
    frame11=Frame(frame1, bg="lightgreen")
    frame11.pack(pady=10)
    
    #Input para la fecha de ida
    lb2=Label(frame11, text="Fecha Ida",bg="lightgreen", font=("Helvetica", 14))
    lb2.grid(row=0, column=0, pady=10, padx=45)
    c1=Calendar(frame11, selectmode="day", date_pattern="yyyy-mm-dd")
    c1.grid(row=1, column=0, pady=10, padx=45)
    
    #Input para la fecha de vuelta
    lb3=Label(frame11, text="Fecha Vuelta",bg="lightgreen", font=("Helvetica", 14))
    lb3.grid(row=0, column=1, pady=10, padx=45)
    c2=Calendar(frame11, selectmode="day", date_pattern="yyyy-mm-dd")
    c2.grid(row=1, column=1, pady=10, padx=45)
    
    #Creamos el frame para el input del acompañamiento y el medio de transporte
    frame12=Frame(frame1, bg="lightgreen")
    frame12.pack(pady=10)
    
    #Input para el acompañante
    lb5=Label(frame12, text="Acompañante",bg="lightgreen", font=("Helvetica", 14))
    lb5.grid(row=0, column=0, pady=10, padx=45)
    valores1=["Mi Amor", "Solito..", "Familia"]
    entry3=ttk.Combobox(frame12, value=valores1)
    entry3.grid(row=1, column=0, padx=45)
    entry3.current()
    
    #Input para el medio de transporte
    lb6=Label(frame12, text="Transporte",bg="lightgreen", font=("Helvetica", 14))
    lb6.grid(row=0, column=1, pady=10, padx=45)
    valores=["Avion","Autobus","Autobus Verde","Tren/AVE", "La Renfe", "Andando"]
    entry4=ttk.Combobox(frame12, value=valores)
    entry4.grid(row=1, column=1, padx=45)
    entry4.current()
    
    #Boton que nos permitirá insertar los registros
    lbbutton=LabelFrame(frame1, text=" Añadir Desplazamiento ", bg="lightgreen", font=("Helvetica", 14))
    lbbutton.pack(pady=20)
    path=os.getcwd()
    icono_anadir=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_anadir.png"))
    #Le pasamos a la funcion los input de los que queremos obtener su valor (su seleccion)
    btn=Button(lbbutton, image=icono_anadir, command=lambda: confirmacion_insertar(entryp, c1, c2, entry3, entry4, nueva_ventana), bg="lightgreen", bd=0)
    btn.pack(pady=10, padx=10)
 
    nueva_ventana.mainloop()


#Funcion que nos permit vaciar el treeview de registros
def vaciar_tree_principal():
    
    for i in tree.get_children():
        tree.delete(i)

#Funcion que nos permite obtener los datos necesarios del desplazamiento para el treeview 
def inicio():

    #Vaciamos el treeview para volver a insertar
    vaciar_tree_principal()
    
    #Obtenemos todos los registros llamando a la consulta_desplazamientos
    desplazamientos=objeto_consulta.consulta_desplazamientos()
    
    lista_desplazamientos=[list(x) for x in desplazamientos]

    #Damos la forma que queremos al campo de la fecha
    for i in range(len(lista_desplazamientos)):
        lista_desplazamientos[i][2]=desplazamientos[i][2].strftime("%d-%m-%Y")

    #Insertamos los registros en el treeview
    indice=0
    for registro in lista_desplazamientos:
        tree.insert(parent="", index="end", iid=indice, text="",values=tuple(registro))
        indice+=1


#-------------------------------------------------------------------DISEÑO DE LA INTERFAZ
#Ruta del directorio actual
path=os.getcwd()

#Frame global
frame_inic=Frame(root, bg="#fb6b69")
frame_inic.pack(fill="both", expand=True)

#Frame del titulo y bandera
frame_izq=Frame(frame_inic, bg="#fb6b69")
frame_izq.grid(row=0, column=0, padx=50)

titulo=Label(frame_izq, text="On Tour", bg="#fb6b69", font=("Algerian",115))
titulo.pack(pady=5)

icono_band=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_bandera.png"))

band=Label(frame_izq, image=icono_band, bg="#fb6b69")
band.pack(pady=5)

#Frame principal
frame_inicial=Frame(frame_inic, bg="#fb6b69")
frame_inicial.grid(row=0, column=1)

fuente1=Font(family="Nature Beauty", size=38)

#Frame superior para el escudo
frame_top=Frame(frame_inicial,bg="#fb6b69")
frame_top.pack(pady=5)

icono_atm=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_atleti.png"))

atl=Label(frame_top, image=icono_atm, bg="#fb6b69")
atl.pack(pady=5)

#Estilizar el treeview
estilo=ttk.Style()
estilo.theme_use("alt")
estilo.configure("Treeview", background="lighsilver", foreground="black", rowheight=25)
estilo.configure("Treeview.Heading", font=("Calibri",12, "bold"))
estilo.map("Treeview", background=[("selected","#fb6b69")])

#Frame para el treeview
frame_tree=Frame(frame_inicial,bg="#fb6b69")
frame_tree.pack(pady=5)

#Creacion del treeview
tree=ttk.Treeview(frame_tree)
tree.pack(pady=5)

tree["columns"]=("Desplazamiento","Equipo","FechaPartido","Ciudad")

tree.column("#0", width=0,stretch=NO)

for i in tree["columns"]:
    tree.column(i, width=150, minwidth=55, anchor=CENTER)
    tree.heading(i, text=i)

#Frame para los botones superiores
frame2=Frame(frame_inicial,bg="#fb6b69")
frame2.pack(pady=5)

#Boton del mapa
icono_mundo=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_mundo.png"))
btn_paises=Button(frame2, image=icono_mundo, command=ver_mapa, bg="#fb6b69", bd=0)
btn_paises.grid(row=0, column=0, padx=(50,70))

#Boton de nuevo registro
icono_maleta=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_database.png"))
btn_insertar=Button(frame2, image=icono_maleta, command=insertar, bg="#fb6b69", bd=0)
btn_insertar.grid(row=0, column=1, padx=(70,30))

#Frame para los botones inferiores
lframe=Frame(frame_inicial, bg="#fb6b69")
lframe.pack(pady=10)

#Boton del desplazamiento
lframe1=LabelFrame(lframe, text=" Detalle del Desplazamiento ", font=("Calibri", 16, "bold"), bg="#fb6b69")
lframe1.grid(row=0, column=0, padx=20, pady=5)
icono_estadio=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_estadio.png"))
btn_detalle=Button(lframe1, image=icono_estadio, command=detalle_desplazamiento, bg="#fb6b69", bd=0)
btn_detalle.pack(padx=20, pady=5)

#Boton del partido
lframe2=LabelFrame(lframe, text=" Detalle del Partido ", font=("Calibri", 16, "bold"), bg="#fb6b69")
lframe2.grid(row=0, column=1, padx=20, pady=5)
icono_balon=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_balon.png"))
btn_detalle_ciu=Button(lframe2, image=icono_balon, command=detalle_partido, bg="#fb6b69", bd=0)
btn_detalle_ciu.pack(padx=20, pady=5)


#Iniciamos la funcion siempre que arranque la aplicacion
inicio()


root.mainloop()




