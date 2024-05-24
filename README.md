# Customer-Loyalty (Hadoop)
## Project Overview
This project focuses on creating a data pipeline using the Hadoop Ecosystem following the design pattern of the Lambda Architecture. This architecture enables event-driven processing when handling big datasets as it processes large data sets in the batch layer and real-time data in the speed layer.

**Batch Layer**

The process starts by extracting data from CSV files and ingesting it into HDFS. Spark SQL is then used to transform the data, and finally, the data is loaded into the Hive table ```customers_cln```. This process allows efficient management of large and complex datasets, as well as storing and preparing the data for future analysis.

**Speed Layer**

Apache Flume is used to collect real-time data from a shell script that generates order data. The shell script is configured as a source for Flume, and the data is sent to HDFS and HBase as sinks. The data in HDFS is then processed and transformed by Spark Streaming. The processed data is stored in the Hive table ```transactions_cln```, while the data in HBase is stored for efficient random access and analysis.

**Serving Layer**

It consists of Hive and HBase. Hive is used to combine data from the batch layer and speed layer by creating a new table called the ```loyalty``` table that joins data from the ```customers_cln``` and ```transactions_cln``` tables. HBase is used to store data from the speed layer that requires fast random read/write access. HBase shell or APIs can be used to retrieve the data.

In the case of requiring to update the loyalty table with new data, utilizing a workflow tool such as Apache Oozie can efficiently manage these processes. This tool can schedule workflows to run daily, weekly, or at desired intervals to execute Hive scripts that append new data to the existing structure of the ```loyalty``` table, aligning with the changes in the ```customers_cln``` and ```transactions_cln``` tables. This ensures that the data in the ```loyalty``` table remains accurate and ready for further analysis.
## About Dataset

## Architecture
![image](https://github.com/getnkit/Customer-Loyalty/blob/31660049d2b3cc665834784ff39ad75971690cc2/images/Data%20Architecture.png)
