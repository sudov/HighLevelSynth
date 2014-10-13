#include "typedefs.h"
#include "nearest_neighbor.h"
#include <stdio.h>

#define N 2000

void nearest_neighbor(digit &input, bit4 &nearest) {

  // Include the training data stored in a two-dimensional array
  #include "training_data.h"

  bit6 difference = 0;
  digit max_difference = 2000;

  for (unsigned int data = 0; data < N; data++) { 
    for (int possible_result = 0; possible_result < 10; possible_result++) {
      find_difference(input, training_data[possible_result][data], difference);
      if (difference < max_difference) {
        max_difference = difference;
        nearest = possible_result;
      }
    }
    difference = 0;
  }  
}

void find_difference(digit &input, const digit &data, bit6 &difference) {
  digit diff = input ^ data;
  digit counter = 0;

  for (int i = 0; i < 49; i++) {
    if (diff > 0) {
      diff = diff & (diff - 1);
      counter++;
    }
  }

  difference = counter;
}
