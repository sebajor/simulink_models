#include <stdio.h>          //to print stuffs
#include <sys/mman.h>       //for mmap
#include <fcntl.h>          //for the acronyms O_RDRW
#include <lapacke.h>        //for the linalg
#include <time.h>           //to measure time
#include <unistd.h>         //to have the sleep function
#include <stdint.h>        //to have the different types of int

/*  Author: Sebastian Jorquera
 *  Code to measure the time that takes to the powerpc to read a bram from
 *  the FPGA take the data and solve an eigen problem for a symmetrical 
 *  matrix
 */

#define MATRIX_SIZE     16
#define DONE_ADDR       0x01000000
#define DOUT_ADDR       0x01002000
#define EN_ADDR         0x01004000
#define READ_SIZE_ADDR  0x01004100
#define RST_ADDR        0x01004200
#define SEED_ADDR       0x01004300

#define SEED_VALUE      10
#define PAGE_SIZE       4096

void mmap_addr_calc(int addr, int page_size, int* out){
    int base_addr = (addr/page_size)*page_size;
    int offset = addr%page_size;
    out[0] = base_addr;
    out[1] = offset;
}

void eigen_solver(int* bram, float* w, float* z){
    int ldz = MATRIX_SIZE;
    float* data = new float[MATRIX_SIZE*(MATRIX_SIZE+1)/2];
    char jobz = 'V', uplo='U';

    //cast the bram data to float
    for(int i=0; i<(MATRIX_SIZE*(MATRIX_SIZE+1)/2); i++){
        *(data+i) = (float)(*bram+i);
    }
    int info = LAPACKE_sspev(LAPACK_COL_MAJOR, jobz, uplo, MATRIX_SIZE,
                             data, w, z, MATRIX_SIZE); 
    
}

void print_eigen_solution(float* w, float* z){
    printf("Eigenvalues\n");
    for(int i=0; i<MATRIX_SIZE; i++){
        printf("%.4f \n", w[i]);
    }
    printf("Eigen vectors\n");
    for(int i=0; i<MATRIX_SIZE; i++){
        for(int j=0; i<MATRIX_SIZE; j++){
            printf("%.4f ", z[i*MATRIX_SIZE+j]);
        }
        printf("\n");
    }
}

int main(int argc, char* argv[]){
    if(argc < 2){
        printf("You have to enter the number of iterations");
    }
    int fpga_fd = open("/dev/roach/mem", O_RDWR);
    if(fpga_fd == 0){
        printf("Error opening the roach mem file \n");
        return 1;
    }
    printf("roach mem file opened \n");
    //configure the system
    int prot = (PROT_READ | PROT_WRITE);
    int flags = MAP_SHARED;
    size_t length = 4096;
    int addr[2] = {0,0};
    mmap_addr_calc(EN_ADDR, PAGE_SIZE, addr);
    printf("en addr: %i offset: %i", addr[0], addr[1]); 
    int *reg = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the configuration register");

    //now like the index measure 4byte words we jump the right amount
    reg[0]  = 0;                            //en
    reg[64] = MATRIX_SIZE*(MATRIX_SIZE+1)/2;//read_size
    reg[128]= 1;                            //rst
    reg[192]= SEED_VALUE;                   //seed
    sleep(1);
    reg[128] = 0;                           //unreset

    printf("configuration done!");  
    mmap_addr_calc(DONE_ADDR, PAGE_SIZE, addr);
    int *done = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the done signal");

    mmap_addr_calc(DOUT_ADDR, PAGE_SIZE, addr);
    int *bram = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the output bram");
   
    //paramters for the eigen problem
    float* w = new float[MATRIX_SIZE];
    float* z = new float[MATRIX_SIZE*MATRIX_SIZE];
     
    //vars to measure the time
    clock_t start, end;
    float cpu_time=0;
    int count =0;
    reg[0] = 1;
    while(count < atoi(argv[1])){
        if(done[0] == 1){
            start = clock();
            eigen_solver(bram,w,z);
            end = clock();
            cpu_time = ((double)(end-start))/CLOCKS_PER_SEC;
            printf("iter took %.3f secs\n", cpu_time);
            count ++;
            reg[128] = 1;                           //rst
            sleep(1);
            reg[128] = 0;                           //unreset
            //print the solution of the problem to avoid optimization
            print_eigen_solution(w,z);
        }
    }
    return 1;
}

