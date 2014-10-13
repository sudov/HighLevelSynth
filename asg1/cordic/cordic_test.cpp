/*
A testbench for sine and cosine using CORDIC.
1. It generates angles between 1 and NUM_DEGREE and provides those to the cordic function.
2. It compares the result to corresponding sin/cos result computed from the same functions in math.h.
3. It computes the error of the cordic sin/cos result vs. the math.h results. 
4. The values and errors are logged in the file out.dat for debugging purposes.
5. The cumulative errors are printed.

VARIABLES:
    double theta: input angle value
    double &s: output sin value
    double &c: output cos value
*/

#include <math.h>
#include "cordic.h"
#include <stdio.h>
#include <stdlib.h>

double abs_double(double var)
{
    if (var < 0) 
        return -var;
    return var;
}

int main(int argc, char **argv)
{   
    FILE *fp;

    cos_sin_type s = 0; //sin output
    cos_sin_type c = 0; //cos output
    theta_type radian; //radian input

    double zs, zc; // sin and cos values calculated from math.h.

    //Error checking
    double Total_Error_Sin = 0.0;
    double Total_Error_Cos = 0.0;
    double error_sin = 0.0, error_cos = 0.0;

    fp = fopen("out.dat","w");
    // Compute sin/cos values for angles up to NUM_DEGREE
    for (int i = 1; i < NUM_DEGREE; i++) {
        radian = i*M_PI/180;
        cordic(radian, s, c);
        zs = sin((double)radian);
        zc = cos((double)radian);
        error_sin = (abs_double((double)s-zs)/zs)*100.0;
        error_cos = (abs_double((double)c-zc)/zc)*100.0;
        Total_Error_Sin = Total_Error_Sin + error_sin*error_sin;
        Total_Error_Cos = Total_Error_Cos + error_cos*error_cos;

 
        fprintf(fp, "degree=%d, radian=%f, cos=%f:%f, sin=%f:%f, cos_error=%f\%, sin_error=%f\%\n", i, (double)radian, (double)c, zc, (double)s, zs, error_cos, error_sin);
    }

    fclose(fp);
    // Print out root mean square error (RMSE) in percentage
    printf ("Overall_Error_Sin=%f\%, Overall_Error_Cos=%f\%\n", sqrt(Total_Error_Sin/(NUM_DEGREE-1)), sqrt(Total_Error_Cos/(NUM_DEGREE-1)));
    return 0;
}
