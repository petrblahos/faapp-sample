<%inherit file="/base.mako"/>

<h1>${ _("Listing of %s") % request.context }</h1>
Pager:
<a href="${ request.resource_url(request.context, "prev") }">&lt;&lt;</a>
${ request.context.pager[0]*request.context.pager[1]+1 }
-
${ (request.context.pager[0]+1)*request.context.pager[1] }
<a href="${ request.resource_url(request.context, "next") }">&gt;&gt;</a>
<table>
    ${ grid.render() |n}
</table>
<a href="${ request.resource_url(request.context, "new") }">${ _("New") }</a>
<hr>
<form action="${ request.resource_url(request.context, "filter") }" method="GET">
${ request.context.get_q_fs().render() |n }
<input type="submit"></input>
</form>

