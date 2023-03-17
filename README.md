# Euromillions Public API

![Python: 3.11](https://img.shields.io/badge/Python-3.11-blue)
![pip: 22.1.1](https://img.shields.io/badge/pip-22.1.1-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/pedro-mealha/euromillions-api/graphs/commit-activity)

***Prod URL:*** <https://euromillions.api.pedromealha.dev>  
***Staging URL:*** <https://euromillions.staging.api.pedromealha.dev>

***Tech stack***: Python, Flask, PostgreSQL, Docker, Terraform, Github Actions

***DISCLAIMER***:
*Results data in this API are parsed from <https://www.euro-millions.com> website. The data is for informational purposes only, you should not construe such information or other data as financial advice. Nothing contained on this API constitutes a solicitation, recommendation, endorsement, or offer to buy Euromillions tickets. This API is not affiliated in any kind to Euromillions organization.*

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

For the euromillions draws results, we used the website <https://www.euro-millions.com>. It has pages with historic data for all existing draws results. We don't consume any API, we parsed the webpage for the specific data that we need.

For new draws we have the following cronjob running:

```bash
# Every Tuesday and Friday every 15min during 21h-23h
*/15 21-23 * * 2,5 flyctl ssh console -a prod-euromillions-api -C "sh app/scripts/cronjobs/add_draws.sh"

*/15 21-23 * * 2,5 flyctl ssh console -a staging-euromillions-api -C "sh app/scripts/cronjobs/add_draws.sh"
```

This command will run the script to add draws inside our production and staging containers. This way we ensure that the code runs in the same enviornment and we don't need an exposed endpoint to do it.

## Deployments (CI/CD)

We took advantage of the power and simplicity that Github Actions have. It was easy to integrate our deployment flow for staging and production.
We also have Terraform running in all our workflows. Currently, we are using the Github container registry to push a docker image that we will use to run our API. Because Fly.io doesn't allow us to have different environments we needed to create different apps for staging and prod. As soon as we push the image we only need to make a new release to have a new version up and running.
This is a big improvement because now our API is running in a container, allowing to be easier to deploy and maintain.

## Terraform

Luckily we can use Terraform to manage Fly.io infra with code. As there isn't much to do, right now we use terraform to create the app, the app public IPs and domain certificates. For the database, Fly.io still doens't allow to manage them using terraform, so we had to create them manually using `flyctl`. This is integrated into our CI in the staging and prod workflows with their respective workspaces.

## Development

We have two ways to working locally on this project: docker or run flash app.

To get started clone the repo

```bash
git clone https://github.com/pedro-mealha/euromillions-api

cd euromillions-api
```

### Using docker

Build and start docker container

```bash
make start_docker
```

This will start a container with a postgres database and another container with a python image. In the python container it will copy all the projects file, install the requirements and lastly run the flask app.

### Without docker

Make sure you have python 3.11 installed and a postgres database.

Install requirements.

```bash
pip install -r requirements.txt
```

Run flask app

```bash
make start
```

### Migrations

For migrations we are using [yoyo](https://pypi.org/project/yoyo-migrations/).
It's really straight forward but nonetheless we have some commands on Makefile:

To run migrations:

```bash
make migrate
```

To rollback last migration:

```bash
make migrate_rollback
```

To create a new migration it's a little tricky, because we didn't like the .py file for it so we decided to use raw sql files. But this comes with a cost that we need to create new files manually.

Just follow the pattern that already exists and it should be fairly easy.

## License

MIT Licensed (file [LICENSE](LICENSE)).
