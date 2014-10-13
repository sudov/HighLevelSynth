#ifndef CORDIC_H
#define CORDIC_H
#undef BIT_ACCURATE // To ensure that this bit doesn't get set by run.tcl or make
#ifdef BIT_ACCURATE
#include "ap_fixed.h"
#include "ap_int.h"
// Change the following types to ap_int OR ap_fixed for optimized implementations.
typedef ap_fixed<32,2> theta_type;
typedef ap_fixed<32,2> cos_sin_type;
typedef ap_fixed<32,2> val1_t;

#else
typedef double theta_type;
typedef double cos_sin_type;

#endif

// Specify 90 degree as the maximum angle for sin/cos computation.
const int NUM_DEGREE=90;

#define K_CONST 0.60725293510314
// Table of arctangents of negative powers of two, in radians
// angles in radians = atan(2.^-[0:27]);
const theta_type cordic_ctab[64]={0.78539816339744828000,0.46364760900080609000,0.24497866312686414000,0.12435499454676144000,0.06241880999595735000,0.03123983343026827700,0.01562372862047683100,0.00781234106010111110,0.00390623013196697180,0.00195312251647881880,0.00097656218955931946,0.00048828121119489829,0.00024414062014936177,0.00012207031189367021,0.00006103515617420877,0.00003051757811552610,0.00001525878906131576,0.00000762939453110197,0.00000381469726560650,0.00000190734863281019,0.00000095367431640596,0.00000047683715820309,0.00000023841857910156,0.00000011920928955078,0.00000005960464477539,0.00000002980232238770,0.00000001490116119385,0.00000000745058059692,0.00000000372529029846,0.00000000186264514923,0.00000000093132257462,0.00000000046566128731,0.00000000023283064365,0.00000000011641532183,0.00000000005820766091,0.00000000002910383046,0.00000000001455191523,0.00000000000727595761,0.00000000000363797881,0.00000000000181898940,0.00000000000090949470,0.00000000000045474735,0.00000000000022737368,0.00000000000011368684,0.00000000000005684342,0.00000000000002842171,0.00000000000001421085,0.00000000000000710543,0.00000000000000355271,0.00000000000000177636,0.00000000000000088818,0.00000000000000044409,0.00000000000000022204,0.00000000000000011102,0.00000000000000005551,0.00000000000000002776,0.00000000000000001388,0.00000000000000000694,0.00000000000000000347,0.00000000000000000173,0.00000000000000000087,0.00000000000000000043,0.00000000000000000022,0.00000000000000000011};
void cordic(theta_type theta, cos_sin_type &s, cos_sin_type &c);

#endif
