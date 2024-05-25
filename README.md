# Customer-Loyalty (Hadoop)
## Project Overview
This project focuses on building a data pipeline using the Hadoop Ecosystem following the design pattern of the Lambda Architecture. This architecture enables event-driven processing when handling big datasets as it processes large data sets in the batch layer and real-time data in the speed layer.

**Batch Layer**

The process starts by extracting data from CSV files and ingesting it into HDFS. Spark SQL is then used to transform the data, and finally, the data is loaded into the Hive table ```customers_cln```.

**Speed Layer**

Apache Flume is used to collect real-time data from a shell script that generates order data in the form of log files. The shell script is configured as a source for Flume, and the data is sent to HDFS and HBase as sinks. The data in HDFS is then processed and transformed by Spark Streaming. The processed data is stored in the Hive table ```transactions_cln```.

**Serving Layer**

It consists of Hive and HBase. Hive is used to combine data from the batch layer and speed layer by creating a new table called the ```loyalty``` table that joins data from the ```customers_cln``` table and ```transactions_cln``` table. HBase is used to store data from the speed layer that requires fast random read/write access.

To update the ```loyalty``` table with new data, utilize a workflow scheduling tool like Apache Oozie to create repeatable workflows. It schedules workflows to execute Hive scripts appending new data to the existing ```loyalty``` table structure, aligning with changes in the ```customers_cln``` table and ```transactions_cln``` table.

## About Dataset
This dataset consists of customer data from a beverage shop such as names, dates of birth, and contact information. Additionally, this project generates real-time order data for each customer to simulate what orders each customer places and when. All of this data is collected for analysis and customer segmentation by calculating loyalty card point accumulation and offering promotions to customers accordingly.
## Architecture
![image](https://github.com/getnkit/Customer-Loyalty/blob/31660049d2b3cc665834784ff39ad75971690cc2/images/Data%20Architecture.png)
## Implementation
### Step 1:
1. สร้าง file ที่จำเป็นต่อการเริ่มต้นทำโปรเจค ได้แก่ Shell Script, CONF File, และ Python Source File จากนั้น push a file to Git Repository
1.1. Shell Script: เขียนขึ้นเพื่อสร้างข้อมูลคำสั่งซื้อสินค้าสมมติขึ้นมา โดยจะสุ่มเลือก ID ลูกค้า, รายการเครื่องดื่ม, และเวลาที่สั่ง (timestamp) จากนั้นบันทึกข้อมูลดังกล่าวลงในไฟล์ใน directory (HDFS และ HBase) ทุกๆ 30 วินาที.
1.2. CONF File: กำหนดค่าคอนฟิกสำหรับ Apache Flume โดยกำหนดข้อมูล channel, source, และ sink สำหรับ agent ซึ่ง source จะรับไฟล์จาก spool directory และส่งข้อมูลไปยัง channel ที่เชื่อมต่อกับ sink เพื่อบันทึกข้อมูลลงใน HDFS และ HBase
1.3: spark_sql.py: โค้ดนี้ทำการดึงข้อมูลลูกค้าจาก Hive table ```customers``` นำมาทำการทำความสะอาดและจัดรูปแบบข้อมูล และเขียนผลลัพธ์ลงใน HDFS โดยใช้ PySpark.
1.4: spark_streaming.py: โค้ดนี้ทำการอ่านข้อมูลแบบสตรีมจาก structured text files (log files) ที่สร้างขึ้นโดย shell script จากนั้นทำการประมวลผลข้อมูล เลือกคอลัมน์ที่ต้องการ และเขียนข้อมูลในรูปแบบไฟล์ Parquet โดยใช้ Spark Structured Streaming ซึ่งจะมีข้อมูลเพิ่มเข้าไปใหม่ในไฟล์นี้เรื่อยๆ 
2. สร้าง compute engine (VM) บน GCP เพื่อติดตั้ง Cloudera Docker Container สำหรับการใช้งาน Cloudera manager และ Cloudera Hue
3. Install and running Cloudera Docker Container on Ubuntu 20.04, Configure Cloudera Manager, และ Clone Git Repository ตามที่ระบุไว้ในไฟล์ Cloudera installation with Docker.md
4. import ไฟล์ csv ที่จะทำหน้าที่เป็น source systems ของ batch layer ลงบน HDFS
5. สร้าง path สำหรับ Flume sink ของ HDFS เป็น directory และ Flume sink ของ hbase เป็น table
6. เรียกใช้ Flume agent เพื่อส่งข้อมูลไปยัง HDFS และ HBase
nohup & ใช้เพื่อป้องกันไม่ให้ background process หยุดทำงาน แม้ว่าจะออกจากเชลล์หรือปิดเทอร์มินัลลงไปแล้ว
7. เรียกใช้ Shell Script that generates order data in the form of log files และทำหน้าที่เป็น source systems ของ speed layer
8. Execute HiveQL ด้วยโค้ดใน create_hive_customers.sql และ create_hive_transactions.sql เพื่อสร้างตารางขึ้นมาใหม่ โดยอ่านข้อมูลจาก path ที่ระบุไว้
9. เรียกใช้ Spark และรันไฟล์ spark_sql.py และ spark_streaming.py เพื่อทำความสะอาดและประมวลผลข้อมูล
10. Execute HiveQL ด้วยโค้ดใน create_hive_loyalty.sql เพื่อสร้าง External Table ```loyalty``` ขึ้นผ่าน CLI
TABLE (Internal Table) ใช้สำหรับสร้างตารางแบบภายในฐานข้อมูล เมื่อลบตารางออกจากระบบ ข้อมูลก็จะถูกลบไปด้วย
ขณะที่ External Table ใช้สำหรับเชื่อมโยงกับข้อมูลภายนอก เมื่อลบตาราง ข้อมูลจะยังคงอยู่ในแหล่งเก็บข้อมูลภายนอก
การทำงานของ external table คือเพียงแค่ link ไปยังตำแหน่งของข้อมูลจริงภายนอกเท่านั้น ข้อมูลจะไม่ถูกเก็บไว้ในฐานข้อมูล ดังนั้นจึงจำเป็นต้องสร้าง external table ก่อน เพื่อระบบทราบตำแหน่งและโครงสร้างของข้อมูลภายนอกนั้น จากนั้นจึงนำเข้าข้อมูลได้
13. กำหนดสิทธิ์ให้ user cloudera สามารถ write ไฟล์ไปยัง /tmp/default/loyalty/ ได้
By default, หากไม่กำหนดสิทธิ์การเข้าถึงไดเรกทอรี /tmp/default/loyalty จะขึ้น error แบบนี้ (ใส่รูป/error code) 
ดังนั้นจึงต้องกำหนดสิทธิ์การเข้าถึงไดเรกทอรีให้ทุกคนสามารถอ่าน เขียน และดำเนินการได้ ด้วยคำสั่งด้านล่างนี้
(รูป)
**Warning! Using chmod 777 is bad practice because it grants unrestricted read, write, and execute permissions to everyone, which may create security vulnerabilities.**
12. Execute HiveQL ด้วยโค้ดใน insert_hive_loyalty.sql เพื่อ insert ช้อมูลจากตาราง customers_cln และตาราง transactions_cln เข้าไปในตาราง ```loyalty```
7. 
