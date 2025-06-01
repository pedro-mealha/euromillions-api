locals {
  app_name  = "${terraform.workspace}-${var.app_name}"
  subdomain = terraform.workspace == "prod" ? "euromillions.staging" : "euromillions"
}

resource "fly_app" "euromillions_api" {
  count = terraform.workspace == "prod" ? 1 : 0
  name = local.app_name
  org  = "personal"
}

resource "fly_ip" "euromillions_api_ip_v6" {
  count = terraform.workspace == "prod" ? 1 : 0
  app        = local.app_name
  type       = "v6"
  depends_on = [fly_app.euromillions_api]
}

resource "fly_cert" "euromillions_api_cert" {
  count = terraform.workspace == "prod" ? 1 : 0
  app        = local.app_name
  hostname   = "${local.subdomain}.api.pedromealha.dev"
  depends_on = [fly_app.euromillions_api]
}
