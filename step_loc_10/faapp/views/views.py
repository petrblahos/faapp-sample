from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(route_name='top', renderer='/top.mako')
def top(request):
    """
        You can access your db session via request.db.
        To query your orm, you can do things like:
        request.db.Query(model.meta.MyModel).first()
    """
    return { "models": request.context.get_models(), }

@view_config(route_name="list", renderer="/list.mako")
def list(request):
    return { "grid": request.context.get_grid(), }

@view_config(route_name="edit", renderer="/edit.mako")
def edit(request):
    fs = request.context.get_fs()

    if "POST"==request.environ.get("REQUEST_METHOD", "").upper() and request.POST:
        if fs.validate():
            request.db.add(fs.model)
            fs.sync()
            return HTTPFound(location=request.route_url("list", model=request.matchdict["model"]))

    return { 'fs': fs }

@view_config(route_name="delete")
def delete(request):
    obj = request.context.get_object()
    request.db.delete(obj)
    return HTTPFound(location=request.route_url("list", model=request.matchdict["model"]))

