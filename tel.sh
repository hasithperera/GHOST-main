# Basic script to redirect Serial data for GHOST
# author: Hasith Perera (ke8tje@gmail.com)


# replaced as ghost-udp.service
# socat  UDP-RECV:5000 /dev/ttyXR0,raw,echo=0,b230400 & ## wallops interface


# mode icanon - if using ascii and newlines for data
# raw - if binary is used

socat -d -d /dev/ttyXR1,b19200,icanon UDP:127.0.0.2:5000 & 	#Power - WVU
socat -d -d /dev/ttyXR7,b115200,icanon UDP:127.0.0.2:5000 &   	# BRCTC - Spectrometer



socat -d -d /dev/ttyXR6,b230400,raw UDP:127.0.0.2:5000 & 	# WVU - Electric fields
#socat -d -d /dev/ttyXR1,b115200,raw UDP:127.0.0.2:5000 & 	# WVSU - B
#socat -d -d /dev/ttyXR1,b9600,raw UDP:127.0.0.2:5000 & 	        # WVSU - Cube/Arm
socat -d -d /dev/ttyXR5,b115200,raw UDP:127.0.0.2:5000 &        # Spectrometer


#socat -d -d /dev/ttyACM0,b9600,raw UDP:127.0.0.2:5000 & 	# WVU - IRGOW TPRH



