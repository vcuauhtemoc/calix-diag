## Installation
Requires installation of poetry. from your CLI:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Once installed, clone the repo, navigate to the project folder and install the script:
```
cd ~/
cd calix-diag
git clone git@github.com:vcuauhtemoc/calix-diag.git
poetry install
```
## Usage:

```
poetry shell
calix-diag [jump_username] [olt hostname] [ONU UID]
```