service_name=irrigation-system-service
port=5000
version=0.0.1

docker build -t $service_name:v$version .

image_id = $(docker images -q $service_name)

docker run --name $service_name -dp 127.0.0.1:$port:$port $service_name:v$version
