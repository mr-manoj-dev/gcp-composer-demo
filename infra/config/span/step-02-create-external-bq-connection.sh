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


bq mk --connection \
  --connection_type='CLOUD_SPANNER' \
  --properties='{"database":"projects/burner-mankumar24-02/instances/span-demo-01/databases/demo-db-01"}' \
  --project_id=burner-mankumar24-02 \
  --location=us-central1 \
  spn-con-02

end=`date +%s`
runtime=$((end-start))
echo "BiqQuery external connection created and took : ${runtime} seconds!"