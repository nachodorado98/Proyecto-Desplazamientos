from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
import os
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

def detalle_partido():
    pass

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

    else:
        messagebox.showwarning("ATENCIÓN!!!", "Debes introducir todos los parametros.")


#Funcion para crear la interfaz que nos permitirá elegir los datos para insertar nuevos registros
def insertar():
    
    #Creamos la ventana
    nueva_ventana=Toplevel()
    nueva_ventana.title("¡¡Desplazamiento nuevo!!")
    nueva_ventana.geometry("750x670")
    
    #Creamos el frame donde va el titulo
    frame1=Frame(nueva_ventana, bg="lightgreen")
    frame1.pack(fill="both", expand=True)
    
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




