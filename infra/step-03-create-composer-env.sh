#!/bin/bash
start=`date +%s`

# check authorisation
authorizedAccount=$(gcloud auth list --filter=status.ACTIVE --format="value(account)")
if [ -z $authorizedAccount ]; then
    echo "Not authorized to run ...!"
    exit 1
else
    echo "Authorized to run ..."
    if [[<check_parameter>]]; then
        echo "In sufficient arguemt"
        exit 1
    fi
fi    

# Set variables
PROJECT_ID="burner-mankumar24-02"
ENVIRONMENT_NAME="ccpv1-01"
LOCATION="us-central1"



gcloud iam service-accounts add-iam-policy-binding \
    ccp-demo-svc@burner-mankumar24-02.iam.gserviceaccount.com \
    --member service-866897393923@cloudcomposer-accounts.iam.gserviceaccount.com \
    --role roles/composer.ServiceAgentV2Ext



# gcloud composer environments create $ENVIRONMENT_NAME \
#     --project $PROJECT_ID \
#     --location $LOCATION \
#     --image-version composer-2.3.2-airflow-2.4.3 \
#     --network projects/$PROJECT_ID/global/networks/ide-vpc \
#     --subnetwork projects/$PROJECT_ID/regions/$LOCATION/subnetworks/ide-vpc \
#     --service-account ccp-demo-svc@burner-mankumar24-02.iam.gserviceaccount.com \
#     --enable-private-environment \
#     --web-server-allow-all

# Create Composer environment
gcloud composer environments create $ENVIRONMENT_NAME \
    --project $PROJECT_ID \
    --location=$LOCATION \
    --image-version=composer-1.20.12-airflow-2.4.3 \
    --node-count=3 \
    --zone=us-central1-a \
    --machine-type=n1-standard-1 \
    --disk-size=100GB \
    --service-account=ccp-demo-svc@burner-mankumar24-02.iam.gserviceaccount.com \
    --web-server-machine-type=composer-n1-webserver-2 \
    --enable-ip-alias \
    --async

