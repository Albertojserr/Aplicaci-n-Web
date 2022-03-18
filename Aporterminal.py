from lib.ConexAlchemy import ConexionBD
#vamos a pedir por teclado los datos y los guardamos en variables
Dni= input("DNI:")
nombre= input("Nombre:")
apellidos= input("Apellidos:")
comunidad_autonoma= input("Comunidad autonoma:")
provincia= input("Provincia:")
ciudad= input("Ciudad:")
direccion= input("Dirección:")
asignatura= input("Asignatura:")
codigo= int(input("Código de la asignatura:"))
nota=float(input("Nota:"))

conexion = ConexionBD()
conexion.conectar(comunidad_autonoma,provincia,ciudad)
conexion.cerrar()