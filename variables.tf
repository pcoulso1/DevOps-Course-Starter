variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "dev"
}
variable "github_client_id" {
  description = "The OAuth 2 client ID"
}
variable "github_client_secret" {
  description = "The OAuth 2 client secret"
}
variable "github_logon_redirect" {
  description = "The OAuth 2 redirect page"
}
