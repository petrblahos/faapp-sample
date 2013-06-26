# subscribers.py

from pyramid.i18n import get_localizer, TranslationStringFactory

def add_renderer_globals(event):
    request = event['request']
    event['_'] = request.translate
    event['localizer'] = request.localizer

tsf = TranslationStringFactory('faapp')

def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)
    def auto_translate(*args, **kwargs):
        return localizer.translate(tsf(*args, **kwargs))
    request.localizer = localizer
    request.translate = auto_translate

def includeme(config):
    config.add_translation_dirs('faapp:locale')
    config.add_subscriber('faapp.locale.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('faapp.locale.add_localizer', 'pyramid.events.NewRequest')

