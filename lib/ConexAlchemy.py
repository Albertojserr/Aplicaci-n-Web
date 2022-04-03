from sqlalchemy import Column, String, Integer, SmallInteger,create_engine, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# Cree la clase base del objeto:
Base = declarative_base()


def normaliza(texto):
    aux = texto.lower()
    eliminar = { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", " de ": "", " en ": "", " la ": "", " el ": "", " del ": "",  " y ": "", " a ": "" }
    for k, v in eliminar.items():
        aux = aux.replace(k, v)
    aux = aux.replace(" ", "")
    return aux

# Definir objeto de usuario:
class CAutonoma(Base):
    # Nombre de la tabla
    __tablename__ = 'cautonoma'

    # Estructura de la tabla
    codigo = Column(Integer(), primary_key=True)
    nombre = Column(String(100))
    bnombre = Column(String(100))


# Definir objeto de usuario:
class Provincia(Base):
    # Nombre de la tabla
    __tablename__ = 'provincia'

    # Estructura de la tabla
    codigo = Column(Integer(), primary_key=True)
    nombre = Column(String(100))
    cautonoma=Column(SmallInteger(), ForeignKey('cautonoma.codigo'))
    bnombre = Column(String(100))

class Ciudad(Base):
    # Nombre de la tabla
    __tablename__ = 'ciudad'

    # Estructura de la tabla
    codigo = Column(Integer(), primary_key=True)
    nombre = Column(String(100))
    provincia=Column(SmallInteger(), ForeignKey('provincia.codigo'))
    bnombre = Column(String(100))

class Alumno(Base):
    # Nombre de la tabla
    __tablename__ = 'alumno'

    # Estructura de la tabla
    dni = Column(String(9), primary_key=True)
    apellidos = Column(String(100))
    nombre = Column(String(100))
    direccion = Column(String(100))
    ciudad=Column(SmallInteger(), ForeignKey('ciudad.codigo'))

class Asignatura(Base):
    # Nombre de la tabla
    __tablename__ = 'asignatura'

    # Estructura de la tabla
    codigo = Column(Integer(), primary_key=True)
    nombre = Column(String(100))

class Alumno_Asignatura(Base):
    # Nombre de la tabla
    __tablename__ = 'alumno_asignatura'

    # Estructura de la tabla
    codigo = Column(Integer(),ForeignKey('asignatura.codigo'), primary_key=True)
    dni = Column(String(9),ForeignKey('alumno.dni'))
    nota =Column(Float())

class ConexionBD():
    def __init__(self):
        connect_args = {
        'user': 'usrpractica',
        'password': 'pw2203',
        'database': 'dbpractica',
        'host': '127.0.0.1',
        'port': 5432
        }
        engine = create_engine('postgresql+psycopg2://',connect_args=connect_args)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    def añadir(self,objeto):
        self.session.add(objeto)
        self.session.commit()
    def cerrar(self):
        self.session.close()
    def rComunidades(self):
        return self.session.query(CAutonoma).order_by(CAutonoma.nombre).all()
    def rProvincia(self):
        return self.session.query(Provincia.nombre, Provincia.bnombre, CAutonoma.nombre).join(CAutonoma).order_by(CAutonoma.nombre).order_by(Provincia.nombre).all()
        #return self.session.query(Provincia).all()
    def rCiudad(self):
        return self.session.query(Ciudad.nombre, Ciudad.bnombre, Provincia.nombre).join(Provincia).order_by(Provincia.nombre).order_by(Ciudad.nombre).all()
    def rAsignatura(self):
        return self.session.query(Asignatura).order_by(Asignatura.codigo).all()

    def rAsignaturasAlumno(self, alumno):
        return self.session.query(Alumno_Asignatura.nota, Asignatura.codigo, Asignatura.nombre).join(Asignatura).order_by(Asignatura.codigo).all()

    def buscarAsignaturaAlumno(self, dni, asignatura):
        lista=self.session.query(Alumno_Asignatura).filter_by(dni=dni, codigo=asignatura).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None

    def buscarAlumno(self, dni):
        lista=self.session.query(Alumno).filter_by(dni=dni).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None


    def buscarComunidad(self,Bnombre):
        lista=self.session.query(CAutonoma).filter_by(bnombre=Bnombre).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None
    def buscarProvincia(self,Bnombre):
        lista=self.session.query(Provincia).filter_by(bnombre=Bnombre).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None
    def buscarCiudad(self,Bnombre):
        lista=self.session.query(Ciudad).filter_by(bnombre=Bnombre).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None

    def buscarAsignatura(self,codigo):
        lista=self.session.query(Asignatura).filter_by(codigo=codigo).all()
        if len(lista)>0:
            return lista[0]
        else:
            return None


    def conectar(self,dni, nombre, apellidos, comunidad, provincia, ciudad, direccion, codasignatura, nota):
        bcomunidad = normaliza(comunidad)
        bprovincia = normaliza(provincia)
        bciudad = normaliza(ciudad)
        oComunidad = self.buscarComunidad(bcomunidad)
        dni=dni.upper()
        if oComunidad == None:
            self.añadir(CAutonoma(nombre=comunidad,bnombre=bcomunidad))
            oComunidad = self.buscarComunidad(bcomunidad)
        oProvincia = self.buscarProvincia(bprovincia)
        if oProvincia == None:
            self.añadir(Provincia(nombre=provincia,cautonoma=oComunidad.codigo,bnombre=bprovincia))
            oProvincia = self.buscarProvincia(bprovincia)
        oCiudad = self.buscarCiudad(bciudad)
        if oCiudad == None:
            self.añadir(Ciudad(nombre=ciudad,provincia=oProvincia.codigo,bnombre=bciudad))
            oCiudad = self.buscarCiudad(bciudad)
        oAlumno = self.buscarAlumno(dni)
        if oAlumno == None:
            self.añadir(Alumno(dni=dni, nombre=nombre, apellidos=apellidos, ciudad=oCiudad.codigo, direccion=direccion))
            oAlumno = self.buscarAlumno(dni)

        oasignatura = self.buscarAsignatura(codasignatura)
        if oasignatura != None:
            oasignaturaalumno = self.buscarAsignaturaAlumno(dni, codasignatura)
            if oasignaturaalumno == None:
                self.añadir(Alumno_Asignatura(dni=dni, codigo=oasignatura.codigo, nota=nota))
