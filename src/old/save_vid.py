from picamera2 import Picamera2

import glob

picam2 = Picamera2()


num_file = len(glob.glob("./data/*.mp4"))
picam2.start_and_record_video("./data/test_video_{}.mp4".format(num_file+1), duration=10)

