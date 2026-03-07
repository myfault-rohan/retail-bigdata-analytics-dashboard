from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Sales Big Data Processing") \
    .getOrCreate()

df = spark.read.csv("data/online_retail.csv", header=True, inferSchema=True)

df.createOrReplaceTempView("sales")

result = spark.sql("""
SELECT Country,
       SUM(Quantity * UnitPrice) as total_sales
FROM sales
GROUP BY Country
ORDER BY total_sales DESC
""")

result.show()

result.toPandas().to_csv("data/processed_sales.csv", index=False)

spark.stop()
