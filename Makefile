.PHONY: help build push clean

# Define variables
IMAGE_NAME = V8
IMAGE_TAG = latest
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
DOCKER_VERSION = $(shell node -p -e "require('./package.json').version")

build:  ## Build the Docker image
	docker build \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		DOCKER_VERSION=$(DOCKER_VERSION) \
		-t $(IMAGE_NAME):$(IMAGE_TAG) .

push: ## Push the Docker image to a container registry
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)

clean:  ## Remove the Docker image
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

deploy: clean build push  ## Deploy means: clean build push

# Help section
help:  ## Display help message
	@echo '$(IMAGE_NAME):$(IMAGE_TAG) Docker image build file'
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

# Default command
.DEFAULT_GOAL := help
