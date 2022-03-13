
"""
1. Run `env/bin/pip install pyramid_jinja2`
2. Copy this template and put it in `templates/home.jinja2`:

<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ saludos }}</title>
</head>
<body>
<h1>{{ greet }}, {{ saludos }}</h1>
</body>
</html>
"""
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config


@view_config(
    route_name='home',
    renderer='templates/home.jinja2'
)
def home(request):
    return {"valor1": 'Nombre', "valor2": 'Apellidos',"Cuestionario":'Cuestionario'}

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_route('home', '/')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

