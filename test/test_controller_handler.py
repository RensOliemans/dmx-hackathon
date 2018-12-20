from unittest.mock import MagicMock

import pytweening
from numpy import linspace

from Exceptions.Exceptions import ControllerSetLEDException
from color import Color
from config import FPS
from controller_handler import ControllerHandler
from controller import DMXController

start_color = Color(201, 117, 128)
final_color = Color(193, 109, 120)
default_duration = 300
default_ease = 'linear'


def get_controller_mock():
    controller_mock = DMXController(1, 10)
    controller_mock.make_frame = MagicMock()
    controller_mock.send_start = MagicMock()
    controller_mock.send_data = MagicMock()
    controller_mock.send_data_skip = MagicMock()
    controller_mock.send_single = MagicMock()
    return controller_mock


def get_handler():
    controller = get_controller_mock()
    return ControllerHandler(controller), controller


'''                                            Test generate_animation                                   '''


def test_generate_animation_same_colors():
    # Arrange
    handler, _ = get_handler()

    # Act
    animation = handler.generate_animation(start_color, start_color, default_duration, default_ease)
    # Assert
    assert all([x == animation[0] for x in animation])


def test_generate_animation_different_colors():
    # Arrange
    handler, _ = get_handler()

    # Act
    animation = handler.generate_animation(start_color, final_color, default_duration, default_ease)
    # Assert
    assert not all([x == animation[0] for x in animation])


def test_generate_animation_correct_animation():
    # Arrange
    handler, _ = get_handler()
    diff = final_color - start_color
    tween = getattr(pytweening, default_ease)
    correct_animation = [start_color + diff * tween(step)
                         for step in linspace(0, 1, int(FPS * default_duration / 1000))]

    # Act
    animation = handler.generate_animation(start_color, final_color, default_duration, default_ease)
    # Assert
    assert animation == correct_animation


def test_generate_animation_correct_amount():
    # Arrange
    handler, _ = get_handler()
    steps = len(linspace(0, 1, int(FPS * default_duration / 1000)))

    # Act
    animation = handler.generate_animation(start_color, final_color, default_duration, default_ease)

    # Assert
    assert len(animation) == steps


def test_generate_animation_no_steps():
    """
    Method should have only the final color in the list, since the duration is too short to allow even a single
    step
    """
    # Arrange
    handler, _ = get_handler()
    duration = 800 / FPS

    # Act
    animation = handler.generate_animation(start_color, final_color, duration, default_ease)

    # Assert
    assert animation == [final_color]


def test_generate_animation_one_step():
    """
    Method should have only the start color and the final color in the list,
    since there is only one step possible with the duration
    """
    # Arrange
    handler, _ = get_handler()
    duration = 1000 / FPS

    # Act
    animation = handler.generate_animation(start_color, final_color, duration, default_ease)

    # Assert
    assert animation == [start_color, final_color]


def test_generate_animation_different_ease():
    # Arrange
    handler, _ = get_handler()
    ease = "easeInQuad"
    diff = final_color - start_color
    tween = getattr(pytweening, ease)
    wrong_tween = getattr(pytweening, default_ease)
    correct_animation = [start_color + diff * tween(step)
                         for step in linspace(0, 1, int(FPS * default_duration / 1000))]
    wrong_animation = [start_color + diff * wrong_tween(step)
                       for step in linspace(0, 1, int(FPS * default_duration / 1000))]

    # Act
    animation = handler.generate_animation(start_color, final_color, default_duration, ease)

    # Assert
    assert correct_animation == animation
    assert wrong_animation != animation


'''                                              Test play_animation                                           '''


def test_play_animation():
    """ play_animation should call handler.set_led as many times as there are animation frames. """
    # Arrange
    handler, _ = get_handler()
    handler.set_led = MagicMock()

    # Act
    animation = handler.generate_animation(start_color, final_color, default_duration, default_ease)
    handler.play_animation(animation)

    # Assert
    assert handler.set_led.call_count == len(animation)


def test_set_led():
    """ set_led should call controller.send_start with the rgb values, and should call make_frame twice.  """
    # Arrange
    handler, controller = get_handler()
    r, g, b = start_color.r, start_color.g, start_color.b

    # Act
    handler.set_led(r, g, b)

    # Assert
    controller.send_start.assert_called_once_with(0, [r, g, b, 0, 0, 0])
    assert controller.make_frame.call_count == 2


# noinspection PyBroadException
def test_set_led_raise_correct_exception():
    """ if make_frame raise a NameError, set_led should raise a ControllerSetLEDException """
    # Arrange
    handler, controller = get_handler()
    r, g, b = start_color.r, start_color.g, start_color.b
    controller.make_frame = MagicMock(side_effect=NameError('foo'))
    exception = None

    # Act
    try:
        handler.set_led(r, g, b)
    except Exception as e:
        exception = e

    # Assert
    assert exception is not None
    assert type(exception) == ControllerSetLEDException
