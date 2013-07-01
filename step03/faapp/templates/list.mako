<%inherit file="/base.mako"/>

<h1>${ _("Listing of %s") % request.matchdict["model"] }</h1>
<ul>
% for i in q:
<li><a href="${ request.route_url("edit", model=request.matchdict["model"], id=i.id) }">${ i.id }</a> ${ i }
% endfor
</ul>
<a href="${ request.route_url("new", model=request.matchdict["model"]) }">${ _("New") }</a>
<hr>
<table>
    ${ grid.render() |n}
</table>



