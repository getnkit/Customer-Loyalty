# Data Pipelines on Hadoop for Customer Loyalty Program
## Project Overview
This project focuses on building data pipelines using the Hadoop Ecosystem following the design pattern of the Lambda Architecture. This architecture enables event-driven processing when handling big datasets as it processes large data sets in the batch layer and real-time data in the speed layer.

**Batch Layer**

The process starts by extracting data from CSV files and ingesting it into HDFS. Spark SQL is then used to transform the data, and finally, the data is loaded into the Hive table ```customers_cln```.

**Speed Layer**

Apache Flume is used to collect real-time data from a shell script that generates order data in the form of log files. The shell script is configured as a source for Flume, and the data is sent to HDFS and HBase as sinks. The data in HDFS is then processed and transformed by Spark Streaming. The processed data is stored in the Hive table ```transactions_cln```.

**Serving Layer**

It consists of Hive and HBase. Hive is used to combine data from the batch layer and speed layer by creating a new table called the ```loyalty``` table that joins data from the ```customers_cln``` and ```transactions_cln``` tables. HBase is used to store data from the speed layer that requires fast random read/write access.

To update the ```loyalty``` table with new data, utilize a workflow scheduling tool like Apache Oozie to create repeatable workflows. It schedules workflows to execute Hive scripts appending new data to the existing ```loyalty``` table structure, aligning with changes in the ```customers_cln``` and ```transactions_cln``` tables.
## About Dataset
This dataset consists of customer data from a beverage shop such as names, dates of birth, and contact information. Additionally, this project generates real-time order data for each customer to simulate what orders each customer places and when. All of this data is collected for customer analysis and segmentation by calculating loyalty card point accumulation, to support an effective customer loyalty program by offering targeted promotions to customers.
## Architecture
![image](https://github.com/getnkit/Data-Pipelines-on-Hadoop-for-Customer-Loyalty-Program/blob/122228104c802d9363f5bfbc42f39cfb2ebb0637/images/Data%20Architecture.png)
## Implementation
### Step 1: Create the necessary files to start the project, then push the files to the Git Repository
- **Shell Script:** Written to create simulated purchase order data by randomly selecting customer IDs, beverage items, and timestamps. This data will be recorded in files in the directory (HDFS and HBase) every 30 seconds.
- **CONF File:** Configure settings for Apache Flume by defining the channel, source, and sink for the agent. The source will receive files from the spool directory and send data to the channel connected to the sink to store data in HDFS and HBase.
- **spark_sql.py:** This code retrieves customer data from the Hive table ```customers```, cleans and formats the data, and writes the data to HDFS using PySpark.
- **spark_streaming.py:** This code reads streaming data from structured text files (log files) created by the shell script, processes the data, selects the desired columns, and writes the data in Parquet file format to HDFS using Spark Structured Streaming. New data will be continually appended to this file.
### Step 2: Create a compute engine (VM) on GCP to install the Cloudera Docker Container for using Cloudera Manager and Cloudera Hue
![image](https://github.com/getnkit/Data-Pipelines-on-Hadoop-for-Customer-Loyalty-Program/blob/d8829ec3149796b45ae10980c83eaa1716d4fe39/images/Machine%20configuration.png)
![image](https://github.com/getnkit/Data-Pipelines-on-Hadoop-for-Customer-Loyalty-Program/blob/d8829ec3149796b45ae10980c83eaa1716d4fe39/images/Firewalls.png)
![image](https://github.com/getnkit/Data-Pipelines-on-Hadoop-for-Customer-Loyalty-Program/blob/d0c06c9d4662c89aa74859101bddf7bfb0699d3a/images/Boot%20disk.png)
### Step 3: Install and running Cloudera Docker Container on Ubuntu 20.04, Configure Cloudera Manager, and Clone Git Repository as specified in the ```Cloudera installation with Docker.md``` file
![image](https://github.com/getnkit/Customer-Loyalty/blob/eb2c95db1a88358fd652ab3daca16f21c0996a61/images/Cloudera%20Manager%20UI.png)
### Step 4: Import the CSV files that serve as the source systems for the batch layer into HDFS
```
hadoop fs -mkdir /tmp/file
hadoop fs -mkdir /tmp/file/sink
hadoop fs -put /<repository_name>/file/source/customer.csv /tmp/file/sink
```
### Step 5: Create paths for the Flume sink of HDFS as a directory and the Flume sink of HBase as a table
```
hadoop fs -mkdir /tmp/flume
hadoop fs -mkdir /tmp/flume/sink
```
```
hbase shell
create 'spooled_table', 'spool_cf'
scan 'spooled_table'
exit
```
### Step 6: Run the Flume agent to send data to HDFS and HBase
```
nohup flume-ng agent -n tier1 -f /<repository_name>/flume/source/flume_hdfs.conf &
nohup flume-ng agent -n tier2 -f /<repository_name>/flume/source/flume_hbase.conf &
jobs -l
```
Additionally, nohup & is used to prevent background processes from stopping when exiting the shell or closing the terminal
### Step 7: Run the Shell Script that generates order data in the form of log files and serves as the source systems for the speed layer
```
nohup sh /<repository_name>/flume/src_sys.sh &
jobs -l
```
Transaction logs serve as the data source. Flume receives new log entries from the Source and sends them to HDFS and HBase as Sinks.

![image](https://github.com/getnkit/Customer-Loyalty/blob/c36a8fb0b3fd10fc4bfe295f8f30d871f28e94d6/images/Flume%20sink.jpg)
### Step 8: Execute HiveQL with the code in ```create_hive_customers.sql``` and ```create_hive_transactions.sql``` to create new internal tables through the Query Editor.
Because performance is the priority, one should consider using an internal table, as it is stored and managed within the Hive Metastore, allowing for optimized data access and processing.
### Step 9: Run the spark-submit command to execute the ```spark_sql.py``` and ```spark_streaming.py``` files to clean and process the data
```
nohup spark-submit /<repository_name>/spark_streaming/spark_streaming.py & 
```
### Step 10: Execute HiveQL with the code in ```create_hive_customers_cln.sql``` and ```create_hive_transactions_cln.sql``` to create new external tables through the Query Editor.
Because the data is critical and of high importance, one should use an external table so that the underlying data files cannot be dropped even if the 'DROP TABLE' command is run accidentally by the user. This ensures the security of the data.

![image](https://github.com/getnkit/Customer-Loyalty/blob/eb2c95db1a88358fd652ab3daca16f21c0996a61/images/customers_cln%20table.png)
![image](https://github.com/getnkit/Customer-Loyalty/blob/eb2c95db1a88358fd652ab3daca16f21c0996a61/images/transactions_cln%20table.png)
### Step 11: Execute HiveQL with the code in ```create_hive_loyalty.sql``` to create a new external table through the CLI
```
hive -f /<repository_name>/sql/create_hive_loyalty.sql
```
### Step 12: Grant the cloudera user write permissions to the /tmp/default/loyalty/ directory
By default, if access permissions are not granted to the /tmp/default/loyalty/ directory, an error like this will occur:
```
Error while compiling statement: FAILED: RuntimeException Cannot create staging directory 'hdfs://quickstart.cloudera:8020/tmp/default/loyalty/data_dt=2024-05-23/.hive-staging_hive_2024-05-23_15-41-45_235_4724603800764227713-1': Permission denied: user=cloudera, access=WRITE, inode="/tmp/default/loyalty":root:supergroup:drwxr-xr-x
```
Therefore, we need to grant read, write, and execute permissions to everyone for this directory using the following command:
```
hadoop fs -chmod 777 /tmp/default/loyalty
```
**Warning! Using chmod 777 is bad practice because it grants unrestricted read, write, and execute permissions to everyone, which may create security vulnerabilities.**
### Step 13: Import the ```insert_hive_loyalty.sql``` file into HDFS. This file will retrieve data from the ```customers_cln``` and ```transactions_cln``` tables and insert it into the ```loyalty``` table
```
hadoop fs -put /<repository_name>/sql/insert_hive_loyalty.sql /tmp/file
```
![image](https://github.com/getnkit/Customer-Loyalty/blob/eb2c95db1a88358fd652ab3daca16f21c0996a61/images/loyalty%20table.png)

Separating the Hive scripts for creating the ```loyalty``` table (Step 11) and the scripts for inserting data into the table provides flexibility in managing workflows, including the ability to independently schedule data insertion.
### Step 14: Use Oozie to create workflows, then configure coordinators to trigger the workflow to run on specified dates and times
![image](https://github.com/getnkit/Customer-Loyalty/blob/eb2c95db1a88358fd652ab3daca16f21c0996a61/images/Oozie%20Dashboard.png)
### Step 15: Use Cloudera Manager to monitor the health and performance of the cluster components
![image](https://github.com/getnkit/Data-Pipelines-on-Hadoop-for-Customer-Loyalty-Program/blob/deb32df61f37251d234d67f38eb3c9e70d54c053/images/Services%20Monitoring.png)
