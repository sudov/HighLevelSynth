#include "typedefs.h"
#include "nearest_neighbor.h"
#include <stdio.h>
#include <iostream>
using namespace std;

#define N 2000

void nearest_neighbor(digit &input, bit4 &nearest) {

  // Include the training data stored in a two-dimensional array
  #include "training_data.h"

  bit6 difference = 0;
  // digit max_difference = 2000;
  digit nearest_candidate_list[10];

  for (int j = 0; j < 10; j++) {
    nearest_candidate_list[j] = 49;;
  }

  pipelines: for (unsigned int data = 0; data < N; data++) { 
    #pragma HLS PIPELINE
    unroll_1: for (int possible_result = 0; possible_result < 10; possible_result++) {
      #pragma HLS unroll
      find_difference(input, training_data[possible_result][data], difference);
      // if (difference < max_difference) {
      //   max_difference = difference;
      //   nearest = possible_result;
      // }
      if (difference < nearest_candidate_list[possible_result]) {
        nearest_candidate_list[possible_result] = difference;
      }
    }
    difference = 0;
  } 

  digit nearest_val = nearest_candidate_list[0];
  nearest = 0;
  for (int j = 1; j < 10; j++) {
    if (nearest_candidate_list[j] < nearest_val) {
      nearest_val = nearest_candidate_list[j];
      nearest = j;
    }
  }  
}

void find_difference(digit &input, const digit &data, bit6 &difference) {
  digit diff = input ^ data;
  digit counter = 0;

  unroll_2: for (int i = 0; i < 49; i++) {
    #pragma HLS unroll
    if (diff > 0) {
      diff = diff & (diff - 1);
      counter++;
    }
  }

  difference = counter;
}
