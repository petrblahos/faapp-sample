<%inherit file="/base.mako"/>

<h1>${ _("Tables") }</h1>
<ul>
% for i in models:
    <li><a href="${ request.resource_url(request.context, i) }">${ _(i) }</a></li>
% endfor
</ul>

