TOP ?= uesprit_la
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
