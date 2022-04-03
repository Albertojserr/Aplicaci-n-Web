import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from numpy import argpartition
from lib.ConexAlchemy import ConexionBD

class Ventana(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.cargadatos()
        self.title("Alumnos")
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
        self.lbldni = Label(self, text="DNI del alumno")
        self.dni = ttk.Entry(validate="key",  validatecommand=(self.register(self.validadni), "%S", "%P"))
        self.lbldni.grid(column=0, row=0)
        self.dni.grid(column=1, row=0, sticky=E+W)

        self.framealumno = ttk.Frame(self)
        self.creaCamposAlumno("", "")
        self.framealumno.grid(column=0, row=1, columnspan=3)
        self.frameasignaturas = ttk.Frame(self)
        self.btninserta = ttk.Button(self.frameasignaturas, text="Inserta", command=self.inserta)
        self.creaccaa()
        self.creaprov([])
        self.creaciudad([])
        self.frameasignaturas.grid(column=0, row=2, columnspan=3)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.mainloop()

    def cargadatos(self):
        self.conexion= ConexionBD()
        self.aComunidades = self.conexion.rComunidades()
        self.aProvincias = self.conexion.rProvincia()
        self.aCiudades = self.conexion.rCiudad()
        self.aAsignaturas = self.conexion.rAsignatura()
        self.conexion.cerrar()

        self.accaa = []
        for comunidad in self.aComunidades:
            self.accaa.append(comunidad.nombre)


        self.aprov=[]
        aux = ""
        grupo=[]
        for pnombre, pbnombre, Cnombre in self.aProvincias:
            if Cnombre != aux:
                if aux !="":
                    self.aprov.append({ "ccaa": aux, "provincias": grupo })
                aux = Cnombre
                grupo = []
                grupo.append(pnombre)
            else:
                grupo.append(pnombre)
        self.aprov.append({ "ccaa": aux, "provincias": grupo })

        self.aciud=[]
        aux = ""
        grupo=[]
        for cnombre, cbnombre, pnombre in self.aCiudades:
            if pnombre != aux:
                if aux !="":
                    self.aciud.append({ "provincia": aux, "ciudades": grupo })
                aux = pnombre
                grupo = []
                grupo.append(cnombre)
            else:
                grupo.append(cnombre)
        self.aciud.append({ "provincia": aux, "ciudades": grupo })


        self.oasig=[]
        for asignatura in self.aAsignaturas:
            self.oasig.append(asignatura.codigo + " - " + asignatura.nombre)


    def creaCamposAlumno(self, nombre, apellidos):
        self.lblnombre = Label(self.framealumno, text="Nombre del alumno")
        self.nombre = ttk.Entry(self.framealumno)
        self.lblapellidos = Label(self.framealumno, text="Apellidos del alumno")
        self.apellidos = ttk.Entry(self.framealumno)
        if nombre != "":
            self.nombre.insert(0, nombre)
        if apellidos != "":
            self.apellidos.insert(0, apellidos)
        self.lblnombre.grid(column=0, row=0)
        self.nombre.grid(column=1, row=0, columnspan=2, sticky=E+W)
        self.lblapellidos.grid(column=0, row=1)
        self.apellidos.grid(column=1, row=1, columnspan=2, sticky=E+W)

    def creaccaa(self, ccaa=""):
        self.lblccaa = Label(self.framealumno, text="Comunidad autónoma")
        self.ccaa = ttk.Combobox(self.framealumno, values = self.accaa)
        self.ccaa.bind('<<ComboboxSelected>>', self.ccaamodif)
        self.ccaa.bind("<Return>", self.ccaamodif)
        self.lblccaa.grid(column=0, row=2)
        self.ccaa.grid(column=1, row=2, sticky=E+W)
        if ccaa != "":
            i=0
            for eccaa in self.accaa:
                if eccaa == ccaa:
                    self.ccaa.current(i)
                    break
                i=i+1

    def creaprov(self, lprovs, provincia=""):
        self.lblprov = Label(self.framealumno, text="Provincias")
        self.provincia = ttk.Combobox(self.framealumno, values = lprovs)
        self.provincia.bind('<<ComboboxSelected>>', self.provmodif)
        self.provincia.bind("<Return>", self.provmodif)
        self.lblprov.grid(column=0, row=3)
        self.provincia.grid(column=1, row=3, columnspan=2, sticky=E+W)
        if provincia != "":
            i=0
            for prov in lprovs:
                if prov == provincia:
                    self.provincia.current(i)
                    break
                i=i+1

    def creaciudad(self, lciuds, ciudad=""):
        self.lblciud = Label(self.framealumno, text="Ciudades")
        self.ciudad = ttk.Combobox(self.framealumno, values = lciuds)
        self.ciudad.bind('<<ComboboxSelected>>', self.ciumodif)
        self.ciudad.bind("<Return>", self.ciumodif)
        self.lblciud.grid(column=0, row=4)
        self.ciudad.grid(column=1, row=4, columnspan=2, sticky=E+W)
        if ciudad != "":
            i=0
            for ciud in lciuds:
                if ciud == ciudad:
                    self.ciudad.current(i)
                    break
                i=i+1
        self.lbldireccion = Label(self.framealumno, text="Dirección")
        self.direccion = ttk.Entry(self.framealumno)
        self.lbldireccion.grid(column=0, row=5)
        self.direccion.grid(column=1, row=5, columnspan=2, sticky=E+W)
        self.creacamposasignatura()

    def creacamposasignatura(self):
        self.lblasignatura = Label(self.frameasignaturas, text="Asignatura")
        self.lblnotaasignatura = Label(self.frameasignaturas, text="Nota")
        self.codigoasignatura = ttk.Combobox(self.frameasignaturas, values = self.oasig)
        self.notaasignatura = ttk.Entry(self.frameasignaturas)
        self.lblasignatura.grid(column=0, row=0, columnspan=2)
        self.lblnotaasignatura.grid(column=2, row=0)
        self.codigoasignatura.grid(column=0, row=1, columnspan=2)
        self.notaasignatura.grid(column=2, row=1)
        self.btninserta.grid(column=0, row=2,columnspan=3)

    def ccaamodif(self, evento):
        if self.ccaa.current() == -1:
            ccaa = self.ccaa.get()
            self.accaa.append(ccaa)
            self.creaccaa(ccaa)

        lprovs = []
        hayccaa = False
        for provincia in self.aprov:
            if provincia["ccaa"] == self.ccaa.get():
                lprovs = provincia["provincias"]
                hayccaa = True
                break
        if hayccaa == False:
            self.aprov.append( { "ccaa" : self.ccaa.get(), "provincias": [] })
        self.creaprov(lprovs)

    def provmodif(self, evento):
        if self.provincia.current() == -1:
            hayprov = False
            for provincia in self.aprov:
                if provincia["ccaa"] == self.ccaa.get():
                    provincia["provincias"].append(self.provincia.get())
                    self.creaprov(provincia["provincias"], self.provincia.get())
                    hayprov = True
                    break
            if hayprov == False:
                self.aprov.append( { "ccaa" : self.ccaa.get(), "provincias": [ self.provincia.get() ] })
                self.creaprov([ self.provincia.get() ], self.provincia.get())
        lciuds = []
        for ciudad in self.aciud:
            if ciudad["provincia"] == self.provincia.get():
                lciuds = ciudad["ciudades"]
                break
        self.creaciudad(lciuds)

    def ciumodif(self, evento):
        if self.ciudad.current() == -1:
            hayciud = False
            for ciudad in self.aciud:
                if ciudad["provincia"] == self.provincia.get():
                    ciudad["ciudades"].append(self.ciudad.get())
                    self.creaciudad(ciudad["ciudades"], self.ciudad.get())
                    hayciud = True
                    break
            if hayciud == False:
                self.aciud.append( {"provincia" : self.provincia.get(), "ciudades" : [ self.ciudad.get()] })
                self.creaciudad([ self.ciudad.get()], self.ciudad.get())



    def validadni(self, texto, textoexistente):
        if len(textoexistente)>9:
            return False
        if len(textoexistente)==9:
            if textoexistente[8].isalpha() == False:
                return False
        elif len(textoexistente)<9:
            if textoexistente != "" and textoexistente.isdecimal()==False:
                return False
        return True

    def inserta(self):
        if self.dni.get() =="" or self.nombre.get() =="" or self.apellidos.get() =="" or self.ccaa.get() =="" or self.provincia.get() =="" or self.ciudad.get() =="" or self.direccion.get() =="" or self.codigoasignatura.get()=="" or self.notaasignatura.get() =="":
            messagebox.showwarning(message="No se han rellenado todos los campos", title="Falta de datos")
        else:
            self.conexion = ConexionBD()
            self.conexion.conectar(self.dni.get(),self.nombre.get(),self.apellidos.get(),self.ccaa.get(), self.provincia.get(), self.ciudad.get(), self.direccion.get(),self.codigoasignatura.get().split(" - ")[0],self.notaasignatura.get())
            self.conexion.cerrar()
            self.cargadatos()
            self.codigoasignatura.delete(0,END)
            self.notaasignatura.delete(0,END)

    def ocultar(self):
        self.withdraw()

    def mostrar(self):
        self.deiconify()

if __name__ == '__main__':
    principal = Ventana()