#!/bin/bash

# Build the Docker image if it doesn't exist
docker build -t repocleanup:latest .

# Run the Docker container
docker run --rm -it \
    --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
    --name repocleanup \
    -v $(pwd):/workspace \
    -w /workspace \
    repocleanup:latest
