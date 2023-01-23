from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox
import os


root=Tk()
root.title("APP Desplazamientos")
root.geometry("1550x830")
root.resizable(0,0)

def ver_mapa():
    pass

def insertar():
    pass

def detalle_desplazamiento():
    pass

def detalle_partido():
    pass

path=os.getcwd()

frame_inic=Frame(root, bg="#fb6b69")
frame_inic.pack(fill="both", expand=True)

frame_izq=Frame(frame_inic, bg="#fb6b69")
frame_izq.grid(row=0, column=0, padx=50)

titulo=Label(frame_izq, text="On Tour", bg="#fb6b69", font=("Algerian",115))
titulo.pack(pady=5)

icono_band=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_bandera.png"))

band=Label(frame_izq, image=icono_band, bg="#fb6b69")
band.pack(pady=5)

frame_inicial=Frame(frame_inic, bg="#fb6b69")
frame_inicial.grid(row=0, column=1)

fuente1=Font(family="Nature Beauty", size=38)

frame_top=Frame(frame_inicial,bg="#fb6b69")
frame_top.pack(pady=5)

icono_atm=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_atleti.png"))

atl=Label(frame_top, image=icono_atm, bg="#fb6b69")
atl.pack(pady=5)

estilo=ttk.Style()

estilo.theme_use("alt")

estilo.configure("Treeview", background="lighsilver", foreground="black", rowheight=25)

estilo.configure("Treeview.Heading", font=("Calibri",12, "bold"))

estilo.map("Treeview", background=[("selected","#fb6b69")])

frame_tree=Frame(frame_inicial,bg="#fb6b69")
frame_tree.pack(pady=5)

tree=ttk.Treeview(frame_tree)
tree.pack(pady=5)

tree["columns"]=("Desplazamiento","Equipo","FechaPartido","Ciudad")

tree.column("#0", width=0,stretch=NO)

for i in tree["columns"]:
    tree.column(i, width=150, minwidth=55, anchor=CENTER)
    tree.heading(i, text=i)

frame2=Frame(frame_inicial,bg="#fb6b69")
frame2.pack(pady=5)

icono_mundo=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_mundo.png"))

btn_paises=Button(frame2, image=icono_mundo, command=ver_mapa, bg="#fb6b69", bd=0)
btn_paises.grid(row=0, column=0, padx=(50,70))

icono_maleta=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_database.png"))

btn_insertar=Button(frame2, image=icono_maleta, command=insertar, bg="#fb6b69", bd=0)
btn_insertar.grid(row=0, column=1, padx=(70,30))

lframe=Frame(frame_inicial, bg="#fb6b69")
lframe.pack(pady=10)

lframe1=LabelFrame(lframe, text=" Detalle del Desplazamiento ", font=("Calibri", 16, "bold"), bg="#fb6b69")
lframe1.grid(row=0, column=0, padx=20, pady=5)

icono_estadio=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_estadio.png"))

btn_detalle=Button(lframe1, image=icono_estadio, command=detalle_desplazamiento, bg="#fb6b69", bd=0)
btn_detalle.pack(padx=20, pady=5)

lframe2=LabelFrame(lframe, text=" Detalle del Partido ", font=("Calibri", 16, "bold"), bg="#fb6b69")
lframe2.grid(row=0, column=1, padx=20, pady=5)

icono_balon=PhotoImage(file=os.path.join(path,"Archivos Extra\Iconos\icono_balon.png"))

btn_detalle_ciu=Button(lframe2, image=icono_balon, command=detalle_partido, bg="#fb6b69", bd=0)
btn_detalle_ciu.pack(padx=20, pady=5)


root.mainloop()




