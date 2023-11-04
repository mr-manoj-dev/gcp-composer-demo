# gcp-composer-demo
A sample demo to orchestrate workflow using google composer


login
gcloud auth login

set project-id
gcloud config set project burner-mankumar24-02


container-registry
gcloud auth configure-docker gcr.io

artifact-registry
gcloud auth configure-docker us-central1-docker.pkg.dev




-- build image without name
docker build . -f .docker/dockerfile/Dockerfile

-- create a docker image with given name
docker build -t gcr.io/burner-mankumar24-02/app_image/app-01-image:v0.1.0 -f Dockerfile .

artifact-registry
docker buildx build --platform linux/amd64 -f ./Dockerfile -t us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01-image:v2.1.0 .


-- push image to docker hub
docker push us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01-image:v0.1.0

