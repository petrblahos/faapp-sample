import copy

import formalchemy
from formalchemy import helpers as h
from formalchemy.exceptions import ValidationError
from formalchemy.validators import integer

class TextFieldRenderer(formalchemy.fields.FieldRenderer):
    """
    Render any field as a text field
    """
    def render(self, **kwargs):
        """
            Anything is rendered into a text_field.
        """
        return h.text_field(self.name, value=self.value, **kwargs)

    @property
    def value(self):
        """
            Submitted value, or field value converted to string.
            Return value is always either None or a string.
        """
        v = None
        if not self.field.is_readonly() and self.params is not None:
            # submitted value.  do not deserialize here since that requires
            # valid data, which we might not have
            try:
                v = self._serialized_value()
            except formalchemy.fields.FieldNotFoundError, e:
                pass
        if v:
            return v

        return ""

class QFieldSet(formalchemy.FieldSet):
    """
        Used to construct a filtering form. All fields of this fieldset are
        rendered as faapp.model.tools.TextFieldRenderer.
        Also, fields that are relations are excluded.
    """
    default_renderers = dict([
        (k, TextFieldRenderer)
        for k in formalchemy.FieldSet.default_renderers.iterkeys()
    ])
    def __init__(self, model, **kwargs):
        kwargs["format"] = u'%(name)s'
        super(QFieldSet, self).__init__(model, **kwargs)
        # find relations, we want to exclude them
        exclude = []
        for (k, v) in self._fields.iteritems():
            if v.is_relation:
                exclude.append(v)
        self.configure(pk=False, exclude=exclude)

