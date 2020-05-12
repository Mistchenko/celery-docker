# celery-docker
Docker Django + Celery + Redis; xlrd

## Создать (пересобрать) конткйнер

`docker-compose build`

## Поднять контейнер

`docker-compose up`

или если нужно запустить только один контейнер

`docker-compose up celery`


## Запустить оболочку и удалить образ после выхода

`docker-compose run --rm django bash`