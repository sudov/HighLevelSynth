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
    ap_fixed<32,2> X			= K_CONST;
    ap_fixed<32,2> Y 			= 0;
    ap_fixed<32,2> T 			= 0;
    ap_fixed<32,2> current		= 0;

    for (int step = 0; step < NUM_ITERATIONS; step++) {
    	if (theta > current) {
    		T 	      = X - (Y >> step);
    		Y 	      = (X >> step) + Y;
    		X 	      = T;
    		current  += cordic_ctab[step];
    	} else {
    		T 	      = X + (Y >> step);
    		Y 		  = -(X >> step) + Y;
    		X		  = T;
    		current  -= cordic_ctab[step];
    	}
    }
    c = X;
    s = Y;
}
