import formalchemy
from webhelpers.html import tags

class CommandLinkField(object):
    pass


class CommandLinkRenderer(formalchemy.FieldRenderer):
    """render a field as a text field"""
    def render(self, **kwargs):
        return tags.link_to(
                self.field.label(),
                self.field.parent.active_request.route_url(
                    self.field.name[1:],
                    model=self.field.model.__class__.__name__,
                    id=self.field.model.id,
                )
            )
    render_readonly = render

class Grid(formalchemy.Grid):
    def __init__(self, cls, instances=[], session=None, data=None,
                 request=None, prefix=None):
        super(Grid, self).__init__(cls, instances, session, data, request, prefix)
        self.active_request = request
        assert request
        self.configure(readonly=True)
        self.default_renderers[CommandLinkField] = CommandLinkRenderer

        self.append(formalchemy.Field("_edit", label=request.translate("Edit"), type=CommandLinkField))
        self.append(formalchemy.Field("_delete", label=request.translate("Delete"), type=CommandLinkField))

class Address(Grid):
    pass

