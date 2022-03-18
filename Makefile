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

add-draws: deps
	python3 $(CRONJOBS_PATH)/add_new_draws.py

setup: deps
	python3 $(SCRIPTS_PATH)/setup.py $(year)

new-migration:
	yoyo new ./db/migrations -m "$(name)"

migrate:
	yoyo apply --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

migrate-rollback:
	yoyo rollback --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations

logs-prod:
	heroku logs --tail --app prod-euromillions-api

logs-stg:
	heroku logs --tail --app staging-euromillions-api

start-docker:
	docker-compose up --build -d

start-db:
	docker-compose up --build -d -- db
