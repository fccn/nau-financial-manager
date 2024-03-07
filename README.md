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
poetry env use -- $HOME/.pyenv/versions/3.11.4/bin/python

# Activate the virtual environment
poetry shell
```

## Run locally

### for local development

To start the application outside docker, execute the next command inside a virtual environment.
This will start all the dependencies services on each docker container and the application directly
on the host using the development server:

```bash
make run
```

To start the app and its dependencies on docker, on development mode, run:

```bash
make run-docker
```

You have to install the app package dependencies and run the migrations.
```bash
make install-packages migrate
```

### for local testing the production mode

To check if everything is ok and running using the production mode of the docker images, we have a
wait to run the application on production mode.
This will use the docker target `production` of the docker application image.

```bash
DOCKER_TARGET=production make run-docker
```

## API

This project uses the Django Rest Framework using a token approach for authentication.

The important API are:

- /billing/receipt-link/{transaction_id}/
- /billing/transaction-complete/

You can view the API documentation on:

- Swagger http://localhost:8000/api/docs/
- Redocs  http://localhost:8000/api/redocs/

### Generate a local token for development

To generate a token for local development you should use one of this two commands:

This will create a token for `admin` user.
```bash
make create-token
```

### Generate a token for a production environment

```bash
python manage.py createsuperuser --noinput --username <username> --email <email>

python manage.py drf_create_token <username>
```

## Client
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


# Django commands

  ## Retry all failed transactions of SageX3

  ###### How to use:
```bash
python manage.py retry_failed_transactions
```

  ## Export shared revenue

  This command triggers the export of all the transactions splitted based on the given parameters.

###### Required parameters:
  - start_date: YYYY-MM-DD
  - end_date: YYYY-MM-DD

###### Optional parameters:
  - product_id
  - organization_code

###### How to use:
```bash
python manage.py export_split_revenue  {start_date} {end_date} --product_id={product_id} --organization_code={organization_code}
```

###### Example:
```bash
python manage.py export_split_revenue 2023-12-01 2024-01-01
```
  ## Export shared revenue per organization

  This command triggers the export of all the transactions splitted based on the given parameters per organization.

###### Required parameters:
  - start_date: YYYY-MM-DD
  - end_date: YYYY-MM-DD
  - send_file: true / false

###### Optional parameters:
  - bcc: email@email.com

###### How to use:

To add more than one email as bcc, just open a string and add the emails.

```bash
python manage.py export_split_revenue_per_organizations  {start_date} {end_date} --send_email={send_email} --bcc="{bcc1 bcc2}"
```

###### Example:
```bash
python manage.py export_split_revenue_per_organizations 2023-12-01 2024-01-01 --send_email=true --bcc="bcc1@email.com bcc2@email.com"
```

## Troubleshooting

To create missing `SageX3TransactionInformation` objects that for a bug hasn't been created.

```python
from apps.billing.models import SageX3TransactionInformation, Transaction
transactions = Transaction.objects.all()
for t in transactions:
    SageX3TransactionInformation.objects.get_or_create(transaction=t)
```
