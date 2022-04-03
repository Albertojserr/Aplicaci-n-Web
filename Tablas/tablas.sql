Hacer esto dentro de postgres -> psql

create user usrpractica with encrypted password 'pw2203';

create database dbpractica owner usrpractica;

\c dbpractica

create table CAutonoma (
codigo serial primary key not null,
nombre text not null,
bnombre varchar(100) not null
);

create table Provincia (
codigo serial primary key not null,
nombre text not null,
cautonoma smallint references CAutonoma(codigo) not null,
bnombre varchar(100) not null
);


create table Ciudad (
codigo serial primary key not null,
nombre text not null,
provincia smallint references Provincia(codigo) not null,
bnombre varchar(100) not null
);

create table Alumno (
dni varchar(9) primary key not null,
apellidos text not null,
nombre text not null,
direccion text not null,
ciudad smallint references Ciudad(codigo) not null
);

create table  Asignatura (
codigo varchar(9) primary key not null,
nombre text not null
);

create table  Alumno_Asignatura (
codigo varchar(9) references Asignatura(codigo) not null,
dni varchar(9) references Alumno(dni) not null,
nota smallint not null 
);
La nota es entera sobre 100.

Insertamos las asignaturas que ya están en nuestra base de datos.

insert into Asignatura(codigo,nombre) values ('000242305','Cálculo integral');
insert into Asignatura(codigo,nombre) values ('000242306','Comunicación Técnica en Inglés');
insert into Asignatura(codigo,nombre) values ('000242307','Ecuaciones en Derivadas Parciales');
insert into Asignatura(codigo,nombre) values ('000242308','Introducción a la Programación Paralela y Distribuida');
insert into Asignatura(codigo,nombre) values ('000242309','Métodos numéricos');

Dar permisos al usuario:

GRANT ALL ON CAutonoma TO usrpractica;
GRANT ALL ON Provincia TO usrpractica;
GRANT ALL ON Ciudad TO usrpractica;
GRANT ALL ON Alumno TO usrpractica;
GRANT ALL ON Asignatura TO usrpractica;
GRANT ALL ON Alumno_Asignatura TO usrpractica;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usrpractica;

