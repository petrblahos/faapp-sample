import formalchemy

class Grid(formalchemy.Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(Grid, self).__init__(cls, instances, session, data, request, prefix)
        self.active_request = request
        assert request
        self.configure(readonly=True)

    def render(self, **kwargs):
        kwargs.setdefault("_", self.active_request.translate)
        kwargs.setdefault("ungettext", self.active_request.ungettext)
        kwargs.setdefault("request", self.active_request)
        kwargs.setdefault("lang", self.active_request.locale_name)
        return super(Grid, self).render(**kwargs)


class NonId(Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(NonId, self).__init__(cls, instances, session, data, request, prefix)
        self.configure(readonly=True, pk=True)

