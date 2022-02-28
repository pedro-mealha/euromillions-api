SCRIPTS_PATH=scripts
CRONJOBS_PATH=${SCRIPTS_PATH}/cronjobs

ifneq ("$(wildcard ./.env)","")
	include .env
endif

deps:
	pip3 install -r requirements.txt
	python3 setup.py install --user

start:
	flask run

add_draws:
	python3 $(CRONJOBS_PATH)/add_new_draws.py

setup:
	python3 $(SCRIPTS_PATH)/setup.py $(year)

new_migration:
	yoyo new ./db/migrations -m "$(name)"

migrate:
	yoyo apply --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

migrate_rollback:
	yoyo rollback --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

logs_prod:
	heroku logs --tail --app prod-euromillions-api

logs_stg:
	heroku logs --tail --app staging-euromillions-api

start_docker:
	docker-compose up --build -d

start_db:
	docker-compose up --build -d -- db
