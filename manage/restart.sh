#!/usr/bin/env bash

set -e

cd ..

set -a
source $PWD/.env
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=ore_concentrate-dev
  echo "The development containers are restarting ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.dev.yml restart
  ;;
*)
  export COMPOSE_PROJECT_NAME=ore_concentrate
  echo "The production containers are restarting ..."
  docker compose -f docker/docker-compose.base.yml -f docker/docker-compose.prod.yml restart
  ;;
esac