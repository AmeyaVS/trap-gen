# -*- coding: iso-8859-1 -*-
####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################



# Lets first of all import the necessary files for the
# creation of the processor
import trap
import cxx_writer
from ARMCoding import *
from ARMMethods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
isa.addMethod(restoreSPSR_method)
isa.addMethod(updateAlias_method)
isa.addMethod(AShiftRight_method)
isa.addMethod(RotateRight_method)
isa.addMethod(LSRegShift_method)
isa.addMethod(SignExtend_method)
isa.addMethod(UpdatePSRBitM_method)
isa.addMethod(UpdatePSRAdd_method)
isa.addMethod(UpdatePSRSub_method)

#-------------------------------------------------------------------------------------
# Let's now procede to set the behavior of the instructions
#-------------------------------------------------------------------------------------
#
# Note the special operations:
#
# -- annull(): transforms the current instruction in a NOP; if we are
# in the middle of the execution of some code, it also terminates the
# execution of that part of code (it is like an exception)
# -- flush(): flushes the pipeline stages preceding the one in which
# the flush method has been called
# -- stall(n): stalls the current stage and the preceding ones for n clock
# cycles. If we issue this operation in the middle of the execution of an
# instruction, anyway the execution of that code finished before the stall
# operation has any effect; if that code contains another call to stall(m),
# the pipeline stages are stalled for a total of n+m
# -- THROW_EXCEPTION: a macro for throwing C++ exceptions
#

#____________________________________________________________________________________________________
#----------------------------------------------------------------------------------------------------
# Now using all the defined operations, instruction codings, etc
# I can actually declare the processor instructions
#----------------------------------------------------------------------------------------------------
#____________________________________________________________________________________________________

# ADC instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)rn + (int)operand;
if (CPSR[key_C]){
    rd = ((int)rd) + 1;
}
""")
adc_shift_imm_Instr = trap.Instruction('ADC_si', True, frequency = 5)
adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_shift_imm_Instr.setCode(opCode, 'execute')
adc_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
adc_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
adc_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
adc_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7, 'CPSR' : 0x00000000})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
adc_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 3})
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002})
isa.addInstruction(adc_shift_imm_Instr)
adc_shift_reg_Instr = trap.Instruction('ADC_sr', True, frequency = 5)
adc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_shift_reg_Instr.setCode(opCode, 'execute')
adc_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
adc_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
adc_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
adc_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7, 'CPSR' : 0x00000000})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_reg_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0x20, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16, 'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002})
isa.addInstruction(adc_shift_reg_Instr)
adc_imm_Instr = trap.Instruction('ADC_i', True, frequency = 5)
adc_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_imm_Instr.setCode(opCode, 'execute')
adc_imm_Instr.addBehavior(IncrementPC, 'fetch')
adc_imm_Instr.addBehavior(condCheckOp, 'execute')
adc_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
adc_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_imm_Instr.addBehavior(UpdatePC, 'execute', False)
adc_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 6})
adc_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 0x3f0 + 3})
isa.addInstruction(adc_imm_Instr)

# ADD instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)rn + (int)operand;
""")
add_shift_imm_Instr = trap.Instruction('ADD_si', True, frequency = 6)
add_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_shift_imm_Instr.setCode(opCode, 'execute')
add_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
add_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
add_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
add_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6, 'CPSR' : 0x00000000})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 2})
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002})
isa.addInstruction(add_shift_imm_Instr)
add_shift_reg_Instr = trap.Instruction('ADD_sr', True, frequency = 6)
add_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_shift_reg_Instr.setCode(opCode, 'execute')
add_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
add_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
add_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
add_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
#Test start
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_reg_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0x20, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
add_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16, 'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002}) 
#Test end
isa.addInstruction(add_shift_reg_Instr)
add_imm_Instr = trap.Instruction('ADD_i', True, frequency = 6)
add_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_imm_Instr.setCode(opCode, 'execute')
add_imm_Instr.addBehavior(IncrementPC, 'fetch')
add_imm_Instr.addBehavior(condCheckOp, 'execute')
add_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
add_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_imm_Instr.addBehavior(UpdatePC, 'execute', False)
#Test start
add_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 6})
add_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 0x3f0 + 3})
#Test end
isa.addInstruction(add_imm_Instr)

# AND instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn & operand;
rd = result;
""")
and_shift_imm_Instr = trap.Instruction('AND_si', True, frequency = 6)
and_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_shift_imm_Instr.setCode(opCode, 'execute')
and_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
and_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
and_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
and_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
and_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3, 'CPSR': 0x20000000})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 3})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 3})
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 2})
isa.addInstruction(and_shift_imm_Instr)

and_shift_reg_Instr = trap.Instruction('AND_sr', True, frequency = 6)
and_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_shift_reg_Instr.setCode(opCode, 'execute')
and_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
and_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
and_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
and_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
and_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
#Test start
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3, 'CPSR' : 0x20000000})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x00000000,'REGS[9]': 3, 'REGS[8]': 3, 'REGS[10]': 123}, {'REGS[10]': 123})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1 , 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0 , 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1 , 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0 , 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1 , 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0x20, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16, 'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 0x2})
and_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 3})
#Test start
isa.addInstruction(and_shift_reg_Instr)

and_imm_Instr = trap.Instruction('AND_i', True, frequency = 6)
and_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_imm_Instr.setCode(opCode, 'execute')
and_imm_Instr.addBehavior(IncrementPC, 'fetch')
and_imm_Instr.addBehavior(condCheckOp, 'execute')
and_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
and_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_imm_Instr.addBehavior(UpdatePC, 'execute', False)
and_imm_Instr.addVariable(('result', 'BIT<32>'))
#Test start
and_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 3})
and_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 0x0})
#Test start
isa.addInstruction(and_imm_Instr)

# BRANCH instruction family
opCode = cxx_writer.writer_code.Code("""
if(l == 1) {
    LINKR = PC - 4;
}
PC = PC + (((int)SignExtend(offset, 24)) << 2);
stall(2);
flush();
""")
branch_Instr = trap.Instruction('BRANCH', True, frequency = 7)
branch_Instr.setMachineCode(branch, {}, 'TODO')
branch_Instr.setCode(opCode, 'execute')
branch_Instr.addBehavior(IncrementPC, 'fetch')
branch_Instr.addBehavior(condCheckOp, 'execute')
#branch_Instr.addTest({'cond': 0xe, 'l': 0, 'offset': 0x400}, {'PC': 0x00445560, 'LINKR': 8}, {'PC': 0x00446560, 'LINKR': 8})
branch_Instr.addTest({'cond': 0xe, 'l': 0, 'offset': 0x000400}, {'PC': 0x00445560, 'LINKR': 8}, {'PC': 0x00446560, 'LINKR': 8})
branch_Instr.addTest({'cond': 0xe, 'l': 1, 'offset': 0x400}, {'PC': 0x00445560, 'LINKR': 8}, {'PC': 0x00446560, 'LINKR': 0x0044555C})
isa.addInstruction(branch_Instr)

opCode = cxx_writer.writer_code.Code("""
// Note how the T bit is not considered since we do not bother with
// thumb mode
PC = (rm & 0xFFFFFFFC);
stall(2);
flush();
""")
branch_thumb_Instr = trap.Instruction('BRANCHX', True, frequency = 3)
branch_thumb_Instr.setMachineCode(branch_thumb, {}, 'TODO')
branch_thumb_Instr.setCode(opCode, 'execute')
branch_thumb_Instr.addBehavior(IncrementPC, 'fetch')
branch_thumb_Instr.addBehavior(condCheckOp, 'execute')
branch_thumb_Instr.addTest({'cond': 0xe, 'rm': 0}, {'REGS[0]': 0x00445560}, {'PC': 0x00445560})
branch_thumb_Instr.addTest({'cond': 0xe, 'rm': 0}, {'REGS[0]': 0x00445563}, {'PC': 0x00445560})
isa.addInstruction(branch_thumb_Instr)

# BIC instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn & ~operand;
rd = result;
""")
bic_shift_imm_Instr = trap.Instruction('BIC_si', True, frequency = 3)
bic_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_shift_imm_Instr.setCode(opCode, 'execute')
bic_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
bic_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
bic_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
bic_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
bic_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0, 'CPSR': 0x60000000})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 0})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 0})
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 1})
isa.addInstruction(bic_shift_imm_Instr)

bic_shift_reg_Instr = trap.Instruction('BIC_sr', True, frequency = 3)
bic_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_shift_reg_Instr.setCode(opCode, 'execute')
bic_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
bic_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
bic_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
bic_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
bic_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
#Test Start
bic_shift_reg_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0, 'CPSR': 0x60000000})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 1})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]':0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0x20, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
bic_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16, 'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 1})
#Test End
isa.addInstruction(bic_shift_reg_Instr)

bic_imm_Instr = trap.Instruction('BIC_i', True, frequency = 3)
bic_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_imm_Instr.setCode(opCode, 'execute')
bic_imm_Instr.addBehavior(IncrementPC, 'fetch')
bic_imm_Instr.addBehavior(condCheckOp, 'execute')
bic_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
bic_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_imm_Instr.addBehavior(UpdatePC, 'execute', False)
bic_imm_Instr.addVariable(('result', 'BIT<32>'))
bic_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 0})
bic_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 3})
isa.addInstruction(bic_imm_Instr)

# CMN instruction family
opCode = cxx_writer.writer_code.Code("""
UpdatePSRAddInner(rn, operand);
""")
cmn_shift_imm_Instr = trap.Instruction('CMN_si', True, frequency = 4)
cmn_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_shift_imm_Instr.setCode(opCode, 'execute')
cmn_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
cmn_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')

cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'CPSR': 0x60000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 0, 'REGS[8]': 0xffffffff}, {'CPSR': 0x80000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 0x80000001, 'REGS[8]': 0x7fffffff}, {'CPSR': 0x60000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 0xc0000000, 'REGS[8]': 0x40000000}, {'CPSR': 0x60000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 0, 'REGS[8]': 0}, {'CPSR': 0x40000000})
cmn_shift_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'CPSR': 0x20000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'CPSR': 0x20000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xfffffff8}, {'CPSR': 0x80000000})
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'CPSR': 0x00000000})
isa.addInstruction(cmn_shift_imm_Instr)

cmn_shift_reg_Instr = trap.Instruction('CMN_sr', True, frequency = 4)
cmn_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_shift_reg_Instr.setCode(opCode, 'execute')
cmn_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
cmn_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
#Start Test
#--Functinalities test
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0,'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'CPSR': 0x60000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0,'REGS[9]': 0, 'REGS[8]': 0xffffffff}, {'CPSR': 0x80000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0,'REGS[9]': 0x80000001, 'REGS[8]': 0x7fffffff}, {'CPSR': 0x60000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0,'REGS[9]': 0xc0000000, 'REGS[8]': 0x40000000}, {'CPSR': 0x60000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0,'REGS[9]': 0x00000000, 'REGS[8]': 0x00000000}, {'CPSR': 0x40000000})
#--Condition not satisfy test
cmn_shift_reg_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
#--Operande operation test
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'CPSR': 0x80000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1,'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR': 0x00000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0,'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'CPSR': 0x20000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0,'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xfffffff8}, {'CPSR': 0x80000000})
cmn_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16,'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'CPSR': 0x00000000})
#End Test
isa.addInstruction(cmn_shift_reg_Instr)

cmn_imm_Instr = trap.Instruction('CMN_i', True, frequency = 4)
cmn_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_imm_Instr.setCode(opCode, 'execute')
cmn_imm_Instr.addBehavior(IncrementPC, 'fetch')
cmn_imm_Instr.addBehavior(condCheckOp, 'execute')
cmn_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
cmn_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rotate': 0x00000000, 'immediate': 3   }, {'CPSR': 0x20000000, 'REGS[9]': 3}, {'CPSR': 0x00000000})
cmn_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rotate': 0xe       , 'immediate': 0x3f}, {'CPSR': 0x60000000, 'REGS[9]': 3}, {'CPSR': 0x00000000})
isa.addInstruction(cmn_imm_Instr)

# CMP instruction family
opCode = cxx_writer.writer_code.Code("""
UpdatePSRSubInner(rn, operand);
""")
cmp_shift_imm_Instr = trap.Instruction('CMP_si', True, frequency = 7)
cmp_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_shift_imm_Instr.setCode(opCode, 'execute')
cmp_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
cmp_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
#Condition Faild : do not update CPSR
cmp_shift_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 0xfffffffd, 'REGS[8]': 0x00000003}, {'CPSR': 0x20000000})
#Condition Pass & C flag = Not BorrowFrom(Rn-shift_operand)
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0xfffffffd, 'REGS[8]': 0x00000003}, {'CPSR': 0xa0000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000003}, {'CPSR': 0x80000000})
#Condition Pass & Z flag = (if alu_out == 0 then 1 else 0)
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x60000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
#Condition Pass & N flag = alu_out[31]
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x80000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000003}, {'CPSR': 0x80000000})
#Condition Pass & OverflowFrom(Rn - shifter_operand)
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x10000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
#Logic shift right by immediate 
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000007}, {'CPSR': 0x60000000})
#Arithmetic shift right by immediate
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[9]': 0xffffffff, 'REGS[8]': 0x80000002}, {'CPSR': 0x60000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x20000000})
#Rotate right by immediate
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000006}, {'CPSR': 0x60000000})
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'shift_amm': 8, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000300}, {'CPSR': 0x60000000})
isa.addInstruction(cmp_shift_imm_Instr)

cmp_shift_reg_Instr = trap.Instruction('CMP_sr', True, frequency = 7)
cmp_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_shift_reg_Instr.setCode(opCode, 'execute')
cmp_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
cmp_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
#Condition Faild : do not update CPSR
cmp_shift_reg_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0xfffffffd, 'REGS[8]': 0x00000003}, {'CPSR': 0x20000000})
#Condition Pass & C flag = Not BorrowFrom(Rn-shift_operand)
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0xfffffffd, 'REGS[8]': 0x00000003}, {'CPSR': 0xa0000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000003}, {'CPSR': 0x80000000})
#Condition Pass & Z flag = (if alu_out == 0 then 1 else 0)
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
#Condition Pass & N flag = alu_out[31]
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x80000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000003}, {'CPSR': 0x80000000})
#Condition Pass & OverflowFrom(Rn - shifter_operand)
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x10000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})

#Logic shift left by register
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000001, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000001}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000000}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 33, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000000}, {'CPSR': 0x20000000})
#Logic shift right by register 
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000001, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000004}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000000}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 33, 'REGS[9]': 0x00000002, 'REGS[8]': 0x00000000}, {'CPSR': 0x20000000})
#Arithmetic shift right by register
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000002}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000001, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000007}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x20000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[9]': 0xffffffff, 'REGS[8]': 0x80000000}, {'CPSR': 0x60000000})
#Rotate right by register
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000020, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000003}, {'CPSR': 0x60000000})
cmp_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[0]': 0x00000008, 'REGS[9]': 0x00000003, 'REGS[8]': 0x00000300}, {'CPSR': 0x60000000})
#Add instruction
isa.addInstruction(cmp_shift_reg_Instr)
cmp_imm_Instr = trap.Instruction('CMP_i', True, frequency = 7)
cmp_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_imm_Instr.setCode(opCode, 'execute')
cmp_imm_Instr.addBehavior(IncrementPC, 'fetch')
cmp_imm_Instr.addBehavior(condCheckOp, 'execute')
cmp_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
cmp_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rotate': 0x00000000, 'immediate': 0x00000003}, {'CPSR': 0x00000000, 'REGS[9]': 0x00000003}, {'CPSR': 0x60000000})
cmp_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rotate': 0x0000000e, 'immediate': 0x0000003f}, {'CPSR': 0x00000000, 'REGS[9]': 0x000003f0}, {'CPSR': 0x60000000})
isa.addInstruction(cmp_imm_Instr)
# EOR instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn ^ operand;
rd = result;
""")
eor_shift_imm_Instr = trap.Instruction('EOR_si', True, frequency = 4)
eor_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_shift_imm_Instr.setCode(opCode, 'execute')
eor_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
eor_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
eor_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
eor_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
eor_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0, 'CPSR': 0x60000000})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0})
eor_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 5})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 0xfffffffc})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 2})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 0xfffffffc})
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 0x00200001})
isa.addInstruction(eor_shift_imm_Instr)

eor_shift_reg_Instr = trap.Instruction('EOR_sr', True, frequency = 4)
eor_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_shift_reg_Instr.setCode(opCode, 'execute')
eor_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
eor_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
eor_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
eor_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
eor_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
#if ConditionPassed(cond) then
#    Rd = Rn EOR shifter_operand
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'REGS[0]': 0x00000000, 'REGS[9]': 0x0000ffff, 'REGS[8]': 0x00000f0f, 'REGS[10]' : 0x00000000}, 
                            {'REGS[10]':0x0000f0f0})
#if ConditionPassed(cond) then
#    Rd = Rn EOR shifter_operand
#    if S == 1 and Rd == R15 then
#        CPSR = SPSR
#eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 15, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
#                            {'CPSR' : 0x40000000, 'SPSR' : 0x20000000}, 
#                            {'CPSR' : 0x20000000, 'SPSR' : 0x20000000})
#    else if S == 1 then
#       Normal case
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'REGS[0]': 0x00000000, 'REGS[9]': 0xffffabcd, 'REGS[8]': 0xffff0000, 'REGS[10]' : 0x00000000}, 
                            {'REGS[10]':0x0000abcd})
#       N Flag = Rd[31]
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0xf0000000, 'REGS[8]': 0x70000000, 'REGS[10]' : 0x00000000}, 
                            {'CPSR' : 0x80000000, 'REGS[10]':0x80000000})
#       Z Flag = if Rd == 0 then 1 else 0
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'CPSR' : 0x00000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000000, 'REGS[8]': 0x00000000, 'REGS[10]' : 0x00000000}, 
                            {'CPSR' : 0x40000000, 'REGS[10]':0x00000000})
#       C Flag = shifter_carry_out (Exp: Logic shift left by register shifter_carry_out = C Flag)
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'CPSR' : 0x20000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x00000000, 'REGS[8]': 0x00000000, 'REGS[10]' : 0x00000000}, 
                            {'CPSR' : 0x60000000, 'REGS[10]':0x00000000})
#       V Flag = unaffected
eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'CPSR' : 0x10000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0xffffabcd, 'REGS[8]': 0xffff0000, 'REGS[10]' : 0x00000000}, 
                            {'CPSR' : 0x10000000, 'REGS[10]':0x0000abcd})
        
#    end if
#else
eor_shift_reg_Instr.addTest({'cond' : 0x0, 's': 1, 'rn': 9, 'rd' : 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
                            {'CPSR' : 0x20000000, 'REGS[0]': 0x00000000, 'REGS[9]': 0x0000ffff, 'REGS[8]': 0x00000f0f, 'REGS[10]' : 0x00000000}, 
                            {'CPSR' : 0x20000000, 'REGS[10]':0x00000000})
#end if 
isa.addInstruction(eor_shift_reg_Instr)

eor_imm_Instr = trap.Instruction('EOR_i', True, frequency = 4)
eor_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_imm_Instr.setCode(opCode, 'execute')
eor_imm_Instr.addBehavior(IncrementPC, 'fetch')
eor_imm_Instr.addBehavior(condCheckOp, 'execute')
eor_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
eor_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_imm_Instr.addBehavior(UpdatePC, 'execute', False)
eor_imm_Instr.addVariable(('result', 'BIT<32>'))


#if ConditionPassed(cond) then
#    Rd = Rn EOR shifter_operand
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x0000000f}, 
                      {'REGS[9]': 0x0000ffff,'REGS[10]' : 0x00000000}, 
                      {'REGS[10]':0x0000fff0})
#if ConditionPassed(cond) then
#    Rd = Rn EOR shifter_operand
#    if S == 1 and Rd == R15 then
#        CPSR = SPSR
#eor_shift_reg_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 15, 'rm': 8, 'rs': 0, 'shift_op': 0}, 
#                            {'CPSR' : 0x40000000, 'SPSR' : 0x20000000}, 
#                            {'CPSR' : 0x20000000, 'SPSR' : 0x20000000})
#    else if S == 1 then
#       Normal case
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000001}, 
                      {'REGS[9]': 0x0000ffff,'REGS[10]' : 0x00000000}, 
                      {'REGS[10]':0x0000fffe})
#       N Flag = Rd[31]
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000000}, 
                      {'CPSR' : 0x00000000, 'REGS[9]': 0xf0000000,'REGS[10]' : 0x00000000}, 
                      {'CPSR' : 0x80000000, 'REGS[10]':0xf0000000})
#       Z Flag = if Rd == 0 then 1 else 0
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000000}, 
                      {'CPSR' : 0x00000000, 'REGS[9]': 0x00000000,'REGS[10]' : 0x00000000}, 
                      {'CPSR' : 0x40000000, 'REGS[10]':0x00000000})
#       C Flag = shifter_carry_out (Exp: Logic shift left by register shifter_carry_out = C Flag)
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000000}, 
                      {'CPSR' : 0x20000000, 'REGS[9]': 0x00000000, 'REGS[10]' : 0x00000000}, 
                      {'CPSR' : 0x60000000, 'REGS[10]':0x00000000})
#       V Flag = unaffected
eor_imm_Instr.addTest({'cond' : 0xe, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000000}, 
                      {'CPSR' : 0x10000000, 'REGS[9]': 0x000000cd, 'REGS[10]' : 0x00000000}, 
                      {'CPSR' : 0x10000000, 'REGS[10]':0x000000cd})
#    end if
#else
eor_imm_Instr.addTest({'cond' : 0x0, 's': 1, 'rn': 9, 'rd' : 10, 'rotate': 0x00000000, 'immediate': 0x00000000}, 
                      {'CPSR' : 0x20000000, 'REGS[9]': 0x0000ffff, 'REGS[8]': 0x0000000f, 'REGS[10]' : 0x00000000}, 
                      {'CPSR' : 0x20000000, 'REGS[10]':0x00000000})
#end if 
isa.addInstruction(eor_imm_Instr)
# LDM instruction family
opCode = cxx_writer.writer_code.Code("""
unsigned int numRegsToLoad = 0;
unsigned int loadLatency = 0;
if(s == 0){
    //I'm dealing just with the current registers: LDM type one or three
    //First af all I read the memory in the register I in the register list.
    for(int i = 0; i < 15; i++){
        if((reg_list & (0x00000001 << i)) != 0){
            REGS[i] = dataMem.read_word(start_address);
            start_address += 4;
            numRegsToLoad++;
        }
    }
    loadLatency = numRegsToLoad + 1;

    //I tread in a special way the PC, since loading a value
    //in the PC is like performing a branch.
    if((reg_list & 0x00008000) != 0){
        //I have to load also the PC: it is like a branch; since I don't bother with
        //Thumb mode, bits 0 and 1 of the PC are ignored
        PC = dataMem.read_word(start_address) & 0xFFFFFFFC;
        numRegsToLoad++;
        loadLatency += 2;
        flush();
    }
    // First of all if it is necessary I perform the writeback
    if(w != 0){
        rn = wb_address;
    }
}
else if((reg_list & 0x00008000) != 0){
    //I'm dealing just with the current registers: LDM type one or three
    //First af all I read the memory in the register I in the register list.
    for(int i = 0; i < 15; i++){
        if((reg_list & (0x00000001 << i)) != 0){
            REGS[i] = dataMem.read_word(start_address);
            start_address += 4;
            numRegsToLoad++;
        }
    }
    loadLatency = numRegsToLoad + 1;

    //I tread in a special way the PC, since loading a value
    //in the PC is like performing a branch.
    //I have to load also the PC: it is like a branch; since I don't bother with
    //Thumb mode, bits 0 and 1 of the PC are ignored
    PC = dataMem.read_word(start_address) & 0xFFFFFFFC;
    //LDM type three: in this type of operation I also have to restore the PSR.
    restoreSPSR();
    numRegsToLoad++;
    loadLatency += 2;
    flush();
}
else{
    //I'm dealing with user-mode registers: LDM type two
    //Load the registers common to all modes
    for(int i = 0; i < 16; i++){
        if((reg_list & (0x00000001 << i)) != 0){
            RB[i] = dataMem.read_word(start_address);
            start_address += 4;
            numRegsToLoad++;
        }
    }
    loadLatency = numRegsToLoad + 1;
}
stall(loadLatency);
""")
opCodeDec = cxx_writer.writer_code.Code("""
#ifdef ACC_MODEL
for(int i = 0; i < 16; i++){
    if((reg_list & (0x00000001 << i)) != 0){
        RB[i].lock();
    }
}
#endif
""")
ldm_Instr = trap.Instruction('LDM', True, frequency = 8)
ldm_Instr.setMachineCode(ls_multiple, {'l' : [1]}, 'TODO')
ldm_Instr.setCode(opCode, 'execute')
ldm_Instr.setCode(opCodeDec, 'decode')
ldm_Instr.addBehavior(IncrementPC, 'fetch')
ldm_Instr.addBehavior(condCheckOp, 'execute')
ldm_Instr.addBehavior(LSM_reglist_Op, 'execute')
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x10]': 1234}, {'REGS[1]': 1234})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x10]': 1234}, {'REGS[1]': 1234})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 's': 0, 'w': 1, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x10]': 1234}, {'REGS[1]': 1234, 'REGS[0]': 0x14})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x0e}, {'REGS[0]': 0x10, 'dataMem[0x10]': 1, 'dataMem[0x14]': 2, 'dataMem[0x18]': 3}, {'REGS[1]': 1, 'REGS[2]': 2, 'REGS[3]': 3})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 0, 'w': 1, 'rn': 0, 'reg_list': 0x0e}, {'REGS[0]': 0x10, 'dataMem[0x10]': 1, 'dataMem[0x14]': 2, 'dataMem[0x18]': 3}, {'REGS[1]': 1, 'REGS[2]': 2, 'REGS[3]': 3, 'REGS[0]': 0x1c})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x14]': 1234}, {'REGS[1]': 1234})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x0c]': 1234}, {'REGS[1]': 1234})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 's': 0, 'w': 1, 'rn': 0, 'reg_list': 0x02}, {'REGS[0]': 0x10, 'dataMem[0x14]': 1234}, {'REGS[1]': 1234, 'REGS[0]': 0x14})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 0, 'w': 0, 'rn': 0, 'reg_list': 0x0e}, {'REGS[0]': 0x10, 'dataMem[0x0c]': 1, 'dataMem[0x08]': 2, 'dataMem[0x04]': 3}, {'REGS[1]': 3, 'REGS[2]': 2, 'REGS[3]': 1})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 0, 'w': 1, 'rn': 0, 'reg_list': 0x0e}, {'REGS[0]': 0x10, 'dataMem[0x0c]': 1, 'dataMem[0x08]': 2, 'dataMem[0x04]': 3}, {'REGS[1]': 3, 'REGS[2]': 2, 'REGS[3]': 1, 'REGS[0]': 0x04})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x2000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 1234}, {'RB[13]': 1234, 'RB[21]': 0x888})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x2000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 1234}, {'RB[13]': 1234, 'RB[21]': 0x888})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x6000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 1, 'dataMem[0x14]': 2}, {'RB[13]': 1, 'RB[14]': 2})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x2000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x14]': 1234}, {'RB[13]': 1234, 'RB[21]': 0x888})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x2000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x0c]': 1234}, {'RB[13]': 1234, 'RB[21]': 0x888})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0x6000}, {'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x0c]': 1, 'dataMem[0x08]': 2}, {'RB[13]': 2, 'RB[14]': 1, 'RB[21]': 0x888})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xa000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 0xaaa0, 'dataMem[0x0c]': 456}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[21]': 0x888, 'CPSR' : 0x4444441f})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xa000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 456, 'dataMem[0x14]': 0xaaa0}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[21]': 0x888, 'CPSR' : 0x4444441f})
ldm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xe000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x10]': 456, 'dataMem[0x14]': 2, 'dataMem[0x18]': 0xaaa0}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[14]': 2, 'CPSR' : 0x4444441f})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xa000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x14]': 456, 'dataMem[0x18]': 0xaaa0}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[21]': 0x888, 'CPSR' : 0x4444441f})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xa000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x0c]': 0xaaa0, 'dataMem[0x08]': 456}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[21]': 0x888, 'CPSR' : 0x4444441f})
ldm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 's': 1, 'w': 0, 'rn': 0, 'reg_list': 0xe000}, {'SPSR[1]' : 0x4444441f, 'CPSR' : 0x12, 'RB[0]': 0x10, 'RB[13]': 0x777, 'RB[21]': 0x888, 'dataMem[0x0c]': 0xaaa0, 'dataMem[0x08]': 2, 'dataMem[0x04]': 456}, {'RB[15]': 0xaaa0, 'RB[13]': 456, 'RB[14]': 2, 'RB[21]': 0x888, 'CPSR' : 0x4444441f})
isa.addInstruction(ldm_Instr)

# LDR instruction family
# Normal load instruction
opCode = cxx_writer.writer_code.Code("""
memLastBits = address & 0x00000003;
// if the memory address is not word aligned I have to rotate the loaded value
if(memLastBits == 0){
    value = dataMem.read_word(address);
}
else{
    value = RotateRight(8*memLastBits, dataMem.read_word(address));
}

//Perform the writeback; as usual I have to behave differently
//if a load a value to the PC
if(rd_bit == 15){
    //I don't consider the 2 less significant bits since I don't bother with
    //thumb mode.
    PC = value & 0xFFFFFFFC;
    stall(4);
    flush();
}
else{
    rd = value;
    stall(2);
}
""")
ldr_imm_Instr = trap.Instruction('LDR_imm', True, frequency = 8)
ldr_imm_Instr.setMachineCode(ls_immOff, {'b': [0], 'l': [1]}, 'TODO')
ldr_imm_Instr.setCode(opCode, 'execute')
ldr_imm_Instr.addBehavior(IncrementPC, 'fetch')
ldr_imm_Instr.addBehavior(condCheckOp, 'execute')
ldr_imm_Instr.addBehavior(ls_imm_Op, 'execute')
ldr_imm_Instr.addVariable(('memLastBits', 'BIT<32>'))
ldr_imm_Instr.addVariable(('value', 'BIT<32>'))
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})
isa.addInstruction(ldr_imm_Instr)
ldr_off_Instr = trap.Instruction('LDR_off', True, frequency = 7)
ldr_off_Instr.setMachineCode(ls_regOff, {'b': [0], 'l': [1]}, 'TODO')
ldr_off_Instr.setCode(opCode, 'execute')
ldr_off_Instr.addBehavior(IncrementPC, 'fetch')
ldr_off_Instr.addBehavior(condCheckOp, 'execute')
ldr_off_Instr.addBehavior(ls_reg_Op, 'execute')
ldr_off_Instr.addVariable(('memLastBits', 'BIT<32>'))
ldr_off_Instr.addVariable(('value', 'BIT<32>'))
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})

ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x10})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x18})
ldr_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123456}, {'REGS[1]' : 123456, 'REGS[0]' : 0x08})
isa.addInstruction(ldr_off_Instr)

# LDRB instruction family [B = 1 ; L = 1]
# Normal load instruction
opCode = cxx_writer.writer_code.Code("""
rd = dataMem.read_byte(address);
stall(2);
""")
ldrb_imm_Instr = trap.Instruction('LDRB_imm', True, frequency = 4)
ldrb_imm_Instr.setMachineCode(ls_immOff, {'b': [1], 'l': [1]}, 'TODO')
ldrb_imm_Instr.setCode(opCode, 'execute')
ldrb_imm_Instr.addBehavior(IncrementPC, 'fetch')
ldrb_imm_Instr.addBehavior(condCheckOp, 'execute')
ldrb_imm_Instr.addBehavior(ls_imm_Op, 'execute')
#Load Register Byte(LDRB): immediate offset address mode [I = 0]

#1 - Immediate offset post-indexed
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})
#2 - Immediate offset pre-indexed addressing
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0}, {'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_imm_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'immediate': 0x8}, {'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})

isa.addInstruction(ldrb_imm_Instr)
ldrb_off_Instr = trap.Instruction('LDRB_off', True, frequency = 4)
ldrb_off_Instr.setMachineCode(ls_regOff, {'b': [1], 'l': [1]}, 'TODO')
ldrb_off_Instr.setCode(opCode, 'execute')
ldrb_off_Instr.addBehavior(IncrementPC, 'fetch')
ldrb_off_Instr.addBehavior(condCheckOp, 'execute')
ldrb_off_Instr.addBehavior(ls_reg_Op, 'execute')
#Load Register Byte(LDRB):  scaled/register offset address mode
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})

ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x0, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 0, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x10]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 0, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x10})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 1, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x18]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x18})
ldrb_off_Instr.addTest({'cond': 0xe, 'p': 1, 'u': 0, 'w': 1, 'rn': 0, 'rd': 1, 'shift_amm': 0, 'shift_op': 0, 'rm': 2}, {'REGS[2]' : 0x8, 'REGS[0]' : 0x10, 'dataMem[0x08]': 123}, {'REGS[1]' : 123, 'REGS[0]' : 0x08})
isa.addInstruction(ldrb_off_Instr)

# LDRH instruction family
opCode = cxx_writer.writer_code.Code("""
rd = dataMem.read_half(address);
stall(2);
""")
ldrh_off_Instr = trap.Instruction('LDRH_off', True, frequency = 3)
ldrh_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 0, 1, 1], 'l': [1]}, 'TODO')
ldrh_off_Instr.setCode(opCode, 'execute')
ldrh_off_Instr.addBehavior(IncrementPC, 'fetch')
ldrh_off_Instr.addBehavior(condCheckOp, 'execute')
ldrh_off_Instr.addBehavior(ls_sh_Op, 'execute')
isa.addInstruction(ldrh_off_Instr)

# LDRS H/B instruction family
opCode = cxx_writer.writer_code.Code("""
rd = dataMem.read_half(address);
stall(2);
""")
ldrsh_off_Instr = trap.Instruction('LDRSH_off', True, frequency = 2)
ldrsh_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 1, 1, 1]}, 'TODO')
ldrsh_off_Instr.setCode(opCode, 'execute')
ldrsh_off_Instr.addBehavior(IncrementPC, 'fetch')
ldrsh_off_Instr.addBehavior(condCheckOp, 'execute')
ldrsh_off_Instr.addBehavior(ls_sh_Op, 'execute')
isa.addInstruction(ldrsh_off_Instr)
opCode = cxx_writer.writer_code.Code("""
rd = dataMem.read_byte(address);
stall(2);
""")
ldrsb_off_Instr = trap.Instruction('LDRSB_off', True, frequency = 2)
ldrsb_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 1, 0, 1]}, 'TODO')
ldrsb_off_Instr.setCode(opCode, 'execute')
ldrsb_off_Instr.addBehavior(IncrementPC, 'fetch')
ldrsb_off_Instr.addBehavior(condCheckOp, 'execute')
ldrsb_off_Instr.addBehavior(ls_sh_Op, 'execute')
isa.addInstruction(ldrsb_off_Instr)

#--------------------------- 
#Mutiply instruction family
#---------------------------
opCode = cxx_writer.writer_code.Code("""
rd = ((int)rm * (int)rs) + (int)REGS[rn];

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(2);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(3);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(4);
}
else{
    stall(5);
}
""")
mla_Instr = trap.Instruction('mla_Instr', True, frequency = 4)
mla_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 0, 0, 1]}, 'TODO')
mla_Instr.setCode(opCode, 'execute')
mla_Instr.addBehavior(IncrementPC, 'fetch')
mla_Instr.addBehavior(condCheckOp, 'execute')
mla_Instr.addBehavior(UpdatePSRmul, 'execute', False)

# Operation
#if ConditionPassed(cond) then
#   Rd = (Rm * Rs + Rn)[31:0]
#   if S == 1 then
#       N Flag = Rd[31]
#       Z Flag = if Rd == 0 then 1 else 0
#       C Flag = unaffected
#       V Flag = unaffected
mla_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]' :0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]' :0x00000005})

mla_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]' :0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]' :0x00000005})

mla_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x80000000,'REGS[10]' :0xffffffff})

mla_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000000}, 
                  {'CPSR': 0x40000000,'REGS[10]' :0x00000000})

mla_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x10000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x10000000})

mla_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x20000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x20000000})
#else 
mla_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x20000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x20000000, 'REGS[10]':0x00000000})
#end if
isa.addInstruction(mla_Instr)

#-------------------
# MUL instruction
#-------------------
opCode = cxx_writer.writer_code.Code("""
rd = (int)rm * (int)rs;

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(1);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(2);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(3);
}
else{
    stall(4);
}
""")
mul_Instr = trap.Instruction('mul_Instr', True, frequency = 4)
mul_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 0, 0, 0]}, 'TODO')
mul_Instr.setCode(opCode, 'execute')
mul_Instr.addBehavior(IncrementPC, 'fetch')
mul_Instr.addBehavior(condCheckOp, 'execute')
mul_Instr.addBehavior(UpdatePSRmul, 'execute', False)
# Operation
#if ConditionPassed(cond) then
#   Rd = (Rm * Rs)[31:0]
#   if S == 1 then
#       N Flag = Rd[31]
#       Z Flag = if Rd == 0 then 1 else 0
#       C Flag = unaffected
#       V Flag = unaffected
mul_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rm': 9, 'rs': 8}, 
                  {'REGS[10]' :0x00000000,'REGS[9]' : 0x00000002,'REGS[8]' : 0x00000002}, 
                  {'REGS[10]' :0x00000004})

mul_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rm': 9, 'rs': 8}, 
                  {'REGS[10]' :0x00000000,'REGS[9]' : 0x00000002,'REGS[8]' : 0x00000002}, 
                  {'REGS[10]' :0x00000004})

mul_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rm': 9, 'rs': 8}, 
                  {'CPSR': 0x00000000,'REGS[10]' :0x00000000,'REGS[9]' : 0xffffffff,'REGS[8]' : 0x00000001}, 
                  {'CPSR': 0x80000000,'REGS[10]' :0xffffffff})

mul_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10,'rm': 9, 'rs': 8}, 
                  {'CPSR': 0x00000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000}, 
                  {'CPSR': 0x40000000,'REGS[10]' :0x00000000})

mul_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10,'rm': 9, 'rs': 8}, 
                  {'CPSR': 0x10000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000002,'REGS[8]' : 0x00000002}, 
                  {'CPSR': 0x10000000})

mul_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10,'rm': 9, 'rs': 8}, 
                  {'CPSR': 0x20000000,'REGS[10]' :0x00000000,'REGS[9]' : 0x00000002,'REGS[8]' : 0x00000002}, 
                  {'CPSR': 0x20000000})
#else 
mul_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x20000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x20000000, 'REGS[10]':0x00000000})
#end if
isa.addInstruction(mul_Instr)
#-------------------
# SMLAL instruction
#-------------------
opCode = cxx_writer.writer_code.Code("""
//Perform the operation
long long result = (long long)((((long long)(((long long)((int)rm)) * ((long long)((int)rs)))) + (((long long)rd) << 32)) + (int)REGS[rn]);
//Check if I have to update the processor flags
rd = (int)((result >> 32) & 0x00000000FFFFFFFF);
REGS[rn] = (int)(result & 0x00000000FFFFFFFF);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
smlal_Instr = trap.Instruction('smlal_Instr', True, frequency = 3)
smlal_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 1, 1]}, 'TODO')
smlal_Instr.setCode(opCode, 'execute')
smlal_Instr.addBehavior(IncrementPC, 'fetch')
smlal_Instr.addBehavior(condCheckOp, 'execute')
smlal_Instr.addBehavior(UpdatePSRmul, 'execute', False)
#Operation
#if ConditionPassed(cond) then
#    RdLo = (Rm * Rs)[31:0] + RdLo /* Signed multiplication */
#    RdHi = (Rm * Rs)[63:32] + RdHi + CarryFrom((Rm * Rs)[31:0] + RdLo)
smlal_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000004})
smlal_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000000b,'REGS[9]' : 0x00000002,'REGS[8]' : 0x7fffffff,'REGS[7]' : 0x00000008}, 
                  {'REGS[10]': 0x0000000e,'REGS[9]' : 0xfffffffa})
#    if S == 1 then
#        N Flag = RdHi[31]
#        Z Flag = if (RdHi == 0) and (RdLo == 0) then 1 else 0
#        C Flag = unaffected
#        V Flag = unaffected
smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0xf000000b,'REGS[9]' : 0x00000002,'REGS[8]' : 0x7fffffff,'REGS[7]' : 0x00000008}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0xf000000e,'REGS[9]' : 0xfffffffa})

smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000000}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0xffffffff,'REGS[8]' : 0x00000001,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000001})

smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})

#Failed case
smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001})

#The SMLALS instruction is defined to leave the C and V flags unchanged 
#in ARM  architecture version 5 and above. 
smlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0xfffffff0,'REGS[9]' : 0x00000002,'REGS[8]' : 0x7fffffff,'REGS[7]' : 0x00000008}, 
                  {'CPSR': 0xb0000000, 'REGS[10]': 0xfffffff3,'REGS[9]' : 0xfffffffa})
#else
smlal_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000 })
#endif
isa.addInstruction(smlal_Instr)
#-------------------
# SMULL instruction
#-------------------
opCode = cxx_writer.writer_code.Code("""
//Perform the operation
long long result = (long long)(((long long)((int)rm)) * ((long long)((int)rs)));
//Check if I have to update the processor flags
rd = (int)((result >> 32) & 0x00000000FFFFFFFF);
REGS[rn] = (int)(result & 0x00000000FFFFFFFF);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
smull_Instr = trap.Instruction('smull_Instr', True, frequency = 3)
smull_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 1, 0]}, 'TODO')
smull_Instr.setCode(opCode, 'execute')
smull_Instr.addBehavior(IncrementPC, 'fetch')
smull_Instr.addBehavior(condCheckOp, 'execute')
smull_Instr.addBehavior(UpdatePSRmul, 'execute', False)
#Operation
#if ConditionPassed(cond) then
#    RdLo = (Rm * Rs)[31:0] /* Signed multiplication */
#    RdHi = (Rm * Rs)[63:32]
smull_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x00000000,'REGS[9]' : 0x00000004})
smull_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000000b,'REGS[9]' : 0x00000002,'REGS[8]' : 0x7fffffff,'REGS[7]' : 0x00000008}, 
                  {'REGS[10]': 0x00000003,'REGS[9]' : 0xfffffff8})
#    if S == 1 then
#        N Flag = RdHi[31]
#        Z Flag = if (RdHi == 0) and (RdLo == 0) then 1 else 0
#        C Flag = unaffected
#        V Flag = unaffected
smull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0xfffffffe,'REGS[7]' : 0x00000008}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0xfffffff0})

smull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000000}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

smull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x20000000,'REGS[7]' : 0x00000008}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})
# Failed case
smull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000003,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000006})
#The SMLALS instruction is defined to leave the C and V flags unchanged 
#in ARM  architecture version 5 and above. 
smull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0xb0000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0xfffffffe})
#else
smull_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000 })
#endif
isa.addInstruction(smull_Instr)

#-------------------
# UMLAL instruction
#-------------------
opCode = cxx_writer.writer_code.Code("""
//Perform the operation
unsigned long long result = (unsigned long long)(((unsigned long long)(((unsigned long long)((unsigned int)rm)) * ((unsigned long long)((unsigned int)rs)))) + (((unsigned long long)rd) << 32) + (unsigned int)REGS[rn]);
//Check if I have to update the processor flags
rd = (unsigned int)((result >> 32) & 0x00000000FFFFFFFF);
REGS[rn] = (unsigned int)(result & 0x00000000FFFFFFFFLL);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
umlal_Instr = trap.Instruction('umlal_Instr', True, frequency = 3)
umlal_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 0, 1]}, 'TODO')
umlal_Instr.setCode(opCode, 'execute')
umlal_Instr.addBehavior(IncrementPC, 'fetch')
umlal_Instr.addBehavior(condCheckOp, 'execute')
umlal_Instr.addBehavior(UpdatePSRmul, 'execute', False)
#if ConditionPassed(cond) then
#    RdLo = (Rm * Rs)[31:0] + RdLo    /* Unsigned multiplication */
#    RdHi = (Rm * Rs)[63:32] + RdHi + CarryFrom((Rm * Rs)[31:0] + RdLo)
umlal_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000005})
umlal_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000000b,'REGS[9]' : 0x00000002,'REGS[8]' : 0x80000000,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x0000000c,'REGS[9]' : 0x00000002})
#    if S == 1 then
#        N Flag = RdHi[31]
umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000005})

umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x80000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0x80000000,'REGS[9]' : 0x00000005})

#        Z Flag = if (RdHi == 0) and (RdLo == 0) then 1 else 0
umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000000}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0xffffffff,'REGS[8]' : 0x00000001,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000001})

umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})
#Failed case
umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000001})
#        C Flag = unaffected unaffected
#        V Flag = unaffected unaffected
umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0xffffffff,'REGS[8]' : 0x00000001,'REGS[7]' : 0x00000001}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})
#Failed case
umlal_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0xffffffff})
#else
umlal_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000,'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x30000000,'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000 })
#end
isa.addInstruction(umlal_Instr)
#-------------------
# UMULL instruction
#-------------------
opCode = cxx_writer.writer_code.Code("""
//Perform the operation
unsigned long long result = (unsigned long long)(((unsigned long long)((unsigned int)rm)) * ((unsigned long long)((unsigned int)rs)));
//Check if I have to update the processor flags
rd = (unsigned int)((result >> 32) & 0x00000000FFFFFFFF);
REGS[rn] = (unsigned int)(result & 0x00000000FFFFFFFFLL);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
umull_Instr = trap.Instruction('umull_Instr', True, frequency = 3)
umull_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 0, 0]}, 'TODO')
umull_Instr.setCode(opCode, 'execute')
umull_Instr.addBehavior(IncrementPC, 'fetch')
umull_Instr.addBehavior(condCheckOp, 'execute')
umull_Instr.addBehavior(UpdatePSRmul, 'execute', False)

#if ConditionPassed(cond) then
#    RdHi = (Rm * Rs)[63:32]    /* Unsigned multiplication */
#    RdLo = (Rm * Rs)[31:0]
umull_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000ffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x00000000,'REGS[9]' : 0x00000004})
umull_Instr.addTest({'cond' : 0xe, 's': 0, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'REGS[10]': 0x0000000b,'REGS[9]' : 0x00000002,'REGS[8]' : 0x80000000,'REGS[7]' : 0x00000002}, 
                  {'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})
#    if S == 1 then
#        N Flag = RdHi[31]

# Failed case
umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0xf0000000,'REGS[9]' : 0x00000001,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000004})

umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0xffffffff,'REGS[7]' : 0xffffffff}, 
                  {'CPSR': 0x80000000, 'REGS[10]': 0xfffffffe,'REGS[9]' : 0x00000001})
#        Z Flag = if (RdHi == 0) and (RdLo == 0) then 1 else 0
umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000000,'REGS[7]' : 0x00000000}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000})

umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x20000000,'REGS[7]' : 0x00000008}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0x00000000})
# Failed case
umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x40000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000003,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x00000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000006})
#        C Flag = unaffected    /* See "C and V flags" note */
#        V Flag = unaffected    /* See "C and V flags" note */
umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0xffffffff,'REGS[9]' : 0x00000001,'REGS[8]' : 0xffffffff,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000001,'REGS[9]' : 0xfffffffe})
umull_Instr.addTest({'cond' : 0xe, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000, 'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0xffffffff,'REGS[7]' : 0xffffffff}, 
                  {'CPSR': 0xb0000000, 'REGS[10]': 0xfffffffe,'REGS[9]' : 0x00000001})
#else
umlal_Instr.addTest({'cond' : 0x0, 's': 1, 'rd' : 10, 'rn' : 9, 'rm': 8, 'rs': 7}, 
                  {'CPSR': 0x30000000,'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000,'REGS[8]' : 0x00000002,'REGS[7]' : 0x00000002}, 
                  {'CPSR': 0x30000000,'REGS[10]': 0x00000000,'REGS[9]' : 0x00000000 })
isa.addInstruction(umull_Instr)
# MOV instruction family
opCode = cxx_writer.writer_code.Code("""
rd = operand;
result = operand;
""")
mov_shift_imm_Instr = trap.Instruction('MOV_si', True, frequency = 8)
mov_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_shift_imm_Instr.setCode(opCode, 'execute')
mov_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
mov_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
mov_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
mov_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
mov_shift_imm_Instr.addVariable(('result', 'BIT<32>'))

#if ConditionPassed(cond) then
#    Rd = shifter_operand
#    if S == 1 and Rd == R15 then
#    	CPSR = SPSR
#
#    else if S == 1 then
#    	N Flag = Rd[31]
#    	Z Flag = if Rd == 0 then 1 else 0
#    	C Flag = shifter_carry_out
#    	V Flag = unaffected
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 3})
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffff})
# Rd=0 then Z flag=1
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[8]': 0}, {'CPSR' : 0x40000000, 'REGS[10]': 0}) 
# Rd different from 0 then Z flag=0
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
#shift_imm > 0
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 3}, {'CPSR' : 0x00000000, 'REGS[10]': 6})
#S=0
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000,'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 3})
#else Condition Faild : do not update CPSR
mov_shift_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000,'REGS[8]': 3}, {'CPSR' : 0x20000000})
#endif
#logical shift right
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[8]': 3}, {'CPSR' : 0x40000000, 'REGS[10]': 0}) 
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 1})
#arithmetic shift right
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[8]': 3}, {'CPSR' : 0x40000000, 'REGS[10]': 0}) 
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})  
#Rotate right by immediate
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 1})
mov_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[8]': 3}, {'CPSR' : 0xa0000000, 'REGS[10]': 0x80000001})

isa.addInstruction(mov_shift_imm_Instr)

mov_shift_reg_Instr = trap.Instruction('MOV_sr', True, frequency = 8)
mov_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_shift_reg_Instr.setCode(opCode, 'execute')
mov_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
mov_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
mov_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
mov_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
mov_shift_reg_Instr.addVariable(('result', 'BIT<32>'))

#Logical shift left by register
#if S == 1 then
#    	N Flag = Rd[31]
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0x00000000, 'REGS[10]': 6})
#    	Z Flag = if Rd == 0 then 1 else 0
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 3}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x40000000, 'REGS[10]': 0})
#S=0 do not update CPSR
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':0, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x00000000, 'REGS[10]': 0})
#condition does not satisfied
mov_shift_reg_Instr.addTest({'cond': 0x0, 's':0, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x80000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x80000000})
#Logical shift right by register
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 1})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x40000000, 'REGS[10]': 0})
#Arithmetic shift right by register
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 1})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 0xf0000000}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[0]': 32, 'REGS[8]': 3}, {'CPSR' : 0x40000000, 'REGS[10]': 0})
#Rotate right by register
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mov_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0xa0000000, 'REGS[10]': 0x80000001})

isa.addInstruction(mov_shift_reg_Instr)

mov_imm_Instr = trap.Instruction('MOV_i', True, frequency = 8)
mov_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_imm_Instr.setCode(opCode, 'execute')
mov_imm_Instr.addBehavior(IncrementPC, 'fetch')
mov_imm_Instr.addBehavior(condCheckOp, 'execute')
mov_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
mov_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_imm_Instr.addBehavior(UpdatePC, 'execute', False)
mov_imm_Instr.addVariable(('result', 'BIT<32>'))

mov_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'CPSR' : 0x20000000}, {'CPSR' : 0x20000000, 'REGS[10]':3})
mov_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'CPSR' : 0x20000000}, {'CPSR' : 0x00000000, 'REGS[10]':0x3f0})
mov_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'CPSR' : 0x20000000}, {'CPSR' : 0x20000000, 'REGS[10]':0x3f0})
mov_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'CPSR' : 0x20000000}, {'CPSR' : 0x20000000 })
isa.addInstruction(mov_imm_Instr)

# MRS instruction
opCode = cxx_writer.writer_code.Code("""
if(r == 1){ // I have to save the SPSR
    switch(CPSR[key_mode]){
        case 0x1:{
            //I'm in FIQ mode
            rd = SPSR[0];
            break;}
        case 0x2:{
            //I'm in IRQ mode
            rd = SPSR[1];
            break;}
        case 0x3:{
            //I'm in SVC mode
            rd = SPSR[2];
            break;}
        case 0x7:{
            //I'm in ABT mode
            rd = SPSR[3];
            break;}
        case 0xB:{
            //I'm in UND mode
            rd = SPSR[4];
            break;}
        default:
            break;
    }
}
else{
    // I have to save the CPSR
    rd = CPSR;
}
""")
mrs_Instr = trap.Instruction('mrs_Instr', True, frequency = 3)
mrs_Instr.setMachineCode(move_imm2psr, {'opcode0': [0, 0, 0, 1, 0], 'opcode1': [0, 0], 'mask': [1, 1, 1, 1], 'rotate': [0, 0, 0, 0], 'immediate': [0, 0, 0, 0, 0, 0, 0, 0]}, 'TODO')
mrs_Instr.setCode(opCode, 'execute')
mrs_Instr.addBehavior(IncrementPC, 'fetch')
mrs_Instr.addBehavior(condCheckOp, 'execute')
mrs_Instr.setVarField('rd', ('REGS', 0), 'out')
isa.addInstruction(mrs_Instr)

# MSR instruction family
opCode = cxx_writer.writer_code.Code("""
value = RotateRight(rotate*2, immediate);
//Checking for unvalid bits
if((value & 0x00000010) == 0){
    THROW_EXCEPTION("MSR called with unvalid mode " << std::hex << std::showbase << value << ": we are trying to switch to 26 bit PC");
}
unsigned int currentMode = CPSR[key_mode];
//Firs of all I check whether I have to modify the CPSR or the SPSR
if(r == 0){
    //CPSR
    //Now I modify the fields; note that in user mode I can just update the flags.
    if((mask & 0x1) != 0 && currentMode != 0){
        CPSR &= 0xFFFFFF00;
        CPSR |= value & 0x000000FF;
        //Now if I change mode I also have to update the registry bank
        if(currentMode != (CPSR & 0x0000000F)){
            restoreSPSR();
        }
    }
    if((mask & 0x2) != 0 && currentMode != 0){
        CPSR &= 0xFFFF00FF;
        CPSR |= value & 0x0000FF00;
    }
    if((mask & 0x4) != 0 && currentMode != 0){
        CPSR &= 0xFF00FFFF;
        CPSR |= value & 0x00FF0000;
    }
    if((mask & 0x8) != 0){
        CPSR &= 0x00FFFFFF;
        CPSR |= value & 0xFF000000;
    }
}
else{
    //SPSR
    switch(currentMode){
        case 0x1:{
            //I'm in FIQ mode
            if((mask & 0x1) != 0){
                SPSR[0] &= 0xFFFFFF00;
                SPSR[0] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[0] &= 0xFFFF00FF;
                SPSR[0] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[0] &= 0xFF00FFFF;
                SPSR[0] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[0] &= 0x00FFFFFF;
                SPSR[0] |= value & 0xFF000000;
            }
            break;}
        case 0x2:{
            //I'm in IRQ mode
            if((mask & 0x1) != 0){
                SPSR[1] &= 0xFFFFFF00;
                SPSR[1] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[1] &= 0xFFFF00FF;
                SPSR[1] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[1] &= 0xFF00FFFF;
                SPSR[1] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[1] &= 0x00FFFFFF;
                SPSR[1] |= value & 0xFF000000;
            }
            break;}
        case 0x3:{
            //I'm in SVC mode
            if((mask & 0x1) != 0){
                SPSR[2] &= 0xFFFFFF00;
                SPSR[2] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[2] &= 0xFFFF00FF;
                SPSR[2] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[2] &= 0xFF00FFFF;
                SPSR[2] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[2] &= 0x00FFFFFF;
                SPSR[2] |= value & 0xFF000000;
            }
            break;}
        case 0x7:{
            //I'm in ABT mode
            if((mask & 0x1) != 0){
                SPSR[3] &= 0xFFFFFF00;
                SPSR[3] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[3] &= 0xFFFF00FF;
                SPSR[3] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[3] &= 0xFF00FFFF;
                SPSR[3] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[3] &= 0x00FFFFFF;
                SPSR[3] |= value & 0xFF000000;
            }
            break;}
        case 0xB:{
            //I'm in UND mode
            if((mask & 0x1) != 0){
                SPSR[4] &= 0xFFFFFF00;
                SPSR[4] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[4] &= 0xFFFF00FF;
                SPSR[4] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[4] &= 0xFF00FFFF;
                SPSR[4] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[4] &= 0x00FFFFFF;
                SPSR[4] |= value & 0xFF000000;
            }
            break;}
        default:
            break;
    }
}
""")
msr_imm_Instr = trap.Instruction('msr_imm_Instr', True, frequency = 3)
msr_imm_Instr.setMachineCode(move_imm2psr, {'opcode0': [0, 0, 1, 1, 0], 'opcode1': [1, 0], 'rd': [1, 1, 1, 1]}, 'TODO')
msr_imm_Instr.setCode(opCode, 'execute')
msr_imm_Instr.addBehavior(IncrementPC, 'fetch')
msr_imm_Instr.addBehavior(condCheckOp, 'execute')
msr_imm_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(msr_imm_Instr)

opCode = cxx_writer.writer_code.Code("""
//Checking for unvalid bits
if((rm & 0x00000010) == 0){
    THROW_EXCEPTION("MSR called with unvalid mode " << std::hex << std::showbase << rm << ": we are trying to switch to 26 bit PC");
}
unsigned int currentMode = CPSR[key_mode];
//Firs of all I check whether I have to modify the CPSR or the SPSR
if(r == 0){
    //CPSR
    //Now I modify the fields; note that in user mode I can just update the flags.
    if((mask & 0x1) != 0 && currentMode != 0){
        CPSR &= 0xFFFFFF00;
        CPSR |= rm & 0x000000FF;
        //Now if I change mode I also have to update the registry bank
        if(currentMode != (CPSR & 0x0000000F)){
            restoreSPSR();
        }
    }
    if((mask & 0x2) != 0 && currentMode != 0){
        CPSR &= 0xFFFF00FF;
        CPSR |= rm & 0x0000FF00;
    }
    if((mask & 0x4) != 0 && currentMode != 0){
        CPSR &= 0xFF00FFFF;
        CPSR |= rm & 0x00FF0000;
    }
    if((mask & 0x8) != 0){
        CPSR &= 0x00FFFFFF;
        CPSR |= rm & 0xFF000000;
    }
}
else{
    //SPSR
    switch(currentMode){
        case 0x1:{
            //I'm in FIQ mode
            if((mask & 0x1) != 0){
                SPSR[0] &= 0xFFFFFF00;
                SPSR[0] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[0] &= 0xFFFF00FF;
                SPSR[0] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[0] &= 0xFF00FFFF;
                SPSR[0] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[0] &= 0x00FFFFFF;
                SPSR[0] |= rm & 0xFF000000;
            }
            break;}
        case 0x2:{
            //I'm in IRQ mode
            if((mask & 0x1) != 0){
                SPSR[1] &= 0xFFFFFF00;
                SPSR[1] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[1] &= 0xFFFF00FF;
                SPSR[1] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[1] &= 0xFF00FFFF;
                SPSR[1] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[1] &= 0x00FFFFFF;
                SPSR[1] |= rm & 0xFF000000;
            }
            break;}
        case 0x3:{
            //I'm in SVC mode
            if((mask & 0x1) != 0){
                SPSR[2] &= 0xFFFFFF00;
                SPSR[2] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[2] &= 0xFFFF00FF;
                SPSR[2] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[2] &= 0xFF00FFFF;
                SPSR[2] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[2] &= 0x00FFFFFF;
                SPSR[2] |= rm & 0xFF000000;
            }
            break;}
        case 0x7:{
            //I'm in ABT mode
            if((mask & 0x1) != 0){
                SPSR[3] &= 0xFFFFFF00;
                SPSR[3] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[3] &= 0xFFFF00FF;
                SPSR[3] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[3] &= 0xFF00FFFF;
                SPSR[3] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[3] &= 0x00FFFFFF;
                SPSR[3] |= rm & 0xFF000000;
            }
            break;}
        case 0xB:{
            //I'm in UND mode
            if((mask & 0x1) != 0){
                SPSR[4] &= 0xFFFFFF00;
                SPSR[4] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[4] &= 0xFFFF00FF;
                SPSR[4] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[4] &= 0xFF00FFFF;
                SPSR[4] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[4] &= 0x00FFFFFF;
                SPSR[4] |= rm & 0xFF000000;
            }
            break;}
        default:
            break;
    }
}
""")
msr_reg_Instr = trap.Instruction('msr_reg_Instr', True, frequency = 3)
msr_reg_Instr.setMachineCode(move_imm2psr_reg, {'opcode0': [0, 0, 0, 1, 0], 'opcode1': [1, 0]}, 'TODO')
msr_reg_Instr.setCode(opCode, 'execute')
msr_reg_Instr.addBehavior(IncrementPC, 'fetch')
msr_reg_Instr.addBehavior(condCheckOp, 'execute')
isa.addInstruction(msr_reg_Instr)

# MVN instruction family
opCode = cxx_writer.writer_code.Code("""
result = ~operand;
rd = result;
""")
mvn_shift_imm_Instr = trap.Instruction('MVN_si', True, frequency = 4)
mvn_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 1, 1]}, 'TODO')
mvn_shift_imm_Instr.setCode(opCode, 'execute')
mvn_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
mvn_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
mvn_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
mvn_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mvn_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
mvn_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
#if ConditionPassed(cond) then
#    Rd = NOT shifter_operand
#    if S == 1 and Rd == R15 then
#        CPSR = SPSR
#    else if S == 1 then
#        N Flag = Rd[31]
#        Z Flag = if Rd == 0 then 1 else 0
#        C Flag = shifter_carry_out
#        V Flag = unaffected
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 1}, {'CPSR' : 0xa0000000, 'REGS[10]':0xfffffffe})
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x40000000, 'REGS[10]':0})
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x20000000, 'REGS[10]':1})
# S=0 do not update CPSR
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x20000000, 'REGS[10]':1})
# condition falied
mvn_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x20000000 })
#Logical shift right by immediate
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[8]': 1}, {'CPSR' : 0x80000000, 'REGS[10]':0xffffffff})
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[8]': 0xffffffff}, {'CPSR' : 0xa0000000, 'REGS[10]':0x80000000})
#arithmetic shift right by immediate
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[8]': 3}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffff}) 
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[8]': 0xf0000000}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[8]': 1}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff}) 
#Rotate right by immediate
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[8]': 3}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xfffffffe})
mvn_shift_imm_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 0x7ffffffe})
isa.addInstruction(mvn_shift_imm_Instr)

mvn_shift_reg_Instr = trap.Instruction('MVN_sr', True, frequency = 4)
mvn_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 1, 1]}, 'TODO')
mvn_shift_reg_Instr.setCode(opCode, 'execute')
mvn_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
mvn_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
mvn_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
mvn_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mvn_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
mvn_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
# if S == 1 then
#	N Flag = Rd[31]
#	Z Flag = if Rd == 0 then 1 else 0
#	C Flag = shifter_carry_out
#	V Flag = unaffected

#logical shift left by register
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x20000000, 'REGS[10]': 1})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 3}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 33, 'REGS[8]': 2}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffff})
#S=0 do not update CPSR
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':0, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 33, 'REGS[8]': 2}, {'CPSR' : 0x00000000, 'REGS[10]': 0xffffffff})
#condition does not satisfied
mvn_shift_reg_Instr.addTest({'cond': 0x0, 's':0, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x80000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x80000000})
#Logical shift right by register
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xfffffffe})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 0xabcdefab}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xffffffff})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[0]': 33, 'REGS[8]': 3}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffff})
#Arithmetic shift right by register
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x40000000, 'REGS[10]': 0})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 1, 'REGS[8]': 7}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xfffffffc})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[0]': 2, 'REGS[8]': 7}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xfffffffe})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[0]': 32, 'REGS[8]': 0xf0000000}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[0]': 32, 'REGS[8]': 3}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffff})
#Rotate right by register
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
mvn_shift_reg_Instr.addTest({'cond': 0xe, 's':1, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'CPSR' : 0x00000000, 'REGS[0]': 1, 'REGS[8]': 3}, {'CPSR' : 0x20000000, 'REGS[10]': 0x7ffffffe})
isa.addInstruction(mvn_shift_reg_Instr)

mvn_imm_Instr = trap.Instruction('MVN_i', True, frequency = 4)
mvn_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 1, 1]}, 'TODO')
mvn_imm_Instr.setCode(opCode, 'execute')
mvn_imm_Instr.addBehavior(IncrementPC, 'fetch')
mvn_imm_Instr.addBehavior(condCheckOp, 'execute')
mvn_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
mvn_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mvn_imm_Instr.addBehavior(UpdatePC, 'execute', False)
mvn_imm_Instr.addVariable(('result', 'BIT<32>'))
mvn_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'CPSR' : 0x20000000}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xfffffffc})
mvn_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rd': 10, 'rotate': 1, 'immediate': 0xfc}, {'CPSR' : 0x20000000}, {'CPSR' : 0x80000000, 'REGS[10]': 0xffffffc0})
#S=0 do not update CPSR
mvn_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'CPSR' : 0x20000000}, {'CPSR' : 0x20000000, 'REGS[10]': 0xfffffffc})
#condition does not satisfied
mvn_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'CPSR' : 0x20000000}, {'CPSR' : 0x20000000 })
isa.addInstruction(mvn_imm_Instr)

# ORR instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn | operand;
rd = result;
""")
#if ConditionPassed(cond) then
#    Rd = Rn OR shifter_operand
#    if S == 1 and Rd == R15 then
#        CPSR = SPSR
#    else if S == 1 then
#       N Flag = Rd[31]
#        Z Flag = if Rd == 0 then 1 else 0
#        C Flag = shifter_carry_out
#        V Flag = unaffected
orr_shift_imm_Instr = trap.Instruction('ORR_si', True, frequency = 5)
orr_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 0, 0]}, 'TODO')
orr_shift_imm_Instr.setCode(opCode, 'execute')
orr_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
orr_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
orr_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
orr_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
orr_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
orr_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
#Logical shift left by immediate
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 6, 'REGS[8]': 9}, {'REGS[10]': 15, 'CPSR' : 0x20000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 0, 'REGS[8]': 0}, {'REGS[10]': 0, 'CPSR' : 0x40000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 0xffffffff, 'REGS[8]': 0}, {'REGS[10]': 0xffffffff, 'CPSR' : 0xa0000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'REGS[10]': 0xffffffff, 'CPSR' : 0x80000000})
#S=0 do not update CPSR
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'REGS[10]': 0xffffffff, 'CPSR' : 0x20000000})
#condition does not satisfied
orr_shift_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR' : 0x20000000})
#Logical shift right by immediate
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'CPSR' : 0x00000000, 'REGS[9]': 5, 'REGS[8]': 0xffffffff}, {'REGS[10]': 5, 'CPSR' : 0x20000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'CPSR' : 0x20000000, 'REGS[9]': 5, 'REGS[8]': 6}, {'REGS[10]': 7, 'CPSR' : 0x00000000})
#arithmetic shift right by immediate
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x20000000, 'REGS[9]': 5, 'REGS[8]': 6}, {'REGS[10]': 5, 'CPSR' : 0x00000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'CPSR' : 0x00000000, 'REGS[9]': 5, 'REGS[8]': 0xf0000000}, {'REGS[10]': 0xffffffff, 'CPSR' : 0xa0000000})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 4, 'REGS[8]': 2}, {'REGS[10]': 5})
#Rotate right by immediate
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'REGS[9]': 6, 'REGS[8]': 2}, {'REGS[10]': 7})
orr_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 3}, {'REGS[9]': 15, 'REGS[8]': 1}, {'REGS[10]': 0x8000000f})
isa.addInstruction(orr_shift_imm_Instr)

orr_shift_reg_Instr = trap.Instruction('ORR_sr', True, frequency = 5)
orr_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 0, 0]}, 'TODO')
orr_shift_reg_Instr.setCode(opCode, 'execute')
orr_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
orr_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
orr_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
orr_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
orr_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
orr_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
#logical shift left by register
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[9]': 0xf0000000, 'REGS[8]': 9}, {'CPSR' : 0xa0000000, 'REGS[10]': 0xf0000009})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0, 'REGS[9]': 0, 'REGS[8]': 0}, {'CPSR' : 0x40000000, 'REGS[10]': 0})
#S=0 do not update CPSR
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'CPSR' : 0x20000000, 'REGS[10]': 0xffffffff})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 45, 'REGS[8]': 3}, {'REGS[10]': 45})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 34, 'REGS[8]': 3}, {'REGS[10]': 34})
#condition does not satisfied
orr_shift_reg_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'CPSR' : 0x20000000})
#Logical shift right by register
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 4, 'REGS[8]': 3}, {'REGS[10]': 7})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 4, 'REGS[8]': 3}, {'REGS[10]': 5})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 4, 'REGS[8]': 3}, {'REGS[10]': 4})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 45, 'REGS[8]': 3}, {'REGS[10]': 45})
#Arithmetic shift right by register
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': 14})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': 5})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': 4})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 45, 'REGS[8]': 0xf000f000}, {'REGS[10]': 0xffffffff})
#Rotate right by register
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0, 'REGS[9]': 5, 'REGS[8]': 10}, {'REGS[10]': 15})
orr_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 2, 'REGS[9]': 5, 'REGS[8]': 10}, {'REGS[10]': 0x80000007})
isa.addInstruction(orr_shift_reg_Instr)

orr_imm_Instr = trap.Instruction('ORR_i', True, frequency = 5)
orr_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 0, 0]}, 'TODO')
orr_imm_Instr.setCode(opCode, 'execute')
orr_imm_Instr.addBehavior(IncrementPC, 'fetch')
orr_imm_Instr.addBehavior(condCheckOp, 'execute')
orr_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
orr_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
orr_imm_Instr.addBehavior(UpdatePC, 'execute', False)
orr_imm_Instr.addVariable(('result', 'BIT<32>'))
orr_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rotate': 1, 'immediate': 0xfc}, {'CPSR' : 0x20000000, 'REGS[9]': 0xc0}, {'CPSR' : 0x00000000, 'REGS[10]': 0xff})
#S=0 do not update CPSR
orr_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 3})
orr_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 0x3f3})
#condition does not satisfied
orr_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rotate': 1, 'immediate': 0xfc}, {'CPSR' : 0x20000000, 'REGS[9]': 1}, {'CPSR' : 0x20000000})
isa.addInstruction(orr_imm_Instr)

# RSB instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)operand - (int)rn;
""")
#if ConditionPassed(cond) then
#    Rd = shifter_operand - Rn
#    if S == 1 and Rd == R15 then
#       CPSR = SPSR
#   else if S == 1 then
#       N Flag = Rd[31]
#       Z Flag = if Rd == 0 then 1 else 0
#       C Flag = NOT BorrowFrom(shifter_operand - Rn)
#       V Flag = OverflowFrom(shifter_operand - Rn)
rsb_shift_imm_Instr = trap.Instruction('RSB_si', True, frequency = 4)
rsb_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 1, 1]}, 'TODO')
rsb_shift_imm_Instr.setCode(opCode, 'execute')
rsb_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
rsb_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
rsb_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
rsb_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsb_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
#Logical shift left by immediate
#Z Flag = if Rd == 0 then 1 else 0
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 0, 'CPSR' : 0x60000000})
#C Flag = NOT BorrowFrom(shifter_operand - Rn)
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[9]': 1, 'REGS[8]': 0xffffffff}, {'REGS[10]':0xfffffffe, 'CPSR' : 0x00000000})
#V Flag = OverflowFrom(shifter_operand - Rn)
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 1, 'REGS[8]': 0x80000000}, {'REGS[10]': 0x7fffffff, 'CPSR' : 0x90000000})
#S=0 do not update CPSR
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 9, 'REGS[8]': 10}, {'REGS[10]': 1})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': -2, 'REGS[8]': 3}, {'REGS[10]': 5})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 1, 'REGS[8]': 2}, {'REGS[10]': 3})
#condition does not satisfied
rsb_shift_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 1, 'REGS[8]': 0x80000000}, {'CPSR' : 0x20000000})
#Logical shift right by immediate
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 5, 'REGS[8]': 4}, {'REGS[10]': -5})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 6}, {'REGS[10]': 0})
#arithmetic shift right by immediate
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': -2, 'REGS[8]': 6}, {'REGS[10]': 2})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 1, 'REGS[8]': 0xf0000000}, {'REGS[10]': 0xfffffffe})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 0, 'REGS[8]': 2}, {'REGS[10]': 1})
#Rotate right by immediate
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'REGS[9]': 6, 'REGS[8]': 0}, {'REGS[10]': -6})
rsb_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 3}, {'REGS[9]': 1, 'REGS[8]': 1}, {'REGS[10]': 0x7fffffff})
isa.addInstruction(rsb_shift_imm_Instr)

rsb_shift_reg_Instr = trap.Instruction('RSB_sr', True, frequency = 4)
rsb_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 1, 1]}, 'TODO')
rsb_shift_reg_Instr.setCode(opCode, 'execute')
rsb_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
rsb_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
rsb_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
rsb_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsb_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
#logical shift left by register
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x00000000, 'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'CPSR' : 0x60000000, 'REGS[10]': 0})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[9]': 1, 'REGS[8]': 0xffffffff}, {'CPSR' : 0x00000000, 'REGS[10]': 0xfffffffe})
#S=0 do not update CPSR
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 0, 'REGS[9]': -1, 'REGS[8]': 2}, {'CPSR' : 0x20000000, 'REGS[10]': 3})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1, 'REGS[9]': 2, 'REGS[8]': 1}, {'REGS[10]': 0})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 45, 'REGS[8]': 3}, {'REGS[10]': -45})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 34, 'REGS[8]': 3}, {'REGS[10]': -34})
#condition does not satisfied
rsb_shift_reg_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[0]': 1, 'REGS[9]': 0xffffffff, 'REGS[8]': 1}, {'CPSR' : 0x20000000})
#Logical shift right by register
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 0x7fffffff, 'REGS[8]': 0}, {'REGS[10]': 0x80000001})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 8}, {'REGS[10]': 1})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 4, 'REGS[8]': 3}, {'REGS[10]': -4})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': -4, 'REGS[8]': 3}, {'REGS[10]': 4})
#Arithmetic shift right by register
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': 6})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': 1})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 4, 'REGS[8]': 10}, {'REGS[10]': -4})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 0xf, 'REGS[8]': 0xf000f000}, {'REGS[10]': 0xfffffff0})
#Rotate right by register
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0, 'REGS[9]': 5, 'REGS[8]': 10}, {'REGS[10]': 5})
rsb_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 2, 'REGS[9]': 2, 'REGS[8]': 10}, {'REGS[10]': 0x80000000})
isa.addInstruction(rsb_shift_reg_Instr)

rsb_imm_Instr = trap.Instruction('RSB_i', True, frequency = 4)
rsb_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 1, 1]}, 'TODO')
rsb_imm_Instr.setCode(opCode, 'execute')
rsb_imm_Instr.addBehavior(IncrementPC, 'fetch')
rsb_imm_Instr.addBehavior(condCheckOp, 'execute')
rsb_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
rsb_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsb_imm_Instr.addBehavior(UpdatePC, 'execute', False)
#test starts
rsb_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 0xfc}, {'CPSR' : 0x00000000, 'REGS[9]': 0xc}, {'CPSR' : 0x20000000, 'REGS[10]': 0xf0})
#S=0 do not update CPSR
rsb_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 0})
rsb_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 1, 'immediate': 0xfc}, {'REGS[9]': 0xf}, {'REGS[10]': 0x30})
#condition does not satisfied
rsb_imm_Instr.addTest({'cond': 0x0, 's': 1, 'rn': 9, 'rd': 10, 'rotate': 1, 'immediate': 0xfc}, {'CPSR' : 0x20000000, 'REGS[9]': 1}, {'CPSR' : 0x20000000})
isa.addInstruction(rsb_imm_Instr)

# RSC instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)operand - (int)rn;
if (CPSR[key_C] == 0){
    rd = ((int)rd) -1;
}
""")
rsc_shift_imm_Instr = trap.Instruction('RSC_si', True, frequency = 4)
rsc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 1, 1]}, 'TODO')
rsc_shift_imm_Instr.setCode(opCode, 'execute')
rsc_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
rsc_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
rsc_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
rsc_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsc_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(rsc_shift_imm_Instr)
rsc_shift_reg_Instr = trap.Instruction('RSC_sr', True, frequency = 4)
rsc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 1, 1]}, 'TODO')
rsc_shift_reg_Instr.setCode(opCode, 'execute')
rsc_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
rsc_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
rsc_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
rsc_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsc_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(rsc_shift_reg_Instr)
rsc_imm_Instr = trap.Instruction('RSC_i', True, frequency = 4)
rsc_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 1, 1]}, 'TODO')
rsc_imm_Instr.setCode(opCode, 'execute')
rsc_imm_Instr.addBehavior(IncrementPC, 'fetch')
rsc_imm_Instr.addBehavior(condCheckOp, 'execute')
rsc_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
rsc_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
rsc_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(rsc_imm_Instr)

# SBC instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)rn - (int)operand;
if (CPSR[key_C] == 0){
    rd = ((int)rd) -1;
}
""")
sbc_shift_imm_Instr = trap.Instruction('SBC_si', True, frequency = 4)
sbc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 1, 0]}, 'TODO')
sbc_shift_imm_Instr.setCode(opCode, 'execute')
sbc_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
sbc_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
sbc_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
sbc_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sbc_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(sbc_shift_imm_Instr)
sbc_shift_reg_Instr = trap.Instruction('SBC_sr', True, frequency = 4)
sbc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 1, 0]}, 'TODO')
sbc_shift_reg_Instr.setCode(opCode, 'execute')
sbc_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
sbc_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
sbc_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
sbc_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sbc_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(sbc_shift_reg_Instr)
sbc_imm_Instr = trap.Instruction('SBC_i', True, frequency = 4)
sbc_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 1, 0]}, 'TODO')
sbc_imm_Instr.setCode(opCode, 'execute')
sbc_imm_Instr.addBehavior(IncrementPC, 'fetch')
sbc_imm_Instr.addBehavior(condCheckOp, 'execute')
sbc_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
sbc_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sbc_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(sbc_imm_Instr)

# SUB instruction family
opCode = cxx_writer.writer_code.Code("""
rd = (int)rn - (int)operand;
""")
sub_shift_imm_Instr = trap.Instruction('SUB_si', True, frequency = 5)
sub_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 1, 0]}, 'TODO')
sub_shift_imm_Instr.setCode(opCode, 'execute')
sub_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
sub_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
sub_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
sub_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sub_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)

isa.addInstruction(sub_shift_imm_Instr)
sub_shift_reg_Instr = trap.Instruction('SUB_sr', True, frequency = 5)
sub_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 1, 0]}, 'TODO')
sub_shift_reg_Instr.setCode(opCode, 'execute')
sub_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
sub_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
sub_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
sub_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sub_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(sub_shift_reg_Instr)
sub_imm_Instr = trap.Instruction('SUB_i', True, frequency = 5)
sub_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 1, 0]}, 'TODO')
sub_imm_Instr.setCode(opCode, 'execute')
sub_imm_Instr.addBehavior(IncrementPC, 'fetch')
sub_imm_Instr.addBehavior(condCheckOp, 'execute')
sub_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
sub_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
sub_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(sub_imm_Instr)

# TEQ instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn ^ operand;
UpdatePSRBitM(result, carry);
""")
teq_shift_imm_Instr = trap.Instruction('TEQ_si', True, frequency = 5)
teq_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 0, 1], 's': [1]}, 'TODO')
teq_shift_imm_Instr.setCode(opCode, 'execute')
teq_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
teq_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
teq_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
teq_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(teq_shift_imm_Instr)
teq_shift_reg_Instr = trap.Instruction('TEQ_sr', True, frequency = 5)
teq_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 0, 1], 's': [1]}, 'TODO')
teq_shift_reg_Instr.setCode(opCode, 'execute')
teq_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
teq_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
teq_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
teq_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(teq_shift_reg_Instr)
teq_imm_Instr = trap.Instruction('TEQ_i', True, frequency = 5)
teq_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 0, 1], 's': [1]}, 'TODO')
teq_imm_Instr.setCode(opCode, 'execute')
teq_imm_Instr.addBehavior(IncrementPC, 'fetch')
teq_imm_Instr.addBehavior(condCheckOp, 'execute')
teq_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
teq_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(teq_imm_Instr)

# TST instruction family
opCode = cxx_writer.writer_code.Code("""
result = rn & operand;
UpdatePSRBitM(result, carry);
""")
tst_shift_imm_Instr = trap.Instruction('TST_si', True, frequency = 6)
tst_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 0, 0], 's': [1]}, 'TODO')
tst_shift_imm_Instr.setCode(opCode, 'execute')
tst_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
tst_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
tst_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
tst_shift_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(tst_shift_imm_Instr)
tst_shift_reg_Instr = trap.Instruction('TST_sr', True, frequency = 6)
tst_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 0, 0], 's': [1]}, 'TODO')
tst_shift_reg_Instr.setCode(opCode, 'execute')
tst_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
tst_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
tst_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
tst_shift_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(tst_shift_reg_Instr)
tst_imm_Instr = trap.Instruction('TST_i', True, frequency = 6)
tst_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 0, 0], 's': [1]}, 'TODO')
tst_imm_Instr.setCode(opCode, 'execute')
tst_imm_Instr.addBehavior(IncrementPC, 'fetch')
tst_imm_Instr.addBehavior(condCheckOp, 'execute')
tst_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
tst_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(tst_imm_Instr)

# STM instruction family
opCode = cxx_writer.writer_code.Code("""
int numRegsToStore = 0;
//I use word aligned addresses
start_address &= 0xFFFFFFFC;
//I have to distinguish whether I have to store user-mode registers
//or the currently used ones.
if(s != 0){
    //Now I can save the registers
    //Save the registers common to all modes
    for(int i = 0; i < 8; i++){
        if((reg_list & (0x00000001 << i)) != 0) {
            dataMem.write_word(start_address, REGS[i]);
            start_address += 4;
            numRegsToStore++;
        }
    }
    //Save the User Mode registers.
    for(int i = 8; i < 16; i++){
        if((reg_list & (0x00000001 << i)) != 0) {
            dataMem.write_word(start_address, RB[i]);
            start_address += 4;
            numRegsToStore++;
        }
    }
}
else{
    //Normal registers
    //Save the registers common to all modes; note that using the writeBack strategy
    //and putting the base register in the list of register to be saved is defined by the
    //ARM as an undefined operation; actually most ARM implementations save the original
    //base register if it is first in the register list, otherwise they save the updated
    //version.
    for(int i = 0; i < 16; i++){
        if((reg_list & (0x00000001 << i)) != 0) {
            dataMem.write_word(start_address, REGS[i]);
            start_address += 4;
            numRegsToStore++;
        }
        //Now If necessary I update the base register; it gets updated
        //after the first register has been written.
        if(w != 0 && i == 0){
            rn = wb_address;
        }
    }
}
stall(numRegsToStore);
""")
opCodeDec = cxx_writer.writer_code.Code("""
#ifdef ACC_MODEL
for(int i = 0; i < 16; i++){
    if((reg_list & (0x00000001 << i)) != 0){
        RB[i].isLocked();
    }
}
#endif
""")
stm_Instr = trap.Instruction('STM', True, frequency = 8)
stm_Instr.setMachineCode(ls_multiple, {'l' : [0]}, 'TODO')
stm_Instr.setCode(opCode, 'execute')
stm_Instr.setCode(opCodeDec, 'decode')
stm_Instr.addBehavior(IncrementPC, 'fetch')
stm_Instr.addBehavior(condCheckOp, 'execute')
stm_Instr.addBehavior(LSM_reglist_Op, 'execute')
isa.addInstruction(stm_Instr)

# STR instruction family
# Normal load instruction
opCode = cxx_writer.writer_code.Code("""
dataMem.write_word(address, rd);
stall(1);
""")
str_imm_Instr = trap.Instruction('STR_imm', True, frequency = 8)
str_imm_Instr.setMachineCode(ls_immOff, {'b': [0], 'l': [0]}, 'TODO')
str_imm_Instr.setCode(opCode, 'execute')
str_imm_Instr.addBehavior(IncrementPC, 'fetch')
str_imm_Instr.addBehavior(condCheckOp, 'execute')
str_imm_Instr.addBehavior(ls_imm_Op, 'execute')
str_imm_Instr.addVariable(('memLastBits', 'BIT<32>'))
str_imm_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(str_imm_Instr)
str_off_Instr = trap.Instruction('STR_off', True, frequency = 8)
str_off_Instr.setMachineCode(ls_regOff, {'b': [0], 'l': [0]}, 'TODO')
str_off_Instr.setCode(opCode, 'execute')
str_off_Instr.addBehavior(IncrementPC, 'fetch')
str_off_Instr.addBehavior(condCheckOp, 'execute')
str_off_Instr.addBehavior(ls_reg_Op, 'execute')
str_off_Instr.addVariable(('memLastBits', 'BIT<32>'))
str_off_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(str_off_Instr)
# STRB instruction family
# Normal load instruction
opCode = cxx_writer.writer_code.Code("""
dataMem.write_byte(address, (unsigned char)(rd & 0x000000FF));
stall(1);
""")
strb_imm_Instr = trap.Instruction('STRB_imm', True, frequency = 4)
strb_imm_Instr.setMachineCode(ls_immOff, {'b': [1], 'l': [0]}, 'TODO')
strb_imm_Instr.setCode(opCode, 'execute')
strb_imm_Instr.addBehavior(IncrementPC, 'fetch')
strb_imm_Instr.addBehavior(condCheckOp, 'execute')
strb_imm_Instr.addBehavior(ls_imm_Op, 'execute')
isa.addInstruction(strb_imm_Instr)
strb_off_Instr = trap.Instruction('STRB_off', True, frequency = 4)
strb_off_Instr.setMachineCode(ls_regOff, {'b': [1], 'l': [0]}, 'TODO')
strb_off_Instr.setCode(opCode, 'execute')
strb_off_Instr.addBehavior(IncrementPC, 'fetch')
strb_off_Instr.addBehavior(condCheckOp, 'execute')
strb_off_Instr.addBehavior(ls_reg_Op, 'execute')
isa.addInstruction(strb_off_Instr)
# STRH instruction family
opCode = cxx_writer.writer_code.Code("""
dataMem.write_half(address, (unsigned short)(rd & 0x0000FFFF));
stall(1);
""")
strh_off_Instr = trap.Instruction('STRH_off', True, frequency = 2)
strh_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 0, 1, 1], 'l': [0]}, 'TODO')
strh_off_Instr.setCode(opCode, 'execute')
strh_off_Instr.addBehavior(IncrementPC, 'fetch')
strh_off_Instr.addBehavior(condCheckOp, 'execute')
strh_off_Instr.addBehavior(ls_sh_Op, 'execute')
isa.addInstruction(strh_off_Instr)

# SWP instruction family
opCode = cxx_writer.writer_code.Code("""
memLastBits = rn & 0x00000003;
//Depending whether the address is word aligned or not I have to rotate the
//read word.
temp = dataMem.read_word(rn);
if(memLastBits != 0){
    temp = RotateRight(8*memLastBits, temp);
}
dataMem.write_word(rn, rm);
rd = temp;
stall(3);
""")
swap_Instr = trap.Instruction('SWAP', True, frequency = 2)
swap_Instr.setMachineCode(swap, {'b': [0]}, 'TODO')
swap_Instr.setCode(opCode, 'execute')
swap_Instr.addBehavior(IncrementPC, 'fetch')
swap_Instr.addBehavior(condCheckOp, 'execute')
swap_Instr.addVariable(('temp', 'BIT<32>'))
swap_Instr.addVariable(('memLastBits', 'BIT<32>'))
isa.addInstruction(swap_Instr)
opCode = cxx_writer.writer_code.Code("""
temp = dataMem.read_byte(rn);
dataMem.write_byte(rn, (unsigned char)(rm & 0x000000FF));
rd = temp;
stall(3);
""")
swapb_Instr = trap.Instruction('SWAPB', True, frequency = 1)
swapb_Instr.setMachineCode(swap, {'b': [1]}, 'TODO')
swapb_Instr.setCode(opCode, 'execute')
swapb_Instr.addBehavior(IncrementPC, 'fetch')
swapb_Instr.addBehavior(condCheckOp, 'execute')
swapb_Instr.addVariable(('temp', 'BIT<8>'))
isa.addInstruction(swapb_Instr)
