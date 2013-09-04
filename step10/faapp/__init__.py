from pyramid.config import Configurator

from faapp.model.resources import TopContext

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=TopContext)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.include("faapp.locale")
    config.include("faapp.model")

    config.scan()
    return config.make_wsgi_app()

