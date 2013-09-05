import formalchemy
from formalchemy import helpers as h

class TextFieldRenderer(formalchemy.fields.FieldRenderer):
    """render a field as a text field"""
    def render(self, **kwargs):
        return h.text_field(self.name, value=self.value, **kwargs)


class QFieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 format=u'%(model)s-%(pk)s-%(name)s',
                 request=None):
        super(QFieldSet, self).__init__(model, session, data, prefix, format, request)
        for k in self.default_renderers.keys():
            self.default_renderers[k] = TextFieldRenderer
        # find relations, we want to exclude them
        exclude = []
        for (k, v) in self._fields.iteritems():
            if v.is_relation:
                exclude.append(v)
        self.configure(pk=False, exclude=exclude)


