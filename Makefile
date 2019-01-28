# Copyright (C) 2019 Nicolas Lamirault <nicolas.lamirault@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

APP="cnapp-responder"

VERSION=$(shell \
	grep RELEASE cnapps/version.py \
	|awk -F'=' '{ print $$2 }' \
	|sed -e "s/[' ]//g")

NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

MAKE_COLOR=\033[33;01m%-20s\033[0m

DB_ENGINE = "cockroachdb://cnapps@192.168.99.100:32007/cnapps?sslmode=disable"

SHELL = /bin/bash
DOCKER = docker

IMAGE=$(APP)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo -e "$(OK_COLOR)==== $(APP) [$(VERSION)] ====$(NO_COLOR)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(MAKE_COLOR) : %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Cleanup
	@echo -e "$(OK_COLOR)[$(APP)] Cleanup environnement$(NO_COLOR)"
	@find . -name "*.pyc" | xargs rm -fr
	@find . -name "__pycache__" | xargs rm -fr

.PHONY: init
init: ## Initialize Python environment (python=x.y)
	@echo -e "$(OK_COLOR)[$(APP)] Initialize environnement$(NO_COLOR)"
	@test -f ~/.poetry/bin/poetry || curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
	@test -d venv || python3 -m venv venv
	@. venv/bin/activate && pip3 install --upgrade pip
	@. venv/bin/activate && ~/.poetry/bin/poetry install

.PHONY: pyfmt
pyfmt: ## Python formatting
	@echo -e "$(OK_COLOR)[$(APP)] Python fmt$(NO_COLOR)"
	@black -l 79 cnapps

.PHONY: run
run: ## Run application
	@echo -e "$(OK_COLOR)[$(APP)] Start$(NO_COLOR)"
	@. venv/bin/activate && \
		CNAPPS_DB_ENGINE=$(DB_ENGINE) \
		uvicorn run:app --debug --host=0.0.0.0 --port 9393

#
# Docker
#

.PHONY: docker-build
docker-build: ## Build Docker image for application
	@echo -e "$(OK_COLOR)[$(APP)] Build Docker Image$(NO_COLOR)"
	$(DOCKER) build \
		--build-arg http_proxy=$$http_proxy \
		--build-arg https_proxy=$$https_proxy \
		-t $(NAMESPACE)/$(IMAGE):$(VERSION) .

.PHONY: docker-debug
docker-debug: ## Run a shell into the Docker image
	@echo -e "$(OK_COLOR)[$(APP)] Build Docker Image$(NO_COLOR)"
	@$(DOCKER) run --rm \
		-it $(NAMESPACE)/$(IMAGE):$(VERSION) /bin/bash

.PHONY: docker-run
docker-run: ## Run application using Docker image with ip=x.x.x.x
	@echo -e "$(OK_COLOR)[$(APP)] Run Docker Container$(NO_COLOR)"
	@$(DOCKER) run --rm -p 9191:9191 \
		--name $(APP) $(NAMESPACE)/$(IMAGE):$(VERSION)

#
# Kubernetes
#

.PHONY: minikube-build
minikube-build: ## Build Docker image into Minikube
	@echo -e "$(OK_COLOR)[$(APP)] Deploy application to local Kubernetes$(NO_COLOR)"
	@eval $$(KUBECONFIG=../deploy/minikube/kube-config minikube docker-env -p cnapps); \
		$(DOCKER) build \
			--build-arg http_proxy=$$http_proxy \
			--build-arg https_proxy=$$https_proxy \
			-t $(IMAGE):$(VERSION) .

.PHONY: minikube-deploy
minikube-deploy: minikube-build ## Deploy application into Minikube
	@echo -e "$(OK_COLOR)[$(APP)] Deploy application to local Kubernetes$(NO_COLOR)"
	@./scripts/kubernetes.sh -c minikube -e local -p create -a $(APP) -d deploy/k8s/ -t $(VERSION)

.PHONY: minikube-undeploy
minikube-undeploy: ## Undeploy application into Minikube
	@echo -e "$(OK_COLOR)[$(APP)] Deploy application to local Kubernetes$(NO_COLOR)"
	@./scripts/kubernetes.sh -c minikube -e local -p destroy -a $(APP) -d deploy/k8s/ -t $(VERSION)