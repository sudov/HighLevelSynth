/*
A CORDIC implementation of sine and cosine.

INPUT:
    double theta: Input angle 
    
OUTPUT:
    double &s: Sin output
    double &c: Cos output
*/
 
#include "cordic.h"
#include "ap_fixed.h"
#define K_CONST 0.60725293510314
#define NUM_ITERATIONS 20

void cordic(theta_type theta, cos_sin_type &s, cos_sin_type &c)
{
    double X			= K_CONST;
    double Y 			= 0;
    double T 			= 0;
    double current		= 0;
    
    // Used this to measure bits taken up by double data type
    // std::cout << sizeof(double) << std::endl; 

    for (int step = 0; step < NUM_ITERATIONS; step++) {
    	if (theta > current) {
    		T 	      = X - (Y/(double)(1ULL<<step));
    		Y 	      = (X/(double)(1ULL<<step)) + Y;
    		X 	      = T;
    		current  += cordic_ctab[step];
    	} else {
    		T 	      = X + (Y/(double)(1ULL<<step));
    		Y 		  = -(X/(double)(1ULL<<step)) + Y;
    		X		  = T;
    		current  -= cordic_ctab[step];
    	}
    }
    c = X;
    s = Y;
}
