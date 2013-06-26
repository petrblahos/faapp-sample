import formalchemy

class FieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(FieldSet, self).__init__(model, session, data, prefix, format, request)
        self.post_config()

    def post_config(self):
        pass

