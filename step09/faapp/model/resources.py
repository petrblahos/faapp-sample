import urlparse
import urllib

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
    __name__ = ""
    __parent__ = None
    def __init__(self, request):
        self.request = request
    def get_models(self):
        return meta.model_names
    def __getitem__(self, name):
        return ModelContext(self, name)

class ModelContext(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.request = parent.request
        self.name = name
        self.model = meta.__dict__[self.name]
    def get_parent(self):
        return self.parent
    def get_name(self):
        return self.name
    def get_grid(self):
        grid_class = grids.__dict__.get(self.name, grids.Grid)
        return grid_class(self.model, self.request.db.query(self.model).all(), request=self.request, )
    def __getitem__(self, name):
        params = urlparse.parse_qs(name)
        q = self.request.db.query(self.model)
        for i in get_pk_columns(self.model):
            q = q.filter(i==params[i.name][0])
        return ItemContext(self, q.one())

    __parent__ = property(get_parent)
    __name__ = property(get_name)

class ItemContext(object):
    def __init__(self, parent, obj):
        self.parent = parent
        self.request = self.parent.request
        self.obj = obj
    def get_object(self):
        return self.obj
    def get_parent(self):
        return self.parent
    def get_name(self):
        return urllib.urlencode(get_pk_map(self.obj))
    def get_fs(self):
        fs_class = fieldsets.__dict__.get(self.parent.name, fieldsets.FieldSet)
        try:
            return fs_class(self.obj, request=self.request)
        except KeyError, e:
            return fs_class(self.model, session=self.request.db, request=self.request)
    def __unicode__(self):
        return "%s: %s" % (self.__parent__.__name__, self.__name__)

    __parent__ = property(get_parent)
    __name__ = property(get_name)

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

