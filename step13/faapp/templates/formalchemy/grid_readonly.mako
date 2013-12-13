# -*- coding: utf-8 -*-
<%!
import urllib

from faapp.model.meta import get_pk_map
%>
<thead>
  <tr>
    %for field in collection.render_fields.itervalues():
      <th>${field.label()|h}</th>
    %endfor
  </tr>
</thead>

<tbody>
%for i, row in enumerate(collection.rows):
  <%
  collection._set_active(row)
  %>
  <tr class="${i % 2 and 'odd' or 'even'}">
  %for field in collection.render_fields.itervalues():
    <td>${field.render_readonly()|n}</td>
  %endfor
  <td><a href="${ request.resource_url(request.context, urllib.urlencode(get_pk_map(row))) }">${ _("Edit") }</a>
  <td><a href="${ request.resource_url(request.context, urllib.urlencode(get_pk_map(row)), "delete") }">${ _("Delete") }</a>
  </tr>
%endfor
</tbody>
<br>

