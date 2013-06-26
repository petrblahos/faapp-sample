<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Pylons/Pyramid/pyramid_locmako</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
</head>
<body>
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
</body>
</html>



