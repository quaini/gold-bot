# gold-bot

Final Project for CS 4100: Artificial Intelligence at Northeastern University

Bot Profile: https://lichess.org/@/gold-bot

Helpful Resource for pip Installation: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

The files we contributed to that allow gold-bot to run are:
File  | What That File Does
------------- | -------------
engines/gold-engine.py | Contains our implementation of the monte-carlo method. The actual engine that does the move search given a board state and time to move.
config.yml  | Sets various settings for our bot on Lichess.
engine_wrapper.py | Has the call to our gold-engine.

## All Notes Below From [lichess-bot](https://github.com/ShailChoksi/lichess-bot)
---

# lichess-bot

[![Python Build](https://github.com/ShailChoksi/lichess-bot/actions/workflows/python-build.yml/badge.svg)](https://github.com/ShailChoksi/lichess-bot/actions/workflows/python-build.yml)

A bridge between [Lichess API](https://lichess.org/api#tag/Bot) and bots.


## How to Install

### Mac/Linux:
- NOTE: Only Python 3.7 or later is supported!
- Download the repo into lichess-bot directory
- Navigate to the directory in cmd/Terminal: `cd lichess-bot`
- Install pip: `apt install python3-pip`
- Install virtualenv: `pip install virtualenv`
- Setup virtualenv: `apt install python3-venv`
```
python3 -m venv venv #if this fails you probably need to add Python3 to your PATH
virtualenv .venv -p python3 #if this fails you probably need to add Python3 to your PATH
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```
- Copy `config.yml.default` to `config.yml`
- Edit the variants: `supported_variants` and time controls: `supported_tc` from the config.yml as necessary

### Windows:
- Here is a video on how to install the bot: (https://youtu.be/w-aJFk00POQ). Or you may proceed to the next steps.
- NOTE: Only Python 3.7 or later is supported!
- If you don't have Python, you may download it here: (https://www.python.org/downloads/). When installing it, enable "add Python to PATH", then go to custom installation (this may be not necessary, but on some computers it won't work otherwise) and enable all options (especially "install for all users"), except the last . It's better to install Python in a path without spaces, like "C:\Python\".
- To type commands it's better to use PowerShell. Go to Start menu and type "PowerShell" (you may use cmd too, but sometimes it may not work).
- Then you may need to upgrade pip. Execute "python -m pip install --upgrade pip" in PowerShell.
- Download the repo into lichess-bot directory.
- Navigate to the directory in PowerShell: `cd [folder's adress]` (like "cd C:\chess\lichess-bot").
- Install virtualenv: `pip install virtualenv`.
- Setup virtualenv:
```
python -m venv .venv (if this fails you probably need to add Python to your PATH)
./.venv/Scripts/Activate.ps1 (.\.venv\Scripts\activate.bat should work in cmd in administator mode) (This may not work on Windows, and in this case you need to execute "Set-ExecutionPolicy RemoteSigned" first and choose "Y" there [you may need to run Powershell as administrator]. After you executed the script, change execution policy back with "Set-ExecutionPolicy Restricted" and pressing "Y")
pip install -r requirements.txt
```
- Copy `config.yml.default` to `config.yml`
- Edit the variants: `supported_variants` and time controls: `supported_tc` from the config.yml as necessary (use # to disable certain ones)


## Lichess OAuth
- Create an account for your bot on [Lichess.org](https://lichess.org/signup)
- NOTE: If you have previously played games on an existing account, you will not be able to use it as a bot account
- Once your account has been created and you are logged in, [create a personal OAuth2 token](https://lichess.org/account/oauth/token/create) with the "Play as a bot" selected and add a description
- A `token` e.g. `Xb0ddNrLabc0lGK2` will be displayed. Store this in `config.yml` as the `token` field
- NOTE: You won't see this token again on Lichess.


## Setup Engine
- Place your engine(s) in the `engine.dir` directory
- In `config.yml`, enter the binary name as the `engine.name` field (In Windows you may need to type a name with ".exe", like "lczero.exe")
- Leave the `weights` field empty or see LeelaChessZero section for Neural Nets


## Lichess Upgrade to Bot Account
**WARNING** This is irreversible. [Read more about upgrading to bot account](https://lichess.org/api#operation/botAccountUpgrade).
- run `python lichess-bot.py -u`

## To Quit
- Press CTRL+C
- It may take some time to quit

## LeelaChessZero (Mac/Linux)

- Download the weights for the id you want to play from here: https://lczero.org/play/networks/bestnets/
- Extract the weights from the zip archive and rename it to `latest.txt`
- For Mac/Linux, build the lczero binary yourself following [LeelaChessZero/lc0/README](https://github.com/LeelaChessZero/lc0/blob/master/README.md)
- Copy both the files into the `engine.dir` directory
- Change the `engine.name` and `engine.engine_options.weights` keys in config.yml to `lczero` and `weights.pb.gz`
- You can specify the number of `engine.uci_options.threads` in the config.yml file as well
- To start: `python lichess-bot.py`

## LeelaChessZero (Windows CPU 2021)

- For Windows modern CPUs, download the lczero binary from https://github.com/LeelaChessZero/lc0/releases ex: `lc0-v0.27.0-windows-cpu-dnnl.zip`
- Unzip the file, it comes with lc0.exe , dnnl.dll, and a weights file ex: `703810.pb.gz` (amongst other files)
- all three main files need to be copied to the engines directory
- the lc0.exe should be doubleclicked and the windows safesearch warning about it being unsigned should be cleared (be careful and be sure you have the genuine file)
- Change the `engine.name` key in config.yml to `lc0.exe`, no need to edit config.yml concerning the weights file as the lc0.exe will use whatever *.pb.gz is in the same folder (have only one *pb.gz in the engines directory)
- To start: `python lichess-bot.py`

## For Docker

Use https://github.com/vochicong/lc0-nvidia-docker to easily run lc0 and lichess-bot
inside a Docker container.

## Creating a custom bot

Steps to create a custom bot

1. Do all the steps in the [How to Install](#how-to-install)
2. In the `config.yml`, change the engine protocol to `homemade`
3. Create a class in some file that extends `EngineWrapper` (in `engine_wrapper.py`)
    - Or extend `MinimalEngine` (in `strategies.py`),
      if you don't want to deal with a few random errors.
    - Look at the `strategies.py` file to see some examples.
    - If you don't know what to implement, look at the `EngineWrapper` or `UCIEngine` class.
        - You don't have to create your own engine, even though it's an "EngineWrapper" class.<br>
          The examples just implement `search`.
4. At the bottom of `engine_wrapper.py` change `getHomemadeEngine()` to return your class
    - In this case, you could change it to:

      ```python
      def getHomemadeEngine():
          import strategies
          return strategies.RandomMover
      ```

5. In the folder `engines` create a file named `engine_name`,
   possibly with some explainer text like `dummy engine file`.
    - Required because config.yml has `engine.dir`, and the code checks if it exists

## Tips & Tricks
- You can specify a different config file with the `--config` argument.
- Here's an example systemd service definition:
```
[Unit]
Description=lichess-bot
After=network-online.target
Wants=network-online.target

[Service]
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 /home/thibault/lichess-bot/lichess-bot.py
WorkingDirectory=/home/thibault/lichess-bot/
User=thibault
Group=thibault
Restart=always

[Install]
WantedBy=multi-user.target
```

# Acknowledgements
Thanks to the Lichess team, especially T. Alexander Lystad and Thibault Duplessis for working with the LeelaChessZero
team to get this API up. Thanks to the Niklas Fiekas and his [python-chess](https://github.com/niklasf/python-chess) code which allows engine communication seamlessly.

# License
lichess-bot is licensed under the AGPLv3 (or any later version at your option). Check out LICENSE.txt for the full text.
