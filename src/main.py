
# Author: Hasith Perera
# content: get data fromo VEML 7700

import time
import sys
import os



from DFRobot_VEML7700 import *

veml7700 = DFRobot_VEML7700_I2C(bus_num = 1)

def lux_init():
    if(veml7700.begin() == False):
        print('[!] Light sensor error')
        return 0;
    else:
        return 1


if __name__=='__main__':
    # main program 
    
    print('[i] Start')
    err = lux_init()

    #while(True):
    for i in range(1,20):
        t_o = time.time()
        lux = veml7700.get_ALS_lux()
        time.sleep(.1)
        
        print("{},{}".format(time.time()-t_o,lux))
