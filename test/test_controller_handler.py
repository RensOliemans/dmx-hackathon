from unittest.mock import MagicMock

import pytweening
from numpy import linspace

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
    return controller_mock


def get_handler():
    controller = get_controller_mock()
    return ControllerHandler(controller), controller


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
