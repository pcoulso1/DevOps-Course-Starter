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

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
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

## Trello setup
To run the application you will need to create a Trello account and API key. In order to call their API, you need to first [create an account](https://trello.com/signup), then generate an API key and token by following the [instructions here](https://trello.com/app-key).

For production application a named "ToDoBoard" is required with three lists named;
* ToDo
* InProgress
* Done

To run the e2e tests a "TestBoard" is required with three lists named; 
* ToDo
* InProgress
* Done

## Notes

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like developement mode (which also enables features like hot reloading when you make a file change).
There's also a number of variables which are used to connect to Trello;
* TRELLO_BASE_URL - the URL of the Trello api server e.g. https://api.trello.com/1
* TRELLO_KEY - the Trello key (please Trello setup)
* TRELLO_TOKEN - the Trello key (please Trello setup)

When running `setup.sh`, the `.env.template` file will be copied to `.env` if the latter does not exist.

## Running the tests
This project uses pytest.

```bash
pytest -v tests/
```
You may need to install requirements for setup beforehand, using

```bash
pip install -r requirements-test.txt
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
docker build -t pcoulso1/devops-course-starter:v0.1 .
```

### Running the container

To run the container as a daemon run following command
```
docker run -p 80:5000 \
    -e TRELLO_KEY=<key> \
    -e TRELLO_TOKEN=<token> \
    -d pcoulso1/devops-course-starter:v0.1
```

See section on Trello setup for details of how to obtain the key and token values