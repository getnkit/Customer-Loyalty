#!/bin/bash

# Define the beverage list and prices
declare -a orders=("espresso 65" "cappucino 90" "mocha 80" "latte 70" "chocolate 60" "greentea 60")

# Loop to generate orders
for i in $(seq 1 100)
do
    while true
    do
        # Generate customer IDs
        id=$((1 + $RANDOM % 1000))
        if ((id >= 1 && id <= 801)) || ((id >= 5001 && id <= 5945)) || ((id >= 8000 && id <= 8501));
        then
            break
        else
            continue
        fi
    done
   # Generate order timestamps
   timestamp=$(date +%s)
   # Select random beverages and prices: ${orders[$RANDOM%${#orders[@]}]}
   # Write order data to files
   echo "$id|${orders[$RANDOM%${#orders[@]}]}|$timestamp" >> /Customer_Loyalty/flume/source/hdfs/order_${timestamp}.txt
   echo "$id|${orders[$RANDOM%${#orders[@]}]}|$timestamp" >> /Customer_Loyalty/flume/source/hbase/order_${timestamp}.txt
   # Sleep for 30 seconds before starting the next iteration of the loop
   sleep 30
done
  
