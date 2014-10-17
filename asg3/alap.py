#!/usr/bin/env python

# Tests accessing of instruction operands.
import sys
import os
import llvm 
# top-level, for common stuff
from llvm.core import *

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

    while True:
        # print len(done_instructions)
        # print len(total_instructions)

        if len(done_instructions) == len(total_instructions)-1:
            break;
        for inst in total_instructions:
            if to_string(inst) not in overall_done_instructions:
                uses = ""
                for u in inst.uses:
                    uses += to_string(u)
                # Zero uses?
                if len(inst.uses) <= 0:
                    uses += "None"

                # print "New Run"
                # print inst not in done_instructions
                # print next_inst == to_string(inst)
                # print next_inst == "None"
                # print to_string(inst)
                # print next_inst
                # print inst not in done_instructions and (next_inst == to_string(inst) or next_inst == "None")

                if inst not in done_instructions and (next_inst == to_string(inst) or next_inst == "None"):
                    done_instructions.append(inst)
                    if uses is not "None":
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

    streaks.remove(longest_streak);

    # Initializing true initial values for overall_arr
    for i in range(0, len(longest_streak)):
        overall_arr[i].append(longest_streak[i]);

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
    
    done_instructions = longest_streak;
    streaks.sort(key=len, reverse=True);

    for streak in streaks:
        myset = set(streak)
        streak = list(myset)

    # ALAP algorithm - part 1
    for streak in streaks:
        streak.reverse();
        last_elem = streak[0].partition(' ')[0]
        # debug=0;
        if "*" in last_elem:       
            counter = len(overall_arr)-1;
            for item in streak:
                overall_arr[counter].append(item);
                done_instructions.append(item);
                counter -= 1;

    # ALAP algorithm - part 2
    for streak in streaks:        
        streak.reverse();
        last_elem = streak[0].partition(' ')[0]
        # debug=0;
        if "*" not in last_elem:
            # streak.reverse();
            last_index_added = 0;
            for i in range(0, len(streak)): 
                # if (streak[i] == "tmp374 = tmp373 - x4"):
                #     print streak
                    # operee = streak[i].partition(' ')[0];
                    # operand_str = streak[i].partition(' ')[2].strip('= ');
                    # operand_arr = [];
                    # print "-" in operand_str
                    # operand_str = operand_str.partition('-');
                    # operand_arr.append(operand_str[0])
                    # operand_arr.append(operand_str[2])
                    # operand_arr.append("tmp")
                    # print operee;
                    # print operand_arr;
                    # print operee in operand_arr
                    # print_to_screen(overall_arr)
                    # break;
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
                                else:
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

                                    # if counter == 5 and operee=="tmp373":
                                    #     print streak
                                    #     print "checkpoint";
                                    #     print operee;
                                    #     print operand_arr;
                                    #     print operee in operand_arr;
                                    #     print counter;

                                    if operee in operand_arr:
                                        overall_arr[counter-1].append(streak[i]);
                                        last_index_added = counter-1;
                                        done_instructions.append(streak[i]);
                                        added = 1;
                                        break;
                        counter += 1;
                    if added == 0:
                        last_index_added = 0;
                        streak.reverse(); 
                        # overall_arr[last_index_added].append(streak[i]);
                        # done_instructions.append(streak[i]);
                        # added = 1;
                        # last_index_added = counter-1;
                        for i in range(0, len(streak)): 
                            # if (streak[i] == "tmp374 = tmp373 - x4"):
                            #     print streak
                                # operee = streak[i].partition(' ')[0];
                                # operand_str = streak[i].partition(' ')[2].strip('= ');
                                # operand_arr = [];
                                # print "-" in operand_str
                                # operand_str = operand_str.partition('-');
                                # operand_arr.append(operand_str[0])
                                # operand_arr.append(operand_str[2])
                                # operand_arr.append("tmp")
                                # print operee;
                                # print operand_arr;
                                # print operee in operand_arr
                                # print_to_screen(overall_arr)
                                # break;
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
                                            else:
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

                                                # if counter == 5 and operee=="tmp373":
                                                #     print streak
                                                #     print "checkpoint";
                                                #     print operee;
                                                #     print operand_arr;
                                                #     print operee in operand_arr;
                                                #     print counter;

                                                if operee in operand_arr:
                                                    overall_arr[counter-1].append(streak[i]);
                                                    last_index_added = counter-1;
                                                    done_instructions.append(streak[i]);
                                                    added = 1;
                                                    break;
                                    counter += 1;

    # Close test-case file
    f.close()
 
    #Print Shit to Console
    print_to_screen(overall_arr)

# Prompt CLI usage
if len(sys.argv) < 2:
    sys.exit('Usage: python %s <test>.ll' % sys.argv[0])
# Test exists?
elif not os.path.exists(sys.argv[1]):
    sys.exit('Cannot locate specified test case %s' % sys.argv[1])

run(sys.argv[1])
