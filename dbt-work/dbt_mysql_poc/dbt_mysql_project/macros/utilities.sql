{% macro dynamic_column_selector(columns, table_alias)%}
    {% for column in columns %}
        {{table_alias}}.{{column}}{% if not loop.last %}, {% endif %}
    {% endfor %}
{% endmacro %}

{% macro format_date(date, format) %}
    DATE_FORMAT({{ date }}, '%Y-%m-%d') 
{% endmacro %}

{% macro apply_account_type_logic(account_type_column) %}
     {% do log("account_type_column: " ~ account_type_column, info=True) %}
    CASE 
        WHEN {{account_type_column}} = 'savings' THEN 'SAVINGS_ACCOUNT'
        WHEN {{account_type_column}} = 'current' THEN 'CHECKING_ACCOUNT'
        ELSE  'OTHER_ACCOUNT'
    END
{% endmacro %}