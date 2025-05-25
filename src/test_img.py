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
image = cv2.imread("in.png")




print(image.size)
print(np.shape(image))

gray = image[:,:,0];

print(np.shape(gray))

# show the image
#cv2.imshow('gray',image)
#cv2.waitKey(0)

h = 3040
w = 4040

w_box = 202 # box size in packet


def im2hex_4bit(img,n_packets):
    ''' build custom packet

    img: data
    i: row index
    n_packets: sub packets per row
    '''
    width = np.size[1]
    w_lenght = int(width/n_packets)

    return 0




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

def send_array(sock, arr):
    # Serialize array to bytes
	#memfile = BytesIO()
    # np.save writes shape, dtype, etc.
	#np.save(memfile, arr)
	#memfile.seek(0)
	#data = memfile.read()
	data = arr.tobytes()
    # Prefix with message length
	length = len(data)
	#print(f"bin len:{length}")
    #sock.sendto(struct.pack('!I', length))  # Network byte order
	sock.sendto(data,(UDP_IP, UDP_PORT))


# base91 encoding 
data = img2base91(gray)
data2 = img2hex(gray,0)

# create a socket to send the data via UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#i = 3029
#j = 18
#w_length = int(4040/20)
#print(w_length)
#send_array(sock,gray[i,j*w_length:(j+1)*w_length])
#print("done UDP sending")
#exit()
t_start = time.time()


#send bin
for i in range(0,h):
		
	w_length = int(4040/20) 
	data_packet = "imr{:3x}:".format(i)
	sock.sendto(data_packet.encode('utf-8'),(UDP_IP, UDP_PORT)) #row-header
	data2 = img2hex(gray,i)
	for j in range(0,20):
		data_packet=":{:02}|".format(j)
		sock.sendto(data_packet.encode('utf-8'),(UDP_IP, UDP_PORT))
		send_array(sock,gray[i,j*w_length:(j+1)*w_length])


## send as hex
#for i in range(0,h):
		
#	w_length = int(4040/20)*2 ## extRA 2 ACCOUNTS FOR HEX
#	data_packet = "imr{:4x}:".format(i)
#	sock.sendto(data_packet.encode('utf-8'),(UDP_IP, UDP_PORT)) #row-header
#	data2 = img2hex(gray,i)
#	for j in range(0,20):
#		data_packet=":{:02}|{}".format(j,data2[j*w_length:(j+1)*w_length])
#		sock.sendto(data_packet.encode('utf-8'),(UDP_IP, UDP_PORT))


t_end = time.time()




print("Image sent in:{}".format(t_end-t_start))
sock.close()

