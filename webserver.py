from flask import Flask, render_template, redirect, session
from flask import request, jsonify
from flask_bootstrap import Bootstrap

import log
from Exceptions.Exceptions import InvalidRequestException, ControllerSetLEDException
from config import UPDATE_RATE_MS, CHANNELS, INIT_CHANNEL_VALUE, INIT_CHANNEL
from controller import DMXController
from controller_handler import ControllerHandler
from secret import key as secret_key

logging = log.get_logger(__name__)

app = Flask(__name__)
app.secret_key = secret_key
bootstrap = Bootstrap(app)

c = DMXController(CHANNELS, UPDATE_RATE_MS)
c.set_channel(INIT_CHANNEL, INIT_CHANNEL_VALUE)

HANDLER = ControllerHandler(c)


@app.route('/animate', methods=['POST'])
def animate():
    """Method used when making a light animation (fade to other color)"""
    # Convert to dict (we don't need the multi levels)
    data = {x: request.form.get(x) for x in request.form}
    current_color, duration, ease = HANDLER.animate(data)
    session['color_animate'] = current_color.to_hex().lstrip('#')
    session['duration_animate'] = duration
    session['ease_animate'] = ease
    return redirect('/')


@app.route('/onoff', methods=['POST'])
def onoff():
    """Method used when toggling the lights with a color"""
    data = {x: request.form.get(x) for x in request.form}
    current_color, status = HANDLER.onoff(data)
    session['color_onoff'] = current_color.to_hex().lstrip('#')
    session['status_onoff'] = status
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    # All possible variables that can be given to the Jinja template.
    keys = ['color_animate', 'duration_animate', 'ease_animate', 'color_onoff', 'status_onoff']
    color_animate, duration_animate, ease_animate, color_onoff, status_onoff = [session.get(key)
                                                                                if key in session else ""
                                                                                for key in keys]

    logging.debug(f"Request data: {color_animate}, {duration_animate}, {ease_animate}, {color_onoff}, {status_onoff}")
    return render_template('index.html', color_animate=color_animate, duration_animate=duration_animate,
                           ease_animate=ease_animate, color_onoff=color_onoff, status_onoff=status_onoff)


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
