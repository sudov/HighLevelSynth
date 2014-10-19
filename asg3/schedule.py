#!/usr/bin/env python

# Tests accessing of instruction operands.
import sys
import os
import llvm 
# top-level, for common stuff
from llvm.core import *

# Get the name of an LLVM value
def get_name(val) :
    if (not isinstance(val, Value)):
        return ''
    if isinstance(val, Argument):
        #return val.name + " [in]" 
        return val.name
    if isinstance(val, GlobalVariable):
        #return val.name + " [out]" 
        return val.name 
    if isinstance(val, Instruction):
        if val.opcode_name == 'store':
           return "[store]" 
    if isinstance(val, ConstantInt):
        return str(val.z_ext_value)
    return val.name

# Convenience functions

# Is the value a store?
def is_store(val) :
    if not isinstance(val, Instruction):
        return 0
    return val.opcode_name == 'store'

# Is the value a return?
def is_return(val) :
    if not isinstance(val, Instruction):
        return 0 
    return val.opcode_name == 'ret'

# Is the value a multiplication?
def is_mul(val) :
    if not isinstance(val, Instruction):
        return 0
    if not val.is_binary_op:
        return 0
    return val.opcode_name == 'mul'

# Is the value an addition or a subtraction?
def is_addsub(val) :
    if not isinstance(val, Instruction):
        return 0
    if not val.is_binary_op:
        return 0
    opc = val.opcode_name 
    return opc == 'add' or opc == 'sub' 

# Get the pretty string in C-like syntax of an LLVM value
def to_string(val) :
    # Is an Instruction?
    if isinstance(val, Instruction): 
        opc = val.opcode_name
        # Get the first operand if there is any
        if val.operand_count > 0:
            op0 = val.operands[0]
        # Get the second operand if there is any
        if val.operand_count > 1:
            op1 = val.operands[1]
        # Binary operation
        if val.is_binary_op:
            opc_map = {'add':'+', 'sub':'-', 'mul':'*'}
            if (opc in opc_map): opc = opc_map[opc]
            # Generate string in C-like syntax
            return get_name(val) + ' = ' + get_name(op0) + ' ' + opc + ' ' + get_name(op1)
        # Store operation
        elif opc == 'store':
            # Generate string in C-like syntax
            return '*' + get_name(op1) + ' = ' + get_name(op0)
        # Store operation
        elif opc == 'ret':
            # Generate string in C-like syntax
            return 'return'
        else:
            return opc
    # Is a Constant?
    elif isinstance(val, ConstantInt):
        return get_name(val)
    return '' 

def print_dot(dut, filename):
    file = open("%s.dot" % filename, "w")
    file.write("digraph %s {\n" % filename)
    for inst in dut.basic_blocks[0].instructions:
        for use in inst.uses:
            if get_name(use) == "[store]":
                file.write(" %s -> %s\n" % (get_name(inst), use.operands[1].name))
            else:
                file.write(" %s -> %s\n" % (get_name(inst), get_name(use)))
    file.write("}\n")
    file.close() 

#--------------------------------------------------------------
#                   ASAP scheduling  
#--------------------------------------------------------------
# Custom routine to find AddSub units needed for scheduling algorithm
def calculate_addSub_asap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if is_addsub(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Custom routine to find Mult units needed for scheduling algorithm
def calculate_mul_asap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if is_mul(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Custom routine to find Registers needed for scheduling algorithm
def calculate_resources_asap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if not is_store(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Loops through the schedule passed in the form of a matrix and prints it out.
def print_to_screen_asap(matrix):
    print ""
    print "--------------  ASAP ----------------------"
    for i in range(0, len(matrix)):
        print "Cycle: " + str(i+1);
        for item in matrix[i]:
            print to_string(item);
        print " "

    print "-------------------------------------------"
    #   Update global resource values
    print "ADD-SUB Units : " + str(calculate_addSub_asap(matrix));
    print "MUL Units : " + str(calculate_mul_asap(matrix));
    print "Resource Usage: " + str(calculate_resources_asap(matrix));
    print "-------------------------------------------"
    print ""

# Main function
def run_asap(testcase):
    f = open(testcase)
    m = Module.from_assembly(f)
    dut_name = os.path.splitext(os.path.basename(testcase))[0]
    dut = m.get_function_named(dut_name)
    
    num_instr = len(dut.basic_blocks[0].instructions)
    # This is the two dimensional array that stores the schedule
    overall_arr = [[None for x in range(num_instr)] for y in range(num_instr)]
    total_instructions  = dut.basic_blocks[0].instructions;
    counter             = 0;    # while loop counter
    done_instructions   = [];   # List stores scheduled instructions
    curr_written_to     = [];   # Used to store operees to prevent Read
                                # after Write dependencies.
 
    while True:
        if len(done_instructions) == len(total_instructions)-1:
            break;
        for inst in total_instructions:
            operee = to_string(inst).partition(' ')[0];
            operand_list = [];
            for o in inst.operands:
                operand_list.append(get_name(o));

            if len(operand_list) > 0:
                if (operand_list[0] not in curr_written_to and operand_list[1] not in curr_written_to):
                    if (inst not in done_instructions):
                        curr_written_to.append(operee);
                        done_instructions.append(inst);
                        overall_arr[counter].append(inst);
                if (operand_list[0] in curr_written_to):
                    curr_written_to.append(operee);
                if (operand_list[1] in curr_written_to):
                    curr_written_to.append(operee);         
        curr_written_to = [];
        counter += 1;       

    # Up ahead is cleanup code as the overall_arr is made the size of the worst case schedule wherein every instruction is a chained instruction. Hence the cleanup with the truncation and removal of trailing Nones.

    # Removing Nones
    for i in range(0, num_instr): 
        overall_arr[i] = [x for x in overall_arr[i] if x is not None];

    # Truncating empty subarrays
    truncate = 0;
    for i in range(0, num_instr): 
        if (not overall_arr[i]):
            truncate = i;
            break;
    overall_arr = overall_arr[0:truncate][0:truncate];

    #   Close test-case file
    f.close()

    #   Print the schedule to Console
    print_to_screen_asap(overall_arr)

#--------------------------------------------------------------
#                   ALAP scheduling  
#--------------------------------------------------------------
def is_store_alap(val) :
    last_elem = val.partition(' ')[0]
    if "*" in last_elem: 
        return True;
 
# Is the value a multiplication?
def is_mul_alap(val) :
    operand_str = val.partition(' ')[2].strip('= ');

    if "*" in operand_str:
        return True;
    else:
        return False;

# Is the value an addition or a subtraction?
def is_addsub_alap(val) :
    operand_str = val.partition(' ')[2].strip('= ');

    if "+" in operand_str or "-" in operand_str:
        return True;
    else:
        return False;

# Custom routine to find AddSub units needed for scheduling algorithm
def calculate_addSub_alap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if is_addsub_alap(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Custom routine to find Mult units needed for scheduling algorithm
def calculate_mul_alap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if is_mul_alap(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Custom routine to find Registers needed for scheduling algorithm
def calculate_resources_alap(matrix):
    max_units = 0;
    for column in matrix:
        curr_max_units = 0;
        for item in column:
            if not is_store_alap(item):
                curr_max_units += 1;
        if curr_max_units > max_units:
            max_units = curr_max_units;
    return max_units;

# Loops through the schedule passed in the form of a matrix and prints it out.
def print_to_screen_alap(matrix):
    print ""
    print "--------------  ALAP ----------------------"
    for i in range(0, len(matrix)):
        print "Cycle: " + str(i+1);
        for item in matrix[i]:
            print item;
        print " "
  
    print "-------------------------------------------"
    #   Update global resource values
    print "ADD-SUB Units : " + str(calculate_addSub_alap(matrix));
    print "MUL Units : " + str(calculate_mul_alap(matrix));
    print "Resource Usage: " + str(calculate_resources_alap(matrix));
    print "-------------------------------------------"
    print ""

# Main function
def run_alap(testcase):
    f = open(testcase)
    m = Module.from_assembly(f)
    dut_name = os.path.splitext(os.path.basename(testcase))[0]
    dut = m.get_function_named(dut_name)
    
    num_instr = len(dut.basic_blocks[0].instructions)
    # This is the two dimensional array that stores the schedule
    overall_arr = [[None for x in range(num_instr)] for y in range(num_instr)]
    total_instructions  = dut.basic_blocks[0].instructions;
    done_instructions   = []; 
    overall_done_instructions = [];

    current_streak      = [];
    streaks             = [];
    next_inst           = "None"

    #---------------------------------------------
    #           Create Streaks
    #---------------------------------------------
    while True:
        if len(done_instructions) == len(total_instructions)-1:
            break;
        for inst in total_instructions:
            if to_string(inst) not in overall_done_instructions:
                uses = [] 
                for u in inst.uses:
                    uses.append(to_string(u))
                # Zero uses?
                if len(inst.uses) <= 0:
                    uses.append(None);

                # if "*y17 = mul171" in to_string(inst):
                #     print uses;

                if inst not in done_instructions and (to_string(inst) in next_inst or next_inst == "None"):
                    done_instructions.append(inst)
                    if uses is not None:
                        current_streak.append(to_string(inst))
                        next_inst = uses
                    else:
                        current_streak.append(to_string(inst))
                        next_inst = "Break"
                if (next_inst == "Break"):
                    break;

        next_inst = "None";
        streaks.append(current_streak); 
        current_streak = []; 

    for streak in streaks:
        if "sub115 = mul80 - mul83" in streak:
            print streak;
    #---------------------------------------------
    #           Add All Memory Ops
    #---------------------------------------------   
    done_instructions = [];
    streaks.sort(key=len, reverse=True);

    # Remove duplicates
    for streak in streaks:
        myset = set(streak)
        streak = list(myset)

    for streak in streaks:
        streak.reverse();
        last_elem = streak[0].partition(' ')[0]
        if "*" in last_elem:       
            counter = len(overall_arr)-1;
            for item in streak:
                overall_arr[counter].append(item);
                done_instructions.append(item);
                counter -= 1;
 
    #---------------------------------------------
    #               Add ALU Ops
    #---------------------------------------------
    for streak in streaks:      
        streak.reverse();
        for i in range(0, len(streak)): 
            if (streak[i] not in done_instructions):
                operee = streak[i].partition(' ')[0];
                added = 0;
                counter = 0;
                while counter < len(overall_arr):
                    if added == 1:
                        break;
                    else:
                        for k in range(0, len(overall_arr[counter])):
                            if added == 1:
                                break;
                            elif overall_arr[counter][k] is not None:
                                operand_str = overall_arr[counter][k].partition(' ')[2].strip('= ');
                                operand_arr = []

                                if "+" in operand_str:
                                    operand_str = operand_str.partition('+');
                                    operand_arr.append(operand_str[0].strip(' '))
                                    operand_arr.append(operand_str[2].strip(' '))
                                elif "*" in operand_str:
                                    operand_str = operand_str.partition('*');
                                    operand_arr.append(operand_str[0].strip(' '))
                                    operand_arr.append(operand_str[2].strip(' '))
                                elif "-" in operand_str:
                                    operand_str = operand_str.partition('-');
                                    operand_arr.append(operand_str[0].strip(' '))
                                    operand_arr.append(operand_str[2].strip(' '))

                                if operee in operand_arr:
                                    overall_arr[counter-1].append(streak[i]);
                                    done_instructions.append(streak[i]);
                                    added = 1;
                                    break;
                    counter += 1;
                if added == 0:
                    streak.reverse(); 
                    for i in range(0, len(streak)): 
                        if (streak[i] not in done_instructions):
                            operee = streak[i].partition(' ')[0];
                            added = 0;
                            counter = 0;
                            while counter < len(overall_arr):
                                if added == 1:
                                    break;
                                else:
                                    for k in range(0, len(overall_arr[counter])):
                                        if added == 1:
                                            break;
                                        elif overall_arr[counter][k] is not None:
                                            operand_str = overall_arr[counter][k].partition(' ')[2].strip('= ');
                                            operand_arr = []

                                            if "+" in operand_str:
                                                operand_str = operand_str.partition('+');
                                                operand_arr.append(operand_str[0].strip(' '))
                                                operand_arr.append(operand_str[2].strip(' '))
                                            elif "*" in operand_str:
                                                operand_str = operand_str.partition('*');
                                                operand_arr.append(operand_str[0].strip(' '))
                                                operand_arr.append(operand_str[2].strip(' '))
                                            elif "-" in operand_str:
                                                operand_str = operand_str.partition('-');
                                                operand_arr.append(operand_str[0].strip(' '))
                                                operand_arr.append(operand_str[2].strip(' '))

                                            if operee in operand_arr:
                                                overall_arr[counter-1].append(streak[i]);
                                                last_index_added = counter-1;
                                                done_instructions.append(streak[i]);
                                                added = 1;
                                                break;
                                counter += 1;
    # Removing Nones
    for i in range(0, num_instr): 
        overall_arr[i] = [x for x in overall_arr[i] if x is not None];

    # Truncating empty subarrays
    truncate = 0;
    for i in range(0, num_instr): 
        if (not overall_arr[i]):
            truncate = i;
        else:
            break;
    overall_arr = overall_arr[truncate+1:]

    # Close test-case file
    f.close()
 
    # Print schedule to Console
    print_to_screen_alap(overall_arr)


#--------------------------------------------------------------
#                   Function MAIN  
#--------------------------------------------------------------
# Prompt CLI usage
if len(sys.argv) < 2:
    sys.exit('Usage: python %s <test>.ll' % sys.argv[0])
# Test exists?
elif not os.path.exists(sys.argv[1]):
    sys.exit('Cannot locate specified test case %s' % sys.argv[1])

filename = str(sys.argv[1]).partition('.')[0] + '_results.txt';
f = open(filename,'w') 
old_stdout = sys.stdout
sys.stdout = f
run_asap(sys.argv[1])
run_alap(sys.argv[1])
sys.stdout = old_stdout
f.close

run_asap(sys.argv[1])
run_alap(sys.argv[1])
