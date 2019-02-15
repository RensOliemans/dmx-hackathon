from dmx.model.fixture import Fixture


class RGBLamp(Fixture):

    def __init__(self, channel, dmx_controller):
        self.__channel = channel
        self.__dmx_controller = dmx_controller

    def change_color(self, r, g, b):
        self.__dmx_controller.set_channel(self.__channel, r)
        self.__dmx_controller.set_channel(self.__channel + 1, g)
        self.__dmx_controller.set_channel(self.__channel + 2, b)
        self.__dmx_controller.make_frame()
        self.__dmx_controller.make_frame()

    def shutdown(self):
        self.__dmx_controller.set_channel(self.__channel, 0)
        self.__dmx_controller.set_channel(self.__channel + 1, 0)
        self.__dmx_controller.set_channel(self.__channel + 2, 0)
        self.__dmx_controller.make_frame()
        self.__dmx_controller.make_frame()
        self.__dmx_controller.make_frame()
