from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("SparkTest") \
    .getOrCreate()

data = [("Rohan",1),("AI",2),("BigData",3)]

df = spark.createDataFrame(data, ["Name","Value"])

df.show()

spark.stop()