<%inherit file="/base.mako"/>

<h1>${ _("Listing of %s") % request.context }</h1>
<table>
    ${ grid.render() |n}
</table>
<a href="${ request.resource_url(request.context, "new") }">${ _("New") }</a>

