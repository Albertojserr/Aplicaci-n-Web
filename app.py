import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
#contenido de la pagina, la aplicación
#form es la plantilla de la pagina html
from colander import (
    Boolean,
    Integer,
    Length,
    MappingSchema,
    OneOf,
    SchemaNode,
    SequenceSchema,
    String
)

from deform import (
    Form,
    ValidationFailure,
    widget
)

from deform.widget import OptGroup

from lib.ConexAlchemy import ConexionBD
here = os.path.dirname(os.path.abspath(__file__))


conexion = ConexionBD()
aComunidades = conexion.rComunidades()
aProvincias = conexion.rProvincia()
aCiudades = conexion.rCiudad()
aAsignaturas = conexion.rAsignatura()
conexion.cerrar()

occaa = [ ['0', '- Selecciona -'] ]
gprov = [ ['0', '- Selecciona -'] ]
gciud = [ ['0', '- Selecciona -'] ]
oasig = [ ['0', '- Selecciona -'] ]


for comunidad in aComunidades:
    occaa.append([comunidad.bnombre, comunidad.nombre])

aux = ""
grupo=[]


for pnombre, pbnombre, Cnombre in aProvincias:
    if aux != Cnombre:
        if aux != "":
            gprov.append(OptGroup(aux, *grupo))
        aux = Cnombre
        grupo=[]
    grupo.append([pbnombre, pnombre])

if aux != "":
    gprov.append(OptGroup(aux, *grupo))


aux = ""
grupo=[]
for cnombre, cbnombre, pnombre in aCiudades:
    if aux != pnombre:
        if aux != "":
            gciud.append(OptGroup(aux, *grupo))
        aux = pnombre
        grupo=[]
    grupo.append([cbnombre, cnombre])


if aux != "":
    gciud.append(OptGroup(aux, *grupo))


for asignatura in aAsignaturas:
    oasig.append([asignatura.codigo, asignatura.nombre])

class DateSchema(MappingSchema):
    year = SchemaNode(Integer())
    month = SchemaNode(Integer())
    day = SchemaNode(Integer())

class DatesSchema(SequenceSchema):
    date = DateSchema()

class MySchema(MappingSchema):
    nombre = SchemaNode(String(),
                    description = 'Nombre del alumno')
    apellidos = SchemaNode(String(),
                    description = 'Apellidos del alumno')
    dni = SchemaNode(String(),
                    description = 'DNI del alumno')
    comunidad = SchemaNode(String(), description = 'Comunidad Autónoma', widget = widget.Select2Widget(values=occaa, tags=True))

    provincia = SchemaNode(String(), description = 'Provincia', widget = widget.Select2Widget(values=gprov, tags=True))

    ciudad = SchemaNode(String(), description = 'Ciudad', widget = widget.Select2Widget(values=gciud, tags=True))

    direccion = SchemaNode(String(), description = 'Dirección del alumno')

    asignatura = SchemaNode(String(), description = 'Asignatura', widget = widget.Select2Widget(values=oasig))

    nota = SchemaNode(Integer(), description = 'Nota del alumno (0-100)' )

def form_view(request):
    schema = MySchema()
    myform = Form(schema, buttons=('submit',))
    template_values = {}
    template_values.update(myform.get_widget_resources())

    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            appstruct=myform.validate(controls)
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            conexion = ConexionBD()
            conexion.conectar(appstruct['dni'],appstruct['nombre'],appstruct['apellidos'],appstruct['comunidad'], appstruct['provincia'], appstruct['ciudad'], appstruct['direccion'], appstruct['asignatura'],appstruct['nota'])
            conexion.cerrar()
            valores = appstruct['nombre'] + " " + appstruct['apellidos'] + ". " + appstruct['comunidad'] + " - " + appstruct['provincia'] + " - " + appstruct['ciudad']
            template_values['form'] = valores  + ' <a href="http://localhost:8080">Volver</a>'
        return template_values

    template_values['form'] = myform.render()
    return template_values

if __name__ == '__main__':
    settings = dict(reload_templates=True)
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_view(form_view, renderer=os.path.join(here, 'form.pt'))
    config.add_static_view('static', 'deform:static')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
