# subscribers.py

import os.path

from pyramid.i18n import (
    TranslationStringFactory,
    Translations,
    Localizer,
    get_locale_name,
    get_localizer,
)
from pyramid.interfaces import (
    ILocalizer,
    ITranslationDirectories,
)
from pyramid.threadlocal import get_current_registry

def add_renderer_globals(event):
    """
        Add functions _, ungettext, and localizer to the mako templates.
    """
    request = event['request']
    event['_'] = request.translate
    event['ungettext'] = request.ungettext
    event['localizer'] = request.localizer

tsf = TranslationStringFactory('faapp')

def add_localizer(event):
    """
        Add localizer and supporting functions to the request object.

        Adds request.localizer, and functions translate (which is usually
        mapped to _), ungettext, and sets also environ["fa.translate"]
        function for formalchemy.
    """
    request = event.request
    localizer = get_localizer(request)
    def auto_translate(*args, **kwargs):
        return localizer.translate(tsf(*args, **kwargs))
    def auto_pluralize(*args, **kwargs):
        kwargs.setdefault("domain", "faapp")
        return localizer.pluralize(*args, **kwargs)
    request.localizer = localizer
    request.translate = auto_translate
    request.ungettext = auto_pluralize
    request.environ['fa.translate'] = auto_translate

def includeme(config):
    """
        Initialize the i18n system.
    """
    config.add_translation_dirs('faapp:locale', )
    config.add_subscriber('faapp.locale.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('faapp.locale.add_localizer', 'pyramid.events.NewRequest')
