from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(context="faapp.model.resources.TopContext", renderer='/top.mako')
def top(context, request):
    """
        The data needed to fulfill this request are stored
        in request.context.
    """
    return { "models": context.get_models(), }

class ListItemsView(object):
    """
        A view for listing the objects, and paging and filtering.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context="faapp.model.resources.ModelContext", renderer="/list.mako")
    def list(self):
        return { "grid": self.context.get_grid(), }

    @view_config(context="faapp.model.resources.ModelContext", name="filter")
    def list_filter(self):
        """
            Apply filter in current context, as specified by the request params.
            The request params should be in the form key=value. Then model's
            field key must start with val.
        """
        filter = {}
        for (k, v) in self.request.params.iteritems():
            if v and k in dir(self.context.model):
                filter[k] = v
        self.context.filter = filter
        self.context.reset_pager()
        return HTTPFound(location=self.request.resource_url(self.context))

    @view_config(context="faapp.model.resources.ModelContext", name="prev")
    def list_prev_page(self):
        """
            Move 1 page back.
        """
        self.context.pager = (
            max(0, self.context.pager[0] - 1),
            self.context.pager[1],
        )
        return HTTPFound(location=self.request.resource_url(self.context))

    @view_config(context="faapp.model.resources.ModelContext", name="next")
    def list_next_page(self):
        """
            Move 1 page forward.
        """
        self.context.pager = (self.context.pager[0] + 1, self.context.pager[1])
        return HTTPFound(location=self.request.resource_url(self.context))

@view_config(context="faapp.model.resources.NewItemContext", renderer="/edit.mako")
@view_config(context="faapp.model.resources.ItemContext", renderer="/edit.mako")
def edit(context, request):
    """
        Edit or save the object.
    """
    fs = context.get_fs()

    request_method = request.environ.get("REQUEST_METHOD", "").upper()
    if "POST"==request_method and request.POST:
        if fs.validate():
            request.db.add(fs.model)
            fs.sync()
            return HTTPFound(location=request.resource_url(context.__parent__))

    return { 'fs': fs }

@view_config(context="faapp.model.resources.ItemContext", name="delete")
def delete(context, request):
    """
        Delete the object.
    """
    obj = context.get_object()
    request.db.delete(obj)
    return HTTPFound(location=request.resource_url(context.__parent__))

