# SparkSession was introduced in Spark 2.0 which is a unified API for working with structured data. 
# It combines SparkContext , SQLContext, HiveContext, and StreamingContext.
# My Docker container runs Spark 2.4.4.
# from pyspark import SparkContext (it doesn't need to import)
# from pyspark.streaming import StreamingContext (it doesn't need to import)
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create a SparkSession
spark = SparkSession.builder.appName("strm_spark_job").enableHiveSupport().getOrCreate()

# Setting a checkpoint location enhances fault tolerance by saving processing states and metadata, 
# enabling accurate recovery of streaming queries in Apache Spark after interruptions or errors.
spark.conf.set("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints")

# Define schema for streaming DataFrame
userSchema = StructType().add("customer_id", "integer").add("customer_order", "string").add("order_timestamp", "integer")

# Read streaming data from structured text files

# Choosing to use the .csv() command for reading text files because the data has a delimited structure similar to CSV files, 
# making it more convenient and efficient for managing data, 
# including setting schemas and processing data further, compared to using .textFile().
strmDF = spark \
    .readStream \
    .schema(userSchema) \
    .option("sep", "|") \
    .csv("/tmp/flume/sink")

# Split the 'customer_order' column to extract 'order_menu' and 'order_price'
split_col = split(strmDF['customer_order'], ' ')
strmDF = strmDF.withColumn('order_menu', split_col.getItem(0)) \
            .withColumn('order_price', split_col.getItem(1).cast('integer')) \
            .withColumn("order_timestamp",from_unixtime(col("order_timestamp"),'dd-MM-yyyy HH:mm:ss').cast('string')) \
            .drop('customer_order')

# Define the streaming query to select required columns and write to Parquet format
query = strmDF \
    .selectExpr('customer_id as cust_id','order_menu as odr_menu','order_price as odr_prc','order_timestamp as odr_tms') \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/tmp/default/transactions_cln") \
    .start()

# Wait for the streaming query to terminate
query.awaitTermination()


