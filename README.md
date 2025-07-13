## Клонировать репозиторий
```shell
git clone git@github.com:Valievx/notes-service.git
```

## Запустить сервисы
```shell
docker compose -f docker_compose/app.yaml --env-file .env up -d --build
docker compose -f docker_compose/storages.yaml --env-file .env up -d --build

Или с Makefile:
make all
```

## После запуска:
### - API: http://localhost:8000
### - Документация http://localhost:8000/api/docs/