variable "heroku_email" {
  description = "Heroku account email"
  type        = string
}

variable "heroku_api_key" {
  description = "Heroku API key"
  type        = string
}

variable "flask_env" {
  description = "Flask APP env"
  type        = string
}

variable "url_parser_regex" {
  description = "Regex to parse postgres url"
  type        = string
  default     = "^(?:(?P<driver>[^:/?#]+):)?(?://(?P<user>[^:/?#]*):)?(?:(?P<password>[^:/?#]*))?@(?:(?P<host>[^:/?#]*):)?(?:(?P<port>[^/?#]*))?/(?:(?P<schema>[^/?#]*))?"
}
