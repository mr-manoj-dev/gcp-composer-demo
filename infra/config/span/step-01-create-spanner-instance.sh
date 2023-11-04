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


gcloud spanner instances create span-demo-01 --config=regional-us-central1 \
    --description="span-demo-01" --nodes=1

gcloud spanner databases create demo-db-01 \
  --instance=span-demo-01 

end=`date +%s`
runtime=$((end-start))
echo "Spanner instance creation requested and took : ${runtime} seconds!"