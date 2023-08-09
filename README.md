# Project Nau Receipts Manager

This is a Django application intended to manage billing receipts and also share revenue between partners.

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
pyenv local 3.11.4
```

## Create and activate a virtual environment

```bash
poetry env use 3.11.4

# Activate the virtual environment
poetry shell
```

## Create .env file for enviromnent desired

```bash
cp sample-dev.env .env
```

# TODO: Automate this installation after validation of method and structure
