SCRIPTS_PATH=scripts
CRONJOBS_PATH=${SCRIPTS_PATH}/cronjobs

ifneq ("$(wildcard ./.env)","")
	include .env
endif

start:
	flask run

add-draws:
	python3 -m scripts.cronjobs.add_new_draws

setup:
	python3 -m scripts.setup $(year)

new-migration:
	yoyo new ./db/migrations --sql -m "$(name)"

migrate:
	yoyo apply --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}?schema=${DB_SCHEMA}&port=${DB_PORT}

migrate-rollback:
	yoyo rollback --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}?schema=${DB_SCHEMA}&port=${DB_PORT}

logs-prod:
	flyctl logs --app prod-euromillions-api

logs-stg:
	flyctl logs --app staging-euromillions-api

start-docker:
	docker-compose up --build -d

start-db:
	docker-compose up --build -d -- db
