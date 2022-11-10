

These codes correspond to the linear algebra needed to calculate the directio of arrival for a 4x4 antenna array using the U-ESPRIT algorithm.

The code is constantly streaming an UDP message that contains the estimated number of sources, the eigenvalues of the eigen decomposition of the correlation matrix calculated in the FPGA and the direction of arrival of the signals.
The SERVER\_PORT, SERVER\_ADDR and CLIENT\_ADDR are hardcoded so be sure that you have the right IP address to receive the data coming from the PowerPC.
We measured the execution time that the PowerPC needs to solve the linear algebra problem and is about ~3ms. So, to avoid sending short messages every 3ms we put several DOA computation in one UDP message. The number of DOA estimations in each packet is hardcoded by the PACKET\_LEN.
Then, the UDP message is composed by several DOA estimation that has the following structure:

1. header (int, 4Bytes)                                  : 0xAABBCCDD (mark the begining of the DoA data, could be read as float to make the parsing easier)
2. n sources (float, 4Bytes)                             : Estimated number of sources
3. correlation matrix eigenvalues (16 floats, 4\*16Bytes): Eigenvalues sorted from smallest to largest.
4. DoA (12 complex floats, 12\*2\*4Bytes)                : Predicted x,y DoA. The even indeces correspond to x and the odd indeces correspond to y. This field sent the 12 posible DoA, but only the first n\_sources are valid.

To simulate the correctness of the code we use the LFSR pseudo-random numbers to fill the correlation matrix in the FPGA for the later process in the PowerPC. In case you want to port this code you just need to modify the addresses of the registers in the lines 45-50 and the functions accumulation\_done, reset\_accumulation, enable\_writing and setup\_system.

An important caveat is that the correlation matrix is saved in the FPGA in colmajor and we only need the upper triangle (the correlation matrix is symmetric).


$$
\begin{pmatrix}
a11 & a12 & a13 & a14\\
a21 & a22 & a23 & a24\\
a31 & a32 & a33 & a34\\
a41 & a42 & a43 & a44\\
\end{pmatrix}
\rightarrow
\left[
a11, a12,a22, a13, a23, a33, a14, a24, a34, a44
\right]
$$

