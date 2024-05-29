# How to install and running Cloudera Docker Container on Ubuntu 20.04
### Step 1: Install Docker on Ubuntu following Step 1 from the DigitalOcean guide 
First, update your existing list of packages:
```bash
sudo apt update
```
Next, install a few prerequisite packages which let apt use packages over HTTPS:
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
Then add the GPG key for the official Docker repository to your system:
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
Add the Docker repository to APT sources:
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
This will also update our package database with the Docker packages from the newly added repo.

Make sure you are about to install from the Docker repo instead of the default Ubuntu repo:
```bash
apt-cache policy docker-ce
```
Finally, install Docker:
```bash
sudo apt install docker-ce
```
Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:
```bash
sudo systemctl status docker
```
### Step 2: Pull the Docker image for use on your VM
```bash
sudo docker pull mikelemikelo/cloudera-spark:latest
``` 
### Step 3: Quickly create and run a Cloudera Spark environment on Docker
```
sudo docker run --hostname=quickstart.cloudera --privileged=true -it -p 8888:8888 -p 8080:8080 -p 7180:7180 \
-p 88:88/udp -p 88:88 mikelemikelo/cloudera-spark:latest /usr/bin/docker-quickstart-light
```
### Step 4: Start Cloudera Manager
```
sudo /home/cloudera/cloudera-manager --express && service ntpd start
```
# Configure Cloudera Manager
### Step 1: Use the VM's Public/External IP address to access Cloudera Manager through port 7180
### Step 2: Go to the Hive service and set the configuration of Spark on YARN Service to none
To simplify the system, as using Hive on Spark is more complex than using MapReduce due to the multiple components involved.
### Step 3: Remove unused and unnecessary services, such as Spark and Key-Value Store Indexer Actions
Since the Spark version in this CDH installation is 1.x.x, which does not support Spark Structured Streaming, remove this service and use the Spark Local installation that is already available in the Docker container.
### Step 4: Add Flume service and Select the set of dependencies for your new Flume: HBase, HDFS, and ZooKeeper
* Selecting both HBase and HDFS as dependencies allows Flume to write data to both systems.
* ZooKeeper is used for service distribution and leader election in Flume, which is necessary for its distributed operation.
### Step 5: Start the cluster and wait until all services are in the all-up-and-running state
### Step 6: Use the VM's Public/External IP address to access Cloudera HUE through port 8888

# Clone Git Repository
Press Ctrl+P+Q to detach from the Docker container, leaving it running in the background
Clone Git Repository
```
git clone https://github.com/getnkit/<repository-name>.git
```
Check the container ID of Cloudera:
```
docker container ls
```
Copy the files from the Git repository into the Cloudera Docker container:
```
docker cp <repository-name> <container_id>:/
```
Re-enter or re-attach to the container:
```
docker exec -it <container_id> /bin/bash
```
```
cd ../..
```
Finally, the copied files will be found!
