INSERT INTO {{destination}} ({% for colname in rows[0].keys() %}{{colname}}{% if not loop.last %},{% endif %} {% endfor %})
VALUES
{% for row in rows %}{% for value in row.values() %}('{{value}}'{%if not loop.last%},{%endif%}){%endfor%}{%if not loop.last%},{%endif%}
{%endfor%}
