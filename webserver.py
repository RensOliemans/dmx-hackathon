from flask import Flask, render_template
from flask import request, jsonify
from flask_bootstrap import Bootstrap

import log
from Exceptions.Exceptions import InvalidRequestException, ControllerSetLEDException
from config import UPDATE_RATE_MS, CHANNELS, INIT_CHANNEL_VALUE, INIT_CHANNEL
from controller import DMXController
from controller_handler import ControllerHandler

logging = log.get_logger(__name__)

app = Flask(__name__)
bootstrap = Bootstrap(app)

c = DMXController(CHANNELS, UPDATE_RATE_MS)
c.set_channel(INIT_CHANNEL, INIT_CHANNEL_VALUE)

HANDLER = ControllerHandler(c)


@app.route('/animate', methods=['POST'])
def animate():
    # Convert to dict (we don't need the multi levels)
    data = {x: request.form.get(x) for x in request.form}
    animation = HANDLER.animate(data)
    return jsonify([str(color) for color in animation])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.errorhandler(InvalidRequestException)
def handle_invalid_request(error):
    """ Returns a neat response to an error. """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ControllerSetLEDException)
def handle_controller_set_led_exception(error):
    """ Calls handle_invalid_request, as the same functionality is needed. """
    return handle_invalid_request(error)
