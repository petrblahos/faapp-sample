"""
    Custom FieldSets and FieldSet base.
"""
import formalchemy
import faapp.model.tools


class FieldSet(formalchemy.FieldSet):
    """
        A base Grid, makes sure that request is passed, sets the context
        for localization in templates.
    """
    def __init__(self, model, **kwargs):
        """
            Just to keep the request.
        """
        super(FieldSet, self).__init__(model, **kwargs)
        self.request = kwargs["request"]
        assert kwargs["request"]

    def render(self, **kwargs):
        """
            Set context for localization in the templates and then render.
        """
        kwargs.setdefault("_", self.request.translate)
        kwargs.setdefault("ungettext", self.request.ungettext)
        kwargs.setdefault("request", self.request)
        kwargs.setdefault("lang", self.request.locale_name)
        return super(FieldSet, self).render(**kwargs)


class NonId(FieldSet):
    """
        A specific fieldset for NonId objects with the primary key is shown.
    """
    def __init__(self, model, **kwargs):
        """
            Set the primary keys to be shown too.
        """
        super(NonId, self).__init__(model, **kwargs)
        self.configure(pk=True)

