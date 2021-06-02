variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "dev"
}
variable "loggy_token" {
  sensitive=true
  description = "The loggy customer access token"
}
variable "github_client_id" {
  sensitive=true
  description = "The OAuth 2 client ID"
}
variable "github_client_secret" {
  sensitive=true
  description = "The OAuth 2 client secret"
}
variable "github_logon_redirect" {
  description = "The OAuth 2 redirect page"
}
