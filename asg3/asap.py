#!/usr/bin/env python

# Tests accessing of instruction operands.
import sys
import os
import llvm 
# top-level, for common stuff
from llvm.core import *

# Global resource values
resources 		= 0;
add_sub_units 	= 0;
mul_func_units 	= 0;

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

def print_to_screen(matrix):
	print ""
	print "--------------  ASAP ----------------------"
	for i in range(0, len(matrix)):
		print "Cycle: " + str(i+1);
		for item in matrix[i]:
			print to_string(item);
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
	total_instructions 	= dut.basic_blocks[0].instructions;
	counter 			= 0;
	done_instructions  	= []; 
	curr_written_to 	= [];
 
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

	#	Close test-case file
	f.close()
 	
 	#	Update global resource values
 	calculate_addSub(overall_arr);
 	calculate_mul(overall_arr);
 	calculate_resources(overall_arr);

	#	Print Shit to Console
	print_to_screen(overall_arr)

# Prompt CLI usage
if len(sys.argv) < 2:
	sys.exit('Usage: python %s <test>.ll' % sys.argv[0])
# Test exists?
elif not os.path.exists(sys.argv[1]):
	sys.exit('Cannot locate specified test case %s' % sys.argv[1])

run(sys.argv[1])
