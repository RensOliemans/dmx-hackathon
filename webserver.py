from flask import Flask
from flask import request, jsonify

import log
from config import UPDATE_RATE_MS, CHANNELS, INIT_CHANNEL_VALUE, INIT_CHANNEL
from controller import DMXController
from controller_handler import ControllerHandler

logging = log.get_logger(__name__)
app = Flask(__name__)
c = DMXController(CHANNELS, UPDATE_RATE_MS)
c.set_channel(INIT_CHANNEL, INIT_CHANNEL_VALUE)

HANDLER = ControllerHandler(c)


@app.route('/animate', methods=['POST'])
def animate():
    logging.INFO("Got request {req} on route {route}".format(req=request, route=request.url_rule))
    data = request.get_json()
    animation = HANDLER.animate(data)
    return jsonify([str(color) for color in animation])
