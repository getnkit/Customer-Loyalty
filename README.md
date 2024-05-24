# Customer-Loyalty (Hadoop)
## Project Overview
This project focuses on building a data pipeline using the Hadoop Ecosystem following the design pattern of the Lambda Architecture. This architecture enables event-driven processing when handling big datasets as it processes large data sets in the batch layer and real-time data in the speed layer.

**Batch Layer**

The process starts by extracting data from CSV files and ingesting it into HDFS. Spark SQL is then used to transform the data, and finally, the data is loaded into the Hive table ```customers_cln```.

**Speed Layer**

Apache Flume is used to collect real-time data from a shell script that generates order data in the form of log files. The shell script is configured as a source for Flume, and the data is sent to HDFS and HBase as sinks. The data in HDFS is then processed and transformed by Spark Streaming. The processed data is stored in the Hive table ```transactions_cln```.

**Serving Layer**

It consists of Hive and HBase. Hive is used to combine data from the batch layer and speed layer by creating a new table called the ```loyalty``` table that joins data from the ```customers_cln``` and ```transactions_cln``` tables. HBase is used to store data from the speed layer that requires fast random read/write access.

To update the ```loyalty``` table with new data, utilize a workflow scheduling tool like Apache Oozie to create repeatable workflows. It schedules workflows to execute Hive scripts appending new data to the existing ```loyalty``` table structure, aligning with changes in the ```customers_cln``` and ```transactions_cln``` tables.

## About Dataset
This dataset consists of customer data from a beverage shop such as names, dates of birth, and contact information. Additionally, this project generates real-time order data for each customer to simulate what orders each customer places and when. All of this data is collected for analysis and customer segmentation by calculating loyalty card point accumulation and offering promotions to customers accordingly.
## Architecture
![image](https://github.com/getnkit/Customer-Loyalty/blob/31660049d2b3cc665834784ff39ad75971690cc2/images/Data%20Architecture.png)
## Implementation
### Step 1: 
