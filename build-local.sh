#!/usr/bin/env bash

service_name=irrigation-system-api
port=5000
version=v0.0.1
username=konstantiniakov

docker login

# build local and remote images (remote image for docker hub)
docker build -t $service_name:$version .
image_id=$(docker images -q $service_name)
docker tag $image_id $username/$service_name:$version

# run local docker container
docker run --name $service_name -dp $port:$port $service_name:$version

# push image to hub
docker push $username/$service_name:$version

# add 127.0.0.1:$port:$port not to expose to the outside world
