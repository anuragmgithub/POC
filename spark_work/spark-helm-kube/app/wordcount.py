# spark-helm-kube/wordcount.py

from pyspark.sql import SparkSession
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>")
        sys.exit(-1)

    input_file = sys.argv[1]
    
    spark = SparkSession.builder \
        .appName("WordCount") \
        .getOrCreate()
    
    text_file = spark.read.text(input_file).rdd.map(lambda r: r[0])
    counts = text_file.flatMap(lambda line: line.split(" ")) \
                      .map(lambda word: (word, 1)) \
                      .reduceByKey(lambda a, b: a + b)
    
    for word, count in counts.collect():
        print(f"{word}: {count}")

    spark.stop()

if __name__ == "__main__":
    main()
