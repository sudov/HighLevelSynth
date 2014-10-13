#ifndef NEAREST_NEIGHBOR_H
#define NEAREST_NEIGHBOR_H

#include "typedefs.h"

// Find the difference between input and data, put the output in difference
//   input is a 49-bit value
//   data is a 49-bit value
//   difference is the number of bits that are different between input and data
void find_difference(digit &input, const digit &data, bit6 &difference);

// Counts the number of bits in count_this that is 1
void count_set_bits(digit count_this, bit6 &difference);

// Finds the nearest neighbor to the digit input
// Sets nearest to the digit that is the algorithm's best guess
void nearest_neighbor(digit &input, bit4 &nearest);

#endif
