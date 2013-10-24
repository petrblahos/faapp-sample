# subscribers.py

import os.path

from pyramid.i18n import (
    TranslationStringFactory,
    Translations,
    Localizer,
    get_locale_name,
)
from pyramid.interfaces import (
    ILocalizer,
    ITranslationDirectories,
)
from pyramid.threadlocal import get_current_registry

def add_renderer_globals(event):
    request = event['request']
    event['_'] = request.translate
    event['ungettext'] = request.ungettext
    event['localizer'] = request.localizer

tsf = TranslationStringFactory('faapp')

def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)
    def auto_translate(*args, **kwargs):
        return localizer.translate(tsf(*args, **kwargs))
    def auto_pluralize(*args, **kwargs):
        kwargs.setdefault("domain", "faapp") # or tsf like in auto_translate?
        return localizer.pluralize(*args, **kwargs)
    request.localizer = localizer
    request.translate = auto_translate
    request.ungettext = auto_pluralize
    request.environ['fa.translate'] = auto_translate

def includeme(config):
    config.add_translation_dirs('faapp:locale', 'formalchemy:i18n_resources')
    config.add_subscriber('faapp.locale.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('faapp.locale.add_localizer', 'pyramid.events.NewRequest')

def make_localizer(current_locale_name, translation_directories):
    """ Create a :class:`pyramid.i18n.Localizer` object
    corresponding to the provided locale name from the 
    translations found in the list of translation directories."""
    translations = Translations()
    translations._catalog = {}

    locales_to_try = []
    if '_' in current_locale_name:
        locales_to_try = [current_locale_name.split('_')[0]]
    locales_to_try.append(current_locale_name)

    # intent: order locales left to right in least specific to most specific,
    # e.g. ['de', 'de_DE'].  This services the intent of creating a
    # translations object that returns a "more specific" translation for a
    # region, but will fall back to a "less specific" translation for the
    # locale if necessary.  Ordering from least specific to most specific
    # allows us to call translations.add in the below loop to get this
    # behavior.

    for tdir in translation_directories:
        locale_dirs = []
        for lname in locales_to_try:
            ldir = os.path.realpath(os.path.join(tdir, lname))
            if os.path.isdir(ldir):
                locale_dirs.append(ldir)

        for locale_dir in locale_dirs:
            messages_dir = os.path.join(locale_dir, 'LC_MESSAGES')
            if not os.path.isdir(os.path.realpath(messages_dir)):
                continue
            for mofile in os.listdir(messages_dir):
                mopath = os.path.realpath(os.path.join(messages_dir,
                                                       mofile))
                if mofile.endswith('.mo') and os.path.isfile(mopath):
                    with open(mopath, 'rb') as mofp:
                        domain = mofile[:-3]
                        if "formalchemy"==domain: domain = "faapp"
                        dtrans = Translations(mofp, domain)
                        translations.add(dtrans)

    return Localizer(locale_name=current_locale_name,
                          translations=translations)

def get_localizer(request):
    """ Retrieve a :class:`pyramid.i18n.Localizer` object
    corresponding to the current request's locale name. """
    localizer =  getattr(request, 'localizer', None)

    if localizer is None:
        # no locale object cached on request
        try:
            registry = request.registry
        except AttributeError:
            registry = get_current_registry()

        current_locale_name = get_locale_name(request)
        localizer = registry.queryUtility(ILocalizer, name=current_locale_name)

    if localizer is None:
        # no localizer utility registered yet
        tdirs = registry.queryUtility(ITranslationDirectories, default=[])
        localizer = make_localizer(current_locale_name, tdirs)

        registry.registerUtility(localizer, ILocalizer,
                                 name=current_locale_name)
        request.localizer = localizer

    return localizer



