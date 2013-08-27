import formalchemy
import faapp.model.tools


class FieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(FieldSet, self).__init__(model, session, data, prefix, format, request)
        self.active_request = request
        assert request

    def render(self, **kwargs):
        kwargs.setdefault("_", self.active_request.translate)
        kwargs.setdefault("ungettext", self.active_request.ungettext)
        kwargs.setdefault("request", self.active_request)
        kwargs.setdefault("lang", self.active_request.locale_name)
        return super(FieldSet, self).render(**kwargs)


class NonId(FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(NonId, self).__init__(model, session, data, prefix, format, request)
        self.configure(pk=True)

class Person(FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(Person, self).__init__(model, session, data, prefix, format, request)
        self.configure(options=[ self.number.validate(faapp.model.tools.even), ])


