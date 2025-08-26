## Installation
Requires installation of pipx. from your terminal, run:
```
brew install pipx
pipx ensurepath   # re-open your shell after this
```
Install the script:
```
pipx install git+https://github.com/vcuauhtemoc/calix-diag.git
```

To update:
```
pipx upgrade calix-diag
```
## Usage:

```
Run a command on the OLT and get output:
calix-diag [jump_username] [olt hostname] -c "command"

Get the ONT port from UID:
calix-diag [jump_username] [olt hostname] -g UID
```