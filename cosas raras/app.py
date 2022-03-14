import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator

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


here = os.path.dirname(os.path.abspath(__file__))

"""colors = (('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'))"""

occaa = ( ('0', '- Selecciona -'), ('1', 'Madrid'), ('2', 'Castilla La Mancha') )
oprov = ( ('0', '- Selecciona -'), ('1', 'Madrid'), ('2', 'Toledo'), ('3', 'Cuenca') )
ociud = ( ('0', '- Selecciona -'), ('1', 'Madrid'), ('2', 'Getafe'), ('3', 'Toledo'), ('4', 'Cuenca') )

class Datos:
    def __init__(self,nombre,apellidos):
        self.nombre=nombre
        self.apellidos=apellidos
    def sacarvalores(self):
        return (self.nombre + " " + self.apellidos)
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
    DNI = SchemaNode(String(),validator = Length(max=9),
                      description = 'DNI del alumno')
    comunidad = SchemaNode(String(), description = 'Comunidad Autónoma', widget = widget.Select2Widget(values=occaa))
    
    provincia = SchemaNode(String(), description = 'Provincia', widget = widget.Select2Widget(values=oprov))
    
    ciudad = SchemaNode(String(), description = 'Ciudad', widget = widget.Select2Widget(values=ociud))
    """title = SchemaNode(String(),
                       widget = widget.TextInputWidget(size=40),
                       validator = Length(max=20),
                       description = 'A very short title')
    password = SchemaNode(String(),
                          widget = widget.CheckedPasswordWidget(),
                          validator = Length(min=5))
    is_cool = SchemaNode(Boolean(),
                         default = True)
    dates = DatesSchema()
    color = SchemaNode(String(),
                       widget = widget.RadioChoiceWidget(values=colors),
                       validator = OneOf(('red', 'blue')))"""

def form_view(request):
    schema = MySchema()
    myform = Form(schema, buttons=('submit','clear'))
    template_values = {}
    template_values.update(myform.get_widget_resources())
    caracteristicas=['nombre','apellidos','DNI','comunidad','provincia','ciudad']
    datos={ "nombre": "", 'apellidos': "",'DNI': "",'comunidad': "",'provincia': "",'ciudad': ""}
    if 'submit' in request.POST:
        controls = request.POST.items()
        
        for item in controls:
            if item[0] in caracteristicas:
                datos[item[0]]=item[1]
                #print(item[0] + " " + item[1])
                #print(datos)
        try:
            myform.validate(controls)
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            #print(datos['nombre']+ ' ' + datos['apellidos'])
            template_values['form'] = ' <a href="http://localhost:8080">Volver</a>'
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
