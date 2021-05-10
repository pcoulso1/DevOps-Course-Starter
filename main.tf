terraform {

  backend "azurerm" {
    resource_group_name   = "CreditSuisse1_PeterTaylor-Coulson_ProjectExercise"
    storage_account_name  = "tstate16224"
    container_name        = "tstate"
    key                   = "terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

data "azurerm_resource_group" "main" {
  name = "CreditSuisse1_PeterTaylor-Coulson_ProjectExercise"
  #location = "uksouth"
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-terraformed-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableMongo"
  }
  
  capabilities {
    name = "EnableServerless"
  }
  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }

  # lifecycle {
  #   prevent_destroy = true
  # }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-terraformed-cosmos-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  # lifecycle {
  #   prevent_destroy = true
  # }
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}
resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-todo-pcoulson"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|pcoulso1/todo-app:latest"
  }
  app_settings = {
    "DOCKER_ENABLE_CI"           = "true"
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_URL"                  = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "MONGO_DEFAULT_DATABASE"     = "todoBoard"
    "FLASK_APP"                  = "app"
    "FLASK_ENV"                  = "production"
    "GITHUB_CLIENT_ID"           = "${var.github_client_id}"
    "GITHUB_CLIENT_SECRET"       = "${var.github_client_secret}"
    "GITHUB_LOGON_REDIRECT"      = "${var.github_logon_redirect}"
  }
}
