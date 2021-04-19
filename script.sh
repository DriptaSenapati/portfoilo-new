#!/bin/bash

cd /home/driptasenapati97/portfolio-new/

git pull origin master


if [ $? -eq 0 ]; then
    sudo docker-compose up --build -d
    sudo service supervisor restart
fi
