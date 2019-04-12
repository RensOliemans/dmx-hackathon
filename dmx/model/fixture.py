""""
    This class models a device that works with DMX
"""

from abc import ABC, abstractmethod


class Fixture(ABC):

    @abstractmethod
    def change_color(self, r, g, b, animated):
        raise NotImplementedError('subclasses must override change_color!')

    @abstractmethod
    def shutdown(self):
        raise NotImplementedError('subclasses must override shutdown!')
