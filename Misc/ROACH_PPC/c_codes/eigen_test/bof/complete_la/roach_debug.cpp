#include "matrix_utils.cpp"
#include <sys/mman.h>       //for mmap
#include <fcntl.h>          //for the acronyms O_RDRW
#include <time.h>           //to measure time
#include <unistd.h>         //to have the sleep function
#include <stdint.h>         //to have the different types of int

/*
 * For U-ESPRIT we divided the task in the following structure
 * 1) Check if the FPGA finish the accumulation stage, if ready read the 
 * correlation matrix.
 * 2) Decompose the correlation matrix in eigenvalues and eigenvectors.
 * 3) Predict the number of sources.
 * 4) Solve the DOA.
 */

//like we dont have the source stimation yet I hardcoded the number of source :P
#define SOURCES 5
#define SOURCE_THRESHOLD 0.1

//definitions of roach addresses
#define MATRIX_SIZE     16
#define PAGE_SIZE       4096

#define DONE_ADDR       0x01000000
#define DOUT_ADDR       0x01002000
#define EN_ADDR         0x01004000
#define READ_SIZE_ADDR  0x01004100
#define RST_ADDR        0x01004200
#define SEED_ADDR       0x01004300

#define SEED_VALUE      10

void mmap_addr_calc(int addr, int page_size, int* out){
    /* Calculate the address to match the pages of the pc memory
     * addr: addr that we want to mmap
     * page_size: kernel page size
     * out: array, 0: base address, 1: offset
     */
    int base_addr = (addr/page_size)*page_size;
    int offset = addr%page_size;
    out[0] = base_addr;
    out[1] = offset;
}

int estimate_source(float* eigval, int matrix_size, int threshold){
    //TODO
    return SOURCES;
}

int doa_calculations(int matrix_size, int* d, int16_t* bram, float* eigval, float* eigvec,
        float* Es, float* mu, float* nu, lapack_complex_float* complex_matrix,
        lapack_complex_float* doa
        ){
        int info;
        //read the bram and calculate the eigenvalues
        info = eigen_solver_diag(bram, eigval, eigvec, matrix_size);
        if(info)
            return info;
        //estimate the number of signals
        *d = estimate_source(eigval, matrix_size, SOURCE_THRESHOLD);
        printf("%i \n\n\n", *d);
        select_columns(eigvec, Es, *d);
        //calculate the mu and nu equations for Phi
        info = mu_calc(Es,*d,mu);
        if(info)
            return info;
        info = nu_calc(Es,*d,nu);
        if(info)
            return info;
        //calculate the eigenvalues of the complex matrix Phi_mu+1j*Phi_nu
        real2complex(mu,nu,*d,complex_matrix);
        info = complex_eigproblem(complex_matrix,*d,doa);
        if(info)
            return info;
}

int main(int argc, char* argv[]){
    if(argc < 2){
        printf("You have to enter the number of iterations \n");
    }


    int fpga_fd = open("/dev/roach/mem", O_RDWR);
    if(fpga_fd == 0){
        printf("Error opening the roach mem file \n");
        return 1;
    }
    printf("Roach mem file opened\n");


    //map the registers and memories in the FPGA
    const int prot = (PROT_READ | PROT_WRITE);
    const int flags = MAP_SHARED;
    const size_t length = 4096;
    int addr[2] = {0,0};


    mmap_addr_calc(EN_ADDR, PAGE_SIZE, addr);
    printf("en addr: %i offset: %i \n", addr[0], addr[1]); 
    int *reg = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the configuration register\n");

    printf("configuration done!\n");  
    mmap_addr_calc(DONE_ADDR, PAGE_SIZE, addr);
    int *done = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the done signal\n");
    
    mmap_addr_calc(DOUT_ADDR, PAGE_SIZE, addr);
    int16_t *bram = static_cast<int16_t*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the output bram\n");

    //setup roach
    //now like the index measure 4byte words we jump the right amount
    reg[0]  = 0;                            //en
    reg[64] = MATRIX_SIZE*(MATRIX_SIZE+1)/2;//read_size
    reg[128]= 1;                            //rst
    reg[192]= SEED_VALUE;                   //seed
    sleep(1);
    reg[128] = 0;                           //unreset

    printf("roach configuration done\n");
    
    //variable definitions for doa
    float eigval[MATRIX_SIZE];
    float eigvec[MATRIX_SIZE*MATRIX_SIZE];
    int info, d;   //number of sources
    int const matrix_size= MATRIX_SIZE;
    float Es[MATRIX_SIZE*12];
    float mu[12*12], nu[12*12];
    lapack_complex_float complex_matrix[12*12];
    lapack_complex_float doa[12];
    
    //timing variables
    clock_t start, end;
    float cpu_time;
    int count=0;

    //file to store the time 
    FILE *fptr;
    fptr = fopen("out_file.txt", "w");

    reg[0] = 1; //enable
    //main loop
    while(count< atoi(argv[1])){
        //check status of the done flag
        printf("waiting\n");
        printf("done: %i", done[1]);
        if(done[1]){
            start = clock();
            info  = doa_calculations(matrix_size,&d,bram,eigval,eigvec,Es,mu,nu,
                                    complex_matrix, doa);
            printf("info: %i\n", info);
            if(info!=0){
                printf("LA failed!! \n");
                reg[128] = 1;
                sleep(1);
                reg[128] = 0;
                continue;
            }
            end = clock();
            cpu_time = 1000*((double)(end-start))/CLOCKS_PER_SEC;
            printf("iter took %.3f ms\n", cpu_time);
            count ++; 
            reg[128] = 1;
            sleep(1);
            reg[128] = 0;
            print_complex_matrix(doa, 1,d);
            //print_matrix(Es,d,16);
            //print_matrix(eigvec, 16,16);
            //print_matrix(eigval, 1,16);
            printf("\n\n");
            fprintf(fptr, "%f; \n", cpu_time);
        }
    }
    fclose(fptr);
    munmap(reg, length);
    munmap(bram, length);
    munmap(done, length);
    return 0;
}
