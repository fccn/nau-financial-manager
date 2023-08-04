# Setting up `pyenv` and `poetry` with Python 3.11.4

This guide will walk you through the process of installing `pyenv`, setting up `poetry` within `pyenv`, and using Python version 3.11.4 for your projects.

## Table of Contents

1. Install `pyenv`
2. Install Python 3.11.4
3. Install `poetry`
4. Set Python version for your project
5. Create and activate a virtual environment

## 1. Install `pyenv`

`pyenv` is a tool that allows you to easily install and manage multiple versions of Python on your system.

### Linux/MacOS Instructions:

```bash
# Install pyenv using `brew` (MacOS) or `apt-get` (Linux)
brew install pyenv   # MacOS
sudo apt-get install pyenv   # Ubuntu/Debian
```

# Initialize `pyenv` in your shell (add this to your shell configuration file)
```bash
if [ -n "$ZSH_VERSION" ]; then
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
else
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
fi
```

### Windows Instructions:
For Windows users, you can use the pyenv-win version, which provides similar functionality to pyenv. You can find the installation instructions on the pyenv-win GitHub repository.

## 2. Install Python 3.11.4
Now that pyenv is installed, you can use it to install Python 3.11.4.

```bash
# List available Python versions
pyenv install --list

# Install Python 3.11.4
pyenv install 3.11.4

# Verify the installation
pyenv versions
```

## 3. Install poetry
poetry is a dependency management and packaging tool for Python.

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python -

# Alternatively, you can use `pip` to install poetry
pip install poetry
```

## 4. Set Python version for your project
After installing pyenv and poetry, you can set the desired Python version for your project.

```bash
# Navigate to your project directory
cd /path/to/your/project

# Set Python 3.11.4 as the local version for your project
pyenv local 3.11.4
```

## 5. Create and activate a virtual environment
Now, you can create a virtual environment using poetry and activate it to isolate your project dependencies.

```bash
# Create a virtual environment with poetry
poetry env use 3.11.4

# Activate the virtual environment
poetry shell
```

Your project is now set up with Python version 3.11.4 and isolated within a virtual environment managed by poetry.
