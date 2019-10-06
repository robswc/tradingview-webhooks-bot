![demopic](img/webhooks_bot_logo.png)

![LDA](https://i.imgur.com/l5XVqqb.png)


# Lunar Digital Assets Collaboration

This branch is maintained a developed by Lunar Digital Assets with the help of @robswc - Feel free to pitch in!

# Tradingview-webhooks-bot

tradingview-webhooks-bot is a trading bot, written in python that allows users to place trades with tradingview's webhook alerts.

---

## Quickstart Using Pipenv

Pipenv is a tool that helps users set virtual environments and install dependencies with ease. There are many benefits to creating a virtual environment, especially for those that haev other projects running on the same server.

### Install pipenv and initiate virtual environment

1. Install pipenv `sudo apt install pipenv`
2. Once pipenv is installed, I recommend that you [get familiar with it](https://github.com/pypa/pipenv).
3. Navigate to the folder where you cloned the repo. You should see `Pipfile` and `Pipfile.lock` files.
4. Run command `pipenv install`
5. The dependencies required to get started should now be installed. Check by running command `pipenv graph` - You should see flask and ccxt.
6. If you want to install any other dependencies, or if you get an error that you're missing a depedency, simply use command `pipenv install <dependency>`
7. Starting the virtual environment: `pipenv shell`
8. Starting the flask app: `python webhook-bot.py`

There you go! Nice and simple Python version and virtualenv management.

### Using ngrok for webook data retrieval

Many people are having difficulties with their server properly receiving webhook data from TradingView. The easiest way to get started quickly without ripping your hair out from trying to figure out what's wrong, [ngrok](https://ngrok.com/) can be used to receive the signals. Create a free account, unless you want your server to go down every 8 hours. Navigate to the downloads page, and select your download to match your machine. For example, I am on Ubuntu: `wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip`
