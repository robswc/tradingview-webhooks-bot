![demopic](img/logo.png)

![](https://img.shields.io/github/license/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/github/repo-size/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/github/commit-activity/y/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/twitter/follow/robswc?style=for-the-badge)




# Tradingview-webhooks-bot

tradingview-webhooks-bot is a trading bot, written in python, that allows users to place trades with tradingview's webhook alerts.

### Server

The server is a simple framework for placing and managing trades with tradingview's webhook alerts.

### Interface

The webhooks-bot interface is an *optional* extension of the tradingview-webhooks-bot.  It allows for greater control and visualization of webhook alerts.

---

# Getting Started

### Dependencies

* Python (3.8+)
* Flask
* Dash (optional, interface only)

### Downloading

tradingview-webhooks-bot can be downloaded as a zip or cloned via git (recommended).

### Installing Required Libraries

Once you have downloaded tradingview-webhooks-bot, run the following command 

`pip install -r requirements.txt` within the `tradingview-webhooks-bot` directory.

This will install all the required libraries for tradingview-webhooks-bot to run properly.

### Getting the bot running

In order for the tradingview-webhooks-bot to work, it will need to be running on a computer with open ports.  
There are multiple ways to achieve this. The recommended method is to run the bot on a server, i.e. AWS, Google Cloud, VPS, etc. 
**If you do not have one of these, it is possible to use ngrok.** Below are guides on how to get the bot running using either method.
Since the bot is built with [Flask](https://flask.palletsprojects.com/), **any method to deploy a flask app will work.**

* [Hosting with server](https://flask.palletsprojects.com/en/2.0.x/deploying/index.html) (AWS, Digital Ocean, VPS, etc)
* [Hosting locally](https://github.com/robswc/tradingview-webhooks-bot/wiki/Using-Ngrok) (personal computer)

### Usage

I would highly recommend visiting the *Getting Started* wiki page
and following the *Simple Webhook Event* tutorial.  This will get you
familiar with tradingview-webhooks-bot, enough to then create your own stuff!

* [Getting Started](https://github.com/robswc/tradingview-webhooks-bot/wiki/Getting-Started)

### Interface

The interface is a new way to use the tradingview-webhooks-bot to its full potential.  The interface is an optional GUI that allows for an easier management of webhook alerts.  Interface usage is explained in more detail on the [wiki page](https://github.com/robswc/tradingview-webhooks-bot/wiki/Interface-GUI).
