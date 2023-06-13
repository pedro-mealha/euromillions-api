terraform {
  required_version = ">= 1.0"

  backend "pg" {
    schema_name = "euromillions-api-tf-state"
  }

  required_providers {
    fly = {
      source  = "fly-apps/fly"
      version = "0.0.22"
    }
  }
}
