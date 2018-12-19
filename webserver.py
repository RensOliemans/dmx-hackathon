from flask import Flask
from flask import request, jsonify

import log
from Exceptions.InvalidRequestException import InvalidRequestException
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
    data = request.get_json()
    animation = HANDLER.animate(data)
    return jsonify([str(color) for color in animation])


@app.errorhandler(InvalidRequestException)
def handle_invalid_request(error):
    """ Returns a neat response to an error. """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
