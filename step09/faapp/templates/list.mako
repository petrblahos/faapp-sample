<%inherit file="/base.mako"/>

<h1>${ _("Listing of %s") % request.context.name }</h1>
<table>
    ${ grid.render() |n}
</table>
##<a href="${ request.route_url("edit", model=request.matchdict["model"]) }">${ _("New") }</a>

