"""
Tradingview-webhooks-bot is a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by @robswc

You can follow development on github at: github.com/robswc/tradingview-webhook-bot

I'll include as much documentation here and on the repo's wiki!  I
expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!
"""
import sys
from actions import send_order, parse_webhook, process_alert, get_acctstatus
from auth import get_token
from flask import Flask, request, abort
from loguru import logger
import threading, time


# Create Flask object called app.
app = Flask(__name__)
logger.remove()
logger.add(sys.stderr, colorize=True, format=" {level.icon} <b> {time:HH:mm:ss}</b> | <level>{level}</level> | {message}", level="DEBUG")
logger.level("SIGNAL", no=777, color="<light-blue>", icon="🛰")
logger.level("ORDER", no=776, color="<light-yellow>", icon="◻️")
logger.level("STATUS", no=775, color="<light-magenta>", icon="💰")


def activate_job():
    def run_job():
        while True:
            get_acctstatus()
            time.sleep(60)

    thread = threading.Thread(target=run_job)
    thread.start()


# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'Online.'

@logger.catch
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        data = parse_webhook(request.get_data(as_text=True))
        # Check that the key is correct
        if get_token() == data['key']:
            logger.log("SIGNAL", "{} | Incoming Signal: {}", data['algo'], data['side'])
            process_alert(data)
            return '', 200
        else:
            logger.error("Incoming Signal From Unauthorized User.")
            abort(403)

    else:
        abort(400)

if __name__ == '__main__':
    activate_job()
    app.run(debug=True)
