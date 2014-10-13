#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>

#include "typedefs.h"
#include "nearest_neighbor.h"
#include "ap_int.h"

using namespace std; 

int main() 
{
  // Set up output file to save test bench results
  ofstream outfile;
  outfile.open("out.dat");

  // Read input file for the testing set
  string line;
  ifstream myfile ("testing_set.dat");
  
  if (myfile.is_open())
  {
    int error = 0;
    int num_test_instances = 0;
    
    while (getline(myfile,line))
    {
      // Read handwritten digit input and expected digit    
      digit input_digit = strtoul(line.substr(0, line.find(",")).c_str(), NULL, 16);
      int input_value = strtoul(line.substr(line.find(",")+1,line.length()).c_str(), NULL, 10);
 
      // DUT
      bit4 interpreted_digit = 10;
      nearest_neighbor(input_digit, interpreted_digit);
  
      // Print result messages to console
      num_test_instances++;
      cout << "#" << std::dec << num_test_instances;
      cout << ": \tTestInstance=" << std::hex << input_digit;
      cout << " \tInterpreted=" <<  interpreted_digit << " \tExpected=" << input_value;
      // Print result messages to file
      outfile << "#" << std::dec << num_test_instances;
      outfile << ": \tTestInstance=" << std::hex << input_digit;
      outfile << " \tInterpreted=" <<  interpreted_digit << " \tExpected=" << input_value;
   
     // Check for any difference between k-NN interpreted digit vs. expected digit
     if (interpreted_digit != input_value){
       error++;
       cout << " \t[Mismatch!]";
       outfile << " \t[Mismatch!]";
      }

      cout << endl;
      outfile << endl;

    }   

    // Report overall error out of all testing instances
    cout << "Overall Error = " << double(error)/double(num_test_instances)*100 << "%" << endl;

    // Close input file for the testing set
    myfile.close();
  }
  else cout << "Unable to open file for the testing set!" << endl; 

  // Close output file
  outfile.close();

}
