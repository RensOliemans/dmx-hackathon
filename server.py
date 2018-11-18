from flask import Flask
from flask import request
from controller import set_led
app = Flask(__name__)


@app.route('/animate', methods=['POST'])
def animate():
    color = request.get_json()
    set_led(color['r'], color['g'], color['b'])
    return 'kek'
