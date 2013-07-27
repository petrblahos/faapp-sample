import formalchemy
from pyramid.events import NewRequest

import meta

def db(request):
    session = request.registry.sessionmaker()
    def cleanup(request):
        session.close()
    request.add_finished_callback(cleanup)
    return session

def includeme(config):
    settings = config.registry.settings
    config.registry.sessionmaker = meta.create_sessionmaker(settings, "sqlalchemy.")
    config.add_request_method(db, reify=True)

    formalchemy.config.engine = formalchemy.templates.MakoEngine(
            directories=[ "faapp/templates/formalchemy"],
            input_encoding='utf-8',
            output_encoding='utf-8')

