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
#ep.write(codecs.decode("0401ff0000000000", "hex"))

def set_led(red, green, blue):
    tmp = ""
    tmp = red+green+blue
    ep.write(codecs.decode("0401"+tmp+"000000","hex"))
