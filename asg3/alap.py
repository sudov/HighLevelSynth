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

# Main function
def run(testcase):
    f = open(testcase)
    m = Module.from_assembly(f)
    dut_name = os.path.splitext(os.path.basename(testcase))[0]
    dut = m.get_function_named(dut_name)

    #===-----------------------------------------------------------===
    # Print instructions in DFG under test 
    for inst in dut.basic_blocks[0].instructions:
        # print the instruction in LLVM form
        print "\n"
        print inst

        # Print the instruction in C form
        print "  - C syntax: " + to_string(inst)

        # Print its operation type
        type = "  - Type: " 
        if is_store(inst) :
            type += "STORE"
        elif is_addsub(inst) :
            type += "ADDSUB"
        elif is_mul(inst) :
            type += "MUL"
        elif is_return(inst) :
            type += "RETURN"
        else: 
            type += "UNKNOWN"
        print type 

        # Print its operands in short name 
        operands = "  - Operands: "
        for o in inst.operands:
            operands += get_name(o) + "; "
        # Zero operands?
        if len(inst.operands) <= 0:
            operands += "NONE"
        print operands

        # Print its uses in pretty form
        uses = "  - Uses: "
        for u in inst.uses:
            uses += to_string(u) + "; "
        # Zero uses?
        if len(inst.uses) <= 0:
            uses += "NONE"
        print uses

    # No work left
    f.close()

# Prompt CLI usage
if len(sys.argv) < 2:
    sys.exit('Usage: python %s <test>.ll' % sys.argv[0])
# Test exists?
elif not os.path.exists(sys.argv[1]):
    sys.exit('Cannot locate specified test case %s' % sys.argv[1])

run(sys.argv[1])
