variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "dev"
}
variable "resource_name" {
  description = "The Azure Resrouce group where all resources in this deployment should be created. This reources group must already exist."
  default     = "CreditSuisse1_PeterTaylor-Coulson_ProjectExercise"
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
