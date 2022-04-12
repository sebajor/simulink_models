# Eigen Test

This model is made to measure the time that takes for the PowerPC to read and solve a eigen problem to check the feasibility of use it.

To solve the eigen problem we use the LAPACK library, for that you need to build the [OpenBlas](https://github.com/xianyi/OpenBLAS) for the PowerPC, for that you need to modify the /kernel/power/KERNEL.PPC440 like [says here](https://github.com/xianyi/OpenBLAS/issues/3603).

