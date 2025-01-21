#!/bin/bash

name=$(pwd | sed -r 's/^.+\///')
IMAGE_TAG=${name}

optstring=":t:"

while getopts ${optstring} arg; do
  case ${arg} in
  t)
    echo "${OPTARG}"
    IMAGE_TAG="${OPTARG}"
    ;;
  esac
done

docker build -f docker/Dockerfile -t "${IMAGE_TAG}" .
