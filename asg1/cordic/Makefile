# Extract Vivado HLS include path
VHLS_PATH := $(dir $(shell which vivado_hls))/..
VHLS_INC ?= ${VHLS_PATH}/include

all: cordic_fixed

cordic_fixed: cordic.h cordic.cpp cordic_test.cpp
	g++ -I${VHLS_INC} cordic.cpp cordic_test.cpp -o cordic

clean:
	rm -f cordic out.dat
