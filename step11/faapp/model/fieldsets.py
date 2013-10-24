import formalchemy


class FieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(FieldSet, self).__init__(model, session, data, prefix, format, request)
        self.active_request = request
        assert request

    def render(self, **kwargs):
        kwargs.setdefault("_", self.active_request.translate)
        kwargs.setdefault("request", self.active_request)
        kwargs.setdefault("lang", self.active_request.locale_name)
        return super(FieldSet, self).render(**kwargs)


class NonId(FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(NonId, self).__init__(model, session, data, prefix, format, request)
        self.configure(pk=True)

