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


#Add roles to the service account
SERVICE_ACCOUNT="${CMP_SVC_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com"
for ROLE in "${ROLES[@]}"
do
  echo "gcloud projects add-iam-policy-binding $GCP_PROJECT_ID --member=serviceAccount:$SERVICE_ACCOUNT --role=$ROLE"
  gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="$ROLE"
done


end=`date +%s`
runtime=$((end-start))
echo "All done and took : ${runtime} seconds!"