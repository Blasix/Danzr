# Impotant
**This version of danzr is discontinued and replaced with [Danzr in Java](https://github.com/Blasix/Danzr_Java).**

# Danzr

Do you need a self hosted discord bot that can play music, even from youtube. Then danzr is the bot you need!

<h2>Bugs and features to be implemented</h2>
- [🪲] 8D (surround and stereo sound) not working, gets converted to mono<br>
- [🪲] the playerManager is per bot so the same bot in multiple servers does not work <br><br>
- [➕] /play support for other services then youtube<br>
- [➕] save your own playlists<br>
- [➕] make bot work without having to install XAMPP and python<br>
- [➕] make all messages look consistent<br>
- [➕] add crossfade<br>

## Installation
### Requirments
- [python](https://www.python.org/)
- [ffmpeg](https://ffmpeg.org) (make sure it is added to path)
### Setup
Go to the [Discord devloper portal](https://discord.com/developers/applications/) and create an application

Go to the bot tab and press reset token, you will now get a token.

<img src="https://i.imgur.com/4SvGvb6.png" width="800" alt="generate token">

Open `config.json` and add your discord bot token
### Running it
run these 2 commands:

`pip install -r requirements.txt`

`python index.py`

### Or run it with docker
Make sure [Docker](https://docs.docker.com/get-docker/) is installed

run this command (make sure you replaced the token in the command with your own token):

`docker run -d -e TOKEN=YOUR_TOKEN blasix/danzr`

this command will download the image, then run it in the background.

## Contributing

Before creating an issue, please ensure that it hasn't already been reported/suggested.

The issue tracker is only for bug reports and enhancement suggestions. If you have a question, please ask it in the [Discord server](https://discord.gg/73fj8ez9nC) instead of opening an issue – you will get redirected there anyway.

If you wish to contribute to the Danzr codebase or documentation, feel free to fork the repository and submit a pull request.

## Support
- **[Support Server](https://discord.gg/73fj8ez9nC)**
- **[Send a mail](https://blasix.com/contact)**
