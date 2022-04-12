#include <stdio.h>          //to print stuffs
#include <sys/mman.h>       //for mmap
#include <fcntl.h>          //for the acronyms O_RDRW
#include <lapacke.h>        //for the linalg
#include <time.h>           //to measure time
#include <unistd.h>         //to have the sleep function
#include <stdint.h>        //to have the different types of int


int n = 16;

//registers starting address, all have size 0xFF
int done_addr        = 0x01000000;
int en_addr          = 0x01004000;
int read_size_addr   = 0x01004100;
int rst_addr         = 0x01004200;
int seed_addr        = 0x01004300;

//bram
int bram_start  = 0x01002000;
int bram_size   = 0x4000;


int main(int argc, char *argv[]){
    if(argc<2){
        printf("you have to enter the number of iterations \n");
        return 1;
    }

    //get the mmap file 
    int fpga_fd = open("/dev/roach/mem/",O_RDWR);
    if(fpga_fd == 0){
        printf("Error: cant open mem file \n");
        return 1;
    }
    
    int prot = (PROT_READ | PROT_WRITE);
    int flags = MAP_SHARED;
    
    int8_t* done = static_cast<int8_t*>(mmap(NULL, 0xFF, prot, flags, fpga_fd, done_addr));
    int8_t* en = static_cast<int8_t*>(mmap(NULL, 0xFF, prot, flags, fpga_fd, en_addr));
    int8_t* read_size = static_cast<int8_t*>(mmap(NULL, 0xFF, prot, flags, fpga_fd, read_size_addr));
    int8_t* rst = static_cast<int8_t*>(mmap(NULL, 0xFF, prot, flags, fpga_fd, rst_addr));
    int8_t* seed = static_cast<int8_t*>(mmap(NULL, 0xFF, prot, flags, fpga_fd, seed_addr));
    int16_t* bram_data = static_cast<int16_t*>(mmap(NULL, bram_size, prot, flags, fpga_fd, seed_addr));
    
    //configure the test
    *seed = 10;             //write the seed
    munmap(seed, 0xFF);
    *read_size = n*(n+1)/2;
    munmap(read_size, 0xFF);

    //reset
    *rst = 1;
    sleep(0.1);
    *rst = 0;

    //
    int iters = atoi(argv[1]);
    int count =0;
    
    //variables for the eigen problem
    int ldz = 2;
    float* data = new float[n*(n+1)/2];
    float* w = new float[n];
    float* z = new float[ldz*n];
    char jobz = 'V', uplo='U';
    //vars to measure the time
    clock_t start, end;
    float cpu_time;

    *en = 1;
    while(count < iters){
        if(*done){
            start = clock();
            //cast the bram data to float
            for(int i=0; i<(n*(n+1)/2); i++){
                *(data+i) = (float)(*bram_data+i);
            }
            int info = LAPACKE_sspev(LAPACK_COL_MAJOR, jobz, uplo, n,
                                     data, w, z, ldz); 
            end = clock();
            cpu_time = ((double)(end-start))/CLOCKS_PER_SEC;
            printf("iter took %.3f secs", cpu_time);
            *rst = 1;
            sleep(0.1);
            *rst = 0;
        }
    }
    return 1;
}
