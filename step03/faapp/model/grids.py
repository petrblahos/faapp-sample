import formalchemy


class Grid(formalchemy.Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(Grid, self).__init__(cls, instances, session, data, request, prefix)
        self.post_config()

    def post_config(self):
        self.configure(readonly=True)

class Address(Grid):
    def post_config(self):
        #super(Address, self).post_config()
        # FIXME: we must check that the parent is not being called
        self.configure(readonly=True, exclude=[self.persons])


