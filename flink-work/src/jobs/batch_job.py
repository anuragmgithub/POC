from pyflink.table import EnvironmentSettings, TableEnvironment
import pandas as pd

def run():
    env_settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    table_env = TableEnvironment.create(env_settings)

    sample_data = [
        (1, "Alice", 34),
        (2, "Bob", 45),
        (3, "Cathy", 29),
        (4, "Dave", 41)
    ]

    persons_table = table_env.from_elements(sample_data, ['id', 'name', 'age'])

    # Register the table as Temporary view 
    table_env.create_temporary_view("persons", persons_table)

    # sample query 
    result_table = table_env.sql_query("SELECT * FROM persons WHERE age > 30")

    ## Convert the result to a Pandas DataFrame (for local testing)
    result_pdf = result_table.to_pandas()

    print(result_pdf)

if __name__ == '__main__':
    run()


