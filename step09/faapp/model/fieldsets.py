import formalchemy


"""
def pylons_formencode_gettext(value):
    ""Translates a string ``value`` using pylons gettext first and if
    that fails, formencode gettext.

    This allows to "merge" localized error messages from built-in
    FormEncode's validators with application-specific validators.

    ""
    trans = pylons_gettext(value)
    if trans == value:
        # translation failed, try formencode
        trans = api._stdtrans(value)
    return trans

def translate_with_fa(txt, request):
    pass
"""


class FieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(FieldSet, self).__init__(model, session, data, prefix, format, request)
        self.active_request = request
        assert request

    def render(self, **kwargs):
        if not "_" in kwargs:
            kwargs["_"] = self.active_request.translate
        if not "request" in kwargs:
            kwargs["request"] = self.active_request
        if not "lang" in kwargs:
            kwargs["lang"] = self.active_request.locale_name
        return super(FieldSet, self).render(**kwargs)


class NonId(FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(NonId, self).__init__(model, session, data, prefix, format, request)
        self.configure(pk=True)

