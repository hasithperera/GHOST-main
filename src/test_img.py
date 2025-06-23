import socket
import cv2
import numpy as np

#import base91
import time



# Settings
UDP_IP = "127.0.0.1"	 # Receiver IP
UDP_PORT = 5000				 # Receiver Port
CHUNK_SIZE = 4096			 # Must be <= 65507 for UDP

# Read image and encode to bytes
# show the image
#cv2.imshow('gray',image)
#cv2.waitKey(0)

h = 3040
w = 4040

w_box = 202 # box size in packet





def img2base91(img):
	raw = img[:,0].tobytes()
	enc = base91.encode(raw)
	return enc

def img2hex(img,i):
	hex_array = np.array([format(x, '02x') for x in img[i,:]])
	row = "".join(hex_array)
	#print("test")
	return row



# chatGPT unction to encode np data as binary
import struct
from io import BytesIO

def send_array_udp(sock, arr):
	data = arr.tobytes()
		# Prefix with message length
	length = len(data)
	sock.sendto(data,(UDP_IP, UDP_PORT))


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
			print(data_packet)


	


if (__name__=='__main__'):
	print('main exec')
	image = cv2.imread("in.png")
	gray = image[:,:,0];

	print(np.shape(gray))


	t_start = time.time()
	send_block_img(gray,[])
	t_end = time.time()

	print("Image sent in:{}".format(t_end-t_start))

