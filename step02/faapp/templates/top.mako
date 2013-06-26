<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Pylons/Pyramid/pyramid_locmako</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
</head>
<body>
<h1>${ _("Models") }</h1>
<ul>
% for i in models:
    <li><a href="${ request.route_url("list", model=i) }">${ i } objects</a></li>
% endfor
</ul>

</body>
</html>

