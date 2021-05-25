#!/usr/bin/env bash
set -ex

# Download terraform
wget https://releases.hashicorp.com/terraform/"$TF_VERSION"/terraform_"$TF_VERSION"_linux_amd64.zip 
unzip terraform_"$TF_VERSION"_linux_amd64.zip 

# Install it in Travis CI location
sudo mv terraform /usr/local/bin/ 
rm terraform_"$TF_VERSION"_linux_amd64.zip

# Execute terraform deploy
terraform init
terraform apply -auto-approve -var "github_client_id=$AZURE_GITHUB_CLIENT_ID" -var "github_client_secret=$AZURE_GITHUB_CLIENT_SECRET" -var "github_logon_redirect=$AZURE_GITHUB_LOGON_REDIRECT"

# Call Azure web hoot to restart app
curl -dH -X POST "$(terraform output -raw cd_webhook)"
