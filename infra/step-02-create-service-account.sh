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

# Create a new service account
gcloud iam service-accounts create ccpv1-svc --display-name "Service account used for composer"

# Add the roles to the service account
gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/composer.apiServiceAgent"

gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/composer.apiServiceAgentExtension"

gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/composer.worker"

gcloud projects add-iam-policy-binding burner-mankumar24-02 \
  --member="serviceAccount:ccpv1-svc@burner-mankumar24-02.iam.gserviceaccount.com" \
  --role="roles/container.admin"



end=`date +%s`
runtime=$((end-start))
echo "Execution completed for project: $project_id" and took $runtime seconds."