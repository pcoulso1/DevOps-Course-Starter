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

