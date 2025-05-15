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

#define ports 3 //max ports 7 - 0 index is for the input
#define serial_root "/dev/ttyXR%d"

//serial_id - port map
int serial_id[] = {1,6,7};

//serial_speed
speed_t serial_speed[]={B115200,B115200,B9600};

//exp order
// 0 - WVSU (120 Hz)
// 1 - sim b
// 2 - sim c (10Hz) 9600


#define packet_len 30

int main()
{
    char portname[20];
	


    int fd[ports];
    int rdlen[ports];
    char buf[8][packet_len];



    //new buffers to store data
    char buf_1[20000][packet_len]; 
    int thread_id_1[20000]; 


    int rx_index = 0;
    int tx_index = 0;



    //clean buffer to 0
    for (int i=0;i<8;i++){
    	for(int j=0;j<packet_len;j++){
	buf[i][j] = 0;
	}
    }

	for(int i=0;i<ports;i++){
		sprintf(portname,serial_root,serial_id[i]);
		printf("%s:%d\n",portname,serial_speed[i]);
    	fd[i] = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    	if (fd[i] < 0) {
        	printf("Error opening %s: %s\n", portname, strerror(errno));
        	return -1;
    	}
    	/*baudrate 115200, 8 bits, no parity, 1 stop bit */
    	//set_interface_attribs(fd[i], B115200);
    	
    	set_interface_attribs(fd[i], serial_speed[i]);
	
	//set_mincount(fd, 0);                /* set to pure timed read */
    	tcflush(fd[i], TCIFLUSH);  //flush remove junk
	}



    #pragma omp parallel num_threads(ports+1) shared(buf_1,rx_index,tx_index,thread_id_1)
	{
        int thread_id = omp_get_thread_num();
	int tmp;
	printf("thread_id:%d\n",thread_id);
	
		if(thread_id==ports){
			printf("TX thread is thread %d\n",thread_id);	
			while(rx_index<200){
				//wait till the thread is full

			}
			printf("BUF 1 full\n");
			
			for(int i=0;i<400;i++){
				printf("%d:%s|\n",thread_id_1[i],buf_1[i]);
			}


		}
	
		
	else{


		while(1){

			//v0.1 
			//tmp= read(fd[thread_id], buf[thread_id],packet_len);	
			//if(tmp > 0){
    			//printf("%d:%s|\n",thread_id,buf[thread_id]);
    			//printf("%s",buf[thread_id]);

			tmp = read(fd[thread_id],buf_1[rx_index],packet_len);
			thread_id_1[rx_index] = thread_id;

			printf("|%d,%d:%s\n",thread_id,rx_index,buf_1[rx_index]);
			rx_index++;

			}
		}
	}
}
