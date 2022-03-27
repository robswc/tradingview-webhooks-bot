# initialize our Flask application
from logging import getLogger, DEBUG

from flask import Flask, request, jsonify, render_template

from utils.log import CONSOLE_HANDLER

app = Flask(__name__)

# configure logging
logger = getLogger(__name__)
logger.addHandler(CONSOLE_HANDLER)
logger.setLevel(DEBUG)


@app.route("/", methods=["GET"])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == 'POST':
        logger.info(f'Request Data: {request.get_json()}')
        return jsonify(str('success'))


if __name__ == '__main__':
    app.run(debug=True)
