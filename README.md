## Installation
Requires installation of poetry. from your CLI:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Once installed, clone the repo, navigate to the project folder and install the script:
```
cd ~/
git clone git@github.com git@github.com:PilotFiber/calix-diag.git
cd calix-diag
poetry install
```
## Usage:

```
poetry shell
calix-diag [jump_username] [olt hostname] [ONU UID]
```