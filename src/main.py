
# Author: Hasith Perera
# content: get data fromo VEML 7700

import time
import sys
import os

import config as cfg

from DFRobot_VEML7700 import *
from ahe import *  #basic file io functions

import numpy as np

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
    file_num = get_bin_log_id()
    print(f"[i] save loc:{cfg.data_location}")
    print(f"[i] {file_num} bin files found")

    cfg.log_file = f"{cfg.data_location}light_{file_num+1}.bin"
    #exit()


    t_s = time.time()
    #while(True):


    data = np.zeros([100]);
    for i in range(1,100):
        #t_o = time.time()
        data[i] = veml7700.get_ALS_lux()
        time.sleep(.01)

        #print("{},{}".format(time.time()-t_o,lux))
    print(f"\n total time:{time.time()-t_s}")
    print(data)
