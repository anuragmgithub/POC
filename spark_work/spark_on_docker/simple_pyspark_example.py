# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Simple PySpark Example") \
    .getOrCreate()

# Sample data - you can replace this with your actual data loading logic
data = [("Alice", 25), ("Bob", 30), ("Catherine", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Show the initial DataFrame
print("Initial DataFrame:")
df.show()

# Transformation example: Filter and show only people aged 30 and above
filtered_df = df.filter(col("Age") >= 30)

# Show the transformed DataFrame
print("Filtered DataFrame (Age >= 30):")
filtered_df.show()

# Stop the SparkSession
spark.stop()
