import serial
import time
import os
import glob
import shutil
import cv2
import re

import numpy as np

# Configure the serial port
#ser = serial.Serial('/dev/ttyS0', baudrate=230400) # Replace /dev/ttyS0 with the correct port if needed
home_dir=os.environ['HOME']

def img2hex(img,i):
        hex_array = np.array([format(x, '02x') for x in img[i,:]])
        row = "".join(hex_array)
        #print("test")
        return row


def send_block_img(gray,serial=[]):
## send as hex
        h = gray.shape[0]
        for i in range(0,h):
                w_length = int(gray.shape[1]/20)*2 ## extRA 2 ACCOUNTS FOR HEX
                data_packet = "imr{:4x}:".format(i)
                data2 = img2hex(gray,i)
                for j in range(0,20):
                        data_packet=":{:02}|{}".format(j,data2[j*w_length:(j+1)*w_length])

                        #replace call with serial.write
                        ser.write(data_packet.encode())
                        #print(data_packet)

def convertgray(home_dir,i):
    # read the jpg file
    # convert this to a gray file
    # save it as /path/grayx.jpg
	#st = time.time()
    
    file_input = glob.glob(f"{home_dir}/Pictures/pic{i}-*.jpg")
    if (j == 0):
        img = cv2.imread(file_input[0])
    elif (j == 1):
        img = cv2.imread(file_input[0])	
    elif (j == 2):
        img = cv2.imread(file_input[0])
    elif j == 3:
        img = cv2.imread(file_input[0])
	

    return img

def format_image(img,j):
	# crop image
	#cropped_img = img[800:1600,1000:2000]
	
	#Resize Image
    if j == 0:
        resized_img = img
    elif j == 1:
        resized_img = cv2.resize(img, (0,0), fx = 0.1, fy = 0.1)
    elif j == 2:
        resized_img = cv2.resize(img, (0,0), fx = 0.1, fy = 0.1)
    elif j == 3:
        resized_img = img
    return resized_img  
    
def check_for_files(filepath):
    
    for filepath_object in glob.glob(filepath):
        if os.path.isfile(filepath_object):
            return True
    return False

while True:
    time.sleep(.1)
    i=1
    
    while check_for_files(f"{home_dir}/Pictures/pic{i}-*.jpg") and check_for_files(f"{home_dir}/Pictures/sent{i}.jpg"):
        i+=1
        #print(i)
        #time.sleep(1)
    
    if check_for_files(f"{home_dir}/Pictures/pic{i}-*.jpg"):
        if check_for_files(f"{home_dir}/Pictures/pic{i}-0.jpg"):
            j = 0
        elif check_for_files(f"{home_dir}/Pictures/pic{i}-1.jpg"):
            j = 1
        elif check_for_files(f"{home_dir}/Pictures/pic{i}-2.jpg"):
            j = 2
        elif check_for_files(f"{home_dir}/Pictures/pic{i}-3.jpg"):
            j = 3
        start_time = time.time()
        #final_img = convertgray(home_dir,i)
        #print("{i} start test program")
        final_img = format_image(convertgray(home_dir,i),j)
        
       
        output_path = glob.glob(f"{home_dir}/Pictures/pic{i}-*.jpg")
        cv2.imwrite(output_path[0], final_img)
#        print('Done the thing!')
        print(f"{i} start img tx")
        time_start = time.time()
        
        ser = serial.Serial('/dev/ttyAMA0', baudrate=230400)
        
        if j == 0:
            gray = final_img[:,:,0];
            send_block_img(gray,ser)
        elif j == 1:
            data=open(output_path[0],'rb').read()
            ser.write(data)
        elif j == 2:
            data=open(output_path[0],'rb').read()
            ser.write(data)
        elif j == 3:
            pass
            #send_block_img(final_img,ser)
            
        ser.close()
        
        print(f"{i} end img tx after {(time.time() - time_start)}")
        
        
        shutil.copy(output_path[0], f"{home_dir}/Pictures/sent{i}.jpg")
        
        print(f"[i] img pic{i} done")
        with open('/home/rpi/ghost.log','a+') as fp:
            fp.write("pic{}:{}\n".format(i,time.time()-start_time))
        #ser = serial.Serial('/dev/ttyAMA0', baudrate=230400)
        #ser.write(("$$$").encode('utf-8'))
        #ser.close()

