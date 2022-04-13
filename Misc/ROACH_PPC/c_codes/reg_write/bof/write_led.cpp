#include <stdio.h>
#include <sys/mman.h>   //to have mmap
#include <stdlib.h>     //to have atoi
#include <fcntl.h>      //for the alias O_RDRW
#include <unistd.h>     //to have sleep

/*  This code just write the led value and then writes into the "in" registers
 *  and reads the "out" register.
 *  The only caveat is that you should progam the fpga before running this script
 *  :P
 */


#define IN_ADDR 0x01000000
#define LED_ADDR 0x01000100
#define OUT_ADDR 0x01000200
#define PAGE_SIZE 4096

void mmap_addr_calc(int addr, int page_size, int* out){
    int base_addr = (addr/page_size)*page_size;
    int offset = addr%page_size;
    out[0] = base_addr;
    out[1] = offset;
}


int main(int argc, char* argv[]){
   if(argc < 2){
    printf("You have to enter a number");
    return 1;
   }
    int fpga_fd = open("/dev/roach/mem", O_RDWR);
    if(fpga_fd == 0){
        printf("Error opening the roach mem file \n");
        return 1;
    }
    printf("roach mem file opened \n");

    int prot = (PROT_READ | PROT_WRITE);
    int flags = MAP_SHARED;
    size_t length = 4096;
    int addr[2] = {0,0};
    mmap_addr_calc(LED_ADDR, PAGE_SIZE, addr);
    printf("addr:%i offset:%i \n", addr[0],addr[1]);
    int* led = static_cast<int*>(mmap(NULL, length, prot, flags, fpga_fd, addr[0]));
    printf("memory mapped the led register\n");
     
    //now like led index are in int size we move in 4 bytes
    printf("Writing to the led: %i \n", atoi(argv[1]));
    led[addr[1]>>2] = atoi(argv[1]);

    //write read from the other registers
    printf("Writing to the input %i \n", (atoi(argv[1])+1));
    led[0] = atoi(argv[1])+1;   //i know before hand that the offset is 0
    sleep(0.1);
    printf("Read value from out: %i \n", led[129]);

    

    munmap(led,length);
    return 0;
}
