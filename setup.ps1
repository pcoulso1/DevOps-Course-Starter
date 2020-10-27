# Create and enable a virtual environment
python -m venv env

.\env\scripts\activate.ps1

# Upgrade pip and install required packages
pip install --upgrade pip

(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

# Create a .env file from the .env.template
if (-not (test-path .env)) 
{
    Copy-Item .env.template .env
}