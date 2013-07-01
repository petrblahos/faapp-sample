<%inherit file="/base.mako"/>

<h1>${ _("Models") }</h1>
<ul>
% for i in models:
    <li><a href="${ request.route_url("list", model=i) }">${ i } objects</a></li>
% endfor
</ul>

