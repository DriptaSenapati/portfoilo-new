#!/bin/bash

cd /home/driptasenapati97/portfoilo-new/

git pull origin master


if [ $? -eq 0 ]; then
    docker-compose up --build -d
    service supervisor restart
fi
