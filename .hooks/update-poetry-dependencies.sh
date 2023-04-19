#!/bin/bash

if [ ! -f requirements.txt ]; then
  echo "No requirements file found. Skipping."
  exit 0
fi

if ! poetry --version >/dev/null 2>&1; then
  echo "Seems the poetry is not installed."
  exit 1
fi

xargs poetry add <requirements.txt
exit_code=$?
if [ "$exit_code" != 0 ]; then
  echo "Operation failed with code $exit_code"
  exit $exit_code
fi

if ! git diff --quiet -- pyproject.toml; then
  echo "The pyproject.toml file has uncommitted changes."
  exit 1
fi
