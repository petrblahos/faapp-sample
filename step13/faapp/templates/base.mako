<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Pylons/Pyramid/pyramid_locmako</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
</head>
<body>
<%!
from faapp.model.resources import TopContext
top_context_instance = TopContext(None)
%>
<a href="${ request.resource_url(top_context_instance) }">${ _("HOME") }</a><hr>
${ next.body() }
</body>
</html>



