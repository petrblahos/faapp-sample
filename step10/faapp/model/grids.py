import formalchemy

class Grid(formalchemy.Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(Grid, self).__init__(cls, instances, session, data, request, prefix)
        self.active_request = request
        assert request
        self.configure(readonly=True)

class NonId(Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(NonId, self).__init__(cls, instances, session, data, request, prefix)
        self.configure(readonly=True, pk=True)

