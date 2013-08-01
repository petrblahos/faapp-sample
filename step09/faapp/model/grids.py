import formalchemy
import formalchemy.i18n

formalchemy.i18n.HAS_PYRAMID = 0

def translate_with_fa_factory(request):
    fa_translate = formalchemy.i18n.get_translator(lang=request.locale_name, request=request)

    def translate(*args, **kwargs):
        out = request.translate(*args, **kwargs)
        if out==args[0]:
            out = fa_translate(*args, **kwargs)
        return out

    return translate

class Grid(formalchemy.Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(Grid, self).__init__(cls, instances, session, data, request, prefix)
        self.active_request = request
        assert request
        self.configure(readonly=True)

    def render(self, **kwargs):
        if not "_" in kwargs:
            kwargs["_"] = translate_with_fa_factory(self.active_request)
        if not "lang" in kwargs:
            kwargs["lang"] = self.active_request.locale_name
        if not "request" in kwargs:
            kwargs["request"] = self.active_request
        return super(Grid, self).render(**kwargs)

class NonId(Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(NonId, self).__init__(cls, instances, session, data, request, prefix)
        self.configure(readonly=True, pk=True)

