from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import os

root = Tk()
root.configure(background='#6E6C63')
root.title('Libro Virtual Guardias')

#funciones

def inicio():
    top = Toplevel()
    top.geometry('400x150')
    top.configure(background='#6E6C63')

    #entrys para iniciar
    instalacion = Entry(top, width=100, background='#EAD36E', font=('Arial', 12))
    instalacion.insert(0, 'Instalacion: ')
    instalacion.pack(padx=2, pady=3)
    #entry para indicar la empresa de seguridad
    seguridad = Entry(top, width=100, background='#EAD36E', font=('Arial', 12))
    seguridad.insert(0, 'Seguridad: ')
    seguridad.pack(padx=2, pady=3)
    #entry para indicar de que hora hasta que hora se trabaja
    turno = Entry(top, width=100, background='#EAD36E', font=('Arial', 12))
    turno.insert(0, 'Turno: ')
    turno.pack(padx=2, pady=3)
    #Nombre del guardia de seguridad
    ggss = Entry(top, width=100, background='#EAD36E', font=('Arial', 12))
    ggss.insert(0, 'GGSS: ')
    ggss.pack(padx=2, pady=3)

    iniciar = Button(top, text='Agregar', font=('NORMAL', 12), command=lambda:comenzarTurno(instalacion, seguridad, turno, ggss, top), background='#E6C327')
    iniciar.pack()

def comenzarTurno(instalacion, seguridad, turno, ggss, top):
    os.makedirs("LibroVirtualGGSS/libro", exist_ok=True)

    instalacion = instalacion.get()
    seguridad = seguridad.get()
    turno = turno.get()
    ggss = ggss.get()

    insa.set(instalacion)
    insb.set(seguridad)
    insc.set(turno)
    insd.set(ggss)
    dia = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')

    global id, comienzo

    if (comienzo):
        file = open('libro/{}.txt'.format(id), 'r+')
        file.seek(2) 
        file.write(f' Fecha:{dia} (Inicio de turno)\n {instalacion}\n {seguridad}\n {turno}\n {ggss}')
        file.close()
    else:
        id = datetime.datetime.now().strftime('%d.%m.%y-%H')
        file = open('LibroVirtualGGSS/Libro/{}.txt'.format(id), 'w')
        file.write(f' Fecha:{dia} (Inicio de turno)\n {instalacion}\n {seguridad}\n {turno}\n {ggss}')
        file.close()
        top.destroy()
        comienzo = True

def agregarRonda():
    top = Toplevel()
    top.geometry('450x90')
    top.configure(background='#6E6C63')

    #entrys para agregar ronda
    act = Label(top, text='Actividad', font=('Arial', 10), background='#6E6C63')
    actividad = Entry(top, width=100, background='#EAD36E', font=('Arial', 10))
    act.grid(padx=0, pady=3, row=1, column=1)
    actividad.grid(row=1, column=2)

    obs = Label(top, text='Observacion', font=('Arial', 10), background='#6E6C63')
    observacion = Entry(top, width=100, background='#EAD36E', font=('Arial', 10))
    obs.grid(padx=0, pady=3, row=2, column=1)
    observacion.grid(row=2, column=2)

    boton = Button(top, text='Agregar', command=lambda:listar(actividad, observacion, top), font=('Arial', 10), background='#E6C327', borderwidth=0)
    boton.grid(row=3, column=1)

def listar(actividad, observacion, top):
    global contador, id
    existe = os.path.exists('LibroVirtualGGSS/Libro/{}.txt'.format(id))

    if(existe):
        contador += 1
        hora_actual = datetime.datetime.now().strftime('%H:%M')

        file = open('LibroVirtualGGSS/Libro/{}.txt'.format(id), 'a')
        file.write(f'\n{hora_actual} | {actividad.get()}| {observacion.get()}|')
        file.close()

        
        tabla.insert('', END, values=(hora_actual, actividad.get(), observacion.get()))
        tabla.insert('', END, values=('-------------', '-----------------------', f'------------------------------------------------------------- {contador} -----------------------------------------------------------'))

        top.destroy()

    else:
        messagebox.showerror('error', 'Primero Inicie')

def libro():

    libro = os.path.join(os.path.dirname(__file__),'libro')

    with os.scandir(libro) as jornadas:
        jornadas = [jornadas.name for jornadas in jornadas if jornadas.is_file()]
    
    top = Toplevel()
    top.geometry('200x100')
    top.configure(background='#6E6C63')

    value = StringVar()
    value.set(jornadas[0])

    drop = OptionMenu(top, value, *jornadas)
    drop.pack()
    
    boton = Button(top, text='Ver', command=lambda:verLibro(libro ,value.get()), font=('Arial', 12), background='#E6C327')
    boton.pack()


def verLibro(libro,archivo):
    top = Toplevel()
    top.geometry('800x300')
    top.configure(background='#6E6C63')

    tabla = ttk.Treeview(top)
    tabla['columns'] = ('Hora', 'Actividad', 'Observaciones',) # Definicion de la columns
    # Definicion de los indices
    tabla.column('#0', width=0, stretch=NO)
    tabla.column('Hora', width=80)
    tabla.column('Actividad', width=120)
    tabla.column('Observaciones', width=500)

    tabla.heading('#0')
    tabla.heading('Hora', text='Hora')
    tabla.heading('Actividad', text='Actividad')
    tabla.heading('Observaciones', text='Observaciones')
    tabla.pack()

    file = open(f'{libro}/{archivo}', 'r')
    lineas = file.readlines()
    contador = 0
    rondas = -5

    for linea in lineas:
        contador += 1
        rondas += 1
        if( 1 <= contador <= 5 ):
            tabla.insert('', END, values=('', '', linea))
        elif(contador > 5):
            campos = linea.split('|')
            tabla.insert('', END, values=(campos[0],campos[1], campos[2]))
            tabla.insert('', END, values=('-------------', '---------------------', f'------------------------------------------------ {rondas} ------------------------------------------------'))

def terminar():
    if (comienzo):
        respuesta = messagebox.askokcancel('Termino de Jornada', '¿Desea realizar entrega?')
        if(respuesta):
            hora = datetime.datetime.now().strftime('%H:%M')
            file = open('LibroVirtualGGSS/Libro/{}.txt'.format(id), 'a')
            file.write(f'\n{hora}| Entrega| Se hace termino de jornada')
            file.close()
            root.quit()
        else:
            messagebox.showerror('error', 'Primero Inicie')
        
    

#configuracion de root

titulo = Label(root, text='Libro Virtual', background='#6E6C63', font=('Arial', 20))
titulo.pack()
#contenedor informacion de instalacion y guardiar
contador = 0
comienzo = False
id = ''
insa = StringVar()
insb = StringVar()
insc = StringVar()
insd = StringVar()

detalles = LabelFrame(root)
detalles.configure(background='#6E6C63', borderwidth=0)

instalacion = Label(detalles, textvariable=insa,background='#6E6C63', font=('Arial', 12), width=10)
seguridad = Label(detalles, textvariable=insb,background='#6E6C63', font=('Arial', 12))
turno = Label(detalles, textvariable=insc,background='#6E6C63', font=('Arial', 12))
ggss = Label(detalles, textvariable=insd,background='#6E6C63', font=('Arial', 12))

detalles.pack()

instalacion.grid(row=1, column=1)
seguridad.grid(row=2, column=1)
turno.grid(row=1, column=2)
ggss.grid(row=2, column=2)

# contenedor de todo el libro
cuadrado = Frame(root, padx=10, pady=10)
cuadrado.pack()
cuadrado.configure(background='#6E6C63')

btn_start = Button(cuadrado, text='Inicio', command=inicio, font=('Arial', 12), background='#E6C327')
btn_start.grid(column=1, row=2, padx=10, pady=10)

btn_book = Button(cuadrado, text='Libro', command=libro, font=('Arial', 12), background='#E6C327')
btn_book.grid(column=2, row=2)

tabla = ttk.Treeview(cuadrado)
tabla['columns'] = ('Hora', 'Actividad', 'Observaciones',) # Definicion de la columns
# Definicion de los indices
tabla.column('#0', width=0, stretch=NO)
tabla.column('Hora', width=60)
tabla.column('Actividad', width=100)
tabla.column('Observaciones', width=500)

tabla.heading('#0')
tabla.heading('Hora', text='Hora')
tabla.heading('Actividad', text='Actividad')
tabla.heading('Observaciones', text='Observaciones')

tabla.grid(row=3, column=2)

# Boton ronda y termino de ronda
btn_ronda = Button(cuadrado, text='Ronda', command=lambda:agregarRonda(), font=('Arial', 12), background='#E6C327')
btn_ronda.grid(row=4, column=2, pady=5)

btn_entrega = Button(cuadrado, text='Entrega', command=terminar, font=('Arial', 12), background='#E6C327')
btn_entrega.grid(row=4, column=3)

root.mainloop()