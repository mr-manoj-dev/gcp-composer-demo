#!/bin/bash
start=`date +%s`

# check authorisation
authorizedAccount=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [ -z $authorizedAccount ]; then
    echo "Not authorized to run ...!"
    exit 1
else
    echo "Authorized to run ..."
fi   


config_file="env.config"
if [[ "$OSTYPE" == "darwin"* ]]; then
  config_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
else
  config_file="/home/appuser/infra"
fi

echo "config directory: $config_dir/config/${config_file}"
source $config_dir/config/${config_file}



SERVICE_ACCOUNT="${CMP_SVC_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com"

# Create Composer environment
# gcloud script to create composer-1 Environment
#gcloud composer environments create $CMP_ENVIRONMENT_NAME \
#    --project $GCP_PROJECT_ID \
#    --location=$CMP_LOCATION \
#    --image-version=composer-1.20.12-airflow-2.4.3 \
#    --node-count=3 \
#    --zone=us-central1-a \
#    --machine-type=n1-standard-1 \
#    --service-account=${CMP_SVC_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
#    --enable-ip-alias \
#    --async

gcloud composer environments create $CMP_ENVIRONMENT_NAME \
    --location $CMP_LOCATION \
    --image-version composer-3-airflow-2.7.3 \
    --service-account ${CMP_SVC_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com

end=`date +%s`
runtime=$((end-start))
echo "The request to create composer instance ${CMP_ENVIRONMENT_NAME} submitted. Check the GCP console to see the progress."