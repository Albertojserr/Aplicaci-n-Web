from lib.ConexAlchemy import ConexionBD
#vamos a pedir por teclado los datos y los guardamos en variables
Dni= input("DNI:")
nombre= input("Nombre:")
apellidos= input("Apellidos:")
comunidad_autonoma= input("Comunidad autonoma:")
provincia= input("Provincia:")
ciudad= input("Ciudad:")
direccion= input("Dirección:")
codigo= input("Código de la asignatura:")
nota=int(input("Nota (0-100):"))

conexion = ConexionBD()
conexion.conectar(dni=Dni, nombre=nombre, apellidos=apellidos, comunidad=comunidad_autonoma, provincia=provincia, ciudad=ciudad, direccion=direccion, codasignatura=codigo, nota=nota)
conexion.cerrar()