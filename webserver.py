from flask import Flask, render_template, redirect, session
from flask import request, jsonify
from flask_bootstrap import Bootstrap

import log
from Exceptions.Exceptions import InvalidRequestException, ControllerSetLEDException
from config import UPDATE_RATE_MS, CHANNELS, INIT_CHANNEL_VALUE, INIT_CHANNEL
from controller import DMXController
from controller_handler import ControllerHandler
from secret import key

logging = log.get_logger(__name__)

app = Flask(__name__)
app.secret_key = key
bootstrap = Bootstrap(app)

c = DMXController(CHANNELS, UPDATE_RATE_MS)
c.set_channel(INIT_CHANNEL, INIT_CHANNEL_VALUE)

HANDLER = ControllerHandler(c)


@app.route('/animate', methods=['POST'])
def animate():
    # Convert to dict (we don't need the multi levels)
    data = {x: request.form.get(x) for x in request.form}
    current_color, duration, ease = HANDLER.animate(data)
    session['color'] = current_color.to_hex().lstrip('#')
    session['duration'] = duration
    session['ease'] = ease
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    keys = ['color', 'duration', 'ease']
    if all([key in session for key in keys]):
        color, duration, ease = (session.pop(key) for key in keys)
        logging.debug(f"Got get request with session set, color={color}, duration={duration}, ease={ease}")
        return render_template('index.html', color=color, duration=duration, ease=ease)
    return render_template('index.html')


@app.errorhandler(InvalidRequestException)
def handle_invalid_request(error):
    """ Returns a neat response to an error. """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ControllerSetLEDException)
def handle_controller_set_led_exception(error):
    """ Calls handle_invalid_request, as the same functionality is required. """
    return handle_invalid_request(error)
