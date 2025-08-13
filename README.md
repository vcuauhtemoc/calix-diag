## Installation
Requires installation of poetry. from your CLI, and add the source line to your shell RC file :
```
curl -sSL https://install.python-poetry.org | python3 -
```
Add the following to your shell RC file (.zshrc,.bashrc, etc)
```
export PATH="$HOME/.local/bin:$PATH"
```

Once installed, clone the repo, navigate to the project folder and install the script:
```
cd ~/
git clone git@github.com:vcuauhtemoc/calix-diag.git
cd calix-diag
poetry install
```
## Usage:

```
poetry shell
calix-diag [jump_username] [olt hostname] [ONU UID]
```