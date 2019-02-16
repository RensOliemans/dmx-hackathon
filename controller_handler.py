"""
ControllerHandler module. This module handles the controller, so other entities such as web servers
don't have to know controller-specific things.
"""
import time
import random

import pytweening
from numpy import linspace

from log import logger
from exceptions.exceptions import ControllerSetLEDException, InvalidRequestException
from config import FPS
from color import Color

from dmx.model.rgb_lamp import RGBLamp


class ControllerHandler:
    """
    Handler class; used by the webserver, contains bits of controller functionality
    """

    def __init__(self, controller, current_color=Color(255, 60, 0)):
        self.controller = controller
        self.current_color = current_color
        self.lamp1 = RGBLamp(1, controller)

    def animate(self, request_json):
        """
        This method called when an animate request is done. It connects with the controller.
        :param request_json: data which is gathered from the request
        :return: the final current_color, duration and ease
        """
        logger.debug("Got request with data {}".format(request_json))
        try:
            color = Color.to_rgb(request_json['color'])
            duration = int(request_json['duration'])
            ease = request_json['ease']
        except (TypeError, KeyError, ValueError, AttributeError) as exception:
            logger.error("Request was incorrectly formatted. Was {}".format(request_json))
            raise InvalidRequestException('request should have the Color, Duration and Ease.'
                                          "It was{}".format(request_json), inner_exception=exception)

        animation = self.generate_animation(self.current_color, color,
                                            duration, ease)
        logger.debug("Generated animation: {}".format(animation))

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
            self.lamp1.shutdown()
            pass
        else:
            self.set_led(self.current_color)

        # return color, self.controller.get_status()
        status = random.choice((0, 1))
        return 'On' if status else 'Off'

    def play_animation(self, animation):
        """
        Plays a certain animation
        :param animation: list of Colors, animations to play
        :return: None
        """
        for frame in animation:
            self.set_led(frame)
            time.sleep(1 / FPS)

    def set_led(self, color: Color):
        """
        Sets a LED by calling the controller
        :param: color, (r, g, b), color to set
        :return: None
        """
        try:
            # Instant color changes should not have animated=True since it results in undesired behaviour
            self.lamp1.change_color(color.r, color.g, color.b, True)
        except (NameError, OverflowError) as exception:
            logger.error("Is the controller initialised correctly?")
            raise ControllerSetLEDException('Controller set LED went wrong',
                                            inner_exception=exception)

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
        except (TypeError, AttributeError) as exception:
            logger.error("PyTweening couldn't understand the 'ease' function. Passed ease: {}".format(ease))
            # The 'ease' wasn't a string, or wasn't understood by PyTweening
            raise InvalidRequestException('"ease" was not a valid PyTweening ease',
                                          inner_exception=exception)

        # Get list of colors in the animation
        animation = [start_color + diff * tween(step)
                     for step in linspace(0, 1, int(FPS * duration / 1000))]
        # if duration was too short (no single step was made), add FINAL_COLOR to animation
        if final_color not in animation:
            animation.append(final_color)
        return animation
