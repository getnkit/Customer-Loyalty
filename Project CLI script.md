hadoop fs -put /Customer-Loyalty/file/source/customer.csv
hadoop fs -mkdir /tmp/file/sink
hadoop fs -put /Customer-Loyalty/file/source/customer.csv /tmp/file/sink
mkdir hbase
mkdir hdfs
hadoop fs -mkdir /tmp/flume/sink

hbase shell
create 'spooled_table', 'spool_cf'
scan 'spooled_table'
exit

nohup flume-ng agent -n tier1 -f /Customer-Loyalty/flume/source/flume_hdfs.conf &
nohup flume-ng agent -n tier2 -f /Customer-Loyalty/flume/source/flume_hbase.conf &
jobs -l

sh /Customer-Loyalty/flume/src_sys.sh &
jobs -l

spark-submit /Customer-Loyalty/spark/spark.py
???
hive -f /Customer-Loyalty/sql/create_hive_loyalty.sql

hadoop fs -chmod 777 /tmp/default/loyalty
hadoop fs -put /Customer-Loyalty/sql/insert_hive_loyalty.sql /tmp/file
???

