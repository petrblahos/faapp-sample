<%inherit file="/base.mako"/>

<h1>${ _("Models") }</h1>
<ul>
% for i in models:
    <li><a href="${ request.resource_url(request.context, i) }">${ i } objects</a></li>
% endfor
</ul>

