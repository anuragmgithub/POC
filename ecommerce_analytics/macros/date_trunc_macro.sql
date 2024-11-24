{% macro date_trunc(date_column, unit) %}
    {% if unit == 'year' %}
        DATE_FORMAT({{ date_column }}, '%Y-01-01')
    {% elif unit == 'month' %}
        DATE_FORMAT({{ date_column }}, '%Y-%m-01')
    {% elif unit == 'week' %}
        DATE_SUB({{ date_column }}, INTERVAL WEEKDAY({{ date_column }}) DAY)
    {% elif unit == 'day' %}
        DATE({{ date_column }})
    {% else %}
        {{ date_column }} -- If an invalid unit is passed, just return the original column
    {% endif %}
{% endmacro %}

