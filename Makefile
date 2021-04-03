ifneq ("$(wildcard ./.env)","")
    include .env
endif

start:
	flask run

setup:
	python3 setup.py $(year)

new_migration:
	yoyo new ./db/migrations -m "$(name)"

migrate:
	yoyo apply --database postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_SCHEMA} ./db/migrations
