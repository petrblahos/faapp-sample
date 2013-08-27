<%inherit file="/base.mako"/>

<h1>${ _("Listing of %s") % request.matchdict["model"] }</h1>
<table>
    ${ grid.render() |n}
</table>
<a href="${ request.route_url("edit", model=request.matchdict["model"]) }">${ _("New") }</a>

<br>
${ ungettext("The list has %s item.", "The list has %s items.", len(grid.rows)) % len(grid.rows) }
<br>
${ ungettext("The list contains one item.", "The list contains %(COUNT)s items.", len(grid.rows)) % { "COUNT": len(grid.rows) } }


