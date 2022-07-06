#include "matrix_utils.cpp"
#include <sys/mman.h>       //for mmap
#include <fcntl.h>          //for the acronyms O_RDRW
#include <time.h>           //to measure time
#include <unistd.h>         //to have the sleep function
#include <stdint.h>         //to have the different types of int

//socket stuffs
//standard symbols
#include <unistd.h>
#include <string.h>
//sockets
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>

/*
 *  Author: Sebastian Jorquera
 *
 */


/*
 * For U-ESPRIT we divided the task in the following structure
 * 1) Check if the FPGA finish the accumulation stage, if ready read the 
 * correlation matrix.
 * 2) Decompose the correlation matrix in eigenvalues and eigenvectors.
 * 3) Predict the number of sources.
 * 4) Solve the DOA.
 * 5) Send the DOA, eigenvalues of step 2
 */

//hyperparameters
#define MATRIX_SIZE     16
#define PAGE_SIZE       4096

//meanwhile we dont have the sources estimation
#define SOURCES         5
#define SOURCE_THRESHOLD 0.1

//roach address (check the core_info.tab)
//this are the addresses of the registers and brams
#define DONE_ADDR       0x01000000
#define DOUT_ADDR       0x01002000
#define EN_ADDR         0x01004000
#define READ_SIZE_ADDR  0x01004100
#define RST_ADDR        0x01004200
#define SEED_ADDR       0x01004300

#define SEED_VALUE      10

//socket hyperparameters
#define SERVER_PORT 4567
#define SERVER_ADDR "192.168.1.18"
#define CLIENT_ADDR "192.168.1.100"
#define BUFF_SIZE 100

#define PACKET_LEN 10  //actually is PKT_LEN*(8*8+12*4+2*4)

int accumulation_done(int* en){
    //return 1 if the accumulation in the FPGA is ready
    return en[1];
}

int reset_accumulation(int* rst){
    //reset the accumulator flag and enables a new accumulation
    rst[128] = 1;
    sleep(0.1);
    rst[128] = 0;
    return 0;
}

int enable_writing(int* reg){
    //enable the writing of the correlation bram
    reg[0] = 1;
    return 0;
}

int setup_system(int* reg){
    //setup the debug LFSR system to emulate a 16x16 correlation calculation
    //this one is valid just for the test system 
    reg[0]  = 0;                            //en
    reg[64] = MATRIX_SIZE*(MATRIX_SIZE+1)/2;//read_size
    reg[128]= 1;                            //rst
    reg[192]= SEED_VALUE;                   //seed
    sleep(1);
    reg[128] = 0;                           //unreset
    return 1;
}

struct Packet{
    int32_t dat=0xAABBCCDD;
    float     d=0;
    float eig[16] =  {0};
    lapack_complex_float doa[12] = {0};
};

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


//doa stuffs
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

int main(int argc, char* argv[] ){
    int fpga_fd = open("/dev/roach/mem", O_RDWR);
    if(fpga_fd == 0){
        printf("Error opening the roach mem file \n");
        return 1;
    }
    //printf("Roach mem file opened\n");

    /*  SOCKET STUFFS
     */
    //socket definitions
    int sockfd;
    struct sockaddr_in serv_addr, client_addr;
    //create socket
    if( (sockfd= socket(AF_INET, SOCK_DGRAM, 0))<0 ){
        printf("socket creation failed :(");
        return 1;
    }
    memset(&serv_addr, 0, sizeof(serv_addr));
    memset(&client_addr, 0, sizeof(client_addr));

    //set the server information
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(SERVER_ADDR);
    serv_addr.sin_port = htons(SERVER_PORT);
    //client info
    client_addr.sin_family = AF_INET;
    client_addr.sin_addr.s_addr = inet_addr(CLIENT_ADDR);
    client_addr.sin_port = htons(SERVER_PORT);

    //bind the socket
    if( bind(sockfd, (const struct sockaddr *)&serv_addr,
                sizeof(serv_addr))<0){
        printf("bind failed");
        return 1;
    }
    int len_addr, n;
    len_addr = sizeof(client_addr);

    //
    struct Packet eth_pack[PACKET_LEN];


    //map the registers and memories in the FPGA
    const int prot = (PROT_READ | PROT_WRITE);
    const int flags = MAP_SHARED;
    const size_t length = 4096;
    int addr[2] = {0,0};

    //mmap the necessary registers and memories
    //modify this with the system address
    //reg:  reset the accumulation
    //done: check if the accumulation is ready
    //bram: memory where the correlation values are stored in a 
    //      packed colmajor way (they are symmetric)
    mmap_addr_calc(EN_ADDR, PAGE_SIZE, addr);
    //printf("en addr: %i offset: %i \n", addr[0], addr[1]); 
    int *reg = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the configuration register\n");

    mmap_addr_calc(DONE_ADDR, PAGE_SIZE, addr);
    int *done = static_cast<int*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the done signal\n");
    
    mmap_addr_calc(DOUT_ADDR, PAGE_SIZE, addr);
    int16_t *bram = static_cast<int16_t*>(mmap(NULL, length, prot,flags, fpga_fd, addr[0]));
    printf("Memory mapped the output bram\n");
    
    //configure the system
    setup_system(reg);
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
    int counter=0;

    enable_writing(reg);
    while(1){
        info = accumulation_done(done);
        printf("%i",info);
        if(info){
            start = clock();
            info  = doa_calculations(matrix_size,&d,bram,eigval,eigvec,Es,mu,nu,
                                    complex_matrix, doa);
            if(info){
                printf("LA failed \n");
                reset_accumulation(reg);
                continue;
            }
            reset_accumulation(reg);
            memcpy(eth_pack[counter].eig, eigval, sizeof(eigval));
            memcpy(eth_pack[counter].doa, doa, sizeof(doa));
            eth_pack[counter].d = (float)d;
            //send data
            counter ++;
            if(counter==PACKET_LEN){
                sendto(sockfd, (char*)&eth_pack, sizeof(eth_pack), MSG_CONFIRM,
                    (const struct sockaddr *)&client_addr, len_addr);  
                counter=0;
            }
            end = clock();
            print_complex_matrix(doa, 1,d);  
            cpu_time = 1000*((double)(end-start))/CLOCKS_PER_SEC;
            printf("iter took %.3f ms\n", cpu_time);
        }
    }  
    munmap(reg, length);
    munmap(bram, length);
    munmap(done, length);
    return 0;
}


