terraform {
  required_version = ">= 0.13"

  backend "pg" {
    schema_name = "euromillions-api-tf-state"
  }

  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.0"
    }
  }
}

provider "heroku" {
  email   = var.heroku_email
  api_key = var.heroku_api_key
}
