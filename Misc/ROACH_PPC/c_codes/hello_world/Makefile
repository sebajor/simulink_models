TOP = hello_world
CXX = powerpc-linux-gnu-g++
C = powerpc-linux-gnu-gcc

all:
	$(CXX) -static $(TOP).cpp -o $(TOP) 

C:
	$(C) -static $(TOP).c -o $(TOP)_c

clean:
	@rm -r $(TOP) $(TOP)_c

	
