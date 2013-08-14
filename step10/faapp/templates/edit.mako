<%inherit file="/base.mako"/>

<h1>${ _("Edit %s") % request.matchdict["model"] }</h1>
<form method="POST">
    ${ fs.render() |n}
<input type="submit"/>
</form>

