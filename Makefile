# Define variables
IMAGE_NAME = V8
IMAGE_TAG = latest
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
DOCKER_VERSION = $(shell node -p -e "require('./package.json').version")

# Build the Docker image
build:
	docker build \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		DOCKER_VERSION=$(DOCKER_VERSION) \
		-t $(IMAGE_NAME):$(IMAGE_TAG) .

# Push the Docker image to a container registry (change the registry URL and username as appropriate)
push:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push docker.io/HamidMolareza/$(IMAGE_NAME):$(IMAGE_TAG)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

# Help section
.PHONY: help
help:
	@echo '$(IMAGE_NAME):$(IMAGE_TAG) Docker image build file'
	@echo "Available targets:"
	@echo "  build: Build the Docker image with the current date as a build and version arguments."
	@echo "  push: Push the Docker image to a container registry."
	@echo "  clean: Remove the Docker image"
	@echo "  help: Show this help message."
	@echo "  deploy: Deploy the Docker image"

# Default command
.DEFAULT_GOAL := help

deploy: clean build push

.PHONY: build push clean
