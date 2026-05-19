# 🐧🐍 Pyenv & Python 3.12 on Ubuntu — Setup Guide

---

## 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

---

## 2. Install pyenv

```bash
curl https://pyenv.run | bash
```

> If you see `WARNING: Can not proceed... Kindly remove the '/home/USER/.pyenv' directory first` — pyenv is already installed, skip this step.

---

## 3. Add pyenv to Your Shell (bashrc)

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

### Verify pyenv is working:

```bash
pyenv --version
# pyenv 2.x.x
```

---

## 4. Install Python 3.12

```bash
pyenv install 3.12.0
```

---

## 5. Set the Python Version

### Globally (system-wide):

```bash
pyenv global 3.12.0
```

### Locally (for a specific project/folder):

```bash
cd ~/Desktop/NeSy/backend
pyenv local 3.12.0
```

> The local version creates a `.python-version` file in the folder and is automatically activated whenever you enter that directory.

---

## 6. Check Python Versions

### Python versions installed on the system:

```bash
ls /usr/bin/python*
```

### Python versions installed via pyenv:

```bash
pyenv versions
```

Example output:
```
  system
* 3.12.0
  3.11.5
```

The `*` indicates the currently active version.

### Check which Python version is currently in use:

```bash
python --version
which python
```

### Check which version is active inside the venv:

```bash
# (while venv is activated)
python --version
which python
```

## Quick Reference

| Action                        | Command                                                      |
|-------------------------------|--------------------------------------------------------------|
| List all pyenv versions       | `pyenv versions`                                             |
| Install a Python version      | `pyenv install 3.12.0`                                       |
| Set global version            | `pyenv global 3.12.0`                                        |
| Set local version             | `pyenv local 3.12.0`                                         |
| Check current version         | `python --version`                                           |
| Check Python path             | `which python`                                               |
| Create venv                   | `python -m venv .venv`                                       |
| Activate venv                 | `source .venv/bin/activate`                                  |
| Deactivate venv               | `deactivate`                                                 |
| Verify SSL                    | `python -c "import ssl; print(ssl.OPENSSL_VERSION)"`         |
