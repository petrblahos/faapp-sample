<%inherit file="/base.mako"/>

<h1>${ _("Edit %s") % request.context }</h1>
<form method="POST">
    ${ fs.render() |n}
<input type="submit"/>
</form>

