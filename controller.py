import usb
import codecs


# find our device
dev = usb.core.find(idVendor=0x10cf, idProduct=0x8062)

# was it found?
if dev is None:
    raise ValueError('Device not found')

try:
    if dev.is_kernel_driver_active(0) is True:
        dev.detach_kernel_driver(0)
except usb.core.USBError as e:
    sys.exit("Kernel driver won't give up control over device: %s" % str(e))

try:
    dev.set_configuration()
    dev.reset()
except usb.core.USBError as e:
    sys.exit("Cannot set configuration the device: %s" % str(e))





# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
#ep.write(codecs.decode("040100000000000102ffffff00000000", "hex"))

class DMX_controller:
    __frame_string = ""

    def __init__(self, channels, update_rate_ms):
        if channels <= 512:
            self.channels = channels
        if update_rate_ms >= 25: 
            self.update_rate_ms = update_rate_ms
        self.frame = [0] * channels
        self.cur_frame = [0] * channels    
    def set_channel(self, channel, value):
       self.frame[channel-1] = value #-1 because dmx starts at channel 1

    def make_frame(self):
        print(self.__frame_string)
        print(ep.write(self.__frame_string))
        
    def send_start(self, skip, data_array):
        self.__frame_string = (4).to_bytes(1, byteorder='big')
        self.__frame_string += (skip+1).to_bytes(1, byteorder = 'big')
        for i in data_array:
            self.__frame_string += (i).to_bytes(1, byteorder ='big')
    def send_data(self, data_array):
        return
    def send_single(self, data):
        return
    def send_data_skip(self, skip, data_array):
        pass





c = DMX_controller(32, 50)
c.set_channel(1, 100)

c.send_start(0,[255,0,0,0,0,0])
c.make_frame()
c.make_frame()

'''
def set_led(red, green, blue):
    tmp = ""
    tmp = red+green+blue
    ep.write(codecs.decode("0401"+tmp+"000000","hex"))


def set_channel(channel, value)
''' 
