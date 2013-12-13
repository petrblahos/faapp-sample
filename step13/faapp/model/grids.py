"""
    Grids.
"""
import formalchemy

class Grid(formalchemy.Grid):
    """
        A base Grid, makes sure that request is passed, sets the context
        for localization in templates.
    """
    def __init__(self, cls, instances=[], **kwargs):
        """
            To keep the request. Also sets the grid readonly.
        """
        super(Grid, self).__init__(cls, instances, **kwargs)
        assert kwargs["request"]
        self.request = kwargs["request"]
        self.configure(readonly=True)

    def render(self, **kwargs):
        """
            Set context for localization in the templates and then render.
        """
        kwargs.setdefault("_", self.request.translate)
        kwargs.setdefault("ungettext", self.request.ungettext)
        kwargs.setdefault("request", self.request)
        kwargs.setdefault("lang", self.request.locale_name)
        return super(Grid, self).render(**kwargs)


class NonId(Grid):
    """
        A specific grid for NonId objects. The primary key is shown in the
        grid.
    """
    def __init__(self, cls, instances=[], **kwargs):
        """
            Set the primary keys to be shown too.
        """
        super(NonId, self).__init__(cls, instances, **kwargs)
        self.configure(readonly=True, pk=True)

