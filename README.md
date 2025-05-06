# model-service

### 1. Launch a Bash session in the container 
docker build -t app

### 2. Run the model on port 8080
docker run -it --rm -p 8080:5001 app