#define TERMINAL    "/dev/ttyUSB0"

#include <errno.h>
#include <fcntl.h> 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>


#include <omp.h>

int set_interface_attribs(int fd, int speed)
{
    struct termios tty;

    if (tcgetattr(fd, &tty) < 0) {
        printf("Error from tcgetattr: %s\n", strerror(errno));
        return -1;
    }

    cfsetospeed(&tty, (speed_t)speed);
    cfsetispeed(&tty, (speed_t)speed);

    tty.c_cflag |= (CLOCAL | CREAD);    /* ignore modem controls */
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;         /* 8-bit characters */
    tty.c_cflag &= ~PARENB;     /* no parity bit */
    tty.c_cflag &= ~CSTOPB;     /* only need 1 stop bit */
    tty.c_cflag &= ~CRTSCTS;    /* no hardware flowcontrol */

    /* setup for non-canonical mode */
    tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    tty.c_oflag &= ~OPOST;

    /* fetch bytes as they become available */
    tty.c_cc[VMIN] = 5;
    tty.c_cc[VTIME] = 10;

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        printf("Error from tcsetattr: %s\n", strerror(errno));
        return -1;
    }
    return 0;
}

void set_mincount(int fd, int mcount)
{
    struct termios tty;

    if (tcgetattr(fd, &tty) < 0) {
        printf("Error tcgetattr: %s\n", strerror(errno));
        return;
    }

    tty.c_cc[VMIN] = mcount ? 1 : 0;
    tty.c_cc[VTIME] = 5;        /* half second timer */

    if (tcsetattr(fd, TCSANOW, &tty) < 0)
        printf("Error tcsetattr: %s\n", strerror(errno));
}

#define ports 2

int main()
{
    char portname[20];


    int fd[ports];
    int rdlen[ports];
    char buf[2][10];

	for(int i=0;i<ports;i++){
		sprintf(portname,"/dev/ttyUSB%d",i);
		printf("%s\n",portname);
    	fd[i] = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    	if (fd[i] < 0) {
        	printf("Error opening %s: %s\n", portname, strerror(errno));
        	return -1;
    	}
    	/*baudrate 115200, 8 bits, no parity, 1 stop bit */
    	set_interface_attribs(fd[i], B115200);
    	//set_mincount(fd, 0);                /* set to pure timed read */
    	tcflush(fd[i], TCIFLUSH);  //flush remove junk
	}

    
    #pragma omp parallel num_threads(2)
	{
        int thread_id = omp_get_thread_num();
		int tmp;
	       

		while(1){
			tmp= read(fd[thread_id], buf[thread_id],10);	
			if(tmp > 0){
    			printf("%d-%s\n",thread_id,buf[thread_id]);
			}
		}
	}
}
