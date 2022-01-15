#!/bin/sh

PROJECT_DIR=app
autoflake --remove-all-unused-imports \
          --recursive \
          --remove-unused-variables \
          --in-place $PROJECT_DIR
black --line-length=80 \
      --experimental-string-processing $PROJECT_DIR
isort $PROJECT_DIR
flake8 $PROJECT_DIR
