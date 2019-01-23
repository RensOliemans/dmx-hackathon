import time
import random

import pytweening
from numpy import linspace

from log import logger
from Exceptions.Exceptions import ControllerSetLEDException, InvalidRequestException
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
        self.current_color: Color = current_color

    def animate(self, request_json):
        """
        This method called when an animate request is done. It connects with the controller.
        :param request_json: data which is gathered from the request
        :return: the final current_color, duration and ease
        """
        logger.debug(f"Got request with data {request_json}")
        try:
            color = Color.to_rgb(request_json['color'])
            duration = int(request_json['duration'])
            ease = request_json['ease']
        except (TypeError, KeyError, ValueError, AttributeError) as e:
            logger.error(f"Request was incorrectly formatted. Was {request_json}")
            raise InvalidRequestException('request should have the Color, Duration and Ease. It was:'
                                          '{req_json}'.format(req_json=request_json), inner_exception=e)

        animation = self.generate_animation(self.current_color, color,
                                            duration, ease)
        logger.debug(f"Generated animation: {animation}" )

        self.play_animation(animation)

        # Last color of the animation is the 'final' color, so the current color of the controller
        self.current_color = animation[-1]
        return self.current_color, duration, ease

    def toggle(self):
        """
        This method is called when the lights need to go on or off.
        :return: status being 1 or 0, after the switch has been done
        """
        # TODO: implement when controller has functionality
        # status = self.controller.get_status()
        status = 0
        if status:
            # Lights are already on, turn them off
            # self.controller.turn_off()
            pass
        else:
            self.set_led(self.current_color.r, self.current_color.g, self.current_color.b)

        # return color, self.controller.get_status()
        status = random.choice((0, 1))
        return 'On' if status else 'Off'

    def play_animation(self, animation):
        for frame in animation:
            self.set_led(frame.r, frame.g, frame.b)
            time.sleep(1 / FPS)

    def set_led(self, r, g, b):
        try:
            self.controller.send_start(0, [r, g, b, 0, 0, 0])
            self.controller.make_frame()
            self.controller.make_frame()
        except (NameError, OverflowError) as e:
            logger.error("Is the controller initialised correctly?")
            raise ControllerSetLEDException('Controller set LED went wrong', inner_exception=e)

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
        try:
            tween = getattr(pytweening, ease)
        except (TypeError, AttributeError) as e:
            logger.error(f"PyTweening couldn't understand the 'ease' function. Passed ease: {ease}")
            # The 'ease' wasn't a string, or wasn't understood by PyTweening
            raise InvalidRequestException('"ease" was not a valid PyTweening ease', inner_exception=e)

        # Get list of colors in the animation
        animation = [start_color + diff * tween(step)
                     for step in linspace(0, 1, int(FPS * duration / 1000))]
        # if duration was too short (no single step was made), add final_color to animation
        if final_color not in animation:
            animation.append(final_color)
        return animation
