#!/bin/bash
set -e

echo "Deploying to Snowflake..."

snowsql -a "$SNOWFLAKE_ACCOUNT" -u "$SNOWFLAKE_USER" -p "$SNOWFLAKE_PASSWORD" -d "$SNOWFLAKE_DB" -s "$SNOWFLAKE_SCHEMA" -q "$(cat sql/create_schema.sql)"
