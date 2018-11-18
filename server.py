from flask import Flask
from flask import request, jsonify
import pytweening
from numpy import linspace
from controller import DMX_controller
from config import FPS
import time
app = Flask(__name__)

c = DMX_controller(32, 50)
c.set_channel(1, 100)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Color(int(self.r + other.r), int(self.g + other.g), int(self.b + other.b))

    def __sub__(self, other):
        return Color(int(self.r - other.r), int(self.g - other.g), int(self.b - other.b))

    def __mul__(self, other):
        return Color(int(self.r * other), int(self.g * other), int(self.b * other))

    __rmul__ = __mul__

    def __str__(self):
        return ', '.join([str(self.r), str(self.g), str(self.b)])


current_color = Color(0, 0, 0)


def set_led(r, g, b):
    c.send_start(0, [r, g, b, 0, 0, 0])
    c.make_frame()
    c.make_frame()


def generate_animation(f, t, duration, ease):
    animation = []
    diff = t - f
    tween = getattr(pytweening, ease)
    for step in linspace(0, 1, int(FPS * duration/1000)):
        s = tween(step)
        color = f + diff * s
        animation.append(color)
    return animation


def play_animation(animation):
    for frame in animation:
        set_led(frame.r, frame.g, frame.b)
        time.sleep(1 / FPS)


@app.route('/animate', methods=['POST'])
def animate():
    global current_color
    data = request.get_json()
    color = data['color']
    animation = generate_animation(current_color, Color(
        color['r'], color['g'], color['b']), data['duration'], data['ease'])
    play_animation(animation)
    current_color = animation[-1]
    return jsonify([str(color) for color in animation])
