# Extract Vivado HLS include path
VHLS_PATH := $(dir $(shell which vivado_hls))/..
VHLS_INC ?= ${VHLS_PATH}/include

all: nearest_neighbor.cpp testbench.cpp
	g++ -I${VHLS_INC} nearest_neighbor.cpp testbench.cpp -o digitrec
clean:
	rm -f digitrec vivado_hls.log
