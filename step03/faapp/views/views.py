from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from faapp.model import meta, grids, fieldsets

@view_config(route_name='top', renderer='/top.mako')
def top(request):
    """
        You can access your db session via request.db.
        To query your orm, you can do things like:
        request.db.Query(model.meta.MyModel).first()
    """
    return { 'models': meta.model_names, }

@view_config(route_name="list", renderer="/list.mako")
def list(request):
    model = meta.__dict__.get(request.matchdict["model"])
    grid = grids.__dict__.get(request.matchdict["model"], grids.Grid)(model, request.db.query(model).all(), )
    return { "q": request.db.query(model).all(), "grid": grid, }

@view_config(route_name="edit", renderer="/edit.mako")
@view_config(route_name="new", renderer="/edit.mako")
def edit(request):
    model = meta.__dict__.get(request.matchdict["model"])
    fs_class = fieldsets.__dict__.get(request.matchdict["model"], fieldsets.FieldSet)

    if "id" in request.matchdict:
        obj = request.db.query(model).filter(model.id==request.matchdict["id"]).first()
        fs = fs_class(obj, request=request)
    else:
        fs = fs_class(model, session=request.db, request=request)

    if "POST"==request.environ.get("REQUEST_METHOD", "").upper() and request.POST:
        if fs.validate():
            request.db.add(fs.model)
            fs.sync()
            return HTTPFound(location=request.route_url("list", model=request.matchdict["model"]))

    return { 'fs': fs }

