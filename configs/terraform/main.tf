resource "heroku_app" "euromillions-api" {
  name = "${terraform.workspace}-euromillions-api"

  region = "eu"
  stack  = "container"

  config_vars = {
    EUROMILLIONS_MIN_YEAR     = "2004"
    EUROMILLIONS_WEB_BASE_URL = "https://www.euro-millions.com"
    FLASK_APP                 = "euromillions_api"
    FLASK_ENV                 = var.flask_env
  }
}

resource "heroku_addon" "database" {
  name = "${terraform.workspace}-euromillions-api-db"
  plan = "heroku-postgresql:hobby-dev"

  app = heroku_app.euromillions-api.name
}

locals {
  db_vars = regex(var.url_parser_regex, heroku_addon.database.config_var_values.DATABASE_URL)
}

resource "heroku_app_config_association" "db-vars" {
  app_id = heroku_app.euromillions-api.id

  sensitive_vars = {
    DATABASE_URL = heroku_addon.database.config_var_values.DATABASE_URL
    DB_SCHEMA    = local.db_vars.schema
    DB_USER      = local.db_vars.user
    DB_PASSWORD  = local.db_vars.password
    DB_HOST      = local.db_vars.host
    DB_PORT      = local.db_vars.port
  }
}
