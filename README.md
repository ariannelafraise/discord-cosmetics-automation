# Discord Cosmetics Automation

/!\ Use at your own risk /!\

This is a python tool to automatically switch cosmetics (randomly). Cosmetics are: avatar decorations and profile effects.

## Installation
1. Clone this repository
```sh
git clone https://github.com/ariannelafraise/discord-cosmetics-automation.git
```
2. Install the requirements
```sh
pip install -r requirements.txt
```
3. Create a `.env` file containing:
```
TOKEN=YOUR_DISCORD_TOKEN
```

## Usage
>Loop mode (**-l**): Be careful of rate limits. This tool only allows as low as 15 seconds cooldown to not spam the Discord API.

Switching all cosmetics once (**-b**):
```sh
python dca.py -b
```
Switching all cosmetics every 30 seconds (**-l**):
```sh
python dca.py -b -l 30
```
Switching profile effect only (**-p**):
```sh
python dca.py -p
```
Switching avatar decoration only (**-a**):
```sh
python dca.py -a -l 15
```

## Conversion to a Linux command
1. Add a python shebang
2. Rename `dca.py` to `dca`
3. Add to path
4. Test it: `dca --version`