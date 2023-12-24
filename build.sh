#!/usr/bin/env bash

service_name=irrigation-system-api
port=5000
version=0.0.1
username=konstantiniakov

docker login

docker build -t $service_name:v$version .
#docker run --name $service_name -dp $port:$port $service_name:v$version

image_id=$(docker images -q $service_name)
docker tag $image_id $username/$service_name:v$version
docker push $username/$service_name:v$version

# 127.0.0.1:$port:$port not to expose to the outside world

# set up databases on pi
# docker run --name smart-home-postgres -d --restart unless-stopped -p 5432:5432 -e POSTGRES_PASSWORD=
# -v ${PWD}/home/pi/data:/var/lib/postgresql/data postgres:16.1
#docker run --name smart-home-timescaledb -d --restart unless-stopped -p 5431:5432 -e POSTGRES_PASSWORD=
#-v ${PWD}/home/pi/data:/var/lib/postgresql/data timescale/timescaledb:latest-pg16

# pull and run image on pi
# sudo docker pull $username/$service_name:v$version
# sudo docker run --add-host=host.docker.internal:host-gateway --name $service_name -d --restart unless-stopped -p $port:$port $username/$service_name:v$version