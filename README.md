# Euromillions Public API
![Python: 3.9](https://img.shields.io/badge/Python-3.9-blue)
![pip: 21.0.1](https://img.shields.io/badge/pip-21.0.1-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/WeNeedThePoh/euromillions-api/graphs/commit-activity)

***Live URL:*** https://euro-millions-api.herokuapp.com

***Tech stack***: Python, Flask, PostgreSQL, Docker

***DISCLAIMER***: *Results data in this API are from https://www.euro-millions.com website HTML directly. The data is for informational purposes only, you should not construe any such information or other material as financial or other advice. Nothing contained on this API constitutes a solicitation, recommendation, endorsement, or offer to buy Euromillions tickets. This API is not affiliated in any kind to any Euromillions contest.*

A small REST API for Euromillions contest. Here you will find all results since 2004 and some statistics/analytics.

The endpoint to fecth draws has some cool features for filtering the draws by `year` or `dates`.

This was done due to the lack of a way to get this data easily. As this information is of public knowledge, institutions should provide an API for it.
Meanwhile, with these endpoints, the community can build amazing products around the Euromillions context, either a mobile app or a web app.

My goal will also be to build a web app to allow to generate numbers to play based on statistics/analytics.

## Docs

For the documentation we used the OpenAPI specification. We have all the available endpoints with the schemas and examples for each use case. It's not just because is an industry standard to use it but also because is really easy to update and to read.

Regarding the database we use the Database markup language -- DBML for short. Again it's really amazing and can put any new joiner into speed right away. There is also an online tool to visualize the table schemas.

**You can check the current docs** [here](https://euromillios-api.readme.io)

## Third-party data

For the euromillions draws results, we used the website https://www.euro-millions.com. It has pages with historic data for all existing draws results. We don't consume any API, we parsed the webpage for the specific data that we need.

For new draws we have the following cronjob running:
```
# Every Tuesday and Friday every 15min during 21h-23h
*/15 21-23 * * 2,5 curl -X POST 'https://euro-millions-api.herokuapp.com/draws'
```

## Deployments (CI/CD)

We are using heroku for hosting, so we have heroku directly connect to github, so every time we push to `main` we will trigger a new deploy to production. With this we have a true CI/CD deployment strategy, so whenever we push something is going straight to production.

We are using only one buildpack, that is the [python buildpack](https://github.com/heroku/heroku-buildpack-python) from heroku themselves.

To run the flask app we are simply using a Procfile and using the `web` command to initiate the flask app.

## Development

We have two ways to working locally on this project: docker or run flash app.

To get started clone the repo
```
git clone https://github.com/WeNeedThePoh/euromillions-api

cd euromillions-api
```

### Using docker
Build and start docker container
```
make start_docker
```

This will start a container with a postgres database and another container with a python image. In the python container it will copy all the projects file, install the requirements and lastly run the flask app.


### Without docker
Make sure you have python 3.9 installed and a postgres database.

Install requirements.
```
pip3.9 install -r requirements.txt
```

Run flask app
```
make start
```

### Migrations
For migrations we are using [yoyo](https://pypi.org/project/yoyo-migrations/).
It's really straight forward but nonetheless we have some commands on Makefile:

To run migrations:
```
make migrate
```

To rollback last migration:
```
make migrate_rollback
```

To create a new migration it's a little tricky, because we didn't like the .py file for it so we decided to use raw sql files. But this comes with a cost that we need to create new files manually.

Just follow the pattern that already exists and it should be fairly easy.

# License

MIT Licensed (file [LICENSE](LICENSE)).
