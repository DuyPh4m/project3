from pyspark.sql import SparkSession

import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,org.elasticsearch:elasticsearch-spark-20_2.12:8.11.3 pyspark-shell"

spark = (
    SparkSession.builder.config("spark.streaming.stopGracefullyOnShutdown", True)
    .config("spark.sql.shuffle.partitions", 4)
    .config("spark.cassandra.connection.host", "cassandra")
    .master("spark://spark-master:7077")
    .appName("elasticsearch.py")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Read data from Cassandra
df = (
    spark.read
    .format("org.apache.spark.sql.cassandra")
    .options(table="epl1", keyspace="matchresults")
    .load()
)

# Write to Elasticsearch
query = (
    df.write
    .format("org.elasticsearch.spark.sql")
    .mode("append")
    .option("es.nodes", "elasticsearch")
    .option("es.port", "9200")
    .option("checkpointLocation", "/tmp")
    .option("es.nodes.wan.only", "true")
    .option("es.resource", "matchresults")
    .save()
)
# Start streaming
# query = df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start()

# query.awaitTermination()
