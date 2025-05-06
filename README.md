# model-service

### 1. Launch a Bash session in the container 
docker run -it --rm -v ./:/app/model-service/ python:3.12.9-slim bash

### 2. Run the model on port 8080
docker run -it --rm -p 8080:5001 model-serv