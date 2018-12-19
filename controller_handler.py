import time

import pytweening
from numpy import linspace

from config import FPS
from color import Color


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class ControllerHandler:
    """
    Handler class; used by the webserver, contains bits of controller functionality
    """

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

        animation = self.generate_animation(self.current_color, Color(r, g, b),
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

    @staticmethod
    def generate_animation(start_color, final_color, duration, ease):
        """
        Generates an animation for the controller.

        :param start_color: color before the animation
        :param final_color: supposed color after the animation
        :param duration: duration of the animation
        :param ease: the easing function to use
        :return: list of colors in the animation
        """
        diff = final_color - start_color
        tween = getattr(pytweening, ease)
        # Get list of colors in the animation
        animation = [start_color + diff * tween(step)
                     for step in linspace(0, 1, int(FPS * duration / 1000))]
        return animation
