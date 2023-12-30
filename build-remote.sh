#!/usr/bin/env bash

service_name=irrigation-system-api
port=5000
version=v0.0.1
username=konstantiniakov

sudo docker login

# set up postgres and timescaledb on pi
sudo docker run --name smart-home-postgres -d --restart unless-stopped -p 5432:5432 -e POSTGRES_PASSWORD=$postgres_password -v ${PWD}/home/pi/data:/var/lib/postgresql/data postgres:16.1
sudo docker run --name smart-home-timescaledb -d --restart unless-stopped -p 5431:5432 -e POSTGRES_PASSWORD=$timescale_password -v ${PWD}/home/pi/data:/var/lib/postgresql/data timescale/timescaledb:latest-pg16

# pull and run image on pi
sudo docker pull $username/$service_name:$version
sudo docker run --add-host=host.docker.internal:host-gateway --name $service_name -d --restart unless-stopped -p $port:$port $username/$service_name:$version
