# gcp-composer-demo
A sample demo to orchestrate workflow using google composer


## Authenticate with your GCP identity
```bash
gcloud auth login
```
## set project-id
```bash
gcloud config set project <change_to_your_gcp_project_id>
``````
## Step-01 : Enable APIs
```bash
sh step-01-enable-apis.sh
```
> **NOTE**: The above script shall enable APIs for the use cases along with creation of composer environment and required for use cases. Do update if any new use cases require other APIs.


## Step-02 : Create service account
```bash
sh step-02-create-service-account.sh
```

## Step-03 : Grant required roles to service account created in previous step
```bash
sh step-03-grant-roles-service-account.sh
```
> **NOTE**: The above script shall add roles provided into the config file[/config/env.config] to the service account you just created.


## Step-04 : Create composer insance
```bash
sh step-04-create-composer-env.sh
```
> **NOTE**: This script will submit a request to provision composer instance(v1) with the provided configuration. It usually takes atleast 20 minutes to provision the instance.
Notice your bash console with message like below :
```
name: projects/<your_gcp_project_id>/locations/us-central1/operations/2bf23dcc-265c-49c4-be0d-8e8bac36d26a
The request to create composer instance ccpv1-01 submitted. Check the GCP console to see the progress.
```

## Verify composer instace into GCP console



docker buildx build --platform linux/amd64 -f ./Dockerfile -t us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01:v2.1.2 .

docker push us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01:v2.1.2

docker buildx build --platform linux/amd64 -f ./Dockerfile -t us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-02:v2.1.2 .



gcloud auth configure-docker us-central1-docker.pkg.dev

docker build -t us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01-image:v2.1.2 -f Dockerfile .

docker push us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01-image:v2.1.2