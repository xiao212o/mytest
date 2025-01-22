#!/bin/bash

name="debug/$(pwd | sed -r 's/^.+\///' | sed -r 's/-/_/g')"
hostname=$(echo "$name" | awk -F'/' '{print $NF}' | sed -r 's/^project_//g')
port=8952

if [ "$1" = '--build' ]; then
  bash ./build-docker.sh -t "${name}"
fi

docker-compose up -d --remove-orphans

pwd=$(pwd)
docker run --hostname="${hostname}":${port} -it --rm \
  -v "/d/pycode/fastapi-app:/app" \
  -p "${port}:8000" \
  --network dev_net \
  "${name}" bash

docker-compose down
