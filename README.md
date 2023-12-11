# Project Nau Financial Manager

This is a Django application intended to manage financial process and also share revenue between partners.

## Running the project

We have two ways to run the project, using docker or using poetry.

## Using Docker (Recommended if you will not develop)

You will need to have docker and docker-compose installed in your machine.

```bash
make run-docker
```

OR

## Preparing enviromnent

This guide is to setup project using `poetry` with Python version 3.11.4 for the project.
optional: you can use docker files to get instances of database and application.

## Setting up `poetry`(version 1.5.1) with Python 3.11.4

One dependency of poetry is `pyenv`.

### Linux (Debian based distributions)

#### Install Developer Packages

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev git
```

#### Install `pyenv` (Same for Linux and Mac)

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
if [ -n "$ZSH_VERSION" ]; then
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
else
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
fi
```

#### Install `poetry` Linux

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Install `poetry` MacOS

```bash
brew install poetry
```

## Set Python version in folder the project

Navigate to the folder project and execute:

```bash
pyenv install 3.11.4
pyenv local 3.11.4
```

## Create and activate a virtual environment

```bash
poetry env use 3.11.4

# Activate the virtual environment
poetry shell
```

## Run for DEV

Start the app's dependencies services:
```bash
APP=false make run-docker
```

You have to install the app package dependencies and run the migrations.
```bash
make install-packages migrate
```

To execute the application outside the docker:
```bash
make run
```

## Run for PROD

To start the application using the production mode, run:

```bash
DOCKER_TARGET=production make run-docker
```

## GENERATING AND USING TOKEN

To generate a token you should use one of this two commands:
```bash
make create-token # will create a token for admin user
```
OR
```bash
manage.py drf_create_token user_who_you_want  # will create a token for indicated user
```

# IN YOUR CODE
To use token you need import he class ```from rest_framework.authentication import TokenAuthentication ```
then in your view declare a variable ```authentication_classes``` as list with ```TokenAuthentication``` class.

# IN YOUR CLIENT OR REQUEST
In Headers of request you need to declare a key 'Authorization' with the value 'Token generated_token'

Here is a example:
```bash
headers = { "Authorization": "Token generated_token" }
```

## Troubleshooting

```bash
# TODO: Automate this installation after validation of method and structure
```

Error:
```
org.freedesktop.DBus.Error.UnknownMethod] ('No such interface “org.freedesktop.DBus.Properties
```

Solution:
```bash
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```
