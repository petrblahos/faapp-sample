import formalchemy
from pyramid.events import NewRequest

import meta

def includeme(config):
    settings = config.registry.settings

    config.registry.settings["dbsession"] = meta.create_session(settings, "sqlalchemy.")

    def add_model(event):
        settings = event.request.registry.settings
        event.request.db = settings["dbsession"]

    config.add_subscriber(add_model, NewRequest)

    formalchemy.config.engine = formalchemy.templates.MakoEngine(
            directories=[ "C:/work/misc/python/PYFA/faapp-sample/step05/faapp/templates/formalchemy"],
            input_encoding='utf-8',
            output_encoding='utf-8')

