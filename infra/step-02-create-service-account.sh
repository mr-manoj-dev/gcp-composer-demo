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

# Check for service account already exists or not. Create a new if doesn't exist.
gcloud iam service-accounts describe ${SERVICE_ACCOUNT}
return_code=$?
if [ $return_code -eq 0 ]; then
    echo "Service account already exists!"
else    
    echo "Creating service account : ${SERVICE_ACCOUNT}"
    gcloud iam service-accounts create $CMP_SVC_ACCOUNT --description "service account for composer" --display-name "service account for composer"
fi    

end=`date +%s`
runtime=$((end-start))
echo "All done and took : ${runtime} seconds!"
