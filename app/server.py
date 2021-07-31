# imports
from flask import Flask, request, jsonify, abort, send_file
from bot import bot
__version__ = 2.1

# create flask app
app = Flask(__name__, static_url_path='/components/static/')

# check IPs against whitelist
ip_whitelist = [
    '127.0.0.1',  # local address
    '52.89.214.238',  # tradingview
    '34.212.75.30',  # tradingview
    '54.218.53.128',  # tradingview
    '52.32.178.7',  # tradingview
]


@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip not in ip_whitelist:
        abort(403)


# create routes
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # get json data
        data = request.json

        # give webhooks bot data from webhook
        try:
            bot.load_json(data)
            return jsonify({'status': 'OK'})
        except Exception as e:
            return jsonify({'error': str(e)})


@app.route('/', methods=['GET'])
def landing():
    if request.method == 'GET':
        return send_file('components/static/index.html')


if __name__ == "__main__":
    app.run(debug=True)
