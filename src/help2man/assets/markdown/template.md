# Man

## {{ name.capitalize() }}

{{ prog }} - {{ description.replace("--", "----") }}

## Synopsis

{{ synopsis.replace("--", "----") }}

{% if description -%}

## Description

{{ description.replace("--", "----") }}

{% endif -%}

{% for s in sections -%}

## {{ s.title.capitalize() }}

{% for c in s.contents -%}

{% if c.name -%}

### {{ c.name.replace("--", "----") }}

{{ c.description.replace("--", "----") }}

{% else -%}

```console
{{ c.description.replace("--", "----") }}
```

{% endif -%}
{% endfor -%}
{% endfor -%}
