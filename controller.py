import usb
import codecs
import random
import time
import sys

from log import logger

from dmx.model.rgb_lamp import RGBLamp

# find our device
dev = usb.core.find(idVendor=0x10cf, idProduct=0x8062)

# was it found?
if dev is None:
    logger.error('Device not found')
    raise ValueError('Device not found')

try:
    if dev.is_kernel_driver_active(0) is True:
        dev.detach_kernel_driver(0)
except usb.core.USBError as e:
    logger.error("Kernel driver won't give up control over device: %s", str(e))
    sys.exit("Kernel driver won't give up control over device: %s" % str(e))

dev.set_configuration()



class DMX_controller:

    def __init__(self, update_rate_ms):
        self.update_rate_ms = update_rate_ms
        self.frame = [0] * 512
        self.prev_frame = [0]* 512 

    def set_channel(self, channel, value):
        self.frame[channel-1] = value  # -1 because dmx starts at channel 1

    def make_frame(self):
        cnt = 0
        tmp = [0]*512
        zeros = 0
        for i in range(512):
            tmp[i] = self.frame[i]-self.prev_frame[i] 
        while(cnt<511):
            zeros = self.zeros_after_packet(tmp,cnt)
            if cnt == 0:
                #print("send start chn:"+str(zeros+1))
                self.send_start(zeros,self.frame[zeros:zeros+6])
                cnt = 6 + zeros
            elif cnt > 511:
                break
            else:
                if cnt > 504:
                    if (512 - cnt) == 7:
                        #print("send data ch :"+str(cnt+1))
                        self.send_data(self.frame[cnt:cnt+7])
                        cnt += 7
                    else:
                        #print("send single ch:"+str(cnt+1))
                        self.send_single(self.frame[cnt])
                        cnt += 1
                else:
                    if zeros > 0:
                        #print("send skip ch:" + str(cnt+zeros+1))
                        self.send_data_skip(zeros, self.frame[cnt+zeros:cnt+zeros+6])
                        cnt += zeros + 6
                    else:
                        #print("send data ch:"+str(cnt+1))
                        self.send_data(self.frame[cnt:cnt+7])
                        cnt += 7
        

    def zeros_after_packet(self,data,start):
        cnt = 0
        #can not skip past channel 505
        for i in data[start:505]:
            if i==0:
                cnt += 1
            else:
                break
        if cnt < 255:
            return cnt
        else:
            return 254

    def send_start(self, skip, data_array):
        tmp = (4).to_bytes(1, byteorder='big')
        tmp += (skip+1).to_bytes(1, byteorder='big')
        for i in data_array:
            tmp += (i).to_bytes(1, byteorder='big')
        dev.write(1,tmp)
    def send_data(self, data_array):
        tmp = (2).to_bytes(1, byteorder ='big')
        for i in data_array:
            tmp += (i).to_bytes(1, byteorder='big')
        dev.write(1,tmp)
    def send_single(self, data):
        tmp = (3).to_bytes(1, byteorder = 'big')
        tmp += (data).to_bytes(1, byteorder ='big')
        tmp += (0).to_bytes(6, byteorder = 'big')
        dev.write(1,tmp)
    def send_data_skip(self, skip, data_array):
        tmp = (5).to_bytes(1, byteorder = 'big')
        tmp += (skip).to_bytes(1, byteorder = 'big')
        for i in data_array:
            tmp += (i).to_bytes(1, byteorder = 'big')
        dev.write(1,tmp)
            
   
dmx = DMX_controller(100)
'''
for z in range(1):
    dmx.send_start(0,[0,0,0,0,0,0])
    for i in range (71):
        dmx.send_data([0,0,0,0,0,0,0])
    dmx.send_data([0,0,20+z*20,0,0,0,0])
    dmx.send_single(0)
'''

lamp1 = RGBLamp(508, dmx)
lamp2 = RGBLamp(129,dmx)

lamp2.change_color(0,0,255,False)
cnt = 255
for i in range(255):

    lamp1.change_color(i,cnt,100, True)
    cnt -= 1

'''
for i in range(500):
    dmx.send_start(254,[0,255,255,0,0,0])
    dmx.send_data_skip(245,[0,0,0,0,0,0])
'''
