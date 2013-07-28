from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('top', '/')

    config.add_route("list", "/list/{model}", )
    config.add_route("edit", "/edit/{model}", )
    config.add_route("delete", "/delete/{model}", )

    config.include("faapp.locale")
    config.include("faapp.model")

    config.scan()
    return config.make_wsgi_app()

