# Basic script to redirect Serial data for GHOST
# author: Hasith Perera (ke8tje@gmail.com)
#

socat -d -d UDP-RECV:5000 /dev/ttyXR0,raw,echo=0,b230400 & ## wallops interface


#socat -d -d /dev/ttyXR1,b115200,raw UDP:127.0.0.2:5000 & 	# WVSU - B
socat -d -d /dev/ttyXR1,b115200,icanon UDP:127.0.0.2:5000 & 	# WVSU - B
socat -d -d /dev/ttyXR6,b115200,raw UDP:127.0.0.2:5000 & 	# WVU - Electric fields
socat -d -d /dev/ttyXR7,b9600,raw UDP:127.0.0.2:5000 &   	# sim - slow (10Hz)


socat -d -d /dev/ttyACM0,b9600,raw UDP:127.0.0.2:5000 & 	# WVU - IRGOW TPRH



