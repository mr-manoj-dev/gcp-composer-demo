#!/bin/bash

echo "Hello, world! from app-1"

# Create the directory if it doesn't exist
mkdir -p /airflow/xcom/


cd usr/local/bin/

echo "***** ls -al inside usr/local/bin/ ****"

ls -al

# Copy the file(return.json) into airflow/xcom folder
cp return.json /airflow/xcom/

#change the file permissions to make it readable
chmod +r /airflow/xcom/return.json






