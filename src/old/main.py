
# Author: Hasith Perera
# content: get data fromo VEML 7700

import time
import sys
import os

import config as cfg

from DFRobot_VEML7700 import *
from ahe import *  #basic file io functions

import numpy as np
from scipy.io import savemat

veml7700 = DFRobot_VEML7700_I2C(bus_num = 1)

def lux_init():
    if(veml7700.begin() == False):
        print('[!] Light sensor error')
        return 0;
    else:
        return 1


def write_lux_file(start_id,data=0):
    file_num = start_id+1
    curr_file = "{}ahe_{}.mat".format(cfg.data_location,file_num)
    print(curr_file)
    savemat(curr_file,data)


if __name__=='__main__':
    # main program 
    
    print('[i] Start')
    err = lux_init()
    file_num = get_bin_log_id()
    print(f"[i] save loc:{cfg.data_location}")
    print(f"[i] {file_num} bin files found")

    cfg.log_file = f"{cfg.data_location}light_{file_num+1}.mat"
    #exit()

    data = np.zeros([100]);
    start_id = get_bin_log_id()
    for t_i in range(1,60):
        
        # lux experiment 
        t_s = time.time()
        for i in range(1,100):
            data[i] = veml7700.get_ALS_lux()
            time.sleep(.01)
        print(f"\n total time:{time.time()-t_s}")
        ahe_data = {'time_stamp':t_s,'data':data}
        write_lux_file(start_id+t_i,ahe_data)

    
