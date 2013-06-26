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
    models = []

    for (name, ent) in meta.__dict__.iteritems():
        if name.startswith("_"):
            continue
        if "Base"==name:
            continue
        try:
            if issubclass(ent, meta.Base):
                models.append(name)
        except:
            pass

    return {'project':'faapp', 'db': request.db, 'models': models, }

@view_config(route_name="list", renderer="/list.mako")
def list(request):
    model = meta.__dict__.get(request.matchdict["model"])
    grid = grids.__dict__.get(request.matchdict["model"], grids.Grid)(model, request.db.query(model).all(), )
#    grid = grids.Grid(model, request.db.query(model).all(), )
    return { "q": request.db.query(model).all(), "grid": grid, }

@view_config(route_name="edit", request_method="GET", renderer="/edit.mako")
@view_config(route_name="new", request_method="GET", renderer="/edit.mako")
def edit(request):
    model = meta.__dict__.get(request.matchdict["model"])

    if "id" in request.matchdict:
        obj = request.db.query(model).filter(model.id==request.matchdict["id"]).first()
        fs = fieldsets.FieldSet(obj)
    else:
        fs = fieldsets.FieldSet(model, session=request.db)

    return { 'fs': fs }

@view_config(route_name="edit", request_method="POST", renderer="/edit.mako")
@view_config(route_name="new", request_method="POST", renderer="/edit.mako")
def saveedit(request):
    model = meta.__dict__.get(request.matchdict["model"])

    if "id" in request.matchdict:
        obj = request.db.query(model).filter(model.id==request.matchdict["id"]).first()
        fs = fieldsets.FieldSet(obj, request=request)
    else:
        fs = fieldsets.FieldSet(model, session=request.db, request=request)

    if fs.validate():
        request.db.add(fs.model)
        fs.sync()
    else:
        return { "fs": fs }

    return HTTPFound(location=request.route_url("list", model=request.matchdict["model"]))

