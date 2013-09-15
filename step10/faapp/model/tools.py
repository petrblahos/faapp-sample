import formalchemy
from formalchemy import helpers as h

class TextFieldRenderer(formalchemy.fields.FieldRenderer):
    """render a field as a text field"""
    def render(self, **kwargs):
        return h.text_field(self.name, value=self.value, **kwargs)

    @property
    def value(self):
        """
        Submitted value, or field value converted to string.
        Return value is always either None or a string.
        """
        v = None
        if not self.field.is_readonly() and self.params is not None:
            # submitted value.  do not deserialize here since that requires valid data, which we might not have
            try:
                v = self._serialized_value()
            except formalchemy.fields.FieldNotFoundError, e:
                pass
        if v:
            return v

        return ""


class QFieldSet(formalchemy.FieldSet):
    def __init__(self, model, session=None, data=None, prefix=None,
                 request=None):
        super(QFieldSet, self).__init__(model, session, data, prefix, format=u'%(name)s', request=request, )
        for k in self.default_renderers.keys():
            self.default_renderers[k] = TextFieldRenderer
        # find relations, we want to exclude them
        exclude = []
        for (k, v) in self._fields.iteritems():
            if v.is_relation:
                exclude.append(v)
        self.configure(pk=False, exclude=exclude)


