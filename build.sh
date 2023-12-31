#!/usr/bin/env bash

SERVICE_NAME=irrigation-system-api
VERSION=v0.0.1
USERNAME=konstantiniakov
SERVER=pi@controller.local

printf "VERSION=$VERSION\nSERVICE_NAME=$SERVICE_NAME" >.env;

# empty data folder
rm -rf data/*

# clean up volumes
docker compose down --volumes

# remove docker images and containers
docker container stop $(docker ps -a -q)
docker image rm -f $(docker images -q)

# compose the application locally
docker compose build api

# sign in into hub
docker login

echo Pushing image to Docker Hub
# add username to image tag and push to hub
image_id=$(docker images -q $SERVICE_NAME)
docker tag $image_id $USERNAME/$SERVICE_NAME:$VERSION
docker push $USERNAME/$SERVICE_NAME:$VERSION

## remove containers, images and db data
container_ids=$(ssh $SERVER "sudo docker ps -a -q")
image_ids=$(ssh $SERVER "sudo docker images -a -q")

ssh $SERVER "sudo docker container rm -f ${container_ids//$'\n'/ };\
  sudo docker rmi -f ${image_ids//$'\n'/ }"
ssh $SERVER "sudo rm -rf ~/data/*"

# make directories, copy necessary files
ssh $SERVER "mkdir ~/sql; mkdir ~/data; mkdir ~/config;"

scp sql/init-postgres.sql sql/init-timescale.sql $SERVER:~/sql/
scp docker-compose.yml $SERVER:~/
scp config/.api.env config/.postgres.env config/.timescaledb.env $SERVER:~/config/

## run and compose services
ssh $SERVER "sudo docker pull $USERNAME/$SERVICE_NAME:$VERSION;"
ssh $SERVER "sudo docker run\
 --add-host=host.docker.internal:host-gateway\
 --env-file=./config/.api.env\
 --name $SERVICE_NAME\
 -d\
 --restart unless-stopped\
 -p 5000:5000\
 $USERNAME/$SERVICE_NAME:$VERSION"
ssh $SERVER "sudo docker compose up postgresdb"
##ssh $SERVER "sudo docker compose run timescaledb"
