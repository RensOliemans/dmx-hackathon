"""
Flask webserver file. Handles incoming GET and POST requests and calls the ControllerHandler.
"""
from flask import Flask, render_template, redirect, session, request
from flask_bootstrap import Bootstrap
from usb.core import USBError

from exceptions.exceptions import InvalidRequestException, ControllerSetLEDException
from config import UPDATE_RATE_MS, CHANNELS, INIT_CHANNEL_VALUE, INIT_CHANNEL, secret_key
from controller import DMXController
from controller_handler import ControllerHandler
from log import logger

# pylint: disable=C0103
app = Flask(__name__)
app.secret_key = secret_key
BOOTSTRAP = Bootstrap(app)

CONTROLLER = DMXController(CHANNELS, UPDATE_RATE_MS)
CONTROLLER.set_channel(INIT_CHANNEL, INIT_CHANNEL_VALUE)

HANDLER = ControllerHandler(CONTROLLER)


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


@app.route('/toggle', methods=['POST'])
def toggle():
    """Method used when toggling the lights with a color"""
    status = HANDLER.toggle()
    session['status_toggle'] = status
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    """Method used when user goes to the homepage"""
    # All possible variables that can be given to the Jinja template.
    keys = ['color_animate', 'duration_animate', 'ease_animate', 'color_toggle', 'status_toggle']
    color_animate, duration_animate, ease_animate, color_toggle, status_toggle = [session.get(key)
                                                                                  if key in session
                                                                                  else ""
                                                                                  for key in keys]
    # If someone without a previous session goes to /, there is no status_toggle
    status_toggle = status_toggle or 'Click'

    logger.debug(f"Request data: {color_animate}, {duration_animate}, {ease_animate},"
                 f"{color_toggle}, {status_toggle}")
    return render_template('index.html', color_animate=color_animate,
                           duration_animate=duration_animate, ease_animate=ease_animate,
                           color_toggle=color_animate, status_toggle=status_toggle)


@app.errorhandler(InvalidRequestException)
def handle_invalid_request(error: InvalidRequestException):
    """ Returns a neat response to an error. """
    return render_template('errors/400.html', explanation=error.message), 400


@app.errorhandler(ControllerSetLEDException)
def handle_controller_set_led_exception(error: ControllerSetLEDException):
    """ Calls handle_invalid_request, as the same functionality is required. """
    return render_template('errors/500.html', explanation=error.message), 500


@app.errorhandler(USBError)
def handle_usb_error(error):
    return render_template('errors/500.html', explanation='usb error, remove the usb'), 500


@app.errorhandler(404)
def not_found(_):
    """Return custom 404 page"""
    return render_template('errors/404.html'), 404
