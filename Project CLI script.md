file/source
hadoop fs -mkdir /tmp/file \
hadoop fs -mkdir /tmp/file/sink \
hadoop fs -put /Customer-Loyalty/file/source/customer.csv /tmp/file/sink \

flume/source
mkdir hbase \
mkdir hdfs \
** ls (local) vs hadoop fs -ls (hadoop) \
hadoop fs -mkdir /tmp/flume \
hadoop fs -mkdir /tmp/flume/sink \
 \
hbase shell \
create 'spooled_table', 'spool_cf' \
list \
scan 'spooled_table' \
exit \
 \
 
flume/source
nohup flume-ng agent -n tier1 -f /Customer-Loyalty/flume/source/flume_hdfs.conf & \
nohup flume-ng agent -n tier2 -f /Customer-Loyalty/flume/source/flume_hbase.conf & \
jobs -l \
 \
nohup sh /Customer-Loyalty/flume/src_sys.sh & \
jobs -l \
 \

spark/
spark-submit /Customer-Loyalty/spark/spark.py \
nohup spark-submit /Customer-Loyalty/spark_streaming/spark_streaming.py & \
??? \

query hive ผ่าน CLI
hive -f /Customer-Loyalty/sql/create_hive_loyalty.sql \
 \

Error while compiling statement: FAILED: RuntimeException Cannot create staging directory 'hdfs://quickstart.cloudera:8020/tmp/default/loyalty/data_dt=2024-05-23/.hive-staging_hive_2024-05-23_15-41-45_235_4724603800764227713-1': Permission denied: user=cloudera, access=WRITE, inode="/tmp/default/loyalty":root:supergroup:drwxr-xr-x 
hadoop fs -chmod 777 /tmp/default/loyalty \
hadoop fs -put /Customer-Loyalty/sql/insert_hive_loyalty.sql /tmp/file \
??? \

1. เตรียม batch data
2. เตรียม speed data (log file) โดยการเขียน shell script เพื่อ gen data ขึ้นมา 
3. เตรียม folder, path ทั้ง local, hadoop สำหรับ source, sink ของ flume
sink hdfs เป็น folder
sink hbase เป็น hbase shell > table
4. รัน flume ด้วย nohup
5. รัน shell script ด้วย nohup
6. ไฟล์ไหลเข้าตามที่ config
7. ใช้ hive โดยที่ hive สามารถใส่ query เพื่อปรับเป็น mapreduce ได้ รัน mapreduce เข้าไป
8. สร้าง table hive มาครอบ csv ไฟล์ ทั้ง batch speed
9. clean ด้วย spark ทั้ง batch speed
10. สร้าง table hive ใหม่ ทั้ง batch speed
11. สร้าง loyalty ผ่าน cli
12. ให้สิท 777
13. insert ช้อมูลวันที่ต้องการเข้าไป
14. put ไฟล์ insert loyalty.sql ขึ้น hadoop
15. สร้าง oozie workflow
16. กำหนด coordinator (trigger, ตั้งเวลา)
17. ${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}

