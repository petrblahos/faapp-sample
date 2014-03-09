import logging
import urlparse
import urllib

from sqlalchemy.orm import (
    class_mapper,
    )

import fieldsets, grids, tools
import meta

logger = logging.getLogger("model")

class TopContext(object):
    """
        Contains just the list of orm models.
    """
    __name__ = ""
    __parent__ = None
    def __init__(self, request):
        self.request = request
    def get_models(self):
        """
            Returns a list of orm model names.
        """
        return meta.model_names

    def __getitem__(self, model_name):
        """
            Returns a new ModelContext for given name.
        """
        return ModelContext(self, model_name)

class ModelContext(object):
    """
        We expect the url shema:
            .../Modelname.pager.filter/...
        where both filter and pager are optional. filter is in the query string
        format and contains pairs key=value. If specified, then only the rows
        containing the specified value as a substring is shown. pager is in the
        form page-pagesize, page defaulting to 0, pagesize defaulting to 10. If
        missing, the query will return first 10 rows, otherwise it will show
        rows page*pagesize to (page+1)*pagesize-1.
    """
    PAGER_DEFAULT = (0, 10)
    def __init__(self, parent, name):
        """
            Parses and sanitizes the name (formatted Modelname.pager.filter).
        """
        self.__parent__ = parent
        self.request = parent.request
        spl = name.split(".", 2)
        spl.extend(["", ""])
        self.model_name = spl[0]
        try:
            self.filter = dict(urlparse.parse_qsl(spl[2]))
            # parse_qs maps key to a list of values, we need just one value
        except:
            self.filter = {}
        try:
            self.pager = self.PAGER_DEFAULT
            pg = spl[1].split("-")
            if 2 == len(pg) and pg[0].isdigit() and pg[1].isdigit():
                self.pager = ( int(pg[0]), int(pg[1]) )
        except:
            pass
        self.model = meta.__dict__[self.model_name]

    def reset_pager(self):
        """
            Sets the pager to the first page.
        """
        self.pager = self.PAGER_DEFAULT

    def get_name(self):
        """
            Formats the context into relevant part of url.
        """
        return "%s.%s-%s.%s" % (
            self.model_name,
            self.pager[0], self.pager[1],
            urllib.urlencode(self.filter),
        )
    def get_grid(self):
        """
            Returns a grid for the dataset defined by this context.
        """
        q = self.request.db.query(self.model)
        for (k, v) in self.filter.iteritems():
            q = q.filter(self.model.__dict__[k].like("%s%%" % v))
        grid_class = grids.__dict__.get(self.model_name, grids.Grid)
        pg_start = self.pager[0]*self.pager[1]
        return grid_class(
            self.model,
            q[pg_start:pg_start+self.pager[1]],
            request=self.request,
        )
    def get_q_fs(self):
        """
            Returns a field set to show/edit the filter for this context.
        """
        return tools.QFieldSet(
            self.model,
            session=self.request.db,
            request=self.request,
            data=self.filter,
        )

    def __getitem__(self, name):
        """
            Returns the child context, either for the new item or by the
            primary key.
        """
        if "new"==name:
            return NewItemContext(self)
        params = urlparse.parse_qs(name)
        q = self.request.db.query(self.model)
        for i in class_mapper(self.model).primary_key:
            q = q.filter(i==params[i.name][0])
        return ItemContext(self, q.one())

    def __unicode__(self):
        """
            Formats the context name.
        """
        return self.request.translate(self.model_name)

    __name__ = property(get_name)

class NewItemContext(object):
    """
        A context for creating a new item.
    """
    __name__ = "new"
    def __init__(self, parent):
        self.__parent__ = parent
        self.request = parent.request
        self.model = parent.model
    def get_fs(self):
        """
            Returns an empty field set for the new item.
        """
        fs_class = fieldsets.__dict__.get(
            self.model.__name__,
            fieldsets.FieldSet,
        )
        return fs_class(
            self.model,
            session=self.request.db,
            request=self.request,
        )
    def __unicode__(self):
        return "%s - %s" % (unicode(self.__parent__), "New Item")
        ### FIXME: non-localizable "New Item"

class ItemContext(object):
    """
        A context for an existing item.
    """
    def __init__(self, parent, obj):
        self.__parent__ = parent
        self.request = parent.request
        self.obj = obj
        self.model = parent.model
    def get_object(self):
        """
            Returns the database (ORM) object associated with this context.
        """
        return self.obj
    def get_name(self):
        """
            Returns the name of this context.
        """
        return urllib.urlencode(meta.get_pk_map(self.obj))
    def get_fs(self):
        """
            Returns the fieldset that can edit this db object.
        """
        fs_class = fieldsets.__dict__.get(self.model.__name__, fieldsets.FieldSet)
        try:
            return fs_class(self.obj, request=self.request)
        except KeyError, e:
            return fs_class(self.model, session=self.request.db, request=self.request)
    def __unicode__(self):
        return "%s - %s" % (unicode(self.__parent__), self.__name__)

    __name__ = property(get_name)
