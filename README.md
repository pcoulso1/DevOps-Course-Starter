# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using PowerShell)
```powershell
$ .\setup.ps1
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Add poetry to your path, on Unix it is located at $HOME/.poetry/bin and on Windows at %USERPROFILE%\.poetry\bin and then install the dependecies

```bash
$ poetry install -n
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

To run VSCode in the virtual enviroment created by poetry, run the following commands;
```bash
$ poetry shell
$ code .
```

## MongoDB setup
The application uses MongoDB as it's backing store. During development the [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) service was used which provided a 'free to use' MongoDB cluster that the application can use. To create a MongoDB Atlas cluster sign-up [here](https://www.mongodb.com/try) and select the "I'm learning MongoDB" option.

Select any of the Free to use Cloud vendors (during development the cloud vendor AWS was used in the eu-west-1 region). When creating the cluster select the 'username and password' authentication method, and ensure the correct IP range is added to ensure your application can connect.

For production application the "todoBoard" database will be created with the following collections;
* ToDo
* InProgress
* Done

To run the e2e tests the "testBoard" database will be created with the following collections; 
* ToDo
* InProgress
* Done

### Notes

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like developement mode (which also enables features like hot reloading when you make a file change).
There's also a number of variables which are used to connect to MongoDb;
* MONGO_URL - the full url for the MongoDB including the default database in the connection string e.g. mongodb+srv://user:pwd@cluster0.xrdya.mongodb.net/todoBoard?retryWrites=true&w=majority

When running `setup.sh`, the `.env.template` file will be copied to `.env` if the latter does not exist.

## OAuth Setup

This application uses OAuth for user authentication. The following GitHub documentation link shoes you how to register your application on GitHub for OAuth.
* https://docs.github.com/en/developers/apps/creating-an-oauth-app

Before running your application, the following envirment variable to be set
* GITHUB_CLIENT_ID - Provided when you register your application on GitHub
* GITHUB_CLIENT_SECRET - Provided when you register your application on GitHub
* GITHUB_LOGON_REDIRECT - The URL for OAuth callback to re-direct you to. This should be the homepage URL with /login/callback appended e.g. http://localhost:5000/login/callback

For development purposes it is possible to disable OAuth by setting the following enviroment variable.

* OAUTHLIB_INSECURE_TRANSPORT=1

## Running the tests
This project uses pytest.

```bash
poetry run pytest -v tests/
```
You may need to install requirements for setup beforehand, using

```bash
poetry install
```
The e2e tests require the chromedriver to run. This can be downloaded from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and placed in top level of the project directory  

## Running within Vagrant VM

This project runs Vagrant on Hyper-V please follow these instructions for setup  https://techcommunity.microsoft.com/t5/virtualization/vagrant-and-hyper-v-tips-and-tricks/ba-p/382373

Within the root directory of the project open a cmd.exe as Administrator and execute the following commands;
```
vagrant up
```

The [vagrant documentation](https://www.vagrantup.com/docs/providers/hyperv/limitations.html#limited-networking) at states;

*Vagrant does not yet know how to create and configure new networks for Hyper-V. When launching a machine with Hyper-V, Vagrant will prompt you asking what virtual switch you want to connect the virtual machine to.*

*A result of this is that networking configurations in the Vagrantfile are completely ignored with Hyper-V.*

Although this is not 100% true, it does seem to be accurate when setting up the "forwarded_port" configuration which is ignored

## Running within Docker

### Building docker image
To build the docker image run the following command

```
docker build --target development --tag devops-course-starter:dev-v0.1 .
docker build --target production --tag devops-course-starter:prod-v0.1 .
```

### Running the container

To run the production container as a daemon run following command
```
docker run -p 80:5000 --env-file .env -d devops-course-starter:prod-v0.1
```
Or
```
docker run -p 80:5000 \
    -e MONGO_URL=<url> \
    -e MONGO_DEFAULT_DATABASE=<db name> \
    -d devops-course-starter:prod-v0.1
```

To run the development container as a daemon ensure you mount the project directory within the container e.g. run following command
```
docker run -p 80:5000 --env-file .env --mount type=bind,source=$(pwd),target=/usr/src/app -d devops-course-starter:dev-v0.1
```
Or
```
docker run -p 80:5000 \
    --mount type=bind,source=$(pwd),target=/usr/src/app
    -e MONGO_URL=<url> \
    -e MONGO_DEFAULT_DATABASE=<db name> \
    -d devops-course-starter:dev-v0.1
```

Note: See section on MongoDB setup for details of how to obtain the username / password and setup the .env file.

## Deploying using Teraform



```
TF_VERSION=0.14.7
# Download terraform
wget https://releases.hashicorp.com/terraform/"$TF_VERSION"/terraform_"$TF_VERSION"_linux_amd64.zip 
unzip terraform_"$TF_VERSION"_linux_amd64.zip 

# Execute terraform deploy
terraform init
terraform apply -auto-approve -var "github_client_id=$GITHUB_CLIENT_ID" -var "github_client_secret=$GITHUB_CLIENT_SECRET" -var "github_logon_redirect=$GITHUB_LOGON_REDIRECT"
```
_**Note** : See section for OAuth Setup for GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET and GITHUB_LOGON_REDIRECT_


## Documentation

C4 diagrams have been proded for this application in the file c4model.drawio. These can be viewed at https://app.diagrams.net/

Within this file the  UML diagrams where generated by running;
```
pyreverse.exe -p ToDoApp app.py config.py github_oauth.py item.py mongo_db\config.py mongo_db\item_store.py mongo_db\store.py mongo_db\user_store.py status.py user\user.py user\user_access.py user\user_role.py items_view_model.py

```

Which gerneatess classes_ToDoApp.dot and packages_ToDoApp.dot which can be rendered online at https://dreampuf.github.io/GraphvizOnline to generate svg files which are then loaded into drawio file by importing them into https://app.diagrams.net/ via Arrange -> Insert -> Image... then Open the file
