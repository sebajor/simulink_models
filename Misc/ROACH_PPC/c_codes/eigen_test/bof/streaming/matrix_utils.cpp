#ifndef _LAPACK_
    #include <complex.h>
    #define lapack_complex_float std::complex<float>
    #include <lapacke.h>
    #include <cblas.h>
    #define _LAPACK_
#endif
#include <stdio.h>

/*
 *  Author: Sebastian Jorquera
 */

//matrix definitions
static float Kmu1[12*16] = {
    0.5       , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.70710678, 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5       , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5       , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.70710678,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.70710678, 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.5       , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.5       , 0.70710678, 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5
};

static float Kmu2[12*16] = {
        0.        ,  0.        ,  0.5       ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        , -0.5       ,
        0.        ,  0.        , -0.        ,  0.        ,  0.        ,
       -0.        ,  0.        ,  0.        , -0.        , -0.5       ,
        0.        ,  0.        , -0.        ,  0.        ,  0.        ,
       -0.        ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        ,  0.5       , -0.70710678,  0.        ,  0.        ,
       -0.        ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.5       ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        , -0.        ,  0.        ,  0.        ,
       -0.5       ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.        , -0.        ,  0.        ,  0.        ,
       -0.5       ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.        ,  0.        ,
       -0.        ,  0.        ,  0.5       , -0.70710678,  0.        ,
        0.        , -0.        ,  0.        ,  0.        , -0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.5       ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
       -0.        ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.5       ,  0.        ,  0.        , -0.        ,
       -0.        ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.5       ,  0.        ,  0.        , -0.        ,
        0.        ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.5       , -0.70710678,
        0.        ,  0.        , -0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.5       ,  0.        ,  0.        , -0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.        , -0.        ,
        0.        ,  0.        , -0.5       , -0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.        , -0.        ,
        0.        ,  0.        , -0.5       ,  0.        ,  0.        ,
        0.        , -0.        ,  0.        ,  0.        , -0.        ,
        0.        ,  0.        , -0.        ,  0.        ,  0.5       ,
       -0.70710678,  0.
};

static float Knu1[12*16] = {
       0.5       , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5       , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.70710678, 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5       , 0.        , 0.        , 0.        ,
       0.70710678, 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.        , 0.        , 0.        , 0.70710678, 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.        , 0.        ,
       0.        , 0.70710678, 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.5       ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.5       , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.5       , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.5       , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.5       , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.5
};

static float Knu2[12*16] = {
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.5       ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.5       ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.5       ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.5       ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        , -0.5       , -0.        , -0.        , -0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        , -0.        , -0.5       ,
       -0.        , -0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
       -0.        , -0.        , -0.5       , -0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        , -0.        , -0.        , -0.        ,
       -0.5       , -0.5       , -0.        , -0.        , -0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        , -0.        , -0.5       ,
       -0.        , -0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
       -0.        , -0.        , -0.5       , -0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        , -0.        , -0.        , -0.        ,
       -0.5       ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.5       ,
        0.        ,  0.        ,  0.        , -0.70710678, -0.        ,
       -0.        , -0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.5       ,  0.        ,  0.        ,
       -0.        , -0.70710678, -0.        , -0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.5       ,  0.        , -0.        , -0.        , -0.70710678,
       -0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
        0.        ,  0.        ,  0.        ,  0.5       , -0.        ,
       -0.        , -0.        , -0.70710678,  0.        ,  0.        ,
        0.        ,  0.
};

void print_matrix(float* matrix, int m, int n){
    for(int i=0; i<m; i++){
        for(int j=0; j<n; j++){
            printf("%.4f ",matrix[i*n+j]);  //not sure if its i*m or i*n
        }
        printf("\n");
    }
}

void print_eigenvalues(float* eig_real, float* eig_imag, int n){
    for(int i=0; i<n; i++){
        printf("%.4f+(%.4f )j \n",eig_real[i], eig_imag[i]);
    }
}

void print_complex_matrix(lapack_complex_float* matrix, int n, int m){
    for(int i=0; i<m; i++){
        for(int j=0; j<n; j++){
            printf("%.4f +(%.4f)j ", (matrix[i*n+j]).real(), (matrix[i*n+j]).imag());
        }
        printf("\n");
    }
}

/*
 * documentation: http://www.netlib.org/lapack/explore-html/d4/dca/group__real_g_esing_gaf03d06284b1bfabd3d6c0f6955960533.html
 *example https://www.intel.com/content/www/us/en/develop/documentation/onemkl-lapack-examples/top/least-squares-and-eigenvalue-problems/singular-value-decomposition/gesvd-function/sgesvd-example/lapacke-sgesvd-example-c-column.html
 */

//caution!: the matrix is stored columnwise!

int eigen_solver_diag(int16_t* in_mat, float* eigval, float* eigvec, int matrix_size){
    /*  in_mat: array with the up triagle of a symmetric matrix of size MATRIX_SIZE
     *  ordered in a col major way
     *  eigval: eigen values (array of MATRIX_SIZE)
     *  eigvec: eigen vector (array of MATRIX_SIZExMATRIX_SIZE)
     *  MATRIX_SIZE: dim of the square matrix
     */
    int ldz = matrix_size;
    float* data = new float[matrix_size*(matrix_size+1)/2];
    char jobz = 'V', uplo='U';
    float aux =0;
    //cast the bram data to float
    for(int i=0; i<(matrix_size*(matrix_size+1)/2); i++){
        aux =  ((float)(in_mat[i]));
        data[i] = aux/32768.;
    }
    int info = LAPACKE_sspev(LAPACK_COL_MAJOR, jobz, uplo, matrix_size,
                             data, eigval, eigvec, matrix_size);
    return info;
}

void select_columns(float* eigvec, float* Es, int d){
    /*  eigvec: matrix 16x16 col major
     *  Es: matrix of dx16 (?)
     *  d:  number of selected columns
     */
    int n=0;
    for(int i=15; i>d; i--){
        for(int j=0; j<16; j++){
            Es[n*16+j] = eigvec[16*i+j];
        }
        n++;
    }
}

int svd(float* mat,int m, int n, float* s, float* u, float* vt){ 
    float info;
    float work[n-1];
    LAPACKE_sgesvd(LAPACK_COL_MAJOR,'A','A',m,n, mat,m,s,u,m,vt,n,work);
    if(info!=0){
        return info;
    }
    return 0;
}

/*  To calculate the pseudo inverse we first calculate the sdv decomposition
 *  A = U*S*V^T, then we use that the A'=V*S^-1*U^T. Where S is diagonal, so
 *  S^-1 are the inverse of the diagonal elements.
 */

int pinv(float* mat, int n, int m, float* out){
    // here mat is a NxM matrix and out is also an NxM matrix
    //
    float s[n], u[m*m], vt[n*n]; 
    int info = svd(mat,m, n, s, u, vt);
    if(info!=0){
        printf("error: %i", info);
        return 1;
    }
    
    //calculate the inverse of s (its not a matrix, just a vector)
    /*doc: http://www.netlib.org/lapack/explore-html/df/d28/group__single__blas__level1_ga3252f1f70b29d59941e9bc65a6aefc0a.html
     */
    for(int i=0; i<n;i++){
       s[i] = 1./s[i];
    }

    //compute s*u^T
    //check because u is MxM and S has N elements
    /*doc: http://www.netlib.org/lapack/explore-html/df/d28/group__single__blas__level1_ga3252f1f70b29d59941e9bc65a6aefc0a.html
     */
    for(int i=0; i<n;i++){
        cblas_sscal(m, s[i], &u[i*m],1);
    }
    
    //compute the second multiplication
    //A'=v*s*u^T
    
    /*doc: http://www.netlib.org/lapack/explore-html/db/dc9/group__single__blas__level3_gafe51bacb54592ff5de056acabd83c260.html
     * sgemm computes C=alpha*op(A)*op(B)+beta*C
     * with A mxk, B is kxn
     */
    cblas_sgemm(CblasColMajor, CblasTrans,CblasTrans, n,m,n,1,vt,n,u,m, 0, out,n);
    return 0;
}

int mu_calc(float* Es, int d, float* out){
    // Es: d columns of svd of the correlation matrix
    // d: number of signals
    // out1: output matrix of dxd 
    
    /*  We want to solve K1*Es*Phi = K2*Es
     *  Then we define A = K1*Es, b=K2*Es 
     *  
     *  Kmu = 12x16; Es=16xd; a=12xd
     */
    float a[12*d], b[12*d]; 
    cblas_sgemm(CblasColMajor, CblasNoTrans,CblasNoTrans,12,d,16,1,Kmu1,12,Es,16,
                0,a,12);
    cblas_sgemm(CblasColMajor, CblasNoTrans,CblasNoTrans,12,d,16,1,Kmu2,12,Es,16,
                0,b,12);
    
    float a_inv[12*d];
    int info = pinv(a, d, 12,a_inv);
    if(info){
        printf("Error inverting");
        return info;
    }

    cblas_sgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, d,d,12,1,a_inv,d, b,12,
            0,out,d);
    return 0;
}

int nu_calc(float* Es, int d, float* out){
    // Es: d columns of svd of the correlation matrix
    // d: number of signals
    // out1: output matrix of dxd 
    
    float a[12*d], b[12*d]; 
    cblas_sgemm(CblasColMajor, CblasNoTrans,CblasNoTrans,12,d,16,1,Knu1,12,Es,16,
                0,a,12);
    cblas_sgemm(CblasColMajor, CblasNoTrans,CblasNoTrans,12,d,16,1,Knu2,12,Es,16,
                0,b,12);
    
    float a_inv[12*d];
    int info = pinv(a, d, 12,a_inv);
    if(info){
        printf("Error inverting");
        return info;
    }

    cblas_sgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, d,d,12,1,a_inv,d, b,12,
            0,out,d);
    return 0;
}

void real2complex(float* real, float* imag, int d, lapack_complex_float* complex_matrix){
    /*  real: matrix of dxd
     *  imag: matrix of dxd
     *  d:    dim
     *  complex_matrix: complex mat of dxd
     */
    lapack_complex_float tmp;
    for(int i=0; i<d; i++){
        for(int j=0; j<d; j++){
            tmp = {real[i*d+j], imag[i*d+j]};
            complex_matrix[i*d+j] = tmp;
        }
    }
}

int complex_eigproblem(lapack_complex_float* complex_matrix, int d,
                        lapack_complex_float* eigval){
    /*  Calculate the eigenvalues of a complex matrix
     *  complex_matrix: complex matrix of dxd
     *  d:  dim
     *  eigval: complex array of dim d;
     */
    lapack_complex_float* vl;
    lapack_complex_float* vr;
    int info = LAPACKE_cgeev(LAPACK_COL_MAJOR,'N','N',d,complex_matrix,d,eigval,vl,1,vr,1);
    return info;
}
