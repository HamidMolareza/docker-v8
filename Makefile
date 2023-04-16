.PHONY: help build push clean update-poetry-dependencies watch-actions release-action changelog-action build-push-docker

# Define variables
IMAGE_NAME = d8
IMAGE_TAG = latest
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
DOCKER_VERSION = $(shell node -p -e "require('./package.json').version")

REF := $(if $(ref),$(ref),"dev")
VERSION := $(if $(version),$(version),"")
SKIP_CHANGELOG := $(if $(skip_changelog),$(skip_changelog),true)
CREATE_PR_FOR_BRANCH := $(if $(create_pr_for_branch),$(create_pr_for_branch),"")

build:  ## Build the Docker image
	docker build \
		--build-arg DOCKER_BUILD_DATE=$(BUILD_DATE) \
		--build-arg DOCKER_VERSION=$(DOCKER_VERSION) \
		-t $(IMAGE_NAME):$(IMAGE_TAG) .

push: ## Push the Docker image to a container registry
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)

clean:  ## Remove the Docker image
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

deploy: clean build push  ## Deploy means: clean build push

update-poetry-dependencies:  ## Update poetry dependencies
	cat requirements.txt | xargs poetry add

# Targets for running workflow commands
watch-actions: ## Watch a run until it completes, showing its progress
	gh run watch; notify-send "run is done!"

changelog-action: ## Run changelog action
	gh workflow run Changelog --ref $(REF) -f version=$(VERSION)

release-action: ## Run release action
	gh workflow run Release --ref $(REF) -f skip_changelog=$(SKIP_CHANGELOG) -f version=$(VERSION) -f create_pr_for_branch=$(CREATE_PR_FOR_BRANCH)

build-push-docker: ## Build and Push the Docker image
	gh workflow run 'Push Docker Image' --ref dev

# Targets for running standard-version commands
version: ## Get current program version
	node -p -e "require('./package.json').version"

coverage-action:  ## Generate coverage report
	gh workflow run 'Coverage Report' --ref $(REF)

# Help section
help:  ## Display help message
	@echo '$(IMAGE_NAME):$(IMAGE_TAG) Docker image build file'
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

# Default command
.DEFAULT_GOAL := help
