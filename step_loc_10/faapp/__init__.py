from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('top', '/', factory="faapp.model.resources.TopContext", )

    config.add_route("list", "/list/{model}", factory="faapp.model.resources.OrmContext", )
    config.add_route("edit", "/edit/{model}", factory="faapp.model.resources.OrmContext", )
    config.add_route("delete", "/delete/{model}", factory="faapp.model.resources.OrmContext", )

    config.include("faapp.locale")
    config.include("faapp.model")

    config.scan()
    return config.make_wsgi_app()

