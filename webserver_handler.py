import time

import pytweening
from numpy import linspace

from config import FPS
from webserver import Color


def generate_animation(f, t, duration, ease):
    animation = []
    diff = t - f
    tween = getattr(pytweening, ease)
    for step in linspace(0, 1, int(FPS * duration / 1000)):
        s = tween(step)
        color = f + diff * s
        animation.append(color)
    return animation


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class ControllerHandler:
    def __init__(self, controller, current_color=Color(0, 0, 0)):
        self.controller = controller
        self.current_color = current_color

    def animate(self, request_json):
        """
        This method called when an animate request is done. It connects with the controller.
        :param request_json: data which is gathered from the request
        :return: list of colors in the animation
        """
        color = request_json['color']
        r, g, b = color['r'], color['g'], color['b']

        animation = generate_animation(self.current_color, Color(r, g, b),
                                       request_json['duration'], request_json['ease'])
        self.play_animation(animation)

        # Last color of the animation is the 'final' color, so the current color of the controller
        self.current_color = animation[-1]
        return animation

    def play_animation(self, animation):
        for frame in animation:
            self.set_led(frame.r, frame.g, frame.b)
            time.sleep(1 / FPS)

    def set_led(self, r, g, b):
        self.controller.send_start(0, [r, g, b, 0, 0, 0])
        self.controller.make_frame()
        self.controller.make_frame()
