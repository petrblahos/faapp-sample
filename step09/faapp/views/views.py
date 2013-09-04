from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(context="faapp.model.resources.TopContext", renderer='/top.mako')
def top(request):
    """
        The data needed to fulfill this request are stored
        in request.context.
    """
    return { "models": request.context.get_models(), }

@view_config(context="faapp.model.resources.ModelContext", renderer="/list.mako")
def list(request):
    return { "grid": request.context.get_grid(), }

@view_config(context="faapp.model.resources.NewItemContext", renderer="/edit.mako")
@view_config(context="faapp.model.resources.ItemContext", renderer="/edit.mako")
def edit(request):
    fs = request.context.get_fs()

    if "POST"==request.environ.get("REQUEST_METHOD", "").upper() and request.POST:
        if fs.validate():
            request.db.add(fs.model)
            fs.sync()
            return HTTPFound(location=request.resource_url(request.context.__parent__))

    return { 'fs': fs }

@view_config(context="faapp.model.resources.ItemContext", name="delete", renderer="/edit.mako")
def delete(request):
    obj = request.context.get_object()
    request.db.delete(obj)
    return HTTPFound(location=request.resource_url(request.context.__parent__))

