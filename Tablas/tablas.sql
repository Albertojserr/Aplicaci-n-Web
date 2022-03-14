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


create table Calle (
codigo serial primary key not null,
nombre text not null,
ciudad smallint references Ciudad(codigo) not null,
bnombre varchar(100) not null
);

insert into CAutonoma(nombre, bnombre) values ('Madrid', 'madrid');
insert into CAutonoma(nombre, bnombre) values ('Castilla La Mancha', 'castillamancha');
insert into Provincia(nombre, bnombre, cautonoma) values ('Madrid', 'madrid', 1);
insert into Ciudad(nombre, bnombre, provincia) values ('Madrid', 'madrid', 1);
insert into Calle(nombre, bnombre, ciudad) values ('Gran Vía', 'granvia', 1);

