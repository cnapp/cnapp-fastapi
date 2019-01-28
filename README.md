# CNAPPS / Python FastAPI

Features:

* [x] Logging
* [ ] Metrics
* [ ] Tracing

## Local

Execute in local:

    $ make run

check health:

    $ curl http://127.0.0.1:9393/version
    {"version":"0.1.0"}

    $ curl http://127.0.0.1:9393/health


## Local with Docker

Build the Docker image:

    $ make minikube-build

Run a container:

    $ make docker-run


## Minikube

Build the Docker image into minikube:

    $ make minikube-build

Deploy the application into minikube:

    $ make minikube-deploy

Add to your `/etc/hosts` the URI :

    $ echo $(KUBECONFIG=./deploy/minikube-kube-config minikube ip) fastapi.cnapps.minikube | sudo tee -a /etc/hosts

Then check the service on URL : http://fastapi.cnapps.minikube/

Undeploy the application from minikube:

    $ make minikube-undeploy