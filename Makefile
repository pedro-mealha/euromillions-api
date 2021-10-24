ifneq ("$(wildcard ./.env)","")
	include .env
endif

start:
	flask run

setup:
	python3.9 setup.py $(year)

new_migration:
	yoyo new ./db/migrations -m "$(name)"

migrate:
	yoyo apply --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

migrate_rollback:
	yoyo rollback --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

logs_prod:
	heroku logs --tail --app euro-millions-api

logs_stg:
	heroku logs --tail --app staging-euro-millions-api

start_docker:
	docker-compose up --build -d

start_db:
	docker-compose up --build -d -- db
