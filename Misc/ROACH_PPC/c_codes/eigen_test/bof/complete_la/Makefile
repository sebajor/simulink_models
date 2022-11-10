<<<<<<< HEAD
TOP ?= roach_debug
=======
TOP ?= uesprit_la
>>>>>>> dadcb696233e71373f0ac23593fbb9047fb1ff27
CXX = powerpc-linux-gnu-g++
USR_INC = ?
USR_LIB = ?
BLAS_INC = $(HOME)/Documents/trabajo_dirigido/blas_stuffs/OpenBlasPPC/include
BLAS_LIB = $(HOME)/Documents/trabajo_dirigido/blas_stuffs/OpenBlasPPC/lib
LDLIBS = -lopenblas -lgfortran

CXX_FLAGS = -O2 -fopenmp -static

all:
	$(CXX) $(TOP).cpp -o $(TOP) $(CXX_FLAGS) -I $(BLAS_INC) \
		-L $(BLAS_LIB) $(LDLIBS)
clean:
	@rm -r $(TOP)
