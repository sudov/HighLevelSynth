#!/usr/bin/env python

# Tests accessing of instruction operands.
import sys
import os
import llvm 
# top-level, for common stuff
from llvm.core import *

# Global resource values
resources       = 0;
add_sub_units   = 0;
mul_func_units  = 0;

#===----------------------------------------------------------------------===
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

def print_to_screen(matrix):
    print ""
    print "--------------  ALAP ----------------------"
    for i in range(0, len(matrix)):
        print "Cycle: " + str(i+1);
        for item in matrix[i]:
            print item;
        print " "
    print "-------------------------------------------"
    print ""

# Main function
def run(testcase):
    f = open(testcase)
    m = Module.from_assembly(f)
    dut_name = os.path.splitext(os.path.basename(testcase))[0]
    dut = m.get_function_named(dut_name)
    
    num_instr = len(dut.basic_blocks[0].instructions)
    overall_arr = [[None for x in range(num_instr)] for y in range(num_instr)]
    total_instructions  = dut.basic_blocks[0].instructions;
    done_instructions   = []; 
    overall_done_instructions = [];

    longest_streak      = [];
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

        if (len(current_streak) > len(longest_streak)):
            longest_streak = current_streak;   
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
 
    #Print to Console
    print_to_screen(overall_arr)

# Prompt CLI usage
if len(sys.argv) < 2:
    sys.exit('Usage: python %s <test>.ll' % sys.argv[0])
elif not os.path.exists(sys.argv[1]):
    sys.exit('Cannot locate specified test case %s' % sys.argv[1])

run(sys.argv[1])
