from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(context="faapp.model.resources.TopContext", renderer='/top.mako')
def top(request):
    """
        The data needed to fulfill this request are stored
        in request.context.
    """
    return { "models": request.context.get_models(), }

@view_config(context="faapp.model.resources.TopContext", name="admin1")
def admin1(request):
    from faapp.model import meta
    request.db.query(meta.Person).delete()
    for i in range(1, 101):
        m = meta.Person(name="Person Name %s" % i, number=i)
        request.db.add(m)
    return HTTPFound(location=request.resource_url(request.context))

@view_config(context="faapp.model.resources.ModelContext", renderer="/list.mako")
def list(request):
    return { "grid": request.context.get_grid(), }

@view_config(context="faapp.model.resources.ModelContext", name="filter")
def list_filter(request):
    filter = {}
    for (k, v) in request.params.iteritems():
        if v and k in dir(request.context.model):
            filter[k] = v
    request.context.filter = filter
    request.context.reset_pager()
    return HTTPFound(location=request.resource_url(request.context))

@view_config(context="faapp.model.resources.ModelContext", name="prev")
def list_next_page(request):
    request.context.pager = (max(0, request.context.pager[0]-1), request.context.pager[1])
    return HTTPFound(location=request.resource_url(request.context))
@view_config(context="faapp.model.resources.ModelContext", name="next")
def list_prev_page(request):
    request.context.pager = (request.context.pager[0]+1, request.context.pager[1])
    return HTTPFound(location=request.resource_url(request.context))

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

@view_config(context="faapp.model.resources.ItemContext", name="delete")
def delete(request):
    obj = request.context.get_object()
    request.db.delete(obj)
    return HTTPFound(location=request.resource_url(request.context.__parent__))

