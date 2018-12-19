from flask import Flask
from flask import request, jsonify

from config import UPDATE_RATE_MS, CHANNELS
from controller import DMXController
from webserver_handler import ControllerHandler

app = Flask(__name__)
c = DMXController(CHANNELS, UPDATE_RATE_MS)
c.set_channel(1, 100)

HANDLER = ControllerHandler(c)


@app.route('/animate', methods=['POST'])
def animate():
    data = request.get_json()
    animation = HANDLER.animate(data)
    return jsonify([str(color) for color in animation])
