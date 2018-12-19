from flask import Flask
from flask import request, jsonify

from controller import DMXController
from color import Color
from webserver_handler import ControllerHandler

app = Flask(__name__)
c = DMXController(32, 50)
c.set_channel(1, 100)

CURRENT_COLOR = Color(0, 0, 0)
HANDLER = ControllerHandler(c, current_color=CURRENT_COLOR)


@app.route('/animate', methods=['POST'])
def animate():
    data = request.get_json()
    animation = HANDLER.animate(data)
    return jsonify([str(color) for color in animation])
