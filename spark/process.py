from pyspark.sql import SparkSession
from pyspark.sql.functions import split
from pyspark.sql.functions import col, when

import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,org.elasticsearch:elasticsearch-spark-20_2.12:8.11.3 pyspark-shell"

spark = (
    SparkSession.builder.config("spark.streaming.stopGracefullyOnShutdown", True)
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0")
    .config("spark.sql.shuffle.partitions", 4)
    .master("spark://spark-master:7077")
    .appName("process.py")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Define Kafka source
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "EPL")
    .load()
)

# Convert binary data to string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df = df.withColumn("value", split(df["value"], ","))

# Perform processing
processed_df = df.select(
    df["key"].alias("id"),
    df["value"].getItem(0).alias("season"),
    df["value"].getItem(1).alias("datetime"),
    df["value"].getItem(2).alias("hometeam"),
    df["value"].getItem(3).alias("awayteam"),
    df["value"].getItem(4).cast("int").alias("fthg"),
    df["value"].getItem(5).cast("int").alias("ftag"),
    df["value"].getItem(6).alias("ftr"),
    df["value"].getItem(7).cast("int").alias("hthg"),
    df["value"].getItem(8).cast("int").alias("htag"),
    df["value"].getItem(9).alias("htr"),
    df["value"].getItem(10).alias("referee"),
    df["value"].getItem(11).cast("int").alias("hs"),
    df["value"].getItem(12).cast("int").alias("as"),
    df["value"].getItem(13).cast("int").alias("hst"),
    df["value"].getItem(14).cast("int").alias("ast"),
    df["value"].getItem(15).cast("int").alias("hc"),
    df["value"].getItem(16).cast("int").alias("ac"),
    df["value"].getItem(17).cast("int").alias("hf"),
    df["value"].getItem(18).cast("int").alias("af"),
    df["value"].getItem(19).cast("int").alias("hy"),
    df["value"].getItem(20).cast("int").alias("ay"),
    df["value"].getItem(21).cast("int").alias("hr"),
    df["value"].getItem(22).cast("int").alias("ar"),
)


# Write to Cassandra
query = (
    processed_df.writeStream.outputMode("append")
    .format("org.apache.spark.sql.cassandra")
    .option("spark.cassandra.connection.host", "cassandra")
    .option("spark.cassandra.connection.port", "9042")
    .option("keyspace", "matchresults")
    .option("table", "epl1")
    .option("checkpointLocation", "/tmp")
    .start()
)

# Start streaming
# query = df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start()

query.awaitTermination(30)
