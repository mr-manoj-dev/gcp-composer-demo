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


gcloud composer environments delete $CMP_ENVIRONMENT_NAME \
    --location $CMP_LOCATION

end=`date +%s`
runtime=$((end-start))
echo "The request to create composer instance ${CMP_ENVIRONMENT_NAME} submitted. Check the GCP console to see the progress."