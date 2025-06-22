from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv()

# conn = snowflake.connector.connect(
#     user=os.getenv("SNOWFLAKE_USER"),
#     password=os.getenv("SNOWFLAKE_PASSWORD"),
#     account=os.getenv("SNOWFLAKE_ACCOUNT"),
#     warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
#     database=os.getenv("SNOWFLAKE_DATABASE"),
#     schema=os.getenv("SNOWFLAKE_SCHEMA"),
#     role=os.getenv("SNOWFLAKE_ROLE")
# )



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

# Create a cursor object.
cur = conn.cursor()

# Execute a statement
cur.execute("select count(*) from SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.CALL_CENTER")

# Fetch and print results
for row in cur:
    print(row)

# Clean up
cur.close()
conn.close()
