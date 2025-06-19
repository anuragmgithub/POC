import snowflake.connector
import os

# Load SQL file
with open("snowflake-iac/sql/create_schema.sql", "r") as f:
    sql = f.read()

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

# Execute SQL
with conn.cursor() as cur:
    for stmt in sql.strip().split(";"):
        if stmt.strip():
            cur.execute(stmt)
            print(f"Executed: {stmt.strip()}")

conn.close()
