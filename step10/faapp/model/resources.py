from formalchemy.fields import _pk_one_column
from sqlalchemy.orm import (
    class_mapper,
    )

try:
    from sqlalchemy import exc as sqlalchemy_exceptions
except ImportError:
    from sqlalchemy import exceptions as sqlalchemy_exceptions

import fieldsets, grids
import meta

class TopContext(object):
    def __init__(self, request):
        self.request = request
    def get_models(self):
        return meta.model_names

def get_pk_columns(clazz):
    try:
        return class_mapper(clazz).primary_key
    except sqlalchemy_exceptions.InvalidRequestError:
        # try to get pk from model attribute
        if hasattr(instance, '_pk'):
            return getattr(instance, '_pk', None) or None
        return None
    return columns

def pk(instance):
    columns = get_pk_columns(type(instance))
    return [ (i, _pk_one_column(instance, i)) for i in columns ]

def get_pk_map(instance):
    return dict([ (i[0].name, i[1]) for i in pk(instance) ])

class OrmContext(object):
    def __init__(self, request):
        self.request = request
        self.model = self._get_model()
    def _get_model(self):
        m = self.request.matchdict["model"]
        if not m in meta.model_names:
            raise KeyError("Could not find model %s" % m)
        return meta.__dict__[m]
    def get_object(self):
        q = self.request.db.query(self.model)
        for i in get_pk_columns(self.model):
            q = q.filter(i==self.request.params[i.name])
        return q.one()
    def get_grid(self):
        grid_class = grids.__dict__.get(self.request.matchdict["model"], grids.Grid)
        return grid_class(self.model, self.request.db.query(self.model).all(), request=self.request, )
    def get_fs(self):
        fs_class = fieldsets.__dict__.get(self.request.matchdict["model"], fieldsets.FieldSet)
        try:
            return fs_class(self.get_object(), request=self.request)
        except KeyError, e:
            return fs_class(self.model, session=self.request.db, request=self.request)

