Запуск:
docker compose -f docker_compose/storages.yaml --env-file .env up -d --build
docker compose -f docker_compose/app.yaml --env-file .env up -d --build

Либо через Makefile:
make all