import socket
import cv2
import numpy as np

import base91
import time



# Settings
UDP_IP = "127.0.0.1"   # Receiver IP
UDP_PORT = 5000        # Receiver Port
CHUNK_SIZE = 4096      # Must be <= 65507 for UDP

# Read image and encode to bytes
image = cv2.imread("cameraman.png")




print(image.size)
print(np.shape(image))

gray = image[:,:,0];

print(np.shape(gray))

# show the image
#cv2.imshow('gray',image)
#cv2.waitKey(0)

h = 648;
w = 648;




def img2base91(img):
	raw = img[:,0].tobytes()
	enc = base91.encode(raw)
	return enc

def img2hex(img,i):
	hex_array = np.array([format(x, '02x') for x in img[i,:]])
	row = "".join(hex_array)
	return row

# base91 encoding 
data = img2base91(gray)
data2 = img2hex(gray,0)

# create a socket to send the data via UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(data.encode('utf-8'),(UDP_IP, UDP_PORT))
sock.sendto(data2.encode('utf-8'),(UDP_IP, UDP_PORT))


t_start = time.time()
for i in range(0,h):
	
	data2 = img2hex(gray,i)
	data_packet = "img{:04}::{}".format(i,data2)
	sock.sendto(data_packet.encode('utf-8'),(UDP_IP, UDP_PORT))
t_end = time.time()




print("Image sent in:{}".format(t_end-t_start))
sock.close()

