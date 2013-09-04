import logging
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

logger = logging.getLogger("model")

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
    """
        We expect the url shema:
            .../Modelname|filter|pager/...
        where both filter and pager are optional. filter is in the query string
        format and contains pairs key=value. If specified, then only the rows
        containing the specified value as a substring is shown. pager is in the
        form page-pagesize, page defaulting to 0, pagesize defaulting to 10. If
        missing, the query will return first 10 rows, otherwise it will show
        rows page*pagesize to (page+1)*pagesize-1.
    """
    PAGER_DEFAULT = (0, 10)
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.name = name
        self.request = parent.request
        spl = name.split("|")
        spl.extend(["", ""])
        self.model_name = spl[0]
        try:
            self.filter = urlparse.parse_qs(spl[1])
        except:
            self.filter = {}
        try:
            self.pager = self.PAGER_DEFAULT
            pg = spl[2].split("-")
            if 2==len(pg) and pg[0].isdigit() and pg[1].isdigit():
                self.pager = ( int(pg[0]), int(pg[1]) )
        except:
            pass
        self.model = meta.__dict__[self.model_name]
    def get_name(self):
        return "%s|%s|%s-%s" % (self.model_name, urllib.urlencode(self.filter), self.pager[0], self.pager[1])
    def get_grid(self):
        q = self.request.db.query(self.model)
        for (k, v) in self.filter.iteritems():
            q = q.filter(self.model.__dict__[k].like("%s%%" % v[0]))
        grid_class = grids.__dict__.get(self.name, grids.Grid)
        pg_start = self.pager[0]*self.pager[1]
        return grid_class(self.model, q[pg_start:pg_start+self.pager[1]], request=self.request, )
    def get_fs(self):
        """
            Returns an "empty" fieldset.
        """
        fs_class = fieldsets.__dict__.get(self.name, fieldsets.FieldSet)
        return fs_class(self.model, session=self.request.db, request=self.request)
    def get_q_fs(self):
        fs_class = fieldsets.__dict__.get(self.name, fieldsets.FieldSet)
        return fs_class(self.model, session=self.request.db, request=self.request, data=self.filter, format=u'%(name)s')

    def __getitem__(self, name):
        if "new"==name:
            return NewItemContext(self)
        params = urlparse.parse_qs(name)
        q = self.request.db.query(self.model)
        for i in get_pk_columns(self.model):
            q = q.filter(i==params[i.name][0])
        return ItemContext(self, q.one())

    def __unicode__(self):
        return self.model_name

    __name__ = property(get_name)

class NewItemContext(object):
    __name__ = "new"
    def __init__(self, parent):
        self.__parent__ = parent
        self.request = parent.request
        self.model = parent.model
    def get_fs(self):
        fs_class = fieldsets.__dict__.get(self.__parent__.model.__name__, fieldsets.FieldSet)
        return fs_class(self.model, session=self.request.db, request=self.request)
    def __unicode__(self):
        return "%s - %s" % (self.__parent__.__name__, "New Item")

class ItemContext(object):
    def __init__(self, parent, obj):
        self.__parent__ = parent
        self.request = parent.request
        self.obj = obj
    def get_object(self):
        return self.obj
    def get_name(self):
        return urllib.urlencode(get_pk_map(self.obj))
    def get_fs(self):
        fs_class = fieldsets.__dict__.get(self.__parent__.__name__, fieldsets.FieldSet)
        try:
            return fs_class(self.obj, request=self.request)
        except KeyError, e:
            return fs_class(self.model, session=self.request.db, request=self.request)
    def __unicode__(self):
        return "%s: %s" % (unicode(self.__parent__), self.__name__)

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

